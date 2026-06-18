"""Input validation helpers for the signup form."""
import re

PASSWORD_RE = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{12,}$"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_strong_password(password: str) -> bool:
    """Return True if the password meets complexity requirements.

    At least 12 chars, one lowercase, one uppercase, one digit, one symbol.
    """
    return bool(PASSWORD_RE.match(password))


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def sanitize_injection(user_value: str) -> str:
    """Strip characters that could break out of a quoted SQL literal.

    Note: this is a defense-in-depth helper only. Always use parameterized
    queries as the primary protection against SQL injection.
    """
    return user_value.replace("'", "''").replace("\x00", "")


if __name__ == "__main__":
    assert is_strong_password("Sup3rSecret!pass")
    assert not is_strong_password("weak")
    assert is_valid_email("user@example.com")
    print("all checks passed")
