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


def test_launcher_doctor_is_ready_when_no_dcc_is_detected(tmp_path, monkeypatch):
    monkeypatch.delenv("MAYA_LOCATION", raising=False)
    monkeypatch.delenv("ADSK_3DSMAX_ROOT", raising=False)
    l=Launcher(LauncherConfig(tmp_path/"toolkit",tmp_path/"config"))
    d=l.doctor()
    assert d["status"]=="ready"
    assert set(d["dcc_warnings"])=={"maya","3ds_max"}
    assert d["dcc_failures"]==[]
