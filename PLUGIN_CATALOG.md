

## 第四批：游戏资产生产 / LOD / Unreal / FBX

### 16. Unreal-Maya-Pipeline — Maya
上游：https://github.com/arunprksm/Unreal-Maya-Pipeline
Maya → Unreal 的资产流程参考，适合研究命名、导出和引擎接入自动化。

### 17. 3dsMax Asset Tools for Unreal Engine — 3ds Max
上游：https://github.com/dexise/3dsMax-Asset-Tools-for-Unreal-Engine
GPL-3.0。面向 3ds Max → Unreal 的资产制作/导出辅助工具。作为独立 Submodule 保存，后续直接复用代码前需要遵守 GPL。

### 18. LOD Generator Tool Maya — Maya
上游：https://github.com/NguyenNP-24/LOD-Generator-Tool-Maya
GPL-3.0。用于 Maya 自动生成 LOD，适合研究批量 LOD 工作流。

### 19. Automated LOD Tool — Maya
上游：https://github.com/SaiiPrashanth/Automated_LOD_Tool
MIT。自动化 LOD 生成工具，可作为后续统一 LOD 面板的参考。

### 20. LeeAutoExportFBX — Maya
上游：https://github.com/leetdvn/LeeAutoExportFBX
自动 FBX 导出工具，适合研究 Maya 批量导出和游戏资产发布流程。

### 21. 3dsMax FBX Conform + Batch Render — 3ds Max
上游：https://github.com/Joyxt/3dsmax-fbx-conform_and_batch-render
用于 FBX 规范化和批量处理/渲染，适合接入统一资产发布流程。

## 第四批重点工作流
**模型 → LOD → FBX → Unreal/Unity → 自动检查 → 批量发布**。

下一阶段可以把这些零散工具抽象成自己的统一 UI，而不是让最终用户分别安装多个插件。
