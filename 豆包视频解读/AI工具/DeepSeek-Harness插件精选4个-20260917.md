---
title: 翻完 2464 个 DeepSeek Harness 插件，只推荐这 4 个
updated: 2026-09-17
tags: [AI工具, DeepSeek, Agent, 插件, DSH]
status: active
source: 抖音图文 https://v.douyin.com/k8duzGTukIU/（douyin.com/note/7674529781413220273）· 账号 A.Lux · 2026-08-06 发布
---

# 翻完 2464 个 DeepSeek Harness 插件，只推荐这 4 个

> **视频主张**：插件不是装得越多越强。很多高 Star 项目要么不是 DSH 插件，要么功能重复，要么纯外观娱乐，装进去反而让整套 Harness 臃肿。作者把插件仓库、精选市场加自己已装的插件全部过了一遍，按「真正有用 + 能装 + 不冲突」筛出 4 个。
>
> **核实结论**：4 个推荐插件经官方仓库 / 社区插件目录交叉核实，**全部真实存在**，安装命令与仓库均已确认。

**一句话结论**：DeepSeek Harness（DSH）的正确玩法不是「全装上」，而是「缺什么能力 → 找对应插件 → 判断是否重复 → 再安装」——插件是把模型、记忆、工具、视觉、工作流、回滚机制组合成一套稳定系统的零件，数量不重要，组合才重要。

## 速览：作者推荐的 4 个插件

| 插件 | 补的能力 | 核实状态 | 安装方式（官方/社区口径） |
|---|---|---|---|
| 🧠 Hindsight | 长期记忆：不只「记住」，还能从过去任务反思、调用经验 | ✅ vectorize-io/hindsight，社区目录收录 | `dsh plugin --profile web add @vectorize-io/hindsight-coding-agents` |
| 💻 dsh-TUI | 终端交互：Claude Code 风格全屏 TUI，鲸鱼顶栏、上下文进度条、TPS 仪表 | ✅ ccch1mneyyy/dsh-TUI，约 2490 Star（2026-08 口径），曾被 DSH 官方公众号收录 | `npm install -g @deepseek-harness-tui/dsh-tui` 后运行 `dsh-tui` |
| ⚠️ MisakaNet | 失败经验沉淀：踩过的坑变成可检索的知识，而非留在聊天记录里 | ✅ Ikalus1988/MisakaNet，Git 本地知识库存verified 调试经验 | `dsh plugin add git+https://github.com/Ikalus1988/MisakaNet.git` |
| ⏪ dsh-turn-rewind | 对话 + 工作区状态回滚：改崩了能退，干项目的「安全网」 | ✅ Anionex/dsh-turn-rewind，BSD-3，116 Star；⚠️ 注意 dsh.so 实测记录显示 v0.2.1 GitHub 版在 dsh 0.1.5-rc.2 上运行时验证未通过，建议装 npm 包并选较新版本 | `dsh plugin --profile web add @anionex/dsh-turn-rewind` |

## 视频原文要点（按图整理）

1. **背景**：这次不折腾模型，开始给 DeepSeek Harness 装插件，「终于让 DeepSeek 真正看懂电脑屏幕了」。翻了 2464 个插件（作者自述口径，非官方榜单）。
2. **问题**：插件不是越多越强。高 Star ≠ 值得装——不是 DSH 插件 / 功能高度重复 / 纯外观娱乐，装进去反而臃肿。
3. **筛选标准**：真正有用 + 能装 + 不冲突。
4. **四个最推荐**：Hindsight（长期记忆）、dsh-TUI（终端交互）、MisakaNet（失败经验沉淀）、dsh-turn-rewind（回滚安全网）。
5. **按场景再装**：dsh-agent-teams（多智能体协作，已核实 NanmiCoder/dsh-agent-teams）、dsh-browser（接管正在登录的 Chrome，已核实）、dsh-vision-router——不是没用，是按需安装。其中 dsh-vision-router 本次未单独核实到官方仓库，以实际市场检索为准。
6. **思路升级**：从「有什么插件全部装上」→「缺什么能力 → 找对应插件 → 判断是否重复 → 再安装」。
7. **下一步**：把 4 个装进去跑实测，看究竟是生产力插件还是「看起来很强」。

## 串起来的框架：DSH 插件体系的「能力五层」

