import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_core_imports_without_dcc():
    code = """
import src.core.asset, src.core.task, src.core.pipeline
import src.core.registry, src.core.validation
print("ok")
"""
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr

def test_launcher_import_without_dcc():
    code = "from src.launcher import Launcher; print(Launcher().doctor()['status'])"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "ready" in out.stdout

def test_cli_detect_emits_json():
    out = subprocess.run([sys.executable, "-m", "src.launcher_cli", "detect"],
                         cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    json.loads(out.stdout)

def test_dcc_environment_does_not_force_native_imports():
    env = os.environ.copy()
    env.pop("MAYA_LOCATION", None)
    env.pop("ADSK_3DSMAX_ROOT", None)
    code = "from src.launcher import Launcher; print(Launcher().dcc_status())"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
