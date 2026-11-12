---
title: Agency Agents · 283 个 AI 员工人设（视频说 147 个）
updated: 2026-11-12
tags: [AI工具, AI-Agent, 提示词, 开源项目, GitHub]
status: active
source: 抖音 @地球支线 https://v.douyin.com/O5NLUWPOolE/ ｜ GitHub msitarzewski/agency-agents
---

# 🎭 Agency Agents：把提示词写成"岗位说明书"

> **视频主张**：别再手搓提示词了，GitHub 上有个 7 万星项目，一键部署 147 个"满级 AI 员工"，各有性格、工作流和 KPI。

**一句话结论**：值得存的不是"147 个员工"这个数字，而是它验证的写法——**提示词不是指令，是一份岗位说明书**（身份 + 性格 + 工作流 + 交付物 + 验收指标）。至于数字，视频已经过期了：角色从 147 涨到 283，星标从 7 万涨到 16.8 万。

## 一、视频档案

| 项目 | 内容 |
|:--|:--|
| 平台 / 账号 | 抖音 · @地球支线 |
| 标题 | 狂揽7万星！一键部署147个满级AI员工 别手搓提示词了！GitHub |
| 链接 | https://v.douyin.com/O5NLUWPOolE/ （item_id 7703011052330556111） |
| 发布 / 时长 / 互动 | 未获取（抖音需 App 内打开，页面数据需登录） |

## 二、口径核实表（2026-11-12 实测）

| 项目 | 视频口径 | 实测（GitHub API） |
|:--|:--|:--|
| Star 数 | 7 万 | **167,776** |
| Fork | 未提 | 27,217 |
| 角色（agent）数 | 147 | **283** |
| 部门数 | 12 | **18** |
| 开源协议 | 未提 | MIT |
| 仓库体积 | 未提 | 约 4.7 MB，纯 Markdown，无依赖、无服务 |
| 建仓 / 最后推送 | 未提 | 2025-10-13 / 2026-11-09 |

> 数字每天在变，以查询时点为准。视频大概率录制于项目 7 万星阶段（2025 年底—2026 年初），此后因媒体转载二次爆发。

**18 个部门**：academic（学术）、design、engineering（66 个，最大）、finance、game-development、gis、healthcare、marketing（37 个）、paid-media、product、project-management、research、sales、security、spatial-computing、specialized（59 个）、support、testing。

## 三、它到底是什么（别被"一键部署"误导）

不是模型、不是框架、不是要跑起来的服务。**本质是一批 Markdown 角色卡**，拷进 AI 工具的配置目录就能用。

单个角色文件的结构（以 `engineering/engineering-backend-architect.md` 为例，11KB）：

```
frontmatter：name / description / color / emoji / vibe
├─ Identity & Memory   角色、性格、记忆模式、经验
├─ Core Mission        核心使命，分若干条能力域
├─ Critical Rules      领域硬规则（安全、性能底线）
├─ Technical Deliverables  可交付物 + 真实代码示例
├─ Workflow Process    分步工作流
└─ Success Metrics     验收指标
```

**与普通提示词模板的差别**：

| 维度 | 普通 prompt | 这种角色卡 |
|:--|:--|:--|
| 深度 | 一句"你是一名 XX" | 完整人格 + 记忆模式 + 沟通风格 |
| 流程 | 无 | 分步工作流，每步有明确输出 |
| 交付 | 一段建议 | 代码 / 文档 / 报告模板 |
| 验收 | 无 | 自带成功指标 |

## 四、安装方式（4 种）

1. **桌面 App（官方推荐）**：agencyagents.app，Win/mac/Linux，点选即装、自动更新。
2. **脚本装全部**：`./scripts/install.sh --tool claude-code`
3. **只装一个部门**：`cp engineering/*.md ~/.claude/agents/`
4. **纯当参考**：直接打开 md 抄结构，不装。

`install.sh` 实测支持 17 种工具：claude-code、copilot、antigravity、gemini-cli、opencode、openclaw、cursor、aider、windsurf、qwen、zcode、kimi、codex、osaurus、hermes、vibe、dsh。
**注意：没有 WorkBuddy**，所以"一键部署"对你不成立，只能手动取用（见第六节）。

## 五、对园区/国企真正可能有用的角色

| 你的场景 | 可借鉴的角色文件 | 用法 |
|:--|:--|:--|
| 会议纪要 / 联席会 | `project-management-meeting-notes-specialist` | 拿它的工作流，替换成你的纪要模板 |
| 经营分析 / 收支成本 | `finance-fpa-analyst`、`finance-financial-analyst` | 借分析框架，口径必须换成本单位财务口径 |
| 制度、合同合规审查 | `support-legal-compliance-checker` | **只借审查清单结构**，法律条款不适用中国 |
| 上会汇报 / 领导摘要 | `support-executive-summary-generator` | 一页纸结论 + 依据，正好对口 |
| 项目推进 / 节点管控 | `project-manager-senior`、`project-management-project-shepherd` | 里程碑与风险台账结构 |
| 组织变革 / 流程再造 | `change-management-consultant` | 园区流程优化时用 |
| 数据合规 / 个人信息 | `data-privacy-officer` | 借清单，对照《个人信息保护法》重写 |
| 培训体系 | `corporate-training-designer` | 内训课程设计 |

## 六、本机适配判断

| 问题 | 结论 |
|:--|:--|
| 需要显卡 / GPU？ | **不需要**，纯文本文件，4.7MB |
| 要常驻服务？ | **不需要**，无后台进程、不占内存 |
| 能 7×24 跑？ | 不涉及，它只是提示词素材 |
| 网络能不能下？ | `raw.githubusercontent.com` 被代理拦（实测 25 秒超时）；`api.github.com` 可用（本次全部数据由此取得）；App 走 release 下载 |
| 能装进 WorkBuddy？ | 不能一键装，但可以把 md 内容做成自定义技能/角色提示词，效果等价 |

**建议做法**：不要 283 个全收。挑 3 个（会议纪要、经营分析、合规审查），把里面的美国口径换成你的实际口径（园区租赁、物业、招采、财务），存进 `提示词/`，比装一堆用不上的强。

## 七、三个必须知道的问题

1. **"满级"是营销词**。283 个角色里真正反复打磨的是少数，大量是社区 PR 贡献，质量参差。打开文件看两屏就知道深浅。
2. **KPI 与合规是美国语境**。它的"成功指标"是北美团队口径，法律、税务、隐私条款基本不适用，**照抄会出事**。
3. **权限要给得克制**。这类角色一旦接入编码工具，会读你的本地文件和代码库；在单位电脑上，先限定目录。

## 八、来源说明

- 视频文案未获取（抖音要求 App 内打开，分享页只返回标题），标题与作者取自分享链接；
- 星标、fork、角色数、部门数、协议、体积均由 GitHub API 于 2026-11-12 实测，**非视频口播数据**；
- 角色文件结构取自仓库内 `engineering-backend-architect.md` 原文；
- 本文非视频逐字转录，是"视频线索 + 官方仓库核验"的整理。

## 相关

- [[豆包视频解读/视频笔记目录.md]]
- [[豆包视频解读/AI工具/WorkBuddy高频提示词50条-20260924.md]] — 单条提示词写法
- [[豆包视频解读/AI工具/Claude Code泄露的14条提示词秘籍-20260402.md]] — 禁令式约束
- [[提示词/提示词目录.md]] — 本库提示词总目录
