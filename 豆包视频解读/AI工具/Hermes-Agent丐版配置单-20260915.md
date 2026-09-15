---
title: Hermes Agent 丐版配置单（最低成本部署）
updated: 2026-09-15
tags: [AI工具, Hermes, Agent, 自托管, 配置单]
status: active
source: 抖音@P叔 「六月发了丐版 Hermes 配置单，好多人问有没有…」 https://v.douyin.com/LUxLSi2Jjck/
---

# Hermes Agent 丐版配置单（最低成本部署）

> **视频出处**：抖音「P叔」，六月发过一版丐版 Hermes 配置单，本篇为其延续——回应「有没有更省的方案」。
> **一句话**：Agent 本体免费（MIT），真正的成本只有两块——**服务器 + 模型 API**。丐版的思路是：**服务器砍到 0～5 美元，模型换国产**。

---

## 一、先破除一个误解：它不吃硬件

Hermes Agent（Nous Research 出品，MIT 协议）把重活全外包给云端 API，**本地只做调度和工具执行**——所以它本质是个「派活儿的」，不是「干重活的」。

| 资源 | 实际占用 | 说明 |
|:--|:--|:--|
| 内存 | **约 200～500 MB** | 常有用户 4GB 机器上只跑不到 500MB |
| 磁盘 | 5 GB 足够 | 会话日志 + SQLite 会缓慢增长 |
| CPU | 1 核可跑 | 不跑本地模型几乎不吃 CPU |
| **GPU** | **完全不需要** | 推理都在云上 |
| 网络 | 只要出站 HTTPS | 不需要开入站端口 |

> ⚠️ **唯一吃内存的是浏览器自动化**（Playwright/Chromium）。如果你的 Agent 从来不打开网页，1GB 内存就够；要用浏览器，才需要往上加。

---

## 二、丐版配置单（三档）

### 档位 0：真·零成本 —— Oracle 永久免费 ARM

| 项 | 配置 |
|:--|:--|
| 服务器 | **Oracle Cloud Always Free** |
| 规格 | Ampere A1.Flex｜**4 OCPU + 24GB 内存**（可拆成 2核12G ×2 或 4核6G ×4） |
| 磁盘 | 引导卷最大 200GB |
| 系统 | **Ubuntu 22.04 Minimal aarch64**（注意 `aarch64` 才是 ARM 镜像） |
| 成本 | **￥0 / 月（终生）** |

**为什么推荐**：Oracle 是当前**唯一把「永久免费」长期落实**的大厂。4 核 24GB 跑 Hermes 绰绰有余，甚至富余。

**踩坑清单（务必按顺序做）**：
1. 主区域**选完不可改**——别选圣何塞/东京/首尔（ARM 长期售空），**优先凤凰城**等冷门区；
2. 地址行 1 用**英文填完整地址**，且**与上网 IP、信用卡账单地址保持一致**，否则付款验证报 `abc` 错误；
3. 全程**不要挂代理/VPN**（这是最常见的失败原因）；
4. 信用卡**不接受虚拟卡、预付卡**；会有一笔小额预授权，不实扣；
5. 创建报「**Out of host capacity**」＝容量不足，需用 CLI 脚本**定时重试抢**（社区有现成脚本）；
6. 抢不到就**升级为 Pay As You Go**——仍是免费额度内终生免费，但**优先极高**，且不怕因闲置被回收；
7. 系统选 **Ubuntu 22.04**，24.04 与 ARM 有已知兼容问题。

> 现实预期：免费额度的 ARM 很抢手，可能需要挂几天脚本。**这是零成本的代价**。

### 档位 1：性价比之选 —— Hetzner CX23

| 项 | 配置 |
|:--|:--|
| 规格 | 2 vCPU / **4GB** / 40GB NVMe |
| 成本 | **€3.99/月（约 $4.5）** |

社区公认性价比之王（同规格 DigitalOcean 要 $24/月）。4GB 是**硬门槛**——2GB 会在浏览器自动化或大文件处理时 OOM，且报错不一定优雅，可能污染进行中的会话。

> 若想留余量跑 Docker 后端：Docker 需额外 1～2GB，建议升 **CX33（4核8G，€6.49）**。

### 档位 2：其他可选

| 商家 | 起步价 | 特点 |
|:--|:--|:--|
| OVH VPS-1 | ~$6.46/月 | 4核8G/75GB，**不限流量** |
| Hostinger KVM 2 | $10～20/月 | 有**一键 Hermes 模板**，最省事 |
| Vultr / Linode | $5～6/月 | 机房节点多 |
| DigitalOcean | $24/月（4G） | 文档好但**贵，不推荐** |

---

## 三、模型：丐版的省钱关键

**用国产模型 + 免费额度，API 费可以压到近乎零。**

