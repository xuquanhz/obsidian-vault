---
date: 2026-04-02
source: 抖音 - Ale日记
link: https://v.douyin.com/E-xLGN8Pbr4/
tags:
  - Obsidian
  - Syncthing
  - 同步
  - 多设备
title: AI+Obsidian自动同步Syncthing-20260402
updated: 2026-09-09
status: active
---

# AI + Obsidian 自动同步方案（Syncthing）

利用 Syncthing 实现 Obsidian 本地库与多设备（手机、电脑）的实时自动同步。

---

## 核心方案

- **工具**：Syncthing（跨平台开源同步工具）
- **优势**：零费用、端对端加密、无需上传至云端、数据安全、同步速度快
- **支持平台**：Windows、Mac、Linux、Android、iOS

## 具体操作步骤

1. **下载安装**：在所有设备（电脑 + 手机）上安装 Syncthing
2. **创建同步文件夹**：
   - 电脑端新建 Obsidian 知识库文件夹
   - 手机端创建同名空文件夹
3. **添加设备**：
   - 电脑端 Syncthing 添加手机设备（扫描二维码）
   - 手机端添加电脑设备，双向确认建立连接
4. **共享文件夹**：
   - 电脑端将 Obsidian 库文件夹共享给手机
   - 手机端将空文件夹共享给电脑
5. **配置同步**：
   - 设置同步方向：双向
   - 忽略列表：`.obsidian` 缓存、`.DS_Store`
   - 开启"仅在 Wi-Fi 下同步"节省流量

## 效果

- 电脑端修改/新增笔记 → 手机端自动同步
- 手机端编辑 → 电脑端实时更新
- 实现 Obsidian 笔记在多设备间的"无缝流转"

## 适用场景

- 随身携带笔记，随时随地查阅、修改
- 配合 AI 工具（如 Claude Code）进行本地文档的 AI 对话、总结、分析
