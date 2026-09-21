from src.core.plugins import PluginRegistry, PluginSpec

def test_plugin_registry_does_not_import_plugins(tmp_path):
    h = PluginRegistry([PluginSpec("missing", tmp_path / "missing")]).health()
    assert h[0].state == "missing"

def test_plugin_registry_duplicate_requires_replace(tmp_path):
    r = PluginRegistry()
    s = PluginSpec("x", tmp_path)
    r.register(s)
    try:
        r.register(s)
        assert False
    except KeyError:
        pass

def test_plugin_compatibility(tmp_path):
    r = PluginRegistry([PluginSpec("maya_tool", tmp_path, host="maya", min_host_version="2024", max_host_version="2026")])
    assert r.health({"maya": "2025"})[0].state == "available"
    assert r.health({"maya": "2027"})[0].state == "incompatible"

def test_plugin_quarantine(tmp_path):
    r = PluginRegistry([PluginSpec("x", tmp_path)])
    r.disable("x")
    assert r.health()[0].state == "disabled"
