from src.core.plugin_loader import PluginLoader

def test_plugin_loader_discovery_rejects_outside_path(tmp_path):
    loader=PluginLoader(tmp_path/"toolkit")
    loader.manifest_root.mkdir(parents=True)
    outside=tmp_path/"outside"; outside.mkdir()
    (loader.manifest_root/"bad.json").write_text(
        '{"name":"bad","path":"'+str(outside).replace("\\","\\\\")+'"}',
        encoding="utf-8",
    )
    result=loader.discover()[0]
    assert result["state"]=="invalid_manifest"

def test_plugin_loader_quarantines_import_failure(tmp_path):
    root=tmp_path/"toolkit"
    plugin=root/"plugins"/"shared"/"broken"
    plugin.mkdir(parents=True)
    (plugin/"__init__.py").write_text("raise RuntimeError('plugin boom')",encoding="utf-8")
    manifests=root/"plugin-manifests"; manifests.mkdir(parents=True)
    (manifests/"broken.json").write_text(
        '{"name":"broken","path":"'+str(plugin).replace("\\","\\\\")+'"}',
        encoding="utf-8",
    )
    result=PluginLoader(root).load_python("broken")
    assert not result.ok and result.state=="quarantined"
