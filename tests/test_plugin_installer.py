from src.core.plugin_installer import PluginInstaller

def test_plugin_resolve_known_plugin(tmp_path):
    installer = PluginInstaller(tmp_path)
    spec = installer.resolve("texture-importer")
    assert spec["host"] == "maya"
    assert spec["url"].startswith("https://github.com/")

def test_plugin_source_is_restricted_to_github_https(tmp_path):
    installer = PluginInstaller(tmp_path)
    for source in ("http://github.com/a/b.git", "https://evil.example/a.git", "file:///tmp/a"):
        try:
            installer._validate_source(source)
            assert False
        except ValueError:
            pass

def test_plugin_install_failure_does_not_pollute_destination(tmp_path, monkeypatch):
    installer = PluginInstaller(tmp_path)
    class Result:
        returncode = 1
        stdout = ""
        stderr = "clone failed"
    monkeypatch.setattr(installer, "_git", lambda *args, **kwargs: Result())
    result = installer.install("texture-importer")
    assert not result.ok
    assert not (tmp_path / "plugins" / "maya" / "texture-importer").exists()

def test_plugin_manifest_roundtrip(tmp_path):
    installer = PluginInstaller(tmp_path)
    installer.manifest_root.mkdir(parents=True)
    (installer.manifest_root / "x.json").write_text('{"name":"x","host":"shared"}', encoding="utf-8")
    assert installer.installed() == [{"name":"x","host":"shared"}]
