-- Migration 0007: add full-text search and tags.
-- Run inside a transaction.

BEGIN;

CREATE TABLE IF NOT EXISTS note_tags (
    note_id INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    tag     TEXT    NOT NULL,
    PRIMARY KEY (note_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_note_tags_tag ON note_tags(tag);

CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    title,
    body,
    content='notes',
    content_rowid='id'
);

-- Keep the FTS index in sync with the base table.
CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
    INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;

CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
    INSERT INTO notes_fts(notes_fts, rowid, title, body)
    VALUES ('delete', old.id, old.title, old.body);
END;

COMMIT;
