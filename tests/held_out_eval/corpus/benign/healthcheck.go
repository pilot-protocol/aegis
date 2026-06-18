package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type health struct {
	Status  string `json:"status"`
	Uptime  string `json:"uptime"`
	Version string `json:"version"`
}

var startTime = time.Now()

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	resp := health{
		Status:  "ok",
		Uptime:  time.Since(startTime).Round(time.Second).String(),
		Version: "1.4.2",
	}
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		http.Error(w, "encoding error", http.StatusInternalServerError)
	}
}

func main() {
	http.HandleFunc("/healthz", healthHandler)
	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
