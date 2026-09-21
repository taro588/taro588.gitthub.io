from src.core.installer import ToolkitInstaller

def test_install_creates_owned_structure(tmp_path):
    r=ToolkitInstaller(tmp_path/"toolkit").install()
    assert r.ok
    assert (tmp_path/"toolkit"/"versions").exists()

def test_installer_refuses_outside_root(tmp_path):
    i=ToolkitInstaller(tmp_path/"toolkit")
    try:
        i._owned(tmp_path/"outside")
        assert False
    except ValueError:
        pass

def test_uninstall_does_not_touch_sibling(tmp_path):
    sibling=tmp_path/"user_asset.txt"; sibling.write_text("keep")
    root=tmp_path/"toolkit"; ToolkitInstaller(root).install()
    r=ToolkitInstaller(root).uninstall()
    assert r.ok and sibling.read_text()=="keep"
