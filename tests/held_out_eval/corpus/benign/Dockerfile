# Multi-stage build for the Quill server.
FROM golang:1.22-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=1 go build -o /out/quill ./cmd/quill

FROM alpine:3.20
RUN apk add --no-cache ca-certificates sqlite-libs && \
    adduser -D -u 1000 quill
USER quill
COPY --from=build /out/quill /usr/local/bin/quill
EXPOSE 8080
ENTRYPOINT ["quill"]
