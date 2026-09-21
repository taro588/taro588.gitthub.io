"""Failure-isolation tests for DCC integration."""
from src.dcc.manager import DCCManager
from src.dcc.session import DCCSession
from src.dcc.base import DCCAdapter

class BrokenAdapter(DCCAdapter):
    name = "broken"
    def is_available(self):
        raise RuntimeError("simulated DCC failure")
    def scene_info(self):
        raise RuntimeError("scene unavailable")

class HealthyAdapter(DCCAdapter):
    name = "healthy"
    def is_available(self):
        return True
    def scene_info(self):
        return {"objects": 0}

def test_manager_isolates_broken_dcc():
    manager = DCCManager()
    manager.register("broken", DCCSession(BrokenAdapter()))
    manager.register("healthy", DCCSession(HealthyAdapter()))
    result = manager.connect_all()
    assert result["broken"] is False
    assert result["healthy"] is True
    status = manager.status()
    assert status["broken"]["connected"] is False
    assert status["healthy"]["connected"] is True
