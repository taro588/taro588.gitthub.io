from src.core.pipeline_guard import PipelineGuard

def test_preflight_reports_missing():
    result = PipelineGuard().preflight({"mesh": "x", "uv": None})
    assert not result.ok
    assert result.data["missing"] == ["uv"]

def test_guard_contains_callback_failure():
    result = PipelineGuard().execute("bake", lambda: 1 / 0)
    assert not result.ok
    assert "ZeroDivisionError" in result.message
