from src.core.asset_inspector import inspect_asset
from src.core.validators import run_validators
from src.core.pipeline_guard import PipelineGuard

def test_asset_inspector_handles_invalid_counts():
    report = inspect_asset({"name": "crate", "objects": "bad"})
    assert not report.ok
    assert any(i.code == "OBJECT_COUNT_INVALID" for i in report.issues)

def test_asset_inspector_rejects_non_mapping():
    try:
        inspect_asset([])
        assert False, "non-mapping input should fail"
    except TypeError:
        pass

def test_validators_reject_non_mapping():
    try:
        run_validators([])
        assert False, "non-mapping input should fail"
    except TypeError:
        pass

def test_validators_report_invalid_uv_and_materials():
    report = run_validators({"name": "crate", "triangles": 100, "uv_sets": "bad", "materials": None})
    assert not report.ok
    assert any(i.code == "UV_SETS_INVALID" for i in report.issues)

def test_pipeline_guard_stops_after_failure():
    guard = PipelineGuard()
    results = guard.run([("check", lambda: 1), ("broken", lambda: 1 / 0), ("never", lambda: 1)])
    assert len(results) == 2
    assert not results[-1].ok
