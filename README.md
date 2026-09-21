# GameArt AI Toolkit

一个面向游戏美术生产的 Maya / 3ds Max / PBR / AI 自动化工具平台。

## 项目定位

AI Agent → Pipeline Engine → DCC Adapter → ThirdParty / PBR / Validation → Unreal / Unity

目标是让用户可以用自然语言描述资产需求，由 AI 规划并执行标准化游戏资产生产流程。

## 当前架构

- Core：Asset / Task / Pipeline / Registry / Validation
- DCC：MayaAdapter / MaxAdapter
- AI：Planner / Executor / Reviewer / Vision
- MCP：为 AI 提供结构化 DCC 与 Pipeline 工具
- PBR：统一纹理、材质与 AI/程序化生成接口
- ThirdParty：以 Git Submodule 管理第三方项目

## 文档

- docs/ARCHITECTURE_V1.md
- docs/DEVELOPMENT_ROADMAP.md
- PLUGIN_CATALOG.md

## 核心原则

1. 插件是能力，不是架构。
2. Pipeline 是核心。
3. AI 负责规划与决策，Engine 负责执行。
4. 所有自动化结果必须经过 Validation。
5. 第三方依赖与自研代码隔离。
6. AI Provider 可替换。
7. 云端 AI 与本地 AI 并存。