```
        模型（DeepSeek，纯文本）
              │
   ┌──────────┼──────────┬───────────┐
 记忆层      交互层      安全层       视觉层
 Hindsight  dsh-TUI   turn-rewind  vision 类插件
 MisakaNet            （回滚）
```

- **记忆层**（Hindsight + MisakaNet）：一个正向记「做成了什么、可复用」，一个反向记「踩过什么坑」——经验资产双向沉淀，这正是 Agent 从「能干活」到「越用越顺」的分水岭。
- **交互层**（dsh-TUI）：终端党补 Claude Code 式体验；Web 党可改用 dsh-web-ui / dsh-market（社区目录 3200+ 插件入口）。
- **安全层**（dsh-turn-rewind）：Turn 级检查点 + 回滚预览，但不替代 Git——重要项目仍要提交节点。
- **视觉层**：DeepSeek 主模型是纯文本，看图要靠视觉插件中转（如 modlens、dsh-deepseek-vision 的「视觉模型先读图 → 文字描述交给 DeepSeek」路线）。

## 社区口径补充（视频没说的）

- **DSH 是 DeepSeek 开源的 Agent 运行环境**（deepseek-ai/deepseek-harness），一切皆插件（Cordis 机制），发布数日 GitHub 即破 12 万 Star（媒体口径），目前仍为 Developer Preview，升级可能有破坏性变更。
- **没有官方审核的应用商店**。插件市场（dsh-market）、SkillHub、awesome-dsh-plugin、dshfind 等目录站均为社区维护，与 DeepSeek/幻方无从属关系。
- **安全红线**：插件以当前用户权限运行，可能读文件、用凭据、访问网络，工具调用审批并不能隔离插件代码。社区共识四条：一次只装一个、先看源码和更新记录、陌生插件先在无密钥环境试用、不用就卸载。
- **「2464 个」**：非官方数字。社区插件数增长极快（开放数日即 984 个，市场页面显示 3200+），任何具体计数都只作方向参考。

## 落地对接：本机能不能跑？

| 检查项 | 本机情况 | 结论 |
|---|---|---|
| Node.js | DSH 要求 Node 22.19+ 或 24 | ✅ 本机有 22.22.2 / 24.19.0，满足 |
| pnpm | 装 DSH 插件必需（官方命令走 pnpm） | ✅ 可全局安装，无 GPU 要求 |
| GPU | 无 NVIDIA / 无 CUDA | ✅ 不影响——DSH 跑 API 调用，不吃本地算力 |
| 磁盘 | C 盘仅剩约 4.3G | ⚠️ 建议克隆/安装到 D 盘，DSH_HOME 指到 D 盘 |
| 网络 | 代理拦 GitHub CONNECT | ⚠️ GitHub 仓库形式安装（MisakaNet、turn-rewind 的 github: 源）会受阻；npm 源可走 registry.npmmirror.com（注意镜像同步滞后，可能装到旧版本，需显式 @最新版本号） |
| 7×24 | 笔记本场景 | DSH 默认只监听本机 127.0.0.1:3080，适合本地工具而非长期挂机服务 |

**若要试装**：先全局装 DSH + pnpm → 装 dsh-market（`dsh plugin --profile web add dshmarket`）从市场可视化装其余插件 → 每装一个跑一个真实任务验证再装下一个。与「他」AGENT 项目的插件化思路（能力可插拔、可回滚）是同一套设计哲学，可对照借鉴。

## 来源说明

- 本文非视频逐字转录。图文文案经抖音详情页抓取获得（较完整），插件核实部分依据以下公开来源交叉验证：scriptbyai.com《100 Best DeepSeek Harness Plugins for DSH (2026)》、deepseek-harness-plugin.com 插件目录、dsh.so 插件验证平台、ai-bot.cn《DeepSeek Harness 保姆级教程》、6wolf.com awesome-dsh-plugin 介绍、ima.qq.com 知识库多篇 DSH 实操文章。
- Star 数、插件数等均为 2026 年 8–9 月公开口径，时效性强，安装前请以仓库实时数据为准。

## 相关链接

- [[视频笔记目录]]
- [[豆包视频解读/AI工具/Claude Code泄露的14条提示词秘籍-20260402]] —— 同为 Agent Harness 玩法沉淀
- [[豆包视频解读/AI工具/Hermes-Agent丐版配置单-20260915]] —— 同类 Agent 部署选型
