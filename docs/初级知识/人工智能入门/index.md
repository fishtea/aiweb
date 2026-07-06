# 人工智能入门

## 📖 概述

人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。这些任务包括语音识别、决策、模式识别、自然语言理解等。

> 根据 [Coursera 的定义](https://www.coursera.org/articles/what-is-artificial-intelligence)：「人工智能是计算机系统执行历史上需要人类智能的任务的理论与开发，例如识别语音、做出决策和识别模式。」

---

## 🏛️ AI 的定义与分类

### 强 AI vs 弱 AI

| 类型 | 定义 | 现实情况 |
|-----|------|---------|
| **弱 AI（狭义 AI）** | 专注于执行特定任务（如下棋、推荐、驾驶） | ✅ 我们日常使用的 AI 都属于此类 |
| **强 AI（通用 AI / AGI）** | 达到或超越人类水平的通用智能 | ❌ 目前尚未实现，仍是一个理论概念 |

**来源：** [Coursera — What Is Artificial Intelligence?](https://www.coursera.org/articles/what-is-artificial-intelligence)

### AI 的四种类型（按能力层级）

根据密歇根州立大学 Arend Hintze 教授的分类：

1. **反应式机器（Reactive Machines）** — 没有记忆，仅对当前输入做出反应。例如：深蓝（Deep Blue）下棋 AI。
2. **有限记忆机器（Limited Memory）** — 能利用短期历史数据做出决策。例如：自动驾驶汽车。
3. **心智理论机器（Theory of Mind）** — 能理解他人心理状态。⚠️ 目前仍是理论。
4. **自我意识机器（Self-Aware）** — 能理解世界、他人和自身。🔮 遥远未来的概念。

**来源：** 同上，源自 [GovTech 文章](https://www.govtech.com/computing/understanding-the-four-types-of-artificial-intelligence.html)

---

## 📜 AI 历史里程碑

根据 [Coursera — The History of AI: A Timeline](https://www.coursera.org/articles/history-of-ai) 的详细梳理：

### 1950s — 起源
| 年份 | 事件 | 意义 |
|:----:|------|------|
| 1950 | **艾伦·图灵**提出「图灵测试」 | 首次提出衡量机器智能的标准化方法 |
| 1956 | **达特茅斯会议** | 约翰·麦卡锡（John McCarthy）首次提出「人工智能」一词，标志 AI 作为一门学科的诞生 |

> 达特茅斯会议宣言：「学习或智能的任何特征，原则上都可以被精确描述到机器可以模拟的程度。」

### 1960s–1970s — 早期探索
- **1966：ELIZA 聊天机器人** — MIT 的 Joseph Weizenbaum 创建了第一个聊天机器人，模拟心理治疗师。许多用户相信自己在与真人对话。
- **1966–1972：Shakey 机器人** — 斯坦福研究院开发的第一个移动机器人，配备传感器和摄像头。
- **1974：第一次 AI 冬天** — 英国数学家 Lighthill 发表批评报告，认为 AI 过度承诺但未能兑现，导致大量资金削减。

### 1980s–1990s — 起伏
- **1986：第一辆无人驾驶汽车** — 德国 Ernst Dickmanns 改装的奔驰面包车。
- **1997：深蓝击败卡斯帕罗夫** — IBM 的深蓝（Deep Blue）每秒可评估 2 亿个棋步，在 19 步内击败了世界象棋冠军。

### 2000–2019 — 快速成长
- **2000：Kismet 社交机器人** — MIT 的社交机器人，能识别和模拟人类情感。
- **2004：NASA 火星车** — 使用 AI 自主导航火星地形。
- **2011：IBM Watson 赢得 Jeopardy!** — 展示了自然语言处理的能力。
- **2011：Siri 发布** — 首个大众级别的 AI 语音助手。
- **2012：Geoffrey Hinton 神经网络突破** — 在 ImageNet 竞赛中展示了深度神经网络的强大能力。
- **2016：AlphaGo 击败李世石** — Google DeepMind 的 AI 击败围棋世界冠军。围棋的复杂度是国际象棋的「谷歌倍」（googol 倍），使用了神经网络 + 深度搜索 + 强化学习。
- **2017：Transformer 论文发表** — Google 研究团队发表《Attention Is All You Need》，奠定了现代 LLM 的基础。

### 2020–至今 — AI 爆发
- **2020：GPT-3 发布** — 1750 亿参数的大语言模型。
- **2021：DALL-E 发布** — 文本到图像生成模型。
- **2022：ChatGPT 发布** — 将 AI 带入大众视野。
- **2023–2026：GPT-4、LLaMA、Claude 等模型持续涌现**，AI 能力不断提升。

### 2024-2026 关键节点补充

| 时间 | 事件 | 意义 |
|------|------|------|
| 2024.09 | OpenAI o1 发布 | 推理模型开端，LLM 学会"先思考再回答" |
| 2025.01 | DeepSeek-R1 开源 | 证明推理能力可通过 RL 涌现，性价比震动行业 |
| 2025.04 | LLaMA 4 发布 | 开源转向原生多模态 MoE |
| 2025.08 | GPT-5 发布 | 统一对话与推理，自适应思考深度 |
| 2025.12 | Agentic AI Foundation 成立 | OpenAI+Anthropic 推动 Agent 协议标准化（MCP/AGENTS.md） |
| 2026 | Agent 从 PoC 走向生产 | 企业级 Agent 部署成主流，安全与可观测性成焦点 |

> 趋势：AI 发展重心正从"模型能力"（2020-2024）转向"系统化应用"（2025-2026）。单模型榜单竞争趋缓，Agent 工程、数据治理、安全合规和成本控制成为新的核心议题。

---

## 🔬 AI 的主要分支

```
人工智能（AI）
├── 机器学习（ML）          ← 让计算机从数据中学习
│   ├── 监督学习            ← 有标签数据
│   ├── 无监督学习          ← 无标签数据
│   └── 强化学习            ← 通过奖励/惩罚学习
├── 深度学习（DL）          ← 多层神经网络
│   ├── CNN                ← 图像处理
│   ├── RNN/LSTM           ← 序列数据
│   └── Transformer         ← 现代 NLP 的基础
├── 自然语言处理（NLP）     ← 文本理解和生成
├── 计算机视觉（CV）        ← 图像和视频理解
└── 生成式 AI              ← 创造新内容
    ├── 大语言模型（LLM）    ← 文本生成
    ├── 扩散模型            ← 图像生成
    └── GAN                ← 对抗生成网络
```

---

## 🌍 AI 的现实应用

| 领域 | 应用示例 | 技术 |
|------|---------|------|
| 🏥 医疗 | AI 辅助手术、医学影像诊断 | 计算机视觉、深度学习 |
| 💰 金融 | 欺诈检测、量化交易 | 机器学习、异常检测 |
| 🚗 交通 | 自动驾驶、路线优化 | 强化学习、计算机视觉 |
| 🛒 电商 | 推荐系统、智能客服 | 协同过滤、NLP |
| 🎬 娱乐 | 内容推荐、AI 创作 | 深度学习、生成式 AI |
| 📚 教育 | 个性化学习、智能批改 | 机器学习、NLP |

---

## 🎯 学习建议

### 零基础入门推荐课程
1. **[AI For Everyone — Andrew Ng (Coursera / DeepLearning.AI)](https://www.coursera.org/learn/ai-for-everyone)**
   - ⭐ 4.8 分 · 250 万+ 学员 · 约 6 小时
   - 无需编程、无需数学基础
   - 课程包含 4 个模块：什么是 AI / 构建 AI 项目 / 在组织中引入 AI / AI 与社会

2. **[Introduction to Artificial Intelligence — IBM (Coursera)](https://www.coursera.org/learn/introduction-to-ai)**
   - ⭐ 4.8 分 · 90 万+ 学员
   - 4 个模块：AI 简介与应用 / AI 概念与术语 / AI 与商业转型 / AI 伦理
   - 含动手实验和最终项目

3. **[Microsoft AI for Beginners](https://microsoft.github.io/AI-For-Beginners/)**（免费）
   - 12 周、24 课时的完整课程体系
   - 涵盖 AI 历史、符号 AI、神经网络、计算机视觉、NLP、强化学习、AI 伦理
   - 支持 TensorFlow 和 PyTorch

---

## 🧭 2026 AI 全景：从子领域到技术栈

### AI 的核心子领域

现代 AI 研究围绕以下关键子领域展开：

| 子领域 | 核心问题 | 2026 年状态 |
|--------|---------|------------|
| **推理与问题求解** | 如何让机器进行逻辑推理和规划？ | 推理模型（如 OpenAI o1/o3、DeepSeek-R1）在数学和编程上超过人类专家 |
| **知识表示** | 如何让机器存储和调用知识？ | 知识图谱 + 向量数据库混合方案成为主流 |
| **规划与决策** | 如何在不确定环境中做最优决策？ | 强化学习 + LLM Agent 结合路线日趋成熟 |
| **机器学习** | 如何从数据中自动学习模式？ | 深度学习仍是核心，但数据质量和合成数据成为新焦点 |
| **自然语言处理** | 如何理解和生成人类语言？ | LLM 已接近或超越人类水平（律师考试、医学考试） |
| **感知（计算机视觉）** | 如何从传感器理解世界？ | 多模态模型统一文本+图像+视频理解 |
| **通用智能（AGI）** | 能否实现人类水平的通用智能？ | 仍是开放问题，但推理模型的出现让 AGI 路径更清晰 |

### AI 的核心技术栈（2026）

```
应用层：  ChatGPT / Claude / Gemini / DeepSeek / Copilot
  ↑
模型层：  GPT-4o / Claude 4 / Gemini 2.5 / DeepSeek-R1 / LLaMA 4
  ↑
架构层：  Transformer → MoE（混合专家）/ State Space Models
  ↑
训练层：  预训练 → 监督微调 → RLHF（人类反馈强化学习）
  ↑
数据层：  网页文本、代码、多模态数据 → 数据清洗 → 合成数据
  ↑
硬件层：  NVIDIA H100/B200 GPU · Google TPU · 大规模数据中心
```

### 2026 年 AI 入门推荐路径

1. **先理解概念**（1-2 周）：阅读本文，了解 AI 的分类、子领域和技术全景
2. **上手使用**（立即）：注册 ChatGPT/Claude/DeepSeek，体验 prompt 交互
3. **学习 Python**（2-4 周）：掌握基础语法、NumPy、Pandas
4. **学习机器学习基础**（4-8 周）：Andrew Ng 课程，理解监督/无监督学习
5. **学习深度学习**（4-8 周）：神经网络、反向传播、PyTorch
6. **学习大语言模型**（4-8 周）：Transformer、prompt engineering、RAG

> 💡 **2026 年新趋势**：与其从零写模型，不如先学会 **使用** 和 **微调** 现有模型。开源模型（LLaMA、DeepSeek、Qwen）已足够强大，可本地部署学习。

### AI 的经济与社会影响（2026）

- **电力需求激增**：IEA 预测到 2026 年 AI/数据中心用电将翻倍，相当于日本全国用电量
- **就业变革**：高盛预测到 2030 年，美国数据中心将消耗 8% 电力（2022 年仅 3%）
- **核能复苏**：微软与三里岛核电站签署 20 年供电协议，亚马逊购买核电数据中心
- **监管加速**：欧盟 AI Act 落地，各国纷纷立法规范 AI 发展

---

## 📚 参考来源

1. [What Is Artificial Intelligence? Definition, Uses, and Types — Coursera](https://www.coursera.org/articles/what-is-artificial-intelligence)（2026 年 3 月更新）
2. [The History of AI: A Timeline of Artificial Intelligence — Coursera](https://www.coursera.org/articles/history-of-ai)（2026 年 4 月更新）
3. [AI For Everyone — Coursera / DeepLearning.AI](https://www.coursera.org/learn/ai-for-everyone)
4. [Introduction to Artificial Intelligence (AI) — IBM / Coursera](https://www.coursera.org/learn/introduction-to-ai)
5. [Microsoft AI for Beginners 课程](https://microsoft.github.io/AI-For-Beginners/)
6. [Vaswani et al., "Attention Is All You Need" — Google Research, 2017](https://research.google/pubs/pub46201/)
7. [Artificial Intelligence — Wikipedia](https://en.wikipedia.org/wiki/Artificial_intelligence)（2026 年 7 月查阅）

---

*本页面内容基于真实在线资源编写，所有信息均引用自上述来源。*

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
