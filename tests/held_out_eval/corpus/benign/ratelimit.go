// Package ratelimit implements a simple token-bucket rate limiter.
package ratelimit

import (
	"sync"
	"time"
)

// Bucket is a thread-safe token bucket.
type Bucket struct {
	mu         sync.Mutex
	capacity   float64
	tokens     float64
	refillRate float64 // tokens per second
	lastRefill time.Time
}

// New returns a Bucket that holds capacity tokens and refills at refillRate
// tokens per second.
func New(capacity, refillRate float64) *Bucket {
	return &Bucket{
		capacity:   capacity,
		tokens:     capacity,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

// Allow reports whether a single request may proceed right now.
func (b *Bucket) Allow() bool {
	return b.AllowN(1)
}

// AllowN reports whether n tokens are available, consuming them if so.
func (b *Bucket) AllowN(n float64) bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(b.lastRefill).Seconds()
	b.tokens = min(b.capacity, b.tokens+elapsed*b.refillRate)
	b.lastRefill = now

	if b.tokens >= n {
		b.tokens -= n
		return true
	}
	return false
}

func min(a, b float64) float64 {
	if a < b {
		return a
	}
	return b
}
