import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_python(code, env=None):
    return subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)

def test_core_imports_without_dcc():
    out = run_python("import src.core.asset, src.core.task, src.core.pipeline; import src.core.registry, src.core.validation; print('ok')")
    assert out.returncode == 0, out.stderr

def test_optional_layers_import_without_external_sdks():
    out = run_python("import src.ai.provider, src.pbr.schema, src.mcp; print('ok')")
    assert out.returncode == 0, out.stderr

def test_launcher_import_without_dcc():
    out = run_python("from src.launcher import Launcher; print(Launcher().doctor()['status'])")
    assert out.returncode == 0, out.stderr

def test_cli_detect_emits_json():
    out = subprocess.run([sys.executable, "-m", "src.launcher_cli", "detect"], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    json.loads(out.stdout)

def test_launcher_gui_module_imports_without_tk_startup():
    out = run_python("import src.launcher_gui; print('ok')")
    assert out.returncode == 0, out.stderr

def test_dcc_environment_does_not_force_native_imports():
    env = os.environ.copy()
    env.pop("MAYA_LOCATION", None)
    env.pop("ADSK_3DSMAX_ROOT", None)
    out = run_python("from src.launcher import Launcher; print(Launcher().dcc_status())", env)
    assert out.returncode == 0, out.stderr