| 方案 | 成本 | 适配场景 |
|:--|:--|:--|
| **Kimi（Moonshot）** | 新用户赠 ¥15；100 万 token ≈ ¥12 | 国内直连无延迟，中文强，200 万上下文 |
| **DeepSeek** | 极低 | 日常任务首选，性价比最高 |
| OpenRouter `:free` 模型 | **$0** | 轻量使用，配合档位 0 可全免费 |
| 智谱 GLM / MiniMax | 低 | 国内原生支持，不走代理 |
| Ollama 本地 | $0 | 隐私场景，但需算力 |

> ⚠️ **硬性门槛**：模型必须支持**至少 64K tokens 上下文**——这是技能库和记忆系统运转的底线。

**省钱铁律**：
1. **给 API Key 设硬性消费上限**（OpenRouter 创建 key 时就能设，撞上限即停）；
2. **分级路由**：日常摘要、分类、提取那类活，用便宜模型（`-flash` / mini 级）就够了；贵模型只留给一次性复杂推理任务；
3. 别让定时任务跑在最贵的模型上——**这是超支的头号原因**。

---

## 四、推荐组合（按预算选）

| 预算 | 服务器 | 模型 | 月成本 |
|:--|:--|:--|--:|
| **￥0 党** | Oracle 永久免费 | OpenRouter `:free` 模型 | **￥0** |
| **务实党** | Oracle 免费 / Hetzner CX23 | DeepSeek / Kimi | **￥0～35** |
| **省心党** | Hostinger 一键模板 | Kimi | **约 ￥70～150** |

---

## 五、回到你本机的现实（AMD + 无 NVIDIA + C盘紧张）

你之前定过「本地模型走 ONNX INT8 CPU 版、模型落 D 盘」的路线。Hermes 这条线**不冲突且更省事**——

| 你的约束 | Hermes 的表现 |
|:--|:--|
| AMD 平台、**无 CUDA** | ✅ 完全不需要 GPU，纯 API 调用 |
| C 盘仅剩约 4.3G | ✅ 配置目录 `~/.hermes/` 极小（<5GB），**不需要本地权重** |
| 代理拦 GitHub/HuggingFace | ⚠️ 安装脚本走 GitHub，用 `ghfast.top` 镜像加速 |
| 想 24 小时在线 | ⚠️ 本机做不到（睡眠即断），**必须上 VPS** |

**建议路径**：先在自己笔记本上用 WSL2 装一版跑通（零成本验证），确认有价值后再上 Oracle 免费 VPS 转 7×24。

---

## 六、安装与排错速查

```bash
# 安装（三选一）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash   # 官方
curl -fsSL https://hermes.xaapi.ai/install.sh | bash                 # 国内镜像
# Windows 现已支持原生 PowerShell（早期版本要求 WSL2）

hermes setup          # 配置向导（选模型提供商 + 填 Key）
hermes doctor         # 健康检查，出错先跑这个
hermes model list     # 确认模型已生效
hermes gateway setup  # 接 Telegram / 钉钉 / Slack 等
hermes cron add "…" --schedule "0 8 * * *"   # 定时任务
```

**国内环境先配加速**（否则大概率安装失败）：
```bash
git config --global url."https://mirror.ghproxy.com/https://github.com".insteadOf "https://github.com"
pip config set global.index-url https://mirrors.aliyun.com/simple/
npm config set registry https://mirrors.cloud.tencent.com/npm/ --global
```

**分层排错**：`command not found` → PATH 问题｜安装超时 → 网络/镜像｜Key 无效 → `.env` 变量名或余额｜命令被拒 → 审批模式｜静默失败 → 看 `~/.hermes/logs/errors.log`。

---

## 七、安全红线（照抄官方与社区共识）

1. **永不开启 YOLO 模式**——所有危险命令必须人工审批；
2. API Key 只放 `~/.hermes/.env`（`chmod 600`），**绝不写进 config.yaml 或提交 Git**；
3. 用 Docker 或 SSH 隔离后端跑生产；
4. 定时任务只让 Agent 访问指定工作目录，**不要给它敏感目录的访问权**；
5. 装社区技能前先 `hermes skills inspect` 做安全检查；
6. **定期备份 `~/.hermes/`**——那是 Agent 的整个大脑。

---

## 来源说明

- **原始视频**：抖音「P叔」《六月发了丐版 Hermes 配置单…》。抖音分享页需 App 内打开，**无法获取视频逐字稿**。
- **本篇依据**：同主题公开内容源交叉核实——Hermes 官方站/仓库、CSDN《2026年6月最新 Hermes Agent 完整安装配置与实战指南》、Hetzner/DigitalOcean/OVH 对比文、Oracle 永久免费 ARM 实测文、社区部署实践。
- **性质**：属**开源项目的公开部署方案整理**，非视频逐字转录；价格为 2026 年上半年公开信息，**下单前请复核**。

---

**相关**：[[豆包视频解读/视频笔记目录]]
