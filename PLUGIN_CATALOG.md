# 3D DCC Plugin Library

本目录用于集中管理可复用的 Maya / 3ds Max 开源插件与工具，并为后续自研插件开发提供参考。

## 目录

- `plugins/maya/maya-usd` — Autodesk Maya USD
- `plugins/max/3dsmax-usd` — Autodesk 3ds Max USD
- `plugins/maya/gt-tools` — GT Tools
- `plugins/max/Py3dsMax` — Blur Studio Py3dsMax

## 1. Maya USD

上游：https://github.com/Autodesk/maya-usd  
定位：Maya ↔ OpenUSD 工作流基础插件。

主要功能：
- USD 导入 / 导出
- 直接加载 USD Stage 并在 Maya 中编辑
- Layer Editor
- USD Camera / Light
- MaterialX / LookdevX 集成
- Maya Reference / 动画与缓存工作流
- Python / C++ API，可扩展导入导出流程

版本：上游当前 dev 分支支持 Maya 2023–2027；实际部署应以对应 release 为准。

常用方式：
1. 安装对应 Maya 版本的 MayaUSD。
2. 在 Plug-in Manager 中加载插件。
3. 使用 Maya 的 USD 菜单或 Python API。
4. Python 中可使用 `maya.cmds` 调用 MayaUSD 导入/导出命令。

适合作为后续功能：
- Maya / Max 资产交换
- USD 资产浏览器
- 自动发布 / 版本化
- 材质与贴图路径检查
- 游戏资产批量导出

## 2. 3ds Max USD

上游：https://github.com/Autodesk/3dsmax-usd  
定位：3ds Max ↔ OpenUSD 的官方开源插件。

主要功能：
- USD 导入 / 导出
- 3ds Max USD 场景工作流
- Python API
- C++ SDK 扩展接口
- 适合构建 DCC 跨软件资产管线

常用方式：
1. 使用对应 3ds Max 版本的构建或 release。
2. 安装 / 配置插件。
3. 在 3ds Max 中启用 USD 插件。
4. 使用 UI 或 Python / MAXScript 进行自动化。

适合作为后续功能：
- Max → USD → Maya 自动转换
- 批量资产发布
- 游戏引擎资产中间格式
- 自动材质、路径和单位检查

## 3. GT Tools

上游：https://github.com/TrevisanGMW/gt-tools  
许可证：MIT

定位：Maya 的免费 Python 工具集合。

主要覆盖：
- 建模辅助
- 动画
- Rigging
- Mocap
- Pipeline
- Unity / Unreal 相关流程
- Qt / Python 工具开发

使用：
1. 获取仓库代码。
2. 按项目文档安装。
3. 在 Maya 的 Python 环境中加载工具。
4. 根据工具模块执行对应脚本或 UI。

适合作为后续自研插件的参考：
- Maya Python UI
- 工具面板设计
- 批处理
- Rig / Animation 工具
- Pipeline 工具架构

## 4. Py3dsMax

上游：https://github.com/blurstudio/Py3dsMax  
许可证：GPL

定位：让 3ds Max 的 MAXScript 与 Python 进行双向交互。

主要功能：
- MAXScript → Python
- Python → MAXScript
- Python 模块 / 类访问 MaxScript 对象
- 为 3ds Max Python 自动化提供桥接能力

使用：
1. 按项目文档编译 / 安装对应版本。
2. 在 3ds Max 中加载 Python 扩展。
3. Python 中调用 MaxScript，或从 MaxScript 导入 Python 模块。
4. 用它作为 Python 自动化与旧 MAXScript 工具之间的桥梁。

注意：该项目采用 GPL；如果后续把它的代码直接合并进自研插件，需要遵守 GPL 条款。因此本仓库以 Git submodule 方式保留上游源码，后续开发时应明确代码边界。

## 推荐的后续架构

```
plugins/
├── maya/
│   ├── maya-usd/
│   └── gt-tools/
├── max/
│   ├── 3dsmax-usd/
│   └── Py3dsMax/
└── shared/
    ├── pipeline/
    ├── asset/
    ├── material/
    ├── texture/
    ├── export/
    └── automation/
```

后续自研插件建议不要直接修改上游源码，而是在 `shared/` 或独立的 `src/` 中建立自己的功能层，通过 API / 命令 / Python 接口调用这些上游组件。

## 初始化子模块

```bash
git submodule update --init --recursive
```

## 当前固定版本

- Maya USD: dba37c85c3012bf63a7ae7aabc43aec8a7997ea1
- 3ds Max USD: 66477f2c2c0657c88ea74e43c37c3d9ac31219fc
- GT Tools: 68584b090f82ee442ef2884a0d15e605bb0de96f
- Py3dsMax: 0f59c3e0e398ebee592a7d69ffe8ef632e0c9b0d

固定 commit 的目的是让后续开发环境可复现；更新插件时应单独提交 submodule 指针变化。
