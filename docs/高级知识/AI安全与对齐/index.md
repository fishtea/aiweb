# AI 安全与对齐

> AI 对齐（Alignment）旨在确保 AI 系统的行为符合人类价值观和意图。本页面总结了 RLHF、宪法 AI（Constitutional AI）、红队测试等核心技术。

---

## 1. 什么是 AI 对齐？

AI 对齐解决的核心问题是：**如何确保强大的 AI 系统做"对人类有益"的事情**。随着 LLM 能力提升，对齐变得越来越关键。

主要对齐方法：
- **RLHF** — 基于人类反馈的强化学习
- **RLAIF** — 基于 AI 反馈的强化学习
- **Constitutional AI** — 基于原则的自我对齐
- **红队测试** — 对抗性评估

---

## 2. RLHF（基于人类反馈的强化学习）

**来源：** [PMC - Sociotechnical limits of AI alignment](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137480)

RLHF 是 OpenAI 提出的主流对齐方法，包含三个阶段：

### 阶段 1：监督微调（SFT）
在高质量人工标注数据上微调模型。

### 阶段 2：训练奖励模型
- 收集人类对不同模型输出的偏好比较
- 训练一个奖励模型来预测人类偏好

### 阶段 3：强化学习优化
- 使用 PPO 等 RL 算法，以奖励模型为信号优化策略模型
- 目标：最大化期望奖励，同时约束 KL 散度防止偏离原始模型

### RLHF 的局限性

> *"RLHF presents itself as a straightforward method for ensuring AI oversight and AI safety through value alignment."*

但存在以下问题：
- **人类偏好一致性**：不同群体价值观不同
- **偏好标注偏差**：标注者可能存在系统性偏见
- **可扩展性问题**：随模型能力增长，人类难以评估
- **奖励黑客**：模型可能找到取巧方式获得高分

---

## 3. 宪法 AI（Constitutional AI, CAI）

