---
date: 2026-07-30
source: 抖音 - 小陈同学 c_z
link: https://v.douyin.com/OyuWBmAQ1-U/
tags:
  - Obsidian
  - DeepSeek
  - AI
  - 知识库
---

# Obsidian + DeepSeek 搭建 AI 知识库

Obsidian 搭配 DeepSeek（V4 百万上下文）打造本地 AI 知识库的完整方案。

---

## 方案一：手动工作流（零门槛入门）

### 步骤 1：建立 Obsidian 阵地
- 新建库（Vault），建议保存在非系统盘
- 建立分层目录结构：
  - `00_Inbox` — AI 清洗后的待归类笔记
  - `01_Notes` — 已整理好的正式知识库
  - `attachments` — 图片和多媒体附件

### 步骤 2：准备原材料
- Pandoc 批量转换 Word 文档：`pandoc -t markdown input.docx -o output.txt`
- Windows 截图 OCR（Win+Shift+T）提取文字

### 步骤 3：黄金洗稿提示词模板
将以下指令粘贴到 DeepSeek 中：
> "你是一个顶级的 Obsidian 知识库整理专家…请按以下要求清洗重构：
> 1. 修正错别字和语病
> 2. 整理为 Markdown 标题层级
> 3. 列表项整理为无序列表
> 4. 顶部加上 YAML 元数据（title/date/tags/status）
> 5. 直接输出 Markdown，不要额外闲聊"

### 步骤 4：自动生成双向链接
- 将多篇笔记内容贴给 DeepSeek，让其分析逻辑关联
- 建议插入 `[[双向链接]]`，构建知识网络

---

## 方案二：插件方案（自动化集成）

### 🟢 DeepSeek Note Helper（推荐）
- **核心功能**：当前笔记感知、双向链接解析、Agent 工具调用（全库搜索/新建笔记/追加记录）、YAML 自动化管理
- **安装**：从 GitHub 下载 `main.js`、`styles.css`、`manifest.json` 放入 `.obsidian/plugins/obsidian-deepseek-note-helper/`
- **配置**：填入 DeepSeek API Key，可选修改 API URL 和 Model
- **使用**：点击侧边栏 🤖 图标唤醒 AI 助手
- GitHub：`leoyang1984/obsidian-deepseek-note-helper`

### 🟢 DeepSeek TUI Obsidian 插件
- 在侧边栏嵌入 DeepSeek-TUI，支持流式输出
- 知识库命令：摄取当前文件、编译全库索引、自然语言查询、检查损坏链接
- 类似 Claudian 插件的 DeepSeek 版本
- GitHub：`sunnybluesea/deepseek-obsidian-plugin`

### 🟢 LLM Wiki Parser
- 将拖入的笔记/链接/文档自动消化为结构化知识文件
- 支持 DeepSeek 或小米 MiMo 作为后端
- 支持 docx/pptx/xlsx/md/txt/html/csv/json/yaml/xml 等多种格式
- GitHub：`LiJzd/Obsidian-LLM-WIKI`

---

## 方案三：DeepSeek V4 百万上下文（进阶）

2026 年 DeepSeek V4 的百万上下文能力与 Obsidian 结合实现质的飞跃。

### 为什么选择 Obsidian
- **文件系统直读**：Vault 即文件夹，.md 即源数据
- **双向链接暴露度**：`[[link]]` 语法明文存在，可解析生成知识拓扑
- **插件沙箱安全**：社区插件运行在严格隔离环境中

### 核心工作流
- 将整个 Vault 的核心子集（如 300MB 纯文本）一次性喂给 V4
- AI 基于你的独有知识结构回答问题、生成摘要、发现隐藏逻辑
- 硬件要求：32GB 内存笔记本 + 装好插件的 Obsidian 客户端

### 成功实践关键
- 在会议纪要模板中预设结构（决策项/待办/风险）
- 手动触发 AI 生成执行建议
- 遵循"人类定义问题边界 → AI 提供答案选项 → 人类做最终决策"的闭环

---

## LLM Wiki 思想的知识库结构

借助 AI Agent 自动初始化的推荐目录结构：

```
my-notes/
├── CLAUDE.md      # 规范文件
├── index.md       # 内容索引
├── log.md         # 操作日志
├── entities/      # 实体页
├── concepts/      # 概念页
├── sources/       # 来源摘要
├── summaries/     # 综合分析
└── raw/           # 原始资料库（不可变）
```

---

## 三种方案对比

| 方案 | 适合人群 | 特点 |
|:--|:--|:--|
| **手动工作流** | 新手、想深入理解流程 | 零门槛，提示词模板即用 |
| **插件方案** | 追求效率的用户 | 一键集成，自动化程度高 |
| **V4 百万上下文** | 处理大量本地笔记的专业用户 | 全库理解，发现隐藏逻辑 |

---

Sources:
- 腾讯云开发者社区：https://cloud.tencent.com.cn/developer/article/2686097
- deepseek-obsidian-plugin：https://github.com/sunnybluesea/deepseek-obsidian-plugin
- Obsidian-LLM-WIKI：https://github.com/LiJzd/Obsidian-LLM-WIKI
- obsidian-deepseek-note-helper：https://github.com/leoyang1984/obsidian-deepseek-note-helper
