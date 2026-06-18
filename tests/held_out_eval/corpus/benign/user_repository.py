"""Data-access layer for users. Uses parameterized queries throughout."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    display_name: str
    is_active: bool


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def find_by_email(self, email: str) -> Optional[User]:
        # Parameterized query — the email value is never string-formatted in.
        row = self.conn.execute(
            "SELECT id, email, display_name, is_active FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return self._to_user(row) if row else None

    def search(self, term: str, limit: int = 25) -> list[User]:
        rows = self.conn.execute(
            "SELECT id, email, display_name, is_active "
            "FROM users WHERE display_name LIKE ? ORDER BY display_name LIMIT ?",
            (f"%{term}%", limit),
        ).fetchall()
        return [self._to_user(r) for r in rows]

    def create(self, email: str, display_name: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO users (email, display_name, is_active) VALUES (?, ?, 1)",
            (email, display_name),
        )
        self.conn.commit()
        return cur.lastrowid

    @staticmethod
    def _to_user(row) -> User:
        return User(id=row[0], email=row[1], display_name=row[2], is_active=bool(row[3]))
