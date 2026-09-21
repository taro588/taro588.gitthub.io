from src.core.plugin_installer import PluginInstaller

def test_generate_host_loaders_stays_inside_toolkit(tmp_path):
    root=tmp_path/"toolkit"
    installer=PluginInstaller(root)
    paths=installer.generate_host_loaders()
    assert len(paths)==2
    assert (root/"host-loaders"/"maya"/"gameart_loader.py").exists()
    assert (root/"host-loaders"/"3ds_max"/"gameart_loader.ms").exists()
    assert all(str(root) in p for p in paths)

def test_host_loaders_are_generated_on_successful_install(tmp_path, monkeypatch):
    installer=PluginInstaller(tmp_path/"toolkit")
    class Result:
        returncode=0
        stdout=""
        stderr=""
    def fake_git(*args, **kwargs):
        destination=__import__("pathlib").Path(args[-1])
        destination.mkdir(parents=True)
        (destination/"plugin.py").write_text("PLUGIN=True", encoding="utf-8")
        return Result()
    monkeypatch.setattr(installer, "_git", fake_git)
    result=installer.install("texture-importer")
    assert result.ok
    assert (tmp_path/"toolkit"/"host-loaders"/"maya"/"gameart_loader.py").exists()
