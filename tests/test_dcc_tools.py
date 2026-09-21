from src.dcc.manager import DCCManager
from src.dcc.session import DCCSession
from src.dcc.tools import build_dcc_tool_registry
from src.dcc.base import DCCAdapter

class FakeAdapter(DCCAdapter):
    name = "fake"
    def is_available(self): return True
    def scene_info(self): return {"scene": "test"}
    def ping(self): return {"ok": True, "dcc": self.name}

class BrokenAdapter(DCCAdapter):
    name = "broken"
    def is_available(self): return True
    def scene_info(self): raise RuntimeError("scene boom")
    def ping(self): raise RuntimeError("ping boom")

def test_structured_dcc_tools_route_through_session():
    manager = DCCManager()
    manager.register("fake", DCCSession(FakeAdapter()))
    manager.connect_all()
    registry = build_dcc_tool_registry(manager)
    assert registry.call("scene.ping", dcc="fake")["result"]["ok"]
    assert registry.call("scene.get_info", dcc="fake")["result"]["scene"] == "test"

def test_structured_dcc_tool_failure_isolated():
    manager = DCCManager()
    manager.register("broken", DCCSession(BrokenAdapter()))
    manager.connect_all()
    registry = build_dcc_tool_registry(manager)
    result = registry.call("scene.ping", dcc="broken")
    assert not result["ok"]
    assert "ping boom" in result["error"]
    assert manager.status()["broken"]["connected"]
