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
    def ping(self, value="ok"):
        return {"value": value}

class BrokenOperationAdapter(HealthyAdapter):
    def ping(self, value="ok"):
        raise RuntimeError("operation failed")

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

def test_operation_failure_isolated():
    manager = DCCManager()
    manager.register("broken", DCCSession(BrokenOperationAdapter()))
    manager.connect_all()
    result = manager.execute("broken", "ping")
    assert result["ok"] is False
    assert "operation failed" in result["error"]

def test_unknown_operation_isolated():
    manager = DCCManager()
    manager.register("healthy", DCCSession(HealthyAdapter()))
    manager.connect_all()
    result = manager.execute("healthy", "does_not_exist")
    assert result["ok"] is False
    assert "Unsupported DCC operation" in result["error"]

def test_duplicate_registration_requires_replace():
    manager = DCCManager()
    manager.register("healthy", DCCSession(HealthyAdapter()))
    try:
        manager.register("healthy", DCCSession(HealthyAdapter()))
        assert False, "duplicate registration should fail"
    except KeyError:
        pass
