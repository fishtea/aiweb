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

## 💡 深入理解：语言模型的演进与核心概念

### 从 N-gram 到 Transformer

语言模型的建模方法经历了三次重大飞跃：

| 阶段 | 代表模型 | 核心原理 | 优势 | 局限 |
|------|---------|---------|------|------|
| **统计模型** | N-gram | 基于词频统计预测下一个词 | 简单快速 | 上下文窗口极短(仅前 N-1 个词)、稀疏性大 |
| **神经网络** | RNN / LSTM | 逐步处理序列，学习上下文 | 比 N-gram 更长的上下文记忆 | 梯度消失、不能并行处理、长上下文仍受限 |
| **大规模预训练** | Transformer (GPT/BERT) | 自注意力机制，同时处理所有 token | 全上下文理解、可并行训练、参数量级飞跃 | 计算成本高、上下文窗口有上限 |

> 来源：[Google Developers — 大型语言模型简介](https://developers.google.com/machine-learning/crash-course/llm?hl=zh-cn)（2026 年 1 月更新）

### Token 化（分词）详解

Token 化是将文本切分为最小处理单元的过程。现代 LLM 大多使用**子词分词**（Subword Tokenization）：

- `unwatched` → `un` + `watch` + `ed`
- `cats` → `cat` + `s`
- `antidisestablishmentarianism` → 6 个子字词

**Token 数量估算**（英语环境）：
- 4 个字符 ≈ 1 个 token
- 3/4 个单词 ≈ 1 个 token
- 400 tokens ≈ 300 个英文词

Token 化已不限于文本——该概念已成功应用于计算机视觉和音频生成领域。

### 语言模型的概率本质

LLM 的核心是**概率预测**：给定前文，计算下一个 token 的概率分布。例如句子 *"When I hear rain on my roof, I ____ in my kitchen."* 的可能补全：

| 概率 | 补全词 |
|:----:|:------:|
| 9.4% | 煮汤 |
| 5.2% | 温热水壶 |
| 3.6% | 畏缩 |
| 2.5% | 小憩 |

模型可选择概率最高者，或从高于阈值的候选词中随机采样——这种**随机性**正是 LLM 每次输出略有不同的原因。

### 补充学习资源

| 资源 | 类型 | 说明 |
|------|------|------|
| [Google ML Crash Course: LLM](https://developers.google.com/machine-learning/crash-course/llm) | 课程 | Google 官方的 LLM 入门（含交互式练习） |
| [DataWhale Happy-LLM](https://github.com/datawhalechina/happy-llm) | 开源教程 | 从零搭建大语言模型的中文教程，7 章覆盖 NLP 基础到 LLM 应用 |
| [Botpress：2026 十大 LLM 排名](https://botpress.com/tw/blog/best-large-language-models) | 对比分析 | 2026 年最新模型价格、上下文窗口、能力对比 |

### LLM 能力维度速查

理解一个 LLM，可以从这几个维度建立判断框架：

| 维度 | 关键问题 | 影响 |
|------|---------|------|
| 参数规模 | 多少参数？激活多少？ | 能力上限与硬件需求 |
| 上下文窗口 | 能处理多长输入？ | 长文档、多轮对话、代码库分析 |
| 训练数据 | 数据量、语种、时效截止 | 知识覆盖与新鲜度 |
| 推理能力 | 是否支持思维链/推理模式 | 复杂问题求解 |
| 工具调用 | 是否原生支持函数调用 | Agent 构建能力 |
| 多模态 | 是否支持图/音/视频 | 应用范围 |
| 部署方式 | 闭源 API 还是开源权重 | 成本、隐私、可控性 |
| 许可证 | 商用是否受限 | 企业合规 |

> 新手常见误区：只看"哪个模型最强"。更实用的问法是"我的任务（输入长度、输出格式、准确率要求、预算、隐私要求）适合哪个模型"。选型是综合权衡，不是单维排名。

---

## 🚀 LLM 的实际应用与上手实践

**来源：** 本文内容参考了 freeCodeCamp 的 [A Beginner's Guide to LLMs](https://freecodecamp.org/news/a-beginners-guide-to-large-language-models)（Bhavishya Pandit, 2024 年 8 月）以及 DataCamp 的 [What is an LLM?](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models) 指南。

### LLM 的核心应用场景

| 领域 | 具体应用 | 工作方式 |
|------|---------|---------|
| **内容创作** | 写作助手（如 Grammarly）、自动故事生成 | 给定提示词，模型续写或润色 |
| **客户服务** | 聊天机器人、虚拟助手（Siri/Alexa） | 理解用户查询并实时响应 |
| **医疗健康** | 病历摘要、辅助诊断 | 分析患者数据 + 医学文献 |
| **研究与教育** | 文献综述、AI 辅导 | 提炼大量论文摘要，个性化学习 |
| **娱乐** | 游戏 NPC 对话、音乐/艺术生成 | 动态生成角色交互 |

### LLM 的训练流程（简化版）

根据 freeCodeCamp 文章的描述，LLM 的训练分为四个步骤：

1. **数据收集**：从书籍、网页、论文、社交媒体收集数百万甚至数十亿文档
2. **学习模式**：模型分析数据，学习语法规则、词义关联、上下文关系乃至常识
3. **微调（Fine-Tuning）**：针对特定任务优化模型参数（翻译、摘要、问答等）
4. **评估与测试**：在一系列基准测试上验证准确率、效率和安全性

> **关键洞察**：LLM 不是从单个句子中学习，而是从**数万亿个句子**中提取统计规律。本质上，它是一个经过海量文本训练的概率预测系统。

### 如何用代码调用 LLM？

以下是 freeCodeCamp 文章中展示的实操示例，使用 Replicate 库调用 Meta 的 Llama 3 70B 模型：

```python
import os
import replicate  # pip install replicate

# 从 https://replicate.com/account/api-tokens 获取 Token
os.environ["REPLICATE_API_TOKEN"] = "你的_TOKEN"

api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

# 调用 Llama 3 70B 模型
output = api.run(
    "meta/meta-llama-3-70b-instruct",
    input={"prompt": "用中文解释什么是大语言模型"}
)

# 打印输出
for item in output:
    print(item, end="")
```

通过类似方式，你可以基于 Llama 3、GPT API 或 Claude API 构建各种 AI 应用，只需调整 prompt（提示词）即可适配不同场景。

### 使用建议

- **Prompt 质量决定输出质量**：清晰、具体的提示词远优于模糊的提问
- **善用系统提示词（System Prompt）**：设定角色和规则可以大幅提升输出一致性
- **注意上下文窗口限制**：不同模型支持的输入长度不同（4K-200K token 不等），超出部分会被截断
- **警惕幻觉**：LLM 可能会生成看似合理但实际错误的信息，关键任务需要人工复核

---

## 🧬 2026 LLM 深度解析：架构、训练与能力扩展

### LLM 发展时间线

| 年份 | 里程碑 | 意义 |
|------|--------|------|
| 2017 | Transformer 论文《Attention Is All You Need》 | 奠定所有现代 LLM 的架构基础 |
| 2018 | BERT（Google）、GPT-1（OpenAI） | 预训练 + 微调范式确立 |
| 2019 | GPT-2（15 亿参数） | OpenAI 因"太危险"一度拒绝开源 |
| 2020 | GPT-3（1750 亿参数） | 涌现能力被发现，few-shot learning 震惊学界 |
| 2022 | ChatGPT（GPT-3.5） | 消费级 AI 助手引爆全球，2 个月破亿用户 |
| 2023 | GPT-4、Claude 2、LLaMA 2 | 多模态能力登场，开源模型生态爆发 |
| 2024 | OpenAI o1、Claude 3.5 | **推理模型**诞生——模型学会"先思考再说" |
| 2025 | DeepSeek-R1、GPT-4o、Claude 4 | 开源推理模型性能比肩闭源，成本低 95% |
| 2026 | Gemini 2.5、LLaMA 4 | 多模态 + 推理融合，Agent 能力成熟 |

### 架构核心：Transformer 运作机制

```
输入: "我 喜欢 吃 ___"
         ↓
    [Token 化] → [我] [喜欢] [吃] [MASK]
         ↓
    [嵌入层] → 将每个 token 转为向量 (如 768 维)
         ↓
    [多头注意力] → 计算每个 token 与其他 token 的关联度
         ↓
    [前馈网络] → 非线性变换
         ↓
    [输出层] → 预测下一个 token: "苹果" (概率 0.3) "面包" (0.25) ...
```

**核心创新——自注意力（Self-Attention）**：
- 并行计算所有 token 之间的关系（RNN 必须串行）
- 任意位置的两个 token 可以直接交互（解决长距离依赖）
- 多头注意力 = 多个"视角"同时关注不同方面的关系

### 训练流程

```
阶段 1：预训练（Pre-training）
  数据：数万亿 token 的网页文本、代码、书籍
  任务：预测下一个词（自监督学习）
  成本：GPT-4 级别约 $1 亿+，DeepSeek-V3 约 $560 万
  ↓
阶段 2：监督微调（SFT）
  数据：数万条高质量人工标注的指令-回答对
  任务：让模型学会"遵循指令"
  ↓
阶段 3：RLHF（人类反馈强化学习）
  步骤：收集人类偏好数据 → 训练奖励模型 → PPO 强化学习优化
  效果：让回答更有用、更安全、更符合人类价值观
```

### MoE（混合专家）——2026 年主流架构

传统模型：所有参数参与每次推理 → 计算成本高
**MoE 模型**：只有部分"专家"被激活 → 总参数量大但推理成本低

```
输入 Token → 路由网络（Gating）→ 选择 Top-2 专家 → 加权合并输出
                ↓
        专家 1（代码） 专家 2（数学） 专家 3（常识） 专家 4（翻译）
                                          ↑         ↑
                                    只有被选中的专家被激活
```

DeepSeek-V3（671B 总参数，每次只激活 37B）就是用 MoE 实现高性能+低成本的代表。

### LLM 能力扩展技术

| 技术 | 原理 | 典型场景 |
|------|------|---------|
| **Prompt Engineering** | 精心设计输入提示引导模型行为 | 所有 LLM 交互的基础技能 |
| **RAG（检索增强生成）** | 从外部知识库检索相关文档，注入上下文 | 企业知识问答、客服系统 |
| **Function Calling（工具调用）** | LLM 调用外部 API 获取实时信息或执行操作 | 联网搜索、代码执行、数据库查询 |
| **Chain-of-Thought（思维链）** | 引导模型逐步推理而非直接给答案 | 数学题、逻辑推理、复杂规划 |
| **AI Agent** | 模型自主规划、执行、反思、迭代 | 自动化工作流、多步骤任务 |

### 推理模型（Reasoning Models）——2024-2026 最大突破

传统 LLM：问 → 答（一步到位，复杂问题容易出错）
**推理模型**：问 → 思考 → 思考 → 思考 → 答

- OpenAI o1（2024.09）：IMO 数学资格赛 83% 准确率（GPT-4o 仅 13%）
- DeepSeek-R1（2025.01）：671B 参数开源模型，性能比肩 o1，成本仅 5%
- OpenAI o3（2025.04）：推理能力进一步提升

推理模型的出现被视为通向 AGI 的关键一步。

### 量化——让大模型"瘦身"

| 精度 | 每参数大小 | 70B 模型所需显存 |
|------|-----------|-----------------|
| FP32 | 4 字节 | ~280 GB |
| FP16 | 2 字节 | ~140 GB |
| INT8 | 1 字节 | ~70 GB |
| INT4 | 0.5 字节 | ~35 GB |

通过量化（Quantization）+ LoRA 微调，70B 模型可在消费级硬件上运行（如双 RTX 3090）。

---

## 🧩 LLM 学习路线图：从零到部署的三阶段路径

根据 [Maxime Labonne 的 LLM Course](https://github.com/mlabonne/llm-course)（GitHub 30k+ stars），系统学习 LLM 建议遵循三阶段路径：

### 阶段 1：LLM 基础（LLM Fundamentals）— 可选先修

如果缺乏数学、Python 或神经网络基础，先补充这些知识：

| 模块 | 核心内容 | 推荐资源 |
|------|---------|---------|
| **机器学习数学** | 线性代数（向量、矩阵、特征值）、微积分（导数、梯度）、概率统计（贝叶斯、MLE） | [3Blue1Brown 线性代数](https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)、[StatQuest 统计学](https://www.youtube.com/watch?v=qBigTkBLU6g&list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9) |
| **Python ML** | NumPy、Pandas、Matplotlib、Scikit-learn、数据预处理 | [Real Python](https://realpython.com/)、[Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) |
| **神经网络** | 感知机、激活函数、反向传播、过拟合、MLP | [3Blue1Brown 神经网络](https://www.youtube.com/watch?v=aircAruvnKk)、[Fast.ai](https://course.fast.ai/) |
| **NLP 基础** | Tokenization、BoW/TF-IDF、词嵌入、RNN/LSTM | [Lena Voita NLP 课程](https://lena-voita.github.io/nlp_course/word_embeddings.html)、[Jay Alammar Word2Vec](https://jalammar.github.io/illustrated-word2vec/) |

### 阶段 2：LLM 科学家之路（The LLM Scientist）— 构建最佳 LLM

这个阶段专注于理解和使用最新技术来构建 LLM：

| 模块 | 核心内容 |
|------|---------|
| **1. LLM 架构** | Tokenization → 自注意力机制 → Transformer 解码器 → 采样策略（贪心/束搜索/温度/top-p） |
| **2. 预训练** | 数据准备（FineWeb、RedPajama）→ 分布式训练（数据/流水线/张量并行）→ 训练优化 → 监控 |
| **3. 后训练数据集** | 指令-回答对格式 → 合成数据生成（GPT-4o 生成）→ 数据增强（Rejection Sampling、Auto-Evol）→ 质量过滤 |
| **4. 监督微调（SFT）** | 全参数微调 vs LoRA/QLoRA → Axolotl/Unsloth 工具 → 对话模板（ChatML、Alpaca） |
| **5. 偏好对齐** | RLHF → DPO/ORPO → 奖励模型训练 → 偏好数据构建 |
| **6. 模型评估** | 基准测试（MMLU、HumanEval、GSM8K）→ LLM-as-a-Judge → 自动评估流水线 |
| **7. 量化与部署** | GPTQ/AWQ/GGUF 量化 → vLLM/TGI 推理 → Ollama 本地部署 |
| **8. 合并与 MoE** | MergeKit 模型合并 → 多专家 MoE 构建 |

### 阶段 3：LLM 工程师之路（The LLM Engineer）— 构建 LLM 应用

| 模块 | 核心内容 |
|------|---------|
| **1. Prompt Engineering** | 系统提示、思维链、Few-shot、结构化输出 |
| **2. RAG（检索增强生成）** | 文档分块 → Embedding → 向量数据库 → 检索 → 生成 |
| **3. Agent 智能体** | 工具调用 → 自主规划 → 多 Agent 协作 |
| **4. 评估与可观测性** | LLM 应用测试 → 追踪（Langfuse/LangSmith）→ 质量监控 |

### 核心参考资源

| 资源 | 类型 | 说明 |
|------|------|------|
| [LLM Course (mlabonne)](https://github.com/mlabonne/llm-course) | 课程 | 三阶段路线，30k+ stars |
| [3Blue1Brown Transformer 可视化](https://www.youtube.com/watch?v=wjZofJX0v4M) | 视频 | 初学者友好的 Transformer 介绍 |
| [LLM Visualization](https://bbycroft.net/llm) | 交互式工具 | 3D 可视化 LLM 内部结构 |
| [nanoGPT (Andrej Karpathy)](https://www.youtube.com/watch?v=kCc8FmEb1nY) | 视频 | 从零实现 GPT（2 小时） |
| [LLM Engineer's Handbook](https://packt.link/a/9781836200079) | 书籍 | 端到端 LLM 应用构建实战 |

**来源：** [LLM Course GitHub](https://github.com/mlabonne/llm-course) | [Maxime Labonne 博客](https://mlabonne.github.io/blog/)

---

## 🔬 LLM 架构的核心：自注意力机制详解

根据 LLM Course 和 Google Developers LLM 入门指南，自注意力（Self-Attention）是 Transformer 和所有现代 LLM 的核心创新：

### 自注意力的工作原理

```
输入: "The cat sat on the mat"
      ↓
    每个词转换为 Query、Key、Value 三个向量
      ↓
    计算每个词 Query 与所有词 Key 的点积 → 注意力分数
      ↓
    Softmax 归一化 → 加权求和 Value
      ↓
    输出: 每个位置获得"看了上下文"的新表示
```

### 为什么自注意力如此重要？

- **并行计算**：所有 token 同时处理（RNN 必须串行处理）
- **长距离依赖**：任意位置的两个 token 可直接交互（RNN 需要通过时间步逐层传递）
- **多头注意力（Multi-Head Attention）**：多个"视角"同时关注不同方面的关系

### 采样策略（文本生成方式）

| 策略 | 原理 | 特点 | 适用场景 |
|------|------|------|---------|
| **贪心搜索（Greedy）** | 每次选概率最高的 token | 确定性输出、可能重复 | 要求确定性的任务 |
| **束搜索（Beam Search）** | 保持多个候选序列 | 更优但计算成本更高 | 翻译、摘要 |
| **温度采样（Temperature）** | 调整概率分布的"锐度" | 温度高→多样性高 | 创意写作 |
| **Top-k 采样** | 只从概率最高的 k 个 token 中采样 | 平衡多样性与质量 | 通用 |
| **Nucleus (Top-p) 采样** | 从累积概率达到 p 的最小集合中采样 | 自适应 | 最常用的策略 |

> LLM Course 指出，理解这些解码策略是构建高质量 LLM 应用的**基础技能**——选错策略会导致输出过于重复或过于随机。

**来源：** [LLM Course — LLM Architecture](https://github.com/mlabonne/llm-course) | [Maxime Labonne — Decoding Strategies in LLMs](https://mlabonne.github.io/blog/posts/2023-06-07-Decoding_strategies.html)

---

## 📚 参考来源

1. [What is an LLM? A Guide on Large Language Models — DataCamp](https://www.datacamp.com/blog/what-is-an-llm-a-guide-on-large-language-models)（2023 年 12 月）
2. [Introduction to Large Language Models: Everything You Need to Know for 2025 — Lakera AI](https://www.lakera.ai/blog/large-language-models-guide)（2025 年 5 月）
3. [Vaswani et al., "Attention Is All You Need" — Google Research, 2017](https://research.google/pubs/pub46201/)
4. [Deep Learning Book — Goodfellow et al.](https://www.deeplearningbook.org/)
5. [Andrej Karpathy — Let's build GPT from scratch](https://youtu.be/kCc8FmEb1nY)
6. [Jay Alammar — The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
7. [Large Language Models Professional Certificate — edX / Databricks](https://www.edx.org/professional-certificate/large-language-models)
8. [Bhavishya Pandit — A Beginner's Guide to LLMs (freeCodeCamp)](https://freecodecamp.org/news/a-beginners-guide-to-large-language-models)
9. [Replicate 平台 — 云上运行 ML 模型](https://replicate.com)
10. [Large Language Model — Wikipedia](https://en.wikipedia.org/wiki/Large_language_model)（2026 年 7 月查阅）
11. [LLM Course (mlabonne) — GitHub](https://github.com/mlabonne/llm-course)
12. [LLM Visualization — Brendan Bycroft](https://bbycroft.net/llm)
13. [Maxime Labonne — Decoding Strategies in LLMs](https://mlabonne.github.io/blog/posts/2023-06-07-Decoding_strategies.html)
14. [3Blue1Brown — Visual intro to Transformers](https://www.youtube.com/watch?v=wjZofJX0v4M)

## 2026 年 LLM 入门实践指南

对于 2026 年的初学者，理解和使用 LLM 已经变得前所未有的简单。以下是一份面向初学者的实用指南：

### 什么是 LLM？简单定义

大语言模型（Large Language Model, LLM）是一种在海量文本数据上训练的人工智能模型，能够理解和生成人类语言。它不是查询数据库，也不是搜索网页——而是在训练完成后，将所有"知识"编码为数十亿个参数中的数值权重，形成一个"压缩的世界模型"。

> 来源：[sunqi.org — How Large Language Models Actually Work](https://www.sunqi.org/llm-basics-understanding-en.html)（2026-03-21）

### LLM 的三个关键训练阶段

| 阶段 | 名称 | 描述 |
|------|------|------|
| ① | **预训练（Pre-training）** | 在海量无标注文本上自我监督学习，模型学习语言结构和世界知识 |
| ② | **监督微调（SFT）** | 使用人工标注的高质量问答对训练，教会模型遵循指令 |
| ③ | **RLHF（人类反馈强化学习）** | 人类评估者对输出评分，通过强化学习让模型更符合人类偏好 |

### 常见误区澄清

**误区①：LLM 像搜索引擎一样查询数据库**
事实：训练完成后，LLM 不查询任何外部数据库。回答完全基于参数中编码的模式。这就是为什么 LLM 有知识截止日期，以及为什么会产生"幻觉"（生成听起来合理但不正确的信息）。

**误区②：LLM 在"思考"和"理解"**
事实：LLM 的核心操作是**下一个词预测（next-token prediction）**——根据已有文本，预测最可能的下一个词。通过自注意力（Self-Attention）机制实现长文本关联，但在本质上仍是复杂的统计模式匹配，而非人类的"理解"或"推理"。

### 2026 年热门 LLM

| 模型 | 开发者 | 特点 |
|------|--------|------|
| **GPT-4o / GPT-5** | OpenAI | 多模态能力，生态成熟 |
| **Claude 4** | Anthropic | 长上下文窗口，安全性突出 |
| **Gemini 2.5** | Google | 多模态原生，与 Google 生态深度集成 |
| **Llama 4** | Meta | 开源权重，社区活跃 |
| **DeepSeek-V3 / R1** | 深度求索 | 高性能开源模型，推理能力出色 |
| **Qwen 3** | 阿里云 | 中文能力优秀，多尺寸可选 |

### 如何选择 LLM（2026 年建议）

- **初学入门**：优先使用 ChatGPT（GPT-4o）或 Claude 的免费版本，体验对话式 AI
- **代码开发**：Claude（长上下文+代码能力强）或 DeepSeek（性价比高）
- **本地部署**：从 Ollama + Llama 4 / Qwen 3 开始，无需 GPU 也能运行小参数模型
- **中文场景**：Qwen 3 或 DeepSeek 在中文理解方面表现优异

### 参考来源

- [What Is LLM (Large Language Model)? Beginner's Guide — CoderMantra](https://www.codermantra.com/what-is-llm/)（2026-07-10）
- [How Large Language Models Actually Work — sunqi.org](https://www.sunqi.org/llm-basics-understanding-en.html)（2026-03-21）
- [What Are Large Language Models (LLMs)? — IBM](https://www.ibm.com/think/topics/large-language-models)
- [What is a large language model (LLM)? — Cloudflare](https://www.cloudflare.com/learning/ai/what-is-large-language-model/)

---

*本页面内容基于真实在线资源编写。所有信息均引用自上述来源（截至 2026 年 7 月）。*

---

## 🧩 2026 年 LLM Agent 技术栈入门

> 以下内容基于 Machine Learning Mastery 2026 年 6-7 月的系列文章整理，帮助初学者理解 LLM 在生产环境中的完整技术栈。

### LLM 不再是孤立的模型——它是一整个技术栈

2026 年，一个生产级的 LLM 应用不止是一个模型，而是 **7 个独立的技术层**协同工作：

```
应用层：    用户界面 / Slack / Web App / API
  ↑
编排层：    LangChain / LlamaIndex / 自定义编排
  ↑
记忆层：    短期记忆 / 长期记忆 / 实体图谱
  ↑
检索层：    向量数据库（Pinecone / Chroma / Qdrant）
  ↑
工具层：    搜索 / 计算器 / 代码执行 / 数据库查询 / API 调用
  ↑
模型层：    GPT-5.5 / Claude 4 / Gemini 3.1 / Llama 4
  ↑
部署层：    vLLM / Ollama / Docker / K8s / 监控（LangSmith / Langfuse）
```

### 每一层的核心职责

| 层次 | 核心问题 | 2026 年代表作 |
|:----:|---------|-------------|
| **模型层** | 推理、理解语言、决定下一步做什么 | GPT-5.5、Claude Sonnet 4.6、Gemini 3.1 Pro、Llama 4 |
| **编排层** | 如何组织多步推理和工具调用 | LangChain、LlamaIndex、自定义编排框架 |
| **记忆层** | 跨会话/跨 Agent 的信息持久化 | 向量数据库 + KV 存储 + 实体图谱 |
| **检索层（RAG）** | 如何从外部知识库获取相关信息 | Pinecone、Chroma、Qdrant、Weaviate |
| **工具层** | Agent 如何调用外部 API 执行操作 | Function Calling、MCP（Model Context Protocol） |
| **可观测性层** | 如何追踪、调试和评估 Agent 行为 | LangSmith、Langfuse、Weights & Biases |
| **部署层** | 如何将以上所有内容投入生产 | Docker、Kubernetes、vLLM、Ollama |

### 2026 年模型选型指南

| 需求 | 推荐模型 | 理由 |
|------|---------|------|
| 快速原型 | GPT-5.5 | 速度快、推理准确、生态成熟 |
| 长文档处理 | Claude Sonnet 4.6 | 指令遵循好、价格适中 |
| 大上下文窗口 | Gemini 3.1 Pro | 100 万 token 上下文窗口 |
| 复杂推理 | Claude Opus 4.8 | 深度推理能力最强 |
| 本地部署/隐私 | Llama 4 / Mistral Large 3 | 完全开源、可自托管 |
| 中文优化 | Qwen 3 / DeepSeek-V3 | 中文理解与生成优秀 |

> ⚠️ **2026 年重要转变**：不再有"标准模型"和"推理模型"的硬性区分——GPT-5.5、Claude、Gemini 都已将推理能力内建到单一模型中，只需调整 `reasoning_effort` 参数即可控制思考深度。

### 给初学者的学习路径

1. **从 API 开始**：不要想着从零训练模型。先用 GPT-5.5 或 Claude API 体验 LLM 的能力边界。
2. **掌握 Prompt Engineering**：系统提示、思维链（CoT）、少样本提示——这是与 LLM 交互的基础技能。
3. **理解 RAG 架构**：向量检索 + LLM 生成是企业级 LLM 应用的标准模式。
4. **学习 Function Calling**：让 LLM 能够调用外部工具，是 Agent 能力的核心。
5. **搭建第一个 Agent**：从单一工具的 Agent 开始，逐步增加复杂性。
6. **关注可观测性**：LLM 应用调试是生产环境中的最大难点。

### 参考来源

- [The AI Agent Tech Stack Explained — Machine Learning Mastery](https://machinelearningmastery.com/the-ai-agent-tech-stack-explained/)（Shittu Olumide, 2026-06-27）
- [Context vs. Memory Engineering in Agentic AI Systems — Machine Learning Mastery](https://machinelearningmastery.com/context-vs-memory-engineering-in-agentic-ai-systems/)（Bala Priya C, 2026-07-03）

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-16 00:08:55*
