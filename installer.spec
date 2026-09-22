# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.building.datastruct import Tree
from PyInstaller.utils.hooks import collect_submodules

hiddenimports=collect_submodules("src")
datas=[Tree("src", prefix="src")]

a=Analysis(
    ["src/installer_app.py"],
    pathex=["."],
    hiddenimports=hiddenimports,
    datas=datas,
    binaries=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz=PYZ(a.pure)
exe=EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="GameArtToolkitInstaller",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
