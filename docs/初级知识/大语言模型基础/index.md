# 大语言模型基础

## 📖 概述

大语言模型（Large Language Model，简称 LLM）是当前 AI 领域最具影响力的技术之一。它们是一种使用**深度神经网络**（具体来说是 Transformer 架构）训练的大规模 AI 系统，能够理解和生成人类语言。

> 根据 [DataCamp 的定义](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models)：「LLM 是用于建模和处理人类语言的 AI 系统。它们之所以被称为『大』，是因为这类模型通常由数亿甚至数十亿个参数组成，这些参数定义了模型的行为，并通过海量文本数据预训练而成。」

---

## 🏗️ LLM 的核心技术

### 1. Transformer 架构

LLM 的基础技术是 **Transformer 神经网络**，由 Google 研究人员在 2017 年的论文《[Attention Is All You Need](https://research.google/pubs/pub46201/)》中提出。

**关键创新：自注意力机制（Self-Attention）**

与传统的 RNN 和 CNN 不同，Transformer 的注意力机制允许模型：
- **双向预测：** 根据上下文中的前后词语来理解当前词
- **并行计算：** 所有 token 可以同时处理，训练效率极大提升
- **长距离依赖：** 在上下文窗口内，任意位置的两个 token 可以直接交互

> 根据 [Lakera AI 的 LLM 指南](https://www.lakera.ai/blog/large-language-models-guide)：「自注意力计算每个 token 相对于上下文中所有其他 token 的重要性。」

### 2. Token 化与嵌入

```
输入文本 → Token化 → 嵌入向量 → Transformer处理 → 输出概率分布 → 生成下一个词
```

- **Token：** LLM 处理的基本单位，可以是词、子词或字符。目前最常用的是**子词 Token 化**（如 BPE、SentencePiece）
- **嵌入（Embedding）：** 将每个 token 转换为高维向量，捕捉语义信息

参考资源：
- [Hugging Face Tokenization 教程](https://huggingface.co/learn/nlp-course/chapter2/4?fw=pt)
- [OpenAI tiktoken](https://github.com/openai/tiktoken)

---

## 🔄 训练过程

LLM 的训练分为两个主要阶段：

### 阶段一：预训练（Pre-training）

| 项目 | 说明 |
|------|------|
| **数据** | 互联网上的海量无标签文本 |
| **目标** | 学习语言的统计规律和知识 |
| **方法** | 自监督学习：预测下一个 token |
| **规模** | 需要巨大算力（如 LLaMA 2 使用了 **330 万 GPU 小时** 训练在 **2 万亿 token** 上） |
| **排放** | LLaMA 2 训练排放约 539 吨 CO₂（已由 Meta 碳中和抵消） |

**预训练示例：**
给定句子「猫是黑色的」，模型会自动生成 5 个训练样本：

| 输入（上下文） | 目标预测 |
|:-------------:|:--------:|
| `<SOS>` | 猫 |
| 猫 | 是 |
| 猫是 | 黑 |
| 猫是黑 | 色 |
| 猫是黑色 | 的 |

### 阶段二：微调（Fine-tuning）

在预训练模型的基础上，使用特定领域的标注数据进一步训练，使模型适应特定任务。

**强化学习从人类反馈（RLHF）：**
一种流行的微调方法，通过人类对模型输出的评价来优化模型行为。ChatGPT 的成功很大程度上归功于 RLHF。

---

## 🧪 文本生成过程

当 LLM 生成文本时，实际执行的是：

1. 接收输入文本作为上下文
2. 对上下文进行 token 化
3. 通过 Transformer 计算每个候选 token 的概率
4. 选择下一个 token（贪心解码或采样）
5. 将新 token 加入上下文，重复步骤 2-5
6. 遇到结束标记（EOS）时停止

**解码策略：**
- **贪心解码（Greedy）：** 每次选概率最高的 token
- **采样（Sampling）：** 根据概率分布随机采样，增加输出多样性
- **Top-k / Top-p：** 限制候选集大小，平衡多样性与质量

---

## 💡 主流 LLM 一览

| 模型 | 开发者 | 参数规模 | 特点 |
|:----:|:------:|:--------:|------|
| **GPT-4** | OpenAI | 约 1.8T（推测） | 多模态，ChatGPT 基础 |
| **GPT-3.5** | OpenAI | 175B | ChatGPT（早期版本） |
| **LLaMA 2** | Meta | 7B-70B | 开源，研究友好 |
| **Claude 3** | Anthropic | 未公开 | 注重安全性 |
| **Gemini** | Google | 未公开 | 多模态，原生 |
| **BERT** | Google | 340M | 双向编码器，理解能力强 |
| **PaLM 2** | Google | 340B | 多语言能力强 |

---

## 🚀 主要应用场景

| 应用 | 说明 | 示例 |
|------|------|------|
| **文本生成** | 根据提示生成类人文本 | ChatGPT、Claude |
| **翻译** | 跨语言翻译 | Google Translate、DeepL |
| **情感分析** | 判断文本情感倾向 | 评论分析、舆情监控 |
| **对话 AI** | 智能问答、客服 | ChatGPT、客服机器人 |
| **代码生成** | 根据描述生成代码 | GitHub Copilot、Codex |
| **文本摘要** | 长文自动摘要 | 新闻摘要、会议纪要 |
| **信息检索** | 增强 RAG 系统 | 企业知识库问答 |

---

## ⚠️ 局限性与挑战

| 挑战 | 说明 |
|------|------|
| **幻觉（Hallucination）** | 模型可能生成看似合理但实际错误的内容 |
| **黑箱问题** | 难以解释模型的内部决策过程 |
| **偏见与歧视** | 训练数据中的偏见可能被模型学习并放大 |
| **隐私风险** | 训练数据可能包含个人信息 |
| **计算成本** | 训练和推理需要大量算力和能源 |
| **环境足迹** | 大模型训练产生的碳排放问题 |

**来源：** [DataCamp — What is an LLM?](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models)

---

## 🎯 学习建议

### 从哪里开始？

如果你想系统学习 LLM：

1. **先打基础** — 确保至少学完了机器学习基础和深度学习入门
2. **理解 Transformer** — 阅读 [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)（经典可视化教程）
3. **动手实践** — 使用 Hugging Face 的 transformers 库运行预训练模型
4. **学习 RAG 和提示工程** — 这是当前 LLM 应用开发的核心技能
5. **关注社区** — 阅读 DeepLearning.AI 的 [The Batch 周刊](https://www.deeplearning.ai/the-batch/)

### 推荐学习资源

| 资源 | 类型 | 适合 |
|------|------|------|
| [Lakera AI：Introduction to LLMs](https://www.lakera.ai/blog/large-language-models-guide) | 文章 | 初学者全面了解 |
| [DataCamp：What is an LLM?](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models) | 文章 | 初学者全面了解 |
| [Andrej Karpathy — Let's build GPT from scratch](https://youtu.be/kCc8FmEb1nY) | 视频 | 想深入理解实现 |
| [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course) | 课程 | 动手实践 |
| [Large Language Models Professional Certificate — edX/Databricks](https://www.edx.org/professional-certificate/large-language-models) | 课程 | 系统学习 |
| [Jay Alammar — The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/) | 博客 | 可视化理解 Transformer |

---

## 📚 参考来源

1. [What is an LLM? A Guide on Large Language Models — DataCamp](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models)（2023 年 12 月）
2. [Introduction to Large Language Models: Everything You Need to Know for 2025 — Lakera AI](https://www.lakera.ai/blog/large-language-models-guide)（2025 年 5 月）
3. [Vaswani et al., "Attention Is All You Need" — Google Research, 2017](https://research.google/pubs/pub46201/)
4. [Deep Learning Book — Goodfellow et al.](https://www.deeplearningbook.org/)
5. [Andrej Karpathy — Let's build GPT from scratch](https://youtu.be/kCc8FmEb1nY)
6. [Jay Alammar — The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
7. [Large Language Models Professional Certificate — edX / Databricks](https://www.edx.org/professional-certificate/large-language-models)

---

*本页面内容基于真实在线资源编写。所有信息均引用自上述来源（截至 2026 年 6 月）。*
