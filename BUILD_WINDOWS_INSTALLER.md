# Windows 一键安装器

构建机执行：

    python -m pip install -U pyinstaller
    pyinstaller --clean installer.spec

产物：

    dist/GameArtToolkitInstaller.exe

最终用户只需双击 EXE，不需要安装 Python。

GitHub Actions 也会在推送 v* tag 后自动构建 Windows EXE。