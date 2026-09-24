//! Nothing aegis starts may outlive it.
//!
//! aegis starts two long-lived children: the L2 judge (`llama-server`, on the
//! first judged scan) and `curl` for `install-models`. These tests run the real
//! binary with HOME and PATH pointed at a scratch directory whose `bin/` holds
//! stub versions of both, and check that each stub is gone once aegis is:
//! after a flagged scan (`exit(1)`), after SIGTERM/SIGINT/SIGHUP, and on Linux
//! after SIGKILL. The stub judge is this test binary itself, re-executed as a
//! tiny HTTP server (see `stub_judge_server`), so the tests need nothing beyond
//! /bin/sh and sleep.

#![cfg(unix)]

use std::fs;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::os::unix::fs::PermissionsExt;
use std::os::unix::process::{CommandExt, ExitStatusExt};
use std::path::PathBuf;
use std::process::{Child, Command, ExitStatus, Stdio};
use std::time::{Duration, Instant};

const AEGIS: &str = env!("CARGO_BIN_EXE_aegis");
const STUB_PORT_ENV: &str = "AEGIS_TEST_STUB_JUDGE_PORT";

/// A scratch HOME plus a `bin/` of stub children, removed on drop. Any stub
/// that recorded its pid is SIGKILLed on drop too, so a failing test does not
/// leave a `sleep 600` behind.
struct Sandbox {
    root: PathBuf,
}

impl Sandbox {
    fn new(name: &str) -> Self {
        let root = std::env::temp_dir().join(format!("aegis-lc-{}-{}", name, std::process::id()));
        let _ = fs::remove_dir_all(&root);
        fs::create_dir_all(root.join("home/.aegis/models")).unwrap();
        fs::create_dir_all(root.join("bin")).unwrap();
        Sandbox { root }
    }

    fn home(&self) -> PathBuf {
        self.root.join("home")
    }

    fn stub(&self, name: &str, body: &str) {
        let p = self.root.join("bin").join(name);
        fs::write(&p, format!("#!/bin/sh\n{body}\n")).unwrap();
        fs::set_permissions(&p, fs::Permissions::from_mode(0o755)).unwrap();
    }

    /// `llama-server` stub: records its pid, then becomes the stub HTTP judge
    /// on the `--port` aegis passes, answering every judge prompt with ATTACK.
    fn stub_judge(&self) {
        self.stub(
            "llama-server",
            &format!(
                "echo $$ > \"$HOME/judge.pid\"\n\
                 port=\n\
                 while [ $# -gt 0 ]; do [ \"$1\" = --port ] && port=$2; shift; done\n\
                 {STUB_PORT_ENV}=$port exec \"$AEGIS_TEST_EXE\" --exact stub_judge_server --test-threads=1 -q"
            ),
        );
    }

    /// `curl` stub: records its pid and sleeps, like a 1.8 GB download.
    fn stub_slow_curl(&self) {
        self.stub("curl", "echo $$ > \"$HOME/curl.pid\"\nexec sleep 600");
    }

    fn with_model(&self) {
        fs::write(self.home().join(".aegis/models/Qwen3-1.7B-Q8_0.gguf"), b"stub model").unwrap();
    }

    fn file(&self, name: &str, text: &str) -> PathBuf {
        let p = self.root.join(name);
        fs::write(&p, text).unwrap();
        p
    }

    fn aegis(&self, args: &[&str]) -> Command {
        let mut c = Command::new(AEGIS);
        c.args(args)
            .env_clear()
            .env("HOME", self.home())
            .env("PATH", format!("{}:/usr/bin:/bin", self.root.join("bin").display()))
            .env("TMPDIR", &self.root)
            .env("AEGIS_TEST_EXE", std::env::current_exe().unwrap())
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null());
        // Start from default dispositions whatever the test runner inherited
        // (a backgrounded shell ignores SIGINT), so each test controls them.
        unsafe {
            c.pre_exec(|| {
                for sig in [libc::SIGTERM, libc::SIGINT, libc::SIGHUP] {
                    libc::signal(sig, libc::SIG_DFL);
                }
                Ok(())
            });
        }
        c
    }

    /// Waits for a stub to write `<name>.pid` and returns the pid.
    fn pid(&self, name: &str, within: Duration) -> Option<i32> {
        let p = self.home().join(format!("{name}.pid"));
        let deadline = Instant::now() + within;
        loop {
            if let Some(pid) = fs::read_to_string(&p).ok().and_then(|s| s.trim().parse().ok()) {
                return Some(pid);
            }
            if Instant::now() > deadline {
                return None;
            }
            std::thread::sleep(Duration::from_millis(20));
        }
    }
}

impl Drop for Sandbox {
    fn drop(&mut self) {
        for name in ["judge", "curl"] {
            if let Some(pid) = fs::read_to_string(self.home().join(format!("{name}.pid")))
                .ok()
                .and_then(|s| s.trim().parse::<i32>().ok())
            {
                unsafe { libc::kill(pid, libc::SIGKILL) };
            }
        }
        let _ = fs::remove_dir_all(&self.root);
    }
}

