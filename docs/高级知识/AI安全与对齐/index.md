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

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
