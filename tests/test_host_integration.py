from src.core.host_integration import HostIntegrator

def test_maya_user_setup_is_managed_without_overwriting_user_code(tmp_path, monkeypatch):
    scripts=tmp_path/"maya_scripts"
    monkeypatch.setenv("GAMEART_MAYA_USER_SCRIPTS", str(scripts))
    integrator=HostIntegrator(tmp_path/"toolkit")
    setup=scripts/"userSetup.py"
    scripts.mkdir()
    setup.write_text("print('user code')\n", encoding="utf-8")
    result=integrator.register_maya()
    assert result.ok
    text=setup.read_text(encoding="utf-8")
    assert "print('user code')" in text
    assert "GameArt Toolkit managed block BEGIN" in text
    assert integrator.unregister_maya().ok
    assert "print('user code')" in setup.read_text(encoding="utf-8")

def test_max_registration_is_user_level(tmp_path, monkeypatch):
    root=tmp_path/"toolkit"
    loader=root/"host-loaders"/"3ds_max"
    loader.mkdir(parents=True)
    (loader/"gameart_loader.ms").write_text("-- loader", encoding="utf-8")
    startup=tmp_path/"max_startup"
    monkeypatch.setenv("GAMEART_MAX_USER_STARTUP", str(startup))
    result=HostIntegrator(root).register_max()
    assert result.ok
    assert (startup/"GameArtToolkitStartup.ms").read_text(encoding="utf-8")=="-- loader"
