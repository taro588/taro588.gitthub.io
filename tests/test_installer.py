from src.core.installer import ToolkitInstaller

def test_install_creates_owned_structure(tmp_path):
    r=ToolkitInstaller(tmp_path/"toolkit").install()
    assert r.ok and (tmp_path/"toolkit"/"versions").exists()

def test_repair_creates_missing_structure(tmp_path):
    root=tmp_path/"toolkit"; r=ToolkitInstaller(root).repair()
    assert r.ok and (root/"current").exists()

def test_installer_refuses_outside_root(tmp_path):
    try: ToolkitInstaller(tmp_path/"toolkit")._owned(tmp_path/"outside"); assert False
    except ValueError: pass

def test_uninstall_does_not_touch_sibling(tmp_path):
    sibling=tmp_path/"user_asset.txt"; sibling.write_text("keep")
    root=tmp_path/"toolkit"; ToolkitInstaller(root).install()
    assert ToolkitInstaller(root).uninstall().ok and sibling.read_text()=="keep"

def test_update_source_cannot_be_inside_root(tmp_path):
    root=tmp_path/"toolkit"; ToolkitInstaller(root).install(); source=root/"versions"/"source"; source.mkdir(parents=True)
    assert not ToolkitInstaller(root).stage_update(source).ok

def test_activate_and_rollback_preserves_version_identity(tmp_path):
    root=tmp_path/"toolkit"; i=ToolkitInstaller(root); i.install()
    a=tmp_path/"v1"; a.mkdir(); (a/"marker").write_text("v1")
    b=tmp_path/"v2"; b.mkdir(); (b/"marker").write_text("v2")
    assert i.stage_update(a,"v1").ok and i.activate("v1").ok
    assert i.stage_update(b,"v2").ok and i.activate("v2").ok
    r=i.rollback()
    assert r.ok and r.version=="v1"
    assert (root/"current"/"marker").read_text()=="v1"

def test_manifest_tamper_blocks_activation(tmp_path):
    root=tmp_path/"toolkit"; i=ToolkitInstaller(root); i.install()
    src=tmp_path/"v1"; src.mkdir(); (src/"marker").write_text("good")
    assert i.stage_update(src,"v1").ok
    (root/"versions"/"v1"/"marker").write_text("tampered")
    r=i.activate("v1")
    assert not r.ok and "checksum mismatch" in r.error