/// True while `pid` is a live process. A zombie counts as gone: it has exited
/// and only waits for its (new) parent to reap it.
fn alive(pid: i32) -> bool {
    if unsafe { libc::kill(pid, 0) } != 0 {
        return false;
    }
    #[cfg(target_os = "linux")]
    {
        match fs::read_to_string(format!("/proc/{pid}/stat")) {
            Ok(stat) => !matches!(stat.rsplit_once(") ").map(|(_, rest)| rest.as_bytes()[0]), Some(b'Z') | Some(b'X')),
            Err(_) => false,
        }
    }
    #[cfg(not(target_os = "linux"))]
    {
        match Command::new("ps").args(["-o", "stat=", "-p", &pid.to_string()]).output() {
            Ok(out) => {
                let stat = String::from_utf8_lossy(&out.stdout);
                !stat.trim().is_empty() && !stat.trim_start().starts_with('Z')
            }
            Err(_) => true,
        }
    }
}

fn gone_within(pid: i32, within: Duration) -> bool {
    let deadline = Instant::now() + within;
    while Instant::now() < deadline {
        if !alive(pid) {
            return true;
        }
        std::thread::sleep(Duration::from_millis(20));
    }
    !alive(pid)
}

fn wait_within(child: &mut Child, within: Duration) -> ExitStatus {
    let deadline = Instant::now() + within;
    loop {
        if let Some(st) = child.try_wait().unwrap() {
            return st;
        }
        if Instant::now() > deadline {
            let _ = child.kill();
            let _ = child.wait();
            panic!("aegis (pid {}) still running after {:?}", child.id(), within);
        }
        std::thread::sleep(Duration::from_millis(20));
    }
}

fn signal(child: &Child, sig: libc::c_int) {
    assert_eq!(unsafe { libc::kill(child.id() as i32, sig) }, 0);
}

/// Not a test on its own: the `llama-server` stub re-executes this binary with
/// this filter and `AEGIS_TEST_STUB_JUDGE_PORT` set, and it then serves
/// /health and answers every chat completion with ATTACK until it is killed.
/// Without the env var it returns at once.
#[test]
fn stub_judge_server() {
    let Ok(port) = std::env::var(STUB_PORT_ENV) else { return };
    let listener = TcpListener::bind(("127.0.0.1", port.parse::<u16>().unwrap())).unwrap();
    for conn in listener.incoming() {
        let Ok(mut s) = conn else { continue };
        let _ = s.set_read_timeout(Some(Duration::from_secs(5)));
        let mut req = Vec::new();
        let mut buf = [0u8; 8192];
        // Read the headers, then Content-Length bytes of body.
        let (head_end, want) = loop {
            let Ok(n) = s.read(&mut buf) else { break (None, 0) };
            if n == 0 {
                break (None, 0);
            }
            req.extend_from_slice(&buf[..n]);
            if let Some(i) = req.windows(4).position(|w| w == b"\r\n\r\n") {
                let head = String::from_utf8_lossy(&req[..i]).to_lowercase();
                let len = head
                    .lines()
                    .find_map(|l| l.strip_prefix("content-length:").map(|v| v.trim().parse::<usize>().unwrap_or(0)))
                    .unwrap_or(0);
                break (Some(i + 4), len);
            }
        };
        let Some(head_end) = head_end else { continue };
        while req.len() < head_end + want {
            match s.read(&mut buf) {
                Ok(0) | Err(_) => break,
                Ok(n) => req.extend_from_slice(&buf[..n]),
            }
        }
        let body = if req.starts_with(b"GET") {
            r#"{"status":"ok"}"#
        } else {
            r#"{"choices":[{"message":{"content":"ATTACK"}}]}"#
        };
        let _ = write!(
            s,
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            body.len(),
            body
        );
    }
}

/// LEAK: run_scan ends a flagged scan with process::exit(1), which skipped
/// IntentJudge::drop, so the llama-server aegis had started kept running,
/// reparented to init, with the model loaded and its port bound.
#[test]
fn flagged_scan_stops_the_judge_it_started() {
    let sb = Sandbox::new("flagged");
    sb.with_model();
    sb.stub_judge();
    let note = sb.file("note.txt", "Deploy notes for this week.\n");

    let mut aegis = sb.aegis(&["scan", note.to_str().unwrap()]).spawn().unwrap();
    let st = wait_within(&mut aegis, Duration::from_secs(90));

    let judge = sb.pid("judge", Duration::from_secs(1)).expect("aegis never started the judge server");
    assert_eq!(st.code(), Some(1), "the stub judge says ATTACK, so the scan is flagged: {st:?}");
    assert!(
        gone_within(judge, Duration::from_secs(5)),
        "judge server pid {judge} outlived aegis after a flagged scan"
    );
}

