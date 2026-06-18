.PHONY: setup dev build test lint clean

setup:
	go mod download
	cd web && npm install

dev:
	go run ./cmd/quill --dev

build:
	go build -o bin/quill ./cmd/quill
	cd web && npm run build

test:
	go test -race ./...
	cd web && npm test

lint:
	go vet ./...
	gofmt -l .

clean:
	rm -rf bin/ web/dist/
