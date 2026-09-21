# 启动 GameArt AI Toolkit

## Windows
双击 `START_WINDOWS.bat`。

要求：Python 3.10+。

第一次启动会创建项目自己的 `.venv`，不会修改 Maya / 3ds Max 的 Python 环境。

## PowerShell
运行 `START_WINDOWS.ps1`。

## 开发模式
```bash
python -m src.launcher_cli start
```

## 当前 0.1 Alpha
启动器已经可以独立运行。没有安装 Maya 或 3ds Max 时，Toolkit 仍然可以启动并显示检测结果。

下一阶段会接入真实 Maya / 3ds Max Adapter、安装器和 DCC 内嵌面板。
