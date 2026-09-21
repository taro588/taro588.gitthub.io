

## 第三批：建模 / UV / 重拓扑 / AI 自动化

### 11. froRetopo — Maya
上游：https://github.com/Froyok/froRetopo
MIT。专注 Maya 快速重拓扑，让高模转干净低模更方便。

### 12. OPEN KITBASH — 3ds Max
上游：https://github.com/imanshirani/OPEN_KITBASH
MIT。面向硬表面、环境制作和概念设计的资产浏览/Kitbash 工具，可浏览和插入 MAX/OBJ/FBX，并自动生成缩略图；还包含 Chamfer、FFD、Bend 等辅助功能。citeturn0search6

### 13. Maya-SBTools — Maya
上游：https://github.com/Amatsukast/Maya-SBTools
GPL-3.0。集合 Maya 建模、拓扑、Retopology 等实用脚本，适合作为工具设计参考。

### 14. RizomUV Maya Bridge — Maya
上游：https://github.com/adevra/RizomUV-2024-Maya-Bridge
用于 Maya 与 RizomUV 联动，支持 UV Set、自动 Unwrap、Unfold/Optimize、Pack、UDIM 等工作流。适合游戏资产 UV 自动化。citeturn0search15

### 15. 3dsmax-mcp — 3ds Max
上游：https://github.com/cl0nazepamm/3dsmax-mcp
MIT。通过 MCP 让 AI 客户端直接操作 3ds Max，可创建/编辑模型、曲线、Loft、检查拓扑等。它非常适合作为后续“AI 操作 Max”的基础设施；仓库 README 也提供了建模和 geometry QA 等工具示例。citeturn0search14

### 本批重点
这批把工具链补到了：
**建模 → Kitbash → Retopo → UV → AI 自动化**。

另外，3ds Max 2026 本身已经提供 Retopology Tools 和 Attribute Transfer，可用于重拓扑以及 UV、Normals、Vertex Color 等属性转移，因此后续自研插件可以直接围绕这些原生能力做批处理和一键化，而不是重复造底层轮子。citeturn0search0turn0search2
