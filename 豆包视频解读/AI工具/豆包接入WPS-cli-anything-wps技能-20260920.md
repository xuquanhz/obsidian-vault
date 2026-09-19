---
title: 豆包接入WPS教程——cli-anything-wps技能（GitHub核验版）
updated: 2026-09-20
tags: [AI工具, 豆包, WPS, cli-anything-wps, harness-anything, 自动化, 视频笔记]
status: 已完成
source: 抖音@少陵 https://v.douyin.com/NJ7wFSbIwNI/ ｜ 官方核验：github.com/yb2460/harness-anything、WPS官方社区
---

> **视频主张**：装好 cli-anything-wps 技能后，豆包能直接操作真实 WPS 做 PPT、Word、表格，重复排版工作不再手动做。
> **核心机制**：不是生成文件模拟，而是通过 Windows COM 接口**操控真实的 WPS 程序**——渲染效果与手动操作完全一致。

**一句话结论**：教程真实可信（GitHub 开源项目 + WPS 官方社区背书），豆包「工作」模式全自动安装约 14 分钟；会手动装的人用一条 pip 命令更快。适合 Windows + WPS 用户给豆包装上办公自动化手脚。

## 🎬 视频档案

| 项目 | 内容 |
| --- | --- |
| 作者 | 抖音 @少陵（粉丝 148，获赞 4554） |
| 发布 | 2026-09-19 16:15 |
| 时长 | 24 秒屏录教程 |
| 互动 | 848 赞 / 4 评 / **1310 藏** / 206 转（收藏>点赞，干货型） |
| 标签 | #豆包工作 #豆包操作电脑 #wps #github |
| 热评 | 「要开豆包会员吗？」——视频未回答，以豆包官方现行资费为准 |

## 📹 视频演示流程还原（截帧逐段确认）

1. **切模式**：豆包界面顶部「对话 / 工作」，切到**工作**任务模式 + 本地电脑。
2. **装技能**：直接发对话指令「**帮安装 github 上的 yb2460/harness-anything 技能**」，豆包自动完成（视频记录耗时 **13 分 51 秒**），一次装好 3 个技能：

| 技能 | 功能 | CLI 命令 |
| --- | --- | --- |
| cli-anything-wps | WPS 文字/表格/演示文稿自动化，JSON 驱动 PPT 生成 | `cli-anything-wps` |
| cli-anything-zotero | Zotero 文献管理（搜索/引用/笔记 + 27 个学术技能） | `python -m cli_anything.zotero` |
| cli-anything-photoshop | Photoshop 图像自动化 | `cli-anything-photoshop` |

3. **使用前提**（视频内说明页）：Windows（COM 接口专有，不支持 macOS/Linux）；需已安装对应软件（WPS Office / Zotero / Photoshop）；pywin32 已随包安装。**新装技能需重启当前会话**才会被技能系统识别加载。
4. **下指令**：「参考这里的资料，打开 WPS 自动做一份市场分析报告的 PPT」（可挂本地参考资料，输入框显示 Cli Anything Wps 技能徽章）。
5. **豆包后台执行**（视频过程日志）：验证 WPS 安装状态 → WPS COM 接口可用 → matplotlib 生成图表 → 创建数据文件 → 运行 build.py 生成 PPT。
6. **成品**：**真实 WPS 演示文稿窗口**打开——《新能源汽车市场分析》3 页，含销量数据卡片、饼图、特征标签，渲染与手动制作一致。
7. **收尾**：不需要时让豆包关闭 WPS 或结束当前任务。

## ✅ 视频口径 vs 官方口径核实

| 视频口径 | 官方核验（GitHub README / WPS 社区） | 结论 |
| --- | --- | --- |
| Cli Anything Wps 技能真实存在 | `yb2460/harness-anything` 开源仓库，WPS 官方社区有介绍帖 | ✔️ |
| 让豆包做 PPT/Word/表格 | 47 条 CLI 命令覆盖 Writer（导出 DOCX/PDF/TXT/HTML/RTF/ODT）、Calc（XLSX/PDF/CSV/HTML）、Impress（PPTX/PDF）；PPT 设计系统 4 预设 + 14 布局 + 5 维度质检 | ✔️ 且功能比视频讲的更多 |
| 装好即用 | 系统要求：Windows 10/11 + WPS Office 2019+ + Python 3.10+ + pywin32 | ⚠️ 有前置条件，手动安装时 pywin32 需自己 `pip install pywin32`（豆包自动装时已处理） |
| 「渲染效果和手动一致」 | 底层是 COM 调用真实 WPS 进程，非文件格式模拟 | ✔️ 机制属实 |
| —（视频未提） | 持有 MS Office 者修改 ProgID 可切换操控 Word/Excel/PowerPoint；支持 JSON 输出、REPL、撤销/重做 50 步、后台批量模式 | 📌 补充价值 |
| —（视频未提） | 手动安装仅一条命令：`pip install git+https://github.com/yb2460/cli-anything-wps.git` | 📌 不想等 14 分钟可手动装 |

## 🖥️ 本机适配判断（AMD 主机 / 无 N 卡场景）

| 条件 | 本机状态 | 判定 |
| --- | --- | --- |
| Windows 10/11 | Windows | ✔️ |
| WPS Office 2019+ | 以本机实际安装版本为准 | 大概率 ✔️ |
| Python 3.10+ | 3.13.12 / 3.11.8 已装 | ✔️ |
| pywin32 | 未装，需进 venv 安装 | ⚠️ 一步搞定 |
| GitHub 直连 | 代理拦 CONNECT，**pip install git+github 会失败** | ⚠️ 改走镜像：`pip install git+https://ghfast.top/https://github.com/yb2460/cli-anything-wps.git` |
| 资源占用 | COM 操控真实 WPS，无需 GPU、无大模型 | ✔️ 老机器无压力 |

## 🎯 落地对接

- **在 WorkBuddy 里不需要它**：本知识库会话已有 `tencent-local-office-edit`（实时读写本机 Office/WPS 文件）与 docx/xlsx/pptx 生成技能，做文档表格直接用这些更快。
- **值得借鉴的场景**是「豆包客户端工作模式」：把 GitHub 项目名直接丢给 Agent 让它自己装、自己试错、自己汇报——这套「对话即安装」的交互范式比装什么技能更值得学。
- **与既有笔记联动**：[[豆包视频解读/AI工具/DeepSeek-Harness插件精选4个-20260917]] 同属 Harness 生态（DSH 插件市场），harness-anything 是其本机 CLI 版形态——DSH 走插件市场，本项目走 pip/对话安装。
- **天使之翼归档模块的远期参考**：COM 操控真实 WPS 的格式保真能力，理论上优于 SheetJS 重写文件；但天使之翼是纯浏览器架构调不了 COM，仅当未来做本地归档工具链时可回头取用此路线。

## 📌 来源说明

- 笔记基于 headless 浏览器**分段截帧还原的视频画面**（含安装结果页、过程日志、WPS 成品窗）+ 项目 GitHub README + WPS 官方社区帖交叉核实，非视频原声转录。
- 安装耗时 13'51''、互动数据均为视频画面/截图时点数据；豆包工作模式资费视频未提及，未获证实，以官方为准。

## 相关链接

- [[豆包视频解读/视频笔记目录]]
- [[豆包视频解读/AI工具/DeepSeek-Harness插件精选4个-20260917]]
- [[豆包视频解读/AI工具/大模型缓存命中原理-20260916]]
