import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(*args, env=None):
    return subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,env=env or os.environ.copy())

def test_core_imports_without_dcc():
    out=run("-c","import src.core.asset, src.core.task, src.core.pipeline, src.core.registry, src.core.validation; print('ok')")
    assert out.returncode==0, out.stderr

def test_launcher_import_without_dcc():
    out=run("-c","from src.launcher import Launcher; print(Launcher().doctor()['status'])")
    assert out.returncode==0, out.stderr
    assert out.stdout.strip() in {"ready","degraded"}

def test_cli_detect_emits_json():
    out=run("-m","src.launcher_cli","detect")
    assert out.returncode==0, out.stderr
    json.loads(out.stdout)

def test_cli_lifecycle_help():
    out=run("-m","src.launcher_cli","--help")
    assert out.returncode==0
    for name in ("install","repair","update","activate","rollback","uninstall"): assert name in out.stdout

def test_dcc_environment_does_not_force_native_imports():
    env=os.environ.copy(); env.pop("MAYA_LOCATION",None); env.pop("ADSK_3DSMAX_ROOT",None)
    out=run("-c","from src.launcher import Launcher; print(Launcher().dcc_status())",env=env)
    assert out.returncode==0, out.stderr

def test_plugin_installer_import_without_git_operation():
    out=run("-c","from src.core.plugin_installer import PluginInstaller; print(PluginInstaller('x').resolve('texture-importer')['host'])")
    assert out.returncode==0, out.stderr
    assert out.stdout.strip()=="maya"
