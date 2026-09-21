

## 第五批：PBR 贴图 / 烘焙 / Substance Painter

### 22. texture-importer — Maya / 3ds Max
MIT。根据文件夹中的贴图自动识别并创建材质节点网络，适合 BaseColor / Normal / Roughness / Metallic / AO 自动接材质。citeturn0search13

### 23. ToTex — 3ds Max
3ds Max MaxScript 纹理烘焙工具，可快速将多张纹理 Bake 到指定文件夹。citeturn0search6

### 24. MayaToPainter — Maya
MIT。Maya → Substance Painter 桥接，支持高低模烘焙准备、自动命名和更新模型。citeturn0search2

### 25. SubstancePainterToMaya — Maya
自动读取 Substance Painter 输出的贴图并连接到 Maya 材质，支持 Arnold、VRay、Redshift、Renderman 和 UDIM。citeturn0search1

### 26. rename-lowhigh-proximity — 3ds Max
MIT。根据模型空间位置帮助匹配/重命名 low/high poly 对，专门用于烘焙准备。citeturn0search12

## PBR 自动化方向
Low/High 自动匹配 → Bake → BaseColor/Normal/AO/Roughness/Metallic → 自动导入材质 → UDIM → 引擎材质 → 发布。


## 第六批：程序化 PBR / AI 贴图 / Substance Designer

### 27. PATINA / fal-texture-pbr-generator — Shared
上游：https://github.com/lovisdotio/fal-texture-pbr-generator
MIT。AI PBR 贴图生成器，可通过文字或图片生成 BaseColor、Normal、Roughness、Metallic、Height，并提供 3D 材质预览及 ZIP 导出；项目使用 fal.ai PATINA 模型。citeturn0search0

适合后续接入：
- AI 生成游戏材质
- 图片 → PBR
- 文字 → 无缝材质
- 2K / 4K 贴图生产
- 自动输出 Substance / Unreal / Unity 命名格式

### 28. Procedural-PBR — Shared
上游：https://github.com/Whappens/Procedural-PBR
MIT。Python 程序化 PBR 贴图生成器，包含砖、草、云、液体、水、雪、冰等材质生成器，能够生成 Albedo、Normal、ORM、Displacement，并支持 1K/2K/4K、style 和 seed。citeturn0search6

这个项目特别适合拿来做我们自己的“程序化材质生成核心”。

### 29. SubstanceDesignerTools — Substance Designer
上游：https://github.com/Gil-1/SubstanceDesignerTools
MIT。包含 Substance Designer 的 SBS 工具；其中 Simple Triplanar Texturer 可以基于 Vertex Position / World Space Normal 快速生成 Base Color、Normal、Roughness、Metallic。citeturn0search1

## PBR 自动化核心架构
后续建议将这些工具统一到：

**输入照片/文字 → AI/程序化生成 → Seamless → Height → Normal → Roughness → Metallic → AO → ORM → 2K/4K → 材质预览 → Substance → Maya/Max → Unreal/Unity**

MaterialX 也应作为跨 DCC / 引擎的材质交换层。Khronos 的 MaterialX/glTF 工具已经支持将特定 MaterialX procedural graphs 映射到 glTF PBR。citeturn0search3turn0search9