**来源：** [Constitutional AI: Ethical Alignment for LLMs - Emergent Mind](https://www.emergentmind.com/topics/constitutional-ai-cai), [IterAlign Paper](https://arxiv.org/html/2403.18341v1)

宪法 AI 由 Anthropic 提出（Bai et al., 2022），使用一组自然语言规则（"宪法"）来引导模型行为。

### 两阶段方法

**阶段 1：基于自我批判的监督微调**
1. 从可能有用但未必安全的 LLM 开始
2. 对红队提示生成输出
3. 引导模型进行思维链自我批判——基于宪法识别有害元素
4. 修改输出，形成训练数据集

**阶段 2：基于 AI 反馈的强化学习（RLAIF）**
1. 对有害提示采样成对输出
2. 仅基于宪法原则训练的偏好模型分配奖励
3. 优化策略以最大化宪法奖励

### 宪法原则类型

| 原则类型 | 范围 | 优势 |
|----------|------|------|
| 通用原则 | 广泛 | 鲁棒，但不够精细 |
| 具体原则 | 聚焦 | 细粒度，可定制 |

### IterAlign：迭代宪法对齐

**来源：** [IterAlign: Iterative Constitutional Alignment](https://arxiv.org/html/2403.18341v1)

1. 对抗性红队测试 → 揭示模型弱点
2. 更强的"预言机"LLM 提出新原则修复对齐差距
3. 自我反思与修订
4. 在修订后数据集上监督微调
5. 循环迭代

> **效果：** 无害性提升最高 **13.5%**，使用自动发现的原则

---

## 4. 红队测试（Red Teaming）

红队测试是指**创建故意诱导有害内容的提示词**，以评估模型的安全边界。

### 常见红队方法

| 方法 | 描述 |
|------|------|
| **手动红队** | 人类专家设计对抗性提示 |
| **自动化红队** | 使用 LLM 自动生成攻击提示 |
| **越狱测试** | 尝试绕过安全限制（如 DAN、角色扮演） |
| **提示注入** | 尝试覆盖系统指令 |
| **多轮攻击** | 通过多轮对话逐渐突破限制 |

### 效果数据

| 方法 | 有害输出降低 | 有用性权衡 |
|------|-------------|-----------|
| RLHF | 显著 | 轻微 |
| Constitutional AI | 最高 40.8% | 9.8% |
| IterAlign | 13.5% | 保持 |

### 4.1 从 RLHF 到 DPO 与 GRPO

对齐方法在 2024-2025 年发生重要演进：

| 方法 | 核心思想 | 优势 | 局限 |
|------|---------|------|------|
| **RLHF (PPO)** | 训练奖励模型 + PPO 在线优化 | 效果上限高 | 训练不稳定、需在线采样、成本高 |
| **DPO** | 直接从偏好对优化策略，无需奖励模型 | 简单稳定、离线训练 | 依赖偏好数据质量 |
| **KTO** | 只需"好/坏"单点反馈而非成对比较 | 数据更易获取 | 略逊于 DPO |
| **Constitutional AI / RLAIF** | 用 AI 反馈替代人类反馈 | 可扩展、成本低 | 依赖评判模型质量 |
| **GRPO (RLVR)** | 用可验证奖励（如数学答案）做 RL | 产生推理能力、无需奖励模型 | 需可验证任务 |

> 趋势：偏好对齐主流转向 DPO（简单稳定），推理能力培养转向 RLVR（可验证奖励）。RLHF/PPO 仍在顶级闭源模型中使用，但开源社区已普遍采用更轻量的替代方案。

---

## 5. AI 安全的挑战与未来

### 当前挑战

- **自我批判效果依赖架构**：更强的模型收益更大，弱模型可能模式崩溃
- **原则框架的偏向性**：正向措辞（"应该做什么"）vs 负向措辞（"禁止做什么"）
- **民主合法性**：谁决定 AI 的价值观？
- **技术-社会交叉**：AI 安全不仅是技术问题，也是制度、过程和系统设计问题

### 未来方向

| 方向 | 描述 |
|------|------|
| **民主对齐** | 公众参与价值观设定 |
| **可解释对齐** | 使对齐更加透明可审计 |
| **可扩展监督** | 超越人类评估能力的对齐方法 |
| **多智能体对齐** | 确保 Agent 间交互的安全 |

---

## 🔗 参考资料

- [Constitutional AI: Ethical Alignment for LLMs - Emergent Mind](https://www.emergentmind.com/topics/constitutional-ai-cai)
- [IterAlign: Iterative Constitutional Alignment of LLMs - arXiv](https://arxiv.org/html/2403.18341v1)
- [Helpful, Harmless, Honest? Sociotechnical Limits of AI Alignment - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137480)
- [Constitutional AI Paper Review - Medium](https://medium.com/mlearning-ai/paper-review-constituional-ai-training-llms-using-principles-16c68cfffaef)
- [Inverse Constitutional AI - Harvard](https://dash.harvard.edu/bitstreams/8d79fa6f-a4fc-4cd5-931d-23214597c41d/download)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[平面模型 | 负责任的生成式人工智能工具包 | 面向开发者的谷歌人工智能](https://ai.google.dev/responsible/docs/alignment?hl=zh-cn)**
  - 来源：`ai.google.dev` · 质量分：15 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 对齐是指管理生成式 AI (GenAI) 行为的过程，以确保其输出符合您的产品需求和预期。这些工作是一个开放且活跃的研究领域，您需要确定模型与产品保持一致意味着什么，以及您计划如何强制执行这一点。在本文档中，您可以了解到. ## 提示模板. 提示模板（也称为系统提示）可提供与用户输入和模型输出相关的上下文，具体取决于您的用例，以系统说明和少样本示例的形式引导模型获得更安全、更优质的结果。例如，如果您的目标是高质量. `The follo...

- **[人工智能安全研究人类研究员计划](https://alignment.anthropic.com/2025/anthropic-fellows-program-2026)**
  - 来源：`alignment.anthropic.com` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # 人工智能安全研究人类研究员计划：申请于 2026 年 5 月和 7 月开放。在我们的第一批研究人员中，超过 80% 的研究员发表了论文，包括代理错位、潜意识学习、对新 ASL3 的快速响应越狱和开源电路。今年，我们计划与更多的研究员在更广泛的安全研究领域合作，包括可扩展的监督、对抗鲁棒性和人工智能控制、模型生物体、机械可解释性、人工智能安全和模型福利。研究员为期 4 个月，研究与 Anthropic 整体研究重点相一致的实证研究问题...

- **[大模型对齐的技术路线：人类反馈强化学习与超级对齐的视角探讨 | 大模型安全与对齐读书会 | 集智俱乐部](https://swarma.org/?p=48144)**
  - 来源：`swarma.org` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - **集智俱乐部和安远AI联合举办“大模型安全与对齐”读书会，由多位海内外一线研究者联合发起，针对大模型安全与对齐所涉及的核心技术、理论架构、解决路径以及安全治理等交叉课题，展开共读共研活动。读书会自2024年1月27日正式开始，每周六上午举行，为期8-10周。欢迎从事相关研究与应用工作的朋友报名加入！**. 大模型安全与对齐读书会的第二期，我们邀请到苏黎世联邦理工学院（ETH Zurich）计算机系博士生陈欣和天津大学计算机系博士生沈田...

- **[什么是 RLHF？AI 对齐与人类反馈指南 | Ultralytics](https://ultralytics.com/zh/glossary/reinforcement-learning-from-human-feedback-rlhf)**
  - 来源：`ultralytics.com` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 遇见 YOLO26： 下一代视觉 AI。 下一代实时视觉 AI。. # Reinforcement Learning from Human Feedback (RLHF). 了解从人类反馈中进行强化学习 (RLHF) 如何使 AI 与人类价值观保持一致。探索其核心组件以及与 Ultralytics YOLO26 的集成。. 基于人类反馈的强化学习 (RLHF) 是一种先进的机器学习技术，它通过将人类的直接输入纳入训练循环来改进人工智能模...

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
