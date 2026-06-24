// AEGIS Pilot Protocol app — typed IPC adapter for the AEGIS security daemon.
//
// Exposes aegis scan/health/status/help as callable methods on the Pilot
// overlay network app store. Other agents can call aegis.scan to have
// untrusted content vetted by the local AEGIS instance before processing it.
//
// Standard supervisor lifecycle flags (--addr, --db, --socket, --identity,
// --manifest, --cap-state) are declared but most are unused in this adapter.
package main

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/pilot-protocol/app-store/pkg/ipc"
)

const (
	methodScan   = "aegis.scan"
	methodHealth = "aegis.health"
	methodStatus = "aegis.status"
	methodHelp   = "aegis.help"
)

// ── Request / response types ─────────────────────────────────────────────────

type scanReq struct {
	Text         string `json:"text"`
	CtxSensitive bool   `json:"ctx_sensitive"` // true = treat as skill/memory (T2 patterns active)
}

type scanResp struct {
	Verdict string `json:"verdict"` // "allow", "quarantine", or "block"
	Rule    string `json:"rule"`    // matched rule, if any
	Blocked bool   `json:"blocked"` // true iff verdict is quarantine or block
	Latency string `json:"latency"` // e.g. "3.2ms"
}

type healthResp struct {
	Ok      bool   `json:"ok"`
	Binary  string `json:"binary"`  // path to aegis binary
	Version string `json:"version"` // output of "aegis --version"
}

type statusResp struct {
	Lines []string `json:"lines"` // recent lines from "aegis status"
}

type helpMethod struct {
	Name    string `json:"name"`
	Summary string `json:"summary"`
	Kind    string `json:"kind"`     // utility | status | meta
	Duration string `json:"duration"` // fast | med | slow
}

type helpResp struct {
	App     string       `json:"app"`
	Version string       `json:"version"`
	Methods []helpMethod `json:"methods"`
}

// ── Main ─────────────────────────────────────────────────────────────────────

func main() {
	fs := flag.NewFlagSet("aegis-app", flag.ExitOnError)
	var (
		_        = fs.String("addr", "", "pilot address (opaque)")
		_        = fs.String("db", "", "sqlite path (unused)")
		sockPath = fs.String("socket", "", "unix socket to listen on; set by supervisor")
		_        = fs.String("identity", "", "ed25519 identity file (unused)")
		_        = fs.String("manifest", "", "path to manifest.json (unused)")
		_        = fs.String("cap-state", "", "spend-cap state log (unused)")
	)
	if err := fs.Parse(os.Args[1:]); err != nil {
		log.Fatalf("flag parse: %v", err)
	}
	if *sockPath == "" {
		log.Fatalf("supervisor did not pass --socket; refusing to start")
	}

	logger := log.New(os.Stderr, "aegis-app: ", log.LstdFlags|log.Lmicroseconds)
	sideloaded := os.Getenv("PILOT_SIDELOAD") == "1"
	logger.Printf("starting (sideloaded=%v) on %s", sideloaded, *sockPath)

	if err := os.Remove(*sockPath); err != nil && !os.IsNotExist(err) {
		logger.Fatalf("remove stale socket: %v", err)
	}
	ln, err := net.Listen("unix", *sockPath)
	if err != nil {
		logger.Fatalf("listen: %v", err)
	}
	defer ln.Close()

	d := ipc.NewDispatcher()
	d.Register(methodScan,   handleScan(logger))
	d.Register(methodHealth, handleHealth(logger))
	d.Register(methodStatus, handleStatus(logger))
	d.Register(methodHelp,   handleHelp())

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		<-sigCh
		logger.Printf("shutdown signal received")
		cancel()
		_ = ln.Close()
	}()

	logger.Printf("ready — methods: %v", d.Methods())
	for {
		conn, err := ln.Accept()
		if err != nil {
			if ctx.Err() != nil {
				return
			}
			logger.Printf("accept: %v", err)
			continue
		}
		go func(c net.Conn) {
			defer c.Close()
			if err := ipc.Serve(ctx, c, d); err != nil {
				logger.Printf("serve: %v", err)
			}
		}(conn)
	}
}

// ── Handlers ─────────────────────────────────────────────────────────────────

