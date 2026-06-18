# Quill HTTP API

Base URL: `https://api.quill.example.com/v1`

All requests must include an `Authorization: Bearer <token>` header. Responses
are JSON. Timestamps are ISO 8601 in UTC.

## Notes

### List notes

```
GET /notes?tag=work&limit=25
```

Response:

```json
{
  "notes": [
    { "id": "n_8821", "title": "Standup notes", "tags": ["work"], "updated_at": "2026-06-01T09:12:00Z" }
  ],
  "next_cursor": null
}
```

### Create a note

```
POST /notes
Content-Type: application/json

{ "title": "Idea", "body": "Build a thing", "tags": ["ideas"] }
```

Returns `201 Created` with the new note object.

### Delete a note

```
DELETE /notes/{id}
```

Returns `204 No Content`.

## Rate limits

The API allows 60 requests per minute per token. When exceeded you receive a
`429 Too Many Requests` with a `Retry-After` header.

## Errors

| Status | Meaning                |
|--------|------------------------|
| 400    | Invalid request body   |
| 401    | Missing/invalid token  |
| 404    | Note not found         |
| 429    | Rate limit exceeded    |
