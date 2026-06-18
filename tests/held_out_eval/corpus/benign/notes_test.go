package notes

import "testing"

func TestSlugify(t *testing.T) {
	cases := map[string]string{
		"Hello World":      "hello-world",
		"  Trim  Me  ":     "trim-me",
		"Special!@# Chars": "special-chars",
		"":                 "",
	}
	for in, want := range cases {
		if got := Slugify(in); got != want {
			t.Errorf("Slugify(%q) = %q, want %q", in, got, want)
		}
	}
}

func TestTruncate(t *testing.T) {
	if got := Truncate("hello world", 5); got != "hello…" {
		t.Errorf("got %q", got)
	}
	if got := Truncate("hi", 5); got != "hi" {
		t.Errorf("expected no truncation, got %q", got)
	}
}
