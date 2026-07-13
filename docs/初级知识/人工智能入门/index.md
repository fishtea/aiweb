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

## 🧩 AI 学习方法论：自顶向下 vs 自底向上

根据 [Microsoft AI for Beginners 课程](https://microsoft.github.io/AI-For-Beginners/) 的介绍，实现人工智能有两大基本路径：

### 自顶向下方法（符号推理 / Symbolic Reasoning）

这种方法模拟人类的推理过程——先提取人类专家的**知识**，将其转化为计算机可读的形式（如规则库、知识图谱），再构建**推理引擎**来模拟人类决策。早期 AI 的代表如**专家系统（Expert Systems）** 就属于此类。

**优点**：决策过程透明、可解释。**局限**：知识获取非常困难——许多人类专家无法清晰地解释自己如何做出判断。"从专家那里提取知识、用计算机表示、并保持知识库的准确性" 被证明是一项极其复杂且成本高昂的工作，这直接导致了 1970 年代的"AI 冬天"（AI Winter）。

### 自底向上方法（神经网络 / Neural Networks）

这种方法模拟人脑的基本结构——人工神经元。我们构建**人工神经网络**，通过提供大量示例来训练它解决问题，类似于婴儿通过观察来认识世界。

**优点**：无需显式编程规则，可以从数据中自动学习模式。**局限**：决策过程不透明（黑箱问题），需要大量计算资源和数据。

> 现代 AI 实践中，这两种方法常常结合使用。例如，LLM Agent 同时使用神经网络（理解自然语言）和符号推理（规划、工具调用）。

**来源：** [Microsoft AI for Beginners — Lesson 1: Introduction to AI](https://microsoft.github.io/AI-For-Beginners/)

---

## 📚 Microsoft AI for Beginners：12 周系统课程推荐

[A vitepress site to host the AI for Beginners curriculum.](https://microsoft.github.io/AI-For-Beginners/) 提供了一套完整的 **12 周、24 课时**的 AI 入门课程，涵盖 AI 的所有主要领域：

### 课程结构概览

| 模块 | 主题 | 课时数 |
|------|------|:------:|
| **I. AI 介绍** | AI 的历史、定义与图灵测试 | 1 |
| **II. 符号 AI** | 知识表示、专家系统、本体论与概念图 | 1 |
| **III. 神经网络入门** | 感知机 → 多层感知机 → 框架实操 → 过拟合 | 3 |
| **IV. 计算机视觉** | OpenCV → CNN → 迁移学习 → 自编码器 → GAN → 目标检测 → 语义分割 | 7 |
| **V. 自然语言处理** | 文本表示 → 词嵌入 → 语言建模 → RNN → 生成式 RNN → Transformer/BERT → NER → LLM/提示工程 | 8 |
| **VI. 其他 AI 技术** | 遗传算法、深度强化学习、多智能体系统 | 3 |
| **VII. AI 伦理** | AI 伦理与负责任 AI 原则 | 1 |

### 课程特色

- **双框架支持**：每个重要主题都同时提供 PyTorch 和 TensorFlow 的 Notebook
- **动手实验室**：多数模块配有实践 Lab
- **前/后测验**：每一课都有小测验验证学习成果
- **中文化支持**：提供简体中文翻译版本

> 该课程特别强调 **实践驱动** 的学习方式——每节课都配有可执行的 Jupyter Notebook，让你在写代码中理解概念。

### 适合人群

- 零编程基础或少量编程经验的学习者
- 希望系统掌握 AI 全貌而非只了解某一个领域的入门者
- 教育工作者（该课程还提供了教师指导手册）

**来源：** [Microsoft AI for Beginners GitHub](https://github.com/microsoft/AI-For-Beginners) | [课程在线版本](https://microsoft.github.io/AI-For-Beginners/) | [示例入门代码](https://github.com/microsoft/AI-For-Beginners/tree/main/examples)

---

## 🤖 AI 的核心问题：什么是智能？

Microsoft AI for Beginners 课程提出了一个发人深省的问题：**"猫有智能吗？"** 不同的人会给出不同答案，因为并没有一个普遍接受的"智能测试"。

### 图灵测试（Turing Test）

Alan Turing 在 1950 年提出了**图灵测试**：如果一位人类提问者通过文本对话无法区分对方是真人还是计算机系统，那么这个系统被认为具有智能。

> 2014 年，圣彼得堡开发的聊天机器人 [Eugene Goostman](https://en.wikipedia.org/wiki/Eugene_Goostman) 接近通过图灵测试——它自称是一个 13 岁的乌克兰男孩，利用年龄和文化差异解释了"知识欠缺"。在 5 分钟对话后，它让 30% 的评委相信自己是人类。然而这并不意味着我们创造了一个智能系统——而是系统**创造者**欺骗了人类。

### 智能的两种模型

课程介绍了 AI 领域解决"智能"难题的两种典型路径：

| 维度 | 符号推理（Top-Down） | 神经网络（Bottom-Up） |
|------|:-------------------:|:--------------------:|
| **核心思想** | 提取人类知识 → 表示为规则 → 推理机执行 | 模拟人脑神经元 → 训练网络 → 从数据中学习 |
| **代表技术** | 专家系统、知识图谱、规则引擎 | 深度学习、CNN、Transformer |
| **优势** | 可解释、可验证、精度高 | 无需人类编程规则、自动发现模式 |
| **局限** | 知识提取困难、不擅长感知类任务 | 黑箱、需要大量数据、易过拟合 |
| **典型应用** | 医疗诊断系统、法律推理 | 图像识别、NLP、语音识别 |

**来源：** [Microsoft AI for Beginners — Lesson 1](https://github.com/microsoft/AI-For-Beginners/tree/main/lessons/1-Intro)

---

## 📚 参考来源

1. [What Is Artificial Intelligence? Definition, Uses, and Types — Coursera](https://www.coursera.org/articles/what-is-artificial-intelligence)（2026 年 3 月更新）
2. [The History of AI: A Timeline of Artificial Intelligence — Coursera](https://www.coursera.org/articles/history-of-ai)（2026 年 4 月更新）
3. [AI For Everyone — Coursera / DeepLearning.AI](https://www.coursera.org/learn/ai-for-everyone)
4. [Introduction to Artificial Intelligence (AI) — IBM / Coursera](https://www.coursera.org/learn/introduction-to-ai)
5. [Microsoft AI for Beginners 课程](https://microsoft.github.io/AI-For-Beginners/)
6. [Vaswani et al., "Attention Is All You Need" — Google Research, 2017](https://research.google/pubs/pub46201/)
7. [Artificial Intelligence — Wikipedia](https://en.wikipedia.org/wiki/Artificial_intelligence)（2026 年 7 月查阅）
8. [Microsoft AI for Beginners — Lesson 1: Introduction to AI 原文](https://github.com/microsoft/AI-For-Beginners/tree/main/lessons/1-Intro)

---

## 🧠 2026 Agent 认知架构入门：上下文窗口 ≠ 记忆

根据 [Machine Learning Mastery 2026 年 6 月文章](https://machinelearningmastery.com/context-windows-are-not-memory-what-ai-agent-developers-need-to-understand/)：

许多 AI 初学者看到模型宣称支持"200 万 token 上下文窗口"时，会本能地想："把所有内容塞进 prompt 就行了！" 但这在架构层面是一个根本性的误解。

### 类比：办公桌 vs 文件柜

| 概念 | 类比 | 特点 |
|------|------|------|
| **上下文窗口（Context Window）** | 办公桌面 | 无状态、每次会话结束"被清空" |
| **记忆系统（Memory）** | 文件柜 | 持久化、可跨会话查询 |

> "模型本质上是完全无状态的。每一次 API 调用都从零开始——即使你把 20 万 token 的对话历史传进去，模型也不是'记住'了之前发生的事，而是用几毫秒的时间把它的'整个宇宙'重新读了一遍。"

### 三个关键概念

#### 1. RAG（检索增强生成）= 书架

RAG 系统像一个**大书架**——按需（Just-In-Time）拉取与当前问题最相关的文档片段进入上下文窗口。

⚠️ **Agent 场景的陷阱**：向量相似度 ≠ 语义正确性。比如用户先说"把会议挪到周五"，后说"取消周四，Alice 病了"，向量检索可能同时返回这两条矛盾信息。解决方案：检索后先做冲突消解，如按时间戳取最新记录。

#### 2. 压缩 = 减小信息体积

压缩是**算法层面的 token 削减**——保持底层数据不变，只缩小物理占用。如用 LLMLingua 将 15000 token 压缩到 5000 token，释放上下文空间给核心任务。

```
原始负载（15000 token）→ LLMLingua 压缩 → 5000 token → 送进 prompt
```

#### 3. 摘要 = 单向不可逆

摘要直接**替换原始数据为抽象**，原始信息不可恢复。最佳实践是"分叉存储"：原始对话写入 S3/SQL，摘要进 prompt，需要细节时再检索。

### Agent 记忆的正确姿势：查询—提交循环

要让 Agent 拥有真正的记忆，必须让它扮演**数据库管理员**而非**数据库本身**：

```python
def agent_turn(user_message, entity_graph):
    # 每轮开始时查询已有状态
    current_state = entity_graph.query(subject="User_Dog")
    
    response = model.generate(
        messages=[{"role": "user", "content": user_message}],
        context=current_state
    )
    
    # 每轮结束时提交状态更新
    for call in response.tool_calls:
        entity_graph.update(**call.params)
    
    return response
```

> 核心理念：**别买一张 1000 万 token 的巨型办公桌。给 Agent 配一张普通桌子、一支好铅笔，教它如何打开文件柜。** （来源：Iván Palomares Carrascosa, Machine Learning Mastery, 2026-06-24）

---

## 2026 年人工智能最新趋势

2026 年，AI 正从"问答工具"进化为"协作伙伴"。以下是 2026 年的关键趋势：

### 1. AI Agent（智能体）成为数字同事

AI 不再只是回答问题，而是成为能够独立执行任务的 **Agent（智能体）**。它们像数字同事一样，协助团队完成数据整理、内容生成、个性化推荐等工作。Microsoft 首席产品官 Aparna Chennapragada 指出，一个三人团队借助 AI Agent，可以在数天内发起一场全球营销活动——AI 处理数据分析和内容生成，人类专注于战略和创意方向。

### 2. AI 安全与信任机制

随着 Agent 进入职场，安全防护变得至关重要。Microsoft Security 副总裁 Vasu Jakkal 强调，每个 Agent 都应有明确的身份认证、权限控制和数据管理机制，避免 Agent 成为"携带未检查风险的双重间谍"。2026 年，安全将向"环境化、自主化、内置化"方向发展。

### 3. AI 重塑医疗健康

AI 在医疗领域的应用正从诊断扩展到症状分诊和治疗规划。Microsoft AI 的 Diagnostic Orchestrator（MAI-DxO）在 2025 年以 85.5% 的准确率解决复杂医疗案例，远超经验丰富医生 20% 的平均水平。目前 Copilot 和 Bing 每天回答超过 5000 万个健康问题。

### 4. AI 成为科研助手

2026 年，AI 不再只是总结论文和回答问题——它将主动参与科学发现过程。从生成假设、控制实验工具到与人类科研人员协作，AI 正在成为真正的"实验室助手"。

### 5. AI 基础设施更加智能高效

AI 的发展不再只是建设更多更大的数据中心。新一代分布式 AI"超级工厂"将更密集地打包计算能力，动态路由工作负载，确保每个计算周期和每瓦电力都被充分利用。

### 参考来源

- [What's next in AI: 7 trends to watch in 2026 — Microsoft](https://news.microsoft.com/source/features/ai/whats-next-in-ai-7-trends-to-watch-in-2026/)（2025-12-08）
- [10 Things That Matter in AI Right Now — MIT Technology Review](https://www.technologyreview.com/2026/04/21/1135643/10-ai-artificial-intelligence-trends-technologies-research-2026/)（2026-04-21）
- [Future of AI (2026): Powerful Guide — World of AI Hub](https://worldofaihub.com/the-future-of-ai-7-trends-to-watch-in-2026/)（2026-07-08）

---

*本页面内容基于真实在线资源编写，所有信息均引用自上述来源。*

---

## 2026 年 AI 初学者最佳入门路径

根据 DeepLearning.AI 截至 2026 年 7 月的课程体系，以下是零基础入门 AI 的高效路径：

### 第一站：AI 通识与概念建立

**推荐课程：** [AI For Everyone](https://www.deeplearning.ai/courses/ai-for-everyone/)（Andrew Ng，4.8★）

- **时长**：约 3 周，每周 2 小时
- **适合**：完全零基础，不需要编程
- **内容**：AI 术语解释（机器学习、深度学习、数据科学）、AI 能做什么/不能做什么、如何在组织中推动 AI 项目

### 第二站：Python 编程基础

如果你还没有编程基础，推荐以下免费资源：

- **Kaggle Python 微课程**（免费，交互式 notebook）
- **Coursera: Python for Everybody**（密歇根大学）

> 💡 **2026 年建议**：不需要精通 Python 再开始学 ML——掌握变量、循环、函数、列表/字典即可上手，边学边补。

### 第三站：机器学习基础

**推荐课程：** [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)（Andrew Ng，4.9★，79 万+学员）

- 3 门课程：监督学习 → 高级算法（神经网络、决策树）→ 非监督学习与推荐系统
- 使用 Python（NumPy、scikit-learn）动手实践

### 第四站：深度学习入门

**推荐课程：** [Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)（4.9★，99 万+学员）

- 5 门课覆盖：神经网络基础 → 超参数调优 → ML 项目结构 → CNN → 序列模型/Transformer

### 2026 年 DeepLearning.AI 课程生态全景

截至 2026 年 7 月，DeepLearning.AI 平台提供 **124 门课程**（100 门短期课程 + 13 门完整课程 + 11 门专项课程），覆盖以下热门主题：

| 主题 | 课程数 | 说明 |
|------|:------:|------|
| **GenAI 应用开发** | 58 | 最热门的领域 |
| **提示词工程** | 46 | 涵盖从基础到高级 |
| **AI Agent** | 42 | 2026 年增长最快的方向 |
| **RAG 检索增强** | 31 | 企业级 LLM 应用核心 |
| **LLMOps** | 27 | 模型部署与运维 |
| **微调（Fine-Tuning）** | 17 | LoRA/QLoRA 等高效微调技术 |

课程难度分布：初级 64 门（52%）、中级 60 门（48%），无需博士学位即可入门。

### 第六站：动手实践（比课程更重要）

- **Kaggle 竞赛**：从 Titanic 入门赛开始，逐步参与真实竞赛
- **HuggingFace Spaces**：部署你自己的 AI 应用 demo
- **GitHub 开源项目**：参与 Contributors 贡献代码

> 📌 **2026 年核心建议**：课程只是地图，真正的成长来自"做一个实际项目"。哪怕只是一个简单的聊天机器人、图片分类器或数据分析工具，完整的构建经历远胜过 10 门只看不做的课程。

### 参考来源

- [DeepLearning.AI — Explore Courses](https://learn.deeplearning.ai/courses)（课程目录，截至 2026-07-13）
- [DeepLearning.AI — AI For Everyone](https://www.deeplearning.ai/courses/ai-for-everyone/)
- [Coursera — Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction)

---

## 🌟 2026 年 7 月 AI 前沿速览：从 Technology Review 看最新趋势

> 以下内容基于 MIT Technology Review（2026 年 7 月）和 MIT News 的最新报道整理，帮助初学者了解当前 AI 领域正在发生什么。

### 1. AI Agent（智能体）正在走出概念验证阶段

2026 年最大的趋势是 AI 从"问答工具"向"自主执行者"的转变。Gartner 预测到 2026 年底，40% 的企业应用将集成任务特定的 AI Agent。这意味着初学者不仅要了解"如何用 AI 对话"，更要理解**Agent 的工作方式**——AI 程序自主规划步骤、调用工具、执行任务。

**关键是理解**：Agent 不是单个模型，而是一个**多层技术栈**——底层是基础模型（如 GPT-5.5、Claude 4、Llama 4），上层分别是编排层、记忆层、检索层、工具层、可观测性层和部署层。每一层都可能成为瓶颈，理解全栈比只关注模型更重要。

### 2. 推理能力已成为模型标配

2024 年 OpenAI o1 开辟了"推理模型"这条新路，到 2026 年，推理能力已被整合进入主流模型。GPT-5.5、Claude Sonnet 4.6、Gemini 3.1 Pro 等模型都可以根据任务难度自动调整"思考深度"——简单问题快速回答，复杂问题深入推理。

**对初学者的意义**：你不需要选择"推理模型"还是"普通模型"——它们已经合二为一。只需根据任务复杂度调整推理努力级别（reasoning effort）即可。

### 3. LLM 在科学研究中扮演越来越重要的角色

MIT Technology Review 报道了多个 AI 推动科学发现的案例：AlphaFold 在蛋白质结构预测上的持续突破、LLM 在数学问题求解上的快速进步、AI 辅助药物发现等。Google DeepMind 的诺贝尔奖得主 John Jumper 表示："未来会有越来越多 LLM 对科学产生重大影响。"

### 4. 多 Agent 系统的风险研究正在加速

Google DeepMind 正在呼吁更多科学家研究**多 Agent 系统**的潜在风险——当数百万个 AI Agent 开始相互交互时，可能出现不可预测的涌现行为。这从侧面说明 Agent 技术已经从实验室走向真实世界。

### 5. 人人可参与：AI 程序员的门槛正在降低

MIT Lincoln Laboratory 的最新项目显示，即使是航空军学员也能利用 AI 聊天机器人为军事应用开发程序。AI 辅助编程工具（如 Claude Code、GitHub Copilot）的进步意味着**编程能力的门槛正在降低**——对于 AI 初学者来说，学会"如何用 AI 写代码"比"从零学代码"更高效。

### 参考来源

- [MIT Technology Review — The AI Agent Tech Stack Explained](https://machinelearningmastery.com/the-ai-agent-tech-stack-explained/)（2026-06-27）
- [MIT Technology Review — What's next for AI in 2026](https://www.technologyreview.com/)（2026 年 7 月）
- [MIT News — How novice coders can develop AI programs](https://news.mit.edu/)（2026 年 7 月）
- [Google DeepMind — Multi-agent systems risks](https://www.technologyreview.com/)（2026 年 7 月）

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-09。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-14 00:10:05*
