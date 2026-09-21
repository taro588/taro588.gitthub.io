from src.core.export import safe_export

def test_safe_export_requires_actual_output(tmp_path):
    target = tmp_path / "asset.fbx"
    result = safe_export(lambda: {"exported": True}, target, "fbx")
    assert not result.ok
    assert "did not create" in result.error

def test_safe_export_success(tmp_path):
    target = tmp_path / "asset.fbx"
    result = safe_export(lambda: target.write_text("fbx"), target, "fbx")
    assert result.ok
    assert target.exists()