func handleScan(logger *log.Logger) ipc.Handler {
	return func(_ context.Context, req *ipc.Envelope) (json.RawMessage, error) {
		var args scanReq
		if len(req.Payload) > 0 {
			if err := json.Unmarshal(req.Payload, &args); err != nil {
				return nil, fmt.Errorf("decode scan args: %w", err)
			}
		}
		if args.Text == "" {
			return nil, fmt.Errorf("text is required")
		}

		aegisBin, err := findAegis()
		if err != nil {
			return nil, fmt.Errorf("aegis binary not found: %w", err)
		}

		t0 := time.Now()
		cmd := exec.Command(aegisBin, "scan-pipe")
		cmd.Stdin = strings.NewReader(args.Text)
		var stdout, stderr bytes.Buffer
		cmd.Stdout = &stdout
		cmd.Stderr = &stderr

		runErr := cmd.Run()
		elapsed := time.Since(t0)

		exitCode := 0
		if runErr != nil {
			if exitErr, ok := runErr.(*exec.ExitError); ok {
				exitCode = exitErr.ExitCode()
			} else {
				return nil, fmt.Errorf("aegis scan-pipe exec: %w", runErr)
			}
		}

		resp := scanResp{
			Latency: fmt.Sprintf("%.1fms", float64(elapsed.Microseconds())/1000),
		}
		switch exitCode {
		case 0:
			resp.Verdict = "allow"
			resp.Blocked = false
		case 2:
			resp.Verdict = "quarantine"
			resp.Blocked = true
			resp.Rule = strings.TrimSpace(stdout.String())
		default:
			resp.Verdict = "block"
			resp.Blocked = true
			resp.Rule = strings.TrimSpace(stdout.String())
		}

		logger.Printf("scan exit=%d verdict=%s latency=%s", exitCode, resp.Verdict, resp.Latency)
		return marshalResp(resp)
	}
}

func handleHealth(logger *log.Logger) ipc.Handler {
	return func(_ context.Context, req *ipc.Envelope) (json.RawMessage, error) {
		aegisBin, err := findAegis()
		if err != nil {
			resp := healthResp{Ok: false}
			return marshalResp(resp)
		}

		out, _ := exec.Command(aegisBin, "--version").Output()
		version := strings.TrimSpace(string(out))

		resp := healthResp{
			Ok:      true,
			Binary:  aegisBin,
			Version: version,
		}
		logger.Printf("health check: ok=true version=%q", version)
		return marshalResp(resp)
	}
}

func handleStatus(logger *log.Logger) ipc.Handler {
	return func(ctx context.Context, req *ipc.Envelope) (json.RawMessage, error) {
		aegisBin, err := findAegis()
		if err != nil {
			return nil, fmt.Errorf("aegis binary not found: %w", err)
		}

		// Run 'aegis status' with a short timeout and capture recent lines.
		tctx, cancel := context.WithTimeout(ctx, 3*time.Second)
		defer cancel()
		cmd := exec.CommandContext(tctx, aegisBin, "status", "--tail", "20")
		out, _ := cmd.Output()

		lines := []string{}
		scanner := bufio.NewScanner(strings.NewReader(string(out)))
		for scanner.Scan() {
			line := scanner.Text()
			if line != "" {
				lines = append(lines, line)
			}
		}

		resp := statusResp{Lines: lines}
		logger.Printf("status: %d lines returned", len(lines))
		return marshalResp(resp)
	}
}

func handleHelp() ipc.Handler {
	resp := helpResp{
		App:     "io.pilot.aegis",
		Version: "0.1.4",
		Methods: []helpMethod{
			{
				Name:     "aegis.scan",
				Summary:  "Scan text content for prompt injection, jailbreaks, and infra-impersonation attacks.",
				Kind:     "utility",
				Duration: "fast",
			},
			{
				Name:     "aegis.health",
				Summary:  "Check whether the local AEGIS binary is installed and reachable.",
				Kind:     "status",
				Duration: "fast",
			},
			{
				Name:     "aegis.status",
				Summary:  "Return the last 20 entries from the AEGIS audit log.",
				Kind:     "status",
				Duration: "fast",
			},
			{
				Name:     "aegis.help",
				Summary:  "Discovery: list available methods, their parameters, kind, and latency class.",
				Kind:     "meta",
				Duration: "fast",
			},
		},
	}
	body, _ := json.Marshal(resp)
	return func(_ context.Context, _ *ipc.Envelope) (json.RawMessage, error) {
		return json.RawMessage(body), nil
	}
}

// ── Helpers ───────────────────────────────────────────────────────────────────

func findAegis() (string, error) {
	// 1. Check PATH
	if p, err := exec.LookPath("aegis"); err == nil {
		return p, nil
	}
	// 2. Common install locations
	candidates := []string{
		os.ExpandEnv("$HOME/.local/bin/aegis"),
		"/opt/homebrew/bin/aegis",
		"/usr/local/bin/aegis",
		"/usr/bin/aegis",
	}
	for _, c := range candidates {
		if _, err := os.Stat(c); err == nil {
			return c, nil
		}
	}
	return "", fmt.Errorf("aegis binary not found in PATH or common locations")
}

func marshalResp(v any) (json.RawMessage, error) {
	b, err := json.Marshal(v)
	if err != nil {
		return nil, fmt.Errorf("marshal response: %w", err)
	}
	return json.RawMessage(b), nil
}
