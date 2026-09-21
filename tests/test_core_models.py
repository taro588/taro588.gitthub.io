from src.core.asset import Asset
from src.core.task import Task
from src.core.pipeline import Pipeline
from src.core.registry import Registry
from src.core.validation import ValidationResult

def test_asset_roundtrip():
    a = Asset("crate", "crate.fbx", {"lod": 0})
    assert Asset.from_dict(a.to_dict()).name == "crate"

def test_task_lifecycle():
    t = Task("bake", "bake.create")
    t.succeed({"ok": True})
    assert t.status == "completed"
    t.fail("x")
    assert t.status == "failed"

def test_pipeline_isolates_optional_stage():
    p = Pipeline("test")
    p.add_stage("optional", lambda: 1, required=False)
    p.add_stage("required", lambda: 2)
    out = p.run()
    assert out["ok"]

def test_registry():
    r = Registry()
    r.register("x", 1)
    assert r.get("x") == 1
    assert r.names() == ["x"]

def test_validation_catches_validator_failure():
    result = ValidationResult()
    def bad(data, result):
        raise RuntimeError("boom")
    from src.core.validation import run_validation
    result = run_validation({}, [bad])
    assert not result.ok
    assert result.issues[0].code == "VALIDATOR_FAILED"
