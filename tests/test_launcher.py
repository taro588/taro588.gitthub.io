from src.launcher import Launcher, LauncherConfig

def test_launcher_doctor_reports_storage(tmp_path):
    l=Launcher(LauncherConfig(tmp_path/"toolkit",tmp_path/"config"))
    d=l.doctor()
    assert "launcher" in d and "writable" in d["launcher"]

def test_launcher_repair_creates_config(tmp_path):
    config=LauncherConfig(tmp_path/"toolkit",tmp_path/"config")
    l=Launcher(config)
    result=l.repair()
    assert result["ok"]
    assert config.config_root.exists()
