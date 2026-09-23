---
title: Windows-MCP 开源——AI 直接操作 Windows
updated: 2026-09-23
tags: [AI工具, MCP, Windows, 自动化, computer-use]
status: active
source: 抖音 @电脑依森 https://v.douyin.com/xsm1t8zWsDM/ （item 7688037823143873842）+ GitHub 官方仓库核验
---

# Windows-MCP 开源——AI 直接操作 Windows

> 视频主张：Windows-MCP 开源了，AI 能直接操作你的电脑。已对照 GitHub 官方仓库（CursorTouch/Windows-MCP）逐条核实。

**一句话结论**：真实存在、真开源（MIT）、真被 Claude Desktop 收为官方桌面扩展——它是一套**基于 Windows UI 自动化（UIA 无障碍树）的 MCP 服务器**，让任意大模型获得「键鼠 + 窗口 + 应用启动 + PowerShell」的完整电脑操作能力。与传统截图视觉方案相比，它**不需要视觉模型**，走的是读控件树的路线。

## 项目速览（官方口径）

| 项目 | 内容 |
|:--|:--|
| 仓库 | CursorTouch/Windows-MCP（另有多个镜像 fork） |
| 热度 | 约 6.4k star / 769 fork，最新 release v0.8.2 |
| 许可 | MIT，完全开源 |
| 依赖 | Python 3.13+、UV 包管理器 |
| 系统 | Windows 7 ~ 11 全覆盖（老系统兼容是卖点） |
| 速度 | 单步动作延迟约 0.2~2.5 秒（不同版本口径有差，另加 LLM 推理时间） |
| 集成 | Claude Desktop（官方 Desktop Extension）、Gemini CLI、Qwen Code、Codex CLI、Perplexity Desktop 均给出配置方法 |

## 工具清单（14 件套）

- **基础操作**：Click / Move / Drag / Scroll / Key / Shortcut（快捷键）/ Type / Clipboard
- **感知**：State-Tool（一次性快照：活动窗口 + 可交互元素树 + 截图）、Screenshot-Tool
- **执行**：Launch-Tool（从开始菜单启动应用）、Shell-Tool（执行 PowerShell）、Scrape-Tool（抓网页内容）、Wait-Tool
- 核心亮点是 **State-Tool 的 use_dom 模式**：浏览器自动化时只抓页面内容、过滤掉浏览器 UI 杂音，支持 Chrome/Edge/Firefox

## 视频口径 vs 官方口径

| 视频说法 | 核验结论 |
|:--|:--|
| "AI 能直接操作你的电脑" | ✅ 成立，但走的是 **UIA 控件树**而非纯截图视觉，中文窗口/非英文系统兼容性一般（官方建议英文系统，否则需禁用 Launch/Switch 工具） |
| "开源了" | ✅ MIT 协议，可商用可魔改 |
| （未提）风险 | ⚠️ 官方明写 **Caution**：直接操作操作系统、无沙箱、无审计日志，提示词注入风险真实存在 |

## 已知短板（官方 Limitations 摘录）

1. 依赖无障碍树 → **段落内精确选中文本**做不到（开发中）
2. Type-Tool 是"整段打字"，**不适合在 IDE 里写代码**
3. 单步 0.2~2.5 秒 + LLM 推理，**做不了亚 100ms 实时任务**

## 与同类工具的位置

- **OpenAI computer-use / JEV（System One）**：视觉截图路线 → 看图判断，通用但贵、慢
- **Windows-MCP**：控件树路线 → 不吃视觉模型、任意 LLM 可用、延迟低，但碰见自绘 UI/游戏界面就抓瞎
- 两者可组合：State-Tool 提供结构化状态，视觉模型兜底非常规界面

## 落地对接（本机与园区场景）

- **本机可行性**：✅ 纯 CPU，Python 3.13 + UV 即可，不占 GPU、磁盘占用小（C 盘 4.3G 也装得下，建议装 D 盘）；LLM 走云端 API 即可。比 DSH 更轻。
- **园区办公自动化**：适合把"每天打开 XX 系统录一遍数据"这类重复操作交给 Agent——财务报税门户、物业报修后台、 OA 审批等**没有 API 的老系统**正是它的主场（老系统兼容到 Win7 是差异化优势）
- **风险提示**：绝不在存有客户敏感数据/财务系统登录态的机器上放开了跑；给 Agent 用**专用低权限账户**，Shell-Tool 是最大风险面
- **注意代理**：GitHub 直连被拦，clone 走镜像

## 来源说明

笔记依据 GitHub 官方仓库（CursorTouch/Windows-MCP）README 及第三方评测页核实整理；抖音视频正文文案未能直接抓取，视频口径仅取标题与账号（@电脑依森），非逐字转录。

## 相关链接

- [[视频笔记目录]]
- [[豆包视频解读/AI工具/JEV-SystemOne判断模型-computer-use提速-20260922.md]] — 视觉路线的"快判断"补件
