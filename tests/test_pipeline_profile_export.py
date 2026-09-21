from src.core.pipeline_profile import get_profile
from src.core.export import validate_export_path, safe_export

def test_profiles():
    assert get_profile("UE5_PC").lod_count == 3

def test_export_path_rejects_unknown_format(tmp_path):
    try:
        validate_export_path(tmp_path / "x.obj")
        assert False
    except ValueError:
        pass

def test_safe_export_contains_failure(tmp_path):
    out=safe_export(lambda: 1/0, tmp_path/"x.fbx", "fbx")
    assert not out.ok
    assert "ZeroDivisionError" in out.error

def test_export_rejects_directory(tmp_path):
    try:
        validate_export_path(tmp_path)
        assert False
    except ValueError:
        pass