/// LEAK: a stop signal (the adapter's call timeout, a supervisor stop, Ctrl-C,
/// a closed terminal) killed aegis without destructors and left curl
/// downloading the model, reparented to init.
#[test]
fn stop_signals_stop_the_model_download() {
    for (name, sig) in [("SIGTERM", libc::SIGTERM), ("SIGINT", libc::SIGINT), ("SIGHUP", libc::SIGHUP)] {
        let sb = Sandbox::new(&format!("dl-{name}"));
        sb.stub_slow_curl();
        let mut aegis = sb.aegis(&["install-models"]).spawn().unwrap();
        let curl = sb.pid("curl", Duration::from_secs(10)).expect("install-models never started curl");

        signal(&aegis, sig);
        let st = wait_within(&mut aegis, Duration::from_secs(5));
        assert_eq!(st.signal(), Some(sig), "{name}: aegis should still die of {name}: {st:?}");
        assert!(gone_within(curl, Duration::from_secs(5)), "{name}: curl pid {curl} outlived aegis");
    }
}

/// `nohup aegis daemon` (and `aegis daemon &` from a script) start aegis with
/// SIGHUP/SIGINT ignored. That must stay so: the handler is only installed for
/// signals that are not already ignored.
#[test]
fn ignored_sighup_stays_ignored() {
    let sb = Sandbox::new("nohup");
    sb.stub_slow_curl();
    let mut cmd = sb.aegis(&["install-models"]);
    unsafe {
        cmd.pre_exec(|| {
            libc::signal(libc::SIGHUP, libc::SIG_IGN);
            Ok(())
        });
    }
    let mut aegis = cmd.spawn().unwrap();
    let curl = sb.pid("curl", Duration::from_secs(10)).expect("install-models never started curl");

    signal(&aegis, libc::SIGHUP);
    std::thread::sleep(Duration::from_millis(500));
    assert!(aegis.try_wait().unwrap().is_none(), "aegis died of an ignored SIGHUP");
    assert!(alive(curl), "curl died although aegis ignores SIGHUP");

    signal(&aegis, libc::SIGTERM);
    wait_within(&mut aegis, Duration::from_secs(5));
    assert!(gone_within(curl, Duration::from_secs(5)), "curl pid {curl} outlived aegis");
}

/// SIGKILL runs no handler at all; on Linux the kernel's parent-death signal
/// stops the child instead.
#[cfg(target_os = "linux")]
#[test]
fn sigkill_stops_the_model_download_on_linux() {
    let sb = Sandbox::new("dl-sigkill");
    sb.stub_slow_curl();
    let mut aegis = sb.aegis(&["install-models"]).spawn().unwrap();
    let curl = sb.pid("curl", Duration::from_secs(10)).expect("install-models never started curl");

    signal(&aegis, libc::SIGKILL);
    wait_within(&mut aegis, Duration::from_secs(5));
    assert!(gone_within(curl, Duration::from_secs(5)), "curl pid {curl} outlived a SIGKILLed aegis");
}

/// status/targets/scan used to exec `llama-server --version` on every call even
/// with no model installed (0.2-0.4 s each; once it hung for over 15 s and was
/// orphaned when the caller gave up). With no model, no llama-server runs.
#[test]
fn no_model_means_no_llama_server_process() {
    let sb = Sandbox::new("nomodel");
    sb.stub("llama-server", "touch \"$HOME/llama-server.ran\"");
    let note = sb.file("note.txt", "hello\n");
    for args in [vec!["status"], vec!["targets"], vec!["scan", note.to_str().unwrap()]] {
        let mut aegis = sb.aegis(&args).spawn().unwrap();
        let st = wait_within(&mut aegis, Duration::from_secs(30));
        assert!(st.success(), "aegis {args:?}: {st:?}");
    }
    assert!(!sb.home().join("llama-server.ran").exists(), "aegis ran llama-server with no model installed");
}

/// A judge server that another aegis process started (recorded in
/// ~/.aegis/judge.state) is shared, not owned: a scan that reuses it must leave
/// it running.
#[test]
fn shared_judge_started_elsewhere_keeps_running() {
    let sb = Sandbox::new("shared");
    sb.with_model();
    sb.stub_judge();
    let port = TcpListener::bind("127.0.0.1:0").unwrap().local_addr().unwrap().port();
    let mut server = Command::new(sb.root.join("bin/llama-server"))
        .args(["--port", &port.to_string()])
        .env("HOME", sb.home())
        .env("AEGIS_TEST_EXE", std::env::current_exe().unwrap())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    let deadline = Instant::now() + Duration::from_secs(10);
    while TcpStream::connect(("127.0.0.1", port)).is_err() {
        assert!(Instant::now() < deadline, "stub judge never listened on {port}");
        std::thread::sleep(Duration::from_millis(20));
    }
    fs::write(sb.home().join(".aegis/judge.state"), format!("{port}:{}\n", "ab".repeat(32))).unwrap();

    let note = sb.file("note.txt", "Deploy notes for this week.\n");
    let mut aegis = sb.aegis(&["scan", note.to_str().unwrap()]).spawn().unwrap();
    let st = wait_within(&mut aegis, Duration::from_secs(90));
    assert_eq!(st.code(), Some(1), "the shared stub judge says ATTACK: {st:?}");

    std::thread::sleep(Duration::from_millis(300));
    let still_running = server.try_wait().unwrap().is_none();
    let _ = server.kill();
    let _ = server.wait();
    assert!(still_running, "aegis stopped a judge server it did not start");
}
