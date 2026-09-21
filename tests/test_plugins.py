from pathlib import Path
from src.core.plugins import PluginRegistry, PluginSpec

def test_plugin_registry_does_not_import_plugins(tmp_path):
    registry = PluginRegistry([PluginSpec("missing", tmp_path / "missing")])
    health = registry.health()
    assert health[0].state == "missing"

def test_plugin_registry_duplicate_requires_replace(tmp_path):
    registry = PluginRegistry()
    spec = PluginSpec("x", tmp_path)
    registry.register(spec)
    try:
        registry.register(spec)
        assert False
    except KeyError:
        pass
