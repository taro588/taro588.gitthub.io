"""DCC adapter/session registry."""
from __future__ import annotations

from .session import DCCSession


class DCCManager:
    def __init__(self) -> None:
        self._sessions: dict[str, DCCSession] = {}

    def register(self, name: str, session: DCCSession) -> None:
        self._sessions[name] = session

    def connect_all(self) -> dict[str, bool]:
        return {name: session.connect() for name, session in self._sessions.items()}

    def status(self) -> dict[str, dict]:
        return {name: session.info() for name, session in self._sessions.items()}
