"""DCC adapter/session registry with failure isolation."""
from __future__ import annotations
from .session import DCCSession

class DCCManager:
    def __init__(self) -> None:
        self._sessions: dict[str, DCCSession] = {}

    def register(self, name: str, session: DCCSession) -> None:
        self._sessions[name] = session

    def connect_all(self) -> dict[str, bool]:
        result = {}
        for name, session in self._sessions.items():
            try:
                result[name] = session.connect()
            except Exception as exc:
                session.connected = False
                session.last_error = str(exc)
                result[name] = False
        return result

    def status(self) -> dict[str, dict]:
        result = {}
        for name, session in self._sessions.items():
            try:
                result[name] = session.info()
            except Exception as exc:
                result[name] = {"dcc": name, "available": False, "connected": False, "error": str(exc)}
        return result
