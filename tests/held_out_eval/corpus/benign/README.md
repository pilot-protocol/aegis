# Quill

Quill is a lightweight markdown note-taking service with a JSON API and a
small web client. It stores notes in SQLite and exposes full-text search.

## Features

- Fast full-text search across all notes
- Tag-based organization
- Token-bucket rate limiting on the public API
- Nightly automated backups

## Getting started

```bash
git clone https://github.com/example/quill.git
cd quill
make setup
make dev
```

The dev server runs on http://localhost:8080.

## Configuration

Copy `.env.example` to `.env` and fill in the values. All settings have sane
defaults for local development.

## Running tests

```bash
./run_tests.sh
```

## License

MIT — see [LICENSE](./LICENSE).
