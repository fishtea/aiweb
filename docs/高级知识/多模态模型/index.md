# 多模态模型

> 多模态 AI 模型能够同时处理和理解多种数据类型（文本、图像、音频、视频等）。本页面总结了视觉语言模型（VLM）、CLIP 等核心技术。

---

## 1. 什么是多模态模型？

**来源：** [Vision Language Models Guide - AnnotationBox](https://annotationbox.com/vision-language-models-guide)

视觉语言模型（VLM）是能够理解和处理图像/视频与文本的 AI 系统。它们可以执行：

- **图像描述**（Image Captioning）
- **视觉问答**（Visual Question Answering, VQA）
- **图文搜索**（Text-to-Image Search）
- **视频理解**（Video Understanding）
- **图像生成**（Image Generation）

> *"A vision language model is an AI that understands and processes both images/videos and text."*

---

## 2. VLM 工作原理（三步流程）

**来源：** [Vision Language Models Guide - AnnotationBox](https://annotationbox.com/vision-language-models-guide)

### 步骤 1：多模态输入编码

- **视觉编码器**（ViT、CNN、ConvNeXt）→ 结构化数值表示（视觉嵌入）
- **语言编码器**（Transformer-based LLM）→ 文本嵌入

### 步骤 2：投影与对齐

**视觉-语言投影器**（通常是小 MLP）将视觉特征映射到文本嵌入空间，使得图像 token 和文本 token 能在同一语义空间中处理。

### 步骤 3：Token 融合与生成

集成和融合视觉与文本 token 表示，然后由 **仅解码器语言模型** 自回归生成输出。

**融合方法：**

| 方法 | 描述 |
|------|------|
| **早期融合** | 将图像块和文本视为单一序列 |
| **交叉注意力** | 沿通道维度的交叉注意力 |
| **TokenFusion** | 剪枝单模态 transformer，重用于跨模态融合 |
| **FrameFusion** | 减少视觉 token 70%，精度损失 <3% |

---

## 3. CLIP（对比语言-图像预训练）

**来源：** [Inside CLIP: How Multimodal AI Learns to See and Speak - GoPenAI](https://blog.gopenai.com/inside-clip-how-multimodal-ai-learns-to-see-and-speak-the-same-language-1415f5f92f06), [Exploring OpenAI CLIP - Zilliz](https://zilliz.com/learn/exploring-openai-clip-the-future-of-multimodal-ai-learning)

OpenAI 的 CLIP（Contrastive Language-Image Pre-training）是多模态学习的里程碑模型。

### 核心思想

同时训练两个编码器：
- **图像编码器**（ViT 或 ResNet）
- **文本编码器**（Transformer）

训练目标：最大化匹配图-文对的余弦相似度，最小化不匹配对的相似度。

### 关键创新

- **零样本迁移**：无需微调即可在未见过的任务上表现良好
- **开放词汇**：不限于固定标签集
- **语义对齐**：将视觉和语言统一到同一语义空间

### 应用

- 图文检索
- 零样本分类
- 多模态搜索
- 作为更大 VLM 的视觉编码组件

---

## 4. 主流多模态模型对比

**来源：** [AnnotationBox VLM Guide](https://annotationbox.com/vision-language-models-guide), [Multimodal AI Guide - Meta Intelligence](https://www.meta-intelligence.tech/en/insight-multimodal-ai)

| 模型 | 发布 | 参数量 | 模态 | 特点 |
|------|------|--------|------|------|
| **GPT-4o** | 2024.05 | 未公开 | 文本+图像+音频+视频 | 全模态统一模型，顶级推理能力 |
| **Gemini 1.5 Pro** | 2024.02 | 未公开 | 文本+图像+音频+视频 | 2M+ token 超长上下文 |
| **Claude 3.5 Sonnet** | 2024.06 | 未公开 | 文本+图像 | 宪法 AI，低幻觉 |
| **Qwen2-VL 72B** | 2024.08 | 72B | 文本+图像+视频 | 原生视频理解，多语言 OCR |
| **Llama 3.2 Vision** | 2024.09 | 11B/90B | 文本+图像 | 高效适配器架构 |
| **Molmo 72B** | 2024.09 | 72B | 文本+图像 | 高精度图像指向与空间定位 |
| **LLaVA** | 2023-2024 | 7B-34B | 文本+图像 | 开源社区标杆 |

### 关键洞察

> *"Visual supervision improves experimental interpretation by 10-25% and yields 5-16% gains on text-only scientific reasoning tasks."*

- **闭源模型**：精度领先，但受限于 API 定价和缺乏微调能力
- **开源模型**：性能在闭源模型的 5-10% 以内，提供完全控制和零推理成本

### 4.1 多模态模型的新趋势（2025-2026）

| 趋势 | 说明 | 代表 |
|------|------|------|
| 原生全模态 | 从训练之初融合文/图/音/视频，而非后期拼接 | GPT-4o, Gemini 2.5, Qwen3-VL |
| 视觉 Agent | 看屏幕操作 GUI，完成浏览器/软件自动化 | Claude Computer Use, GPT-5, AutoGLM |
| 统一生成 | 一个模型同时生成文/图/音，而非分离模型 | GPT-4o 图像生成, Gemini |
| 长视频理解 | 输入整段视频做摘要、检索、事件定位 | Gemini 2M 上下文 |
| 文档/版式理解 | 高精度解析表格、图表、公式、手写 | Qwen2.5-VL, LlamaParse |

> 选型建议：通用多模态对话 → GPT-4o / Gemini / Claude；文档与图表理解 → Qwen2.5-VL / MiniCPM-V（开源）；GUI 自动化 → Claude Computer Use / GPT-5；本地部署 → Qwen-VL 系列。

---

## 5. VLM vs 传统语言模型

| 特性 | 传统语言模型 | VLM |
|------|-------------|-----|
| 输入 | 仅文本 | 文本 + 图像/视频 |
| 主要任务 | 文本生成/理解 | 视觉推理与多模态分析 |
| 组件 | 编码器/解码器 | 视觉编码器 + LLM + 投影器 |
| 输出 | 文本 | 文本（描述/分析图像） |
| 上下文 | 语言/语义 | 空间/视觉 + 文本 |

---

## 🔗 参考资料

- [Vision Language Models Guide - AnnotationBox](https://annotationbox.com/vision-language-models-guide)
- [Multimodal AI Guide: Enterprise Applications - Meta Intelligence](https://www.meta-intelligence.tech/en/insight-multimodal-ai)
- [Inside CLIP: How Multimodal AI Learns - GoPenAI](https://blog.gopenai.com/inside-clip-how-multimodal-ai-learns-to-see-and-speak-the-same-language-1415f5f92f06)
- [Exploring OpenAI CLIP - Zilliz](https://zilliz.com/learn/exploring-openai-clip-the-future-of-multimodal-ai-learning)
- [Comprehensive Survey of MLLMs in Vision-Language Tasks - MDPI](https://www.mdpi.com/2079-3197/14/6/125)

---

## 6. 2026 年多模态模型最新进展

### 6.1 Qwen3-VL：视觉 Agent 与空间推理新高度

**来源：** [Qwen3-VL - Ollama Blog (2025-10-14)](https://ollama.com/blog/qwen3-vl)

2025 年 10 月发布的 Qwen3-VL 是 Qwen 系列最强的视觉语言模型，关键能力包括：

- **视觉 Agent（Visual Agent）**：可直接操作 PC 和移动端 GUI——识别界面元素、理解功能语义、调用工具完成任务，标志着 VLM 从"看图说话"进化到"看图操作"
- **视觉编程增强（Visual Coding Boost）**：从图片/视频直接生成 Draw.io 图表、HTML/CSS/JS，打通设计师到开发者的工作流
- **高级空间感知**：判断物体位置、视角和遮挡关系，支持 2D 定位和 3D 空间推理，适用于具身智能（Embodied AI）
- **原生 256K 上下文**（可扩展至 1M）：可处理整本书籍或数小时视频，支持秒级索引
- **增强 OCR**：支持 32 种语言（此前为 19 种），在低光照、模糊、倾斜场景下鲁棒性更强，对稀有/古文字和术语识别能力提升
- **纯文本能力对齐纯 LLM**：文本-视觉无损融合，统一理解

### 6.2 MiniMax M2：面向编程与 Agent 工作流的多模态模型

**来源：** [MiniMax M2 - Ollama Blog (2025-10-28)](https://ollama.com/blog/minimax-m2)

MiniMax M2 是一款专为编程和 Agent 工作流优化的混合专家（MoE）模型：

- **架构**：230B 总参数，仅 10B 激活参数，兼顾低延迟和高吞吐
- **综合智能**：Artificial Analysis 基准测试中，综合得分在开源模型中排名全球第一
- **高级编程能力**：擅长多文件编辑、编码-运行-修复循环和测试验证修复，在 Terminal-Bench 和 (Multi-)SWE-Bench 类任务中表现出色
- **Agent 性能**：可规划和执行跨 Shell、浏览器、检索和代码运行器的长链工具调用
- **部署友好**：低激活参数意味着更低的推理成本和更高的并发能力，特别适合交互式 Agent 和批量采样

### 6.3 本地多模态推理实战：Ollama 引擎升级

**来源：** [Ollama's new engine for multimodal models (2025-05-15)](https://ollama.com/blog/multimodal-models)

Ollama 在 2025 年 5 月推出全新的多模态引擎，首次在本地支持视觉多模态模型：

- 首批支持的模型：Meta Llama 4（109B MoE）、Google Gemma 3、Qwen 2.5 VL、Mistral Small 3.1
- 支持图像输入进行通用多模态理解和推理
- 典型应用：图像描述、位置识别、视频帧分析、文档理解

> 💡 **2026 趋势总结**：多模态模型正从"看懂"进化到"会做"——视觉 Agent 操作 GUI、空间推理支撑具身智能、编程与 Agent 工作流深度融合。开源模型（Qwen3-VL、MiniMax M2）在特定任务上已逼近甚至超越闭源模型。

---

## 7. LLaVA：开源多模态模型的架构标杆

**来源：** [LLaVA Project Page](https://llava-vl.github.io/)（2023-2024）

LLaVA（Large Language-and-Vision Assistant）是首个端到端训练的开源大视觉语言模型，其架构设计和训练方法成为后续众多 VLM 的参考模板。

### 7.1 架构设计

LLaVA 采用简洁的三组件架构：

1. **视觉编码器**：预训练的 CLIP ViT-L/14，负责将图像转换为视觉特征
2. **投影矩阵**：简单线性层（simple projection matrix），将视觉特征映射到 LLM 的文本嵌入空间
3. **大语言模型**：Vicuna（基于 LLaMA），负责理解融合后的多模态表示并生成响应

这种\"视觉编码器 → 投影器 → LLM\"的设计被后续几乎所有开源 VLM 沿用。

### 7.2 两阶段指令微调

LLaVA 提出了**两阶段训练流程**，这一范式成为开源 VLM 训练的标准做法：

| 阶段 | 训练目标 | 更新参数 | 训练数据 |
|------|---------|---------|---------|
| Stage 1: 特征对齐预训练 | 对齐视觉和文本表示空间 | 仅投影矩阵 | CC3M 子集（图像-描述对） |
| Stage 2: 端到端微调 | 学会遵循多模态指令 | 投影矩阵 + LLM | 158K GPT-4 生成的视觉指令数据 |

### 7.3 LLaVA-Instruct-150K 数据集

LLaVA 首次用语言-only GPT-4 生成多模态指令数据，通过 COCO 数据集生成 158K 样本：

| 子集 | 文件大小 | 样本数 | 用途 |
|------|---------|-------|------|
| conversation_58k.json | 126 MB | 58K | 对话式指令 |
| detail_23k.json | 20.5 MB | 23K | 详细描述 |
| complex_reasoning_77k.json | 79.6 MB | 77K | 复杂推理 |

### 7.4 关键成果

- **多模态聊天能力**：在未见过的图像/指令上展现出类似 GPT-4 的多模态行为
- **Science QA 刷新 SOTA**：微调后准确率达 **92.53%**（与 GPT-4 协同）
- **85.1% 相对 GPT-4 得分**：在合成多模态指令跟随数据集上的评估表现

> **历史意义**：LLaVA 证明了\"用纯语言 GPT-4 生成视觉指令数据\"的可行性，大幅降低了高质量多模态训练数据的构建门槛。其两阶段训练范式（特征对齐 → 指令微调）被 Qwen-VL、LLaVA-NeXT、CogVLM 等后续模型广泛采用。

## 8. 多模态模型的应用实践：部署与编程集成

### 8.1 通过 Ollama 快速部署多模态模型

随着 Ollama 多模态引擎的发布（2025年5月），本地运行视觉语言模型变得前所未有的简便。Ollama 支持从命令行直接调用多模态模型，只需传递图像路径即可：

- **Qwen3-VL 235B**：`ollama run qwen3-vl:235b-cloud`，支持多图像输入和拖拽上传
- **Meta Llama 4 109B MoE**：原生视觉理解
- **Google Gemma 3**：轻量级多模态推理
- **MiniMax M2 230B**：10B 激活参数的 MoE 多模态模型

**来源：** [Ollama Qwen3-VL Blog](https://ollama.com/blog/qwen3-vl)（2025-10-14），[Ollama Multimodal Models Blog](https://ollama.com/blog/multimodal-models)（2025-05-15）

### 8.2 多模态模型的编程集成模式

现代多模态模型不仅支持 API 调用，还深度集成到开发工具链中：

**JavaScript 集成（Ollama JS 库）**：
```javascript
import ollama from 'ollama'
const response = await ollama.chat({
  model: 'qwen3-vl:235b-cloud',
  messages: [{
    role: 'user',
    content: '请描述这张图片的内容',
    images: ['./architecture.jpg']
  }]
})
```

**Python 集成（Ollama Python 库）**：
```python
from ollama import chat
response = chat(
  model='qwen3-vl:235b-cloud',
  messages=[{
    'role': 'user',
    'content': 'What is this?',
    'images': ['./diagram.png']
  }]
)
```

**VS Code / Zed 编辑器集成**：MiniMax M2 等模型可以通过 Ollama 直接嵌入 VS Code Copilot Chat 和 Zed Agent 面板，实现多模态辅助编程——从 UI 截图生成代码、从设计稿提取组件逻辑。

**来源：** [MiniMax M2 — Ollama Blog](https://ollama.com/blog/minimax-m2)（2025-10-28）

### 8.3 多模态模型的选型建议（2026 更新）

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 通用多模态对话 | GPT-4o / Gemini 2.5 | 全模态统一，顶级推理 |
| 文档/图表/OCR | Qwen3-VL 235B | 32 语言 OCR，1M 上下文 |
| 编程+Agent 工作流 | MiniMax M2 230B | 10B 激活参数，低延迟高吞吐 |
| GUI 自动化（视觉 Agent） | Qwen3-VL / Claude Computer Use | 操作 PC/移动端界面 |
| 本地部署（隐私敏感） | Qwen2.5-VL / Llama 4 | 完全本地运行 |
| 图像生成 | GPT-4o（原生）/ DALL·E | 文生图融合 |

> 部署建议：生产环境优先考虑延迟和吞吐——MiniMax M2 的 10B 激活参数在交互式 Agent 场景中表现突出。本地开发环境推荐 Qwen3-VL（通过 Ollama），兼顾性能和数据隐私。

---

### 参考来源
- [Qwen3-VL — Ollama Blog](https://ollama.com/blog/qwen3-vl)
- [MiniMax M2 — Ollama Blog](https://ollama.com/blog/minimax-m2)
- [Ollama's new engine for multimodal models](https://ollama.com/blog/multimodal-models)

---

## 9. 2026 多模态模型全景对比与趋势

### 9.1 主流多模态模型能力矩阵（2026 Q3）

| 模型 | 模态支持 | 参数规模 | 上下文 | 开源 | 核心优势 |
|------|---------|---------|--------|------|---------|
| **GPT-4o** | 文本+图像+音频 | 未公开 | 128K | ❌ | 全模态原生融合，实时语音 |
| **Gemini 2.5 Pro** | 文本+图像+音频+视频+代码 | 未公开 | 1M+ | ❌ | 超长上下文，原生多模态 |
| **Claude 3.5 Sonnet** | 文本+图像 | 未公开 | 200K | ❌ | 深度推理+视觉理解 |
| **Qwen3-VL 235B** | 文本+图像+视频 | 235B | 1M | ✅ | 32语言OCR，GUI操作 |
| **MiniMax M2 230B** | 文本+图像 | 230B (10B激活) | 128K | ✅ | 低延迟高吞吐，编程Agent |
| **Llama 4 (109B MoE)** | 文本+图像 | 109B MoE | 128K | ✅ | 开源多模态标杆 |
| **Gemma 3** | 文本+图像 | 1B-27B | 128K | ✅ | 轻量级本地部署 |

### 9.2 2026 多模态模型的四大趋势

**趋势 1：从"看懂"到"会做"——视觉 Agent 崛起**

2026 年多模态模型的竞争焦点已从"理解图像"转向"操作界面"。Qwen3-VL 支持通过视觉理解来操作 PC 和移动端 GUI——识别屏幕元素、理解布局、执行点击和输入。Claude 的 Computer Use 功能则将视觉理解直接转化为桌面操作。多模态模型正成为 AI Agent 的"眼睛和手"。

**趋势 2：全模态原生融合**

GPT-4o 和 Gemini 2.5 代表了真正的"全模态原生"路线——文本、图像、音频在同一个模型内统一处理，而非"视觉编码器 + LLM"的拼接架构。这消除了模态间信息损失，使跨模态推理（如"根据这张图里的文字和背景音乐的氛围写一段文案"）成为可能。

**趋势 3：开源模型的性能追赶**

Qwen3-VL 235B 在 OCR 和文档理解任务上已超越多数闭源模型，MiniMax M2 230B 在编程和 Agent 工作流中表现突出。开源多模态模型的"激活参数/总参数"比（如 M2 的 10B/230B）使其在推理成本和部署灵活性上具有显著优势。

**趋势 4：超长上下文重塑多模态交互**

Gemini 2.5 Pro 的 1M+ token 上下文窗口和 Qwen3-VL 的 1M 上下文，使得"上传整本手册 + 多张截图 → 一次性分析和问答"成为现实。多模态 RAG 的边界正在被超长上下文模糊化。

### 9.3 多模态 Agent 的架构范式

2026 年生产环境中的多模态 Agent 通常采用以下分层架构：

```
用户输入（文本+图像+语音）
       ↓
多模态路由器 → 判断输入类型，分派处理
       ↓
┌──────────┼──────────┐
↓          ↓          ↓
文本通道    视觉通道    音频通道
(GPT-4o)  (Qwen3-VL)  (Gemini)
↓          ↓          ↓
└──────────┼──────────┘
       ↓
融合推理层 → 多模态结果融合与决策
       ↓
Agent 执行层 → 工具调用 / GUI 操作 / API 调用
```

**关键设计原则**：
- **按模态分流**：不同模态走最优模型，避免"一刀切"
- **延迟预算管理**：视觉和音频处理的延迟显著高于纯文本，需要异步管道
- **回退策略**：视觉模型不可用时降级为"文本描述替代图像"

### 9.4 选型决策树（2026 更新版）

```
需要处理什么模态？
├── 仅文本 → 纯 LLM（GPT-4o / Claude / DeepSeek）
├── 文本+图像
│   ├── 云端API → GPT-4o / Gemini 2.5（最强综合能力）
│   ├── 隐私/成本敏感 → Qwen3-VL（开源最强） / MiniMax M2（低延迟）
│   └── 本地部署 → Gemma 3 / Llama 4（轻量）
├── 文本+图像+音频 → Gemini 2.5 Pro / GPT-4o（全模态原生）
├── 视觉Agent（操作GUI） → Qwen3-VL / Claude Computer Use
└── 视频理解 → Gemini 2.5 Pro（1M上下文处理长视频）
```

> 💡 **2026 Q3 核心判断**：多模态不再是"锦上添花"的功能，而是 Agent 的必备能力。视觉理解让 Agent 能操作真实世界界面，音频理解让 Agent 能参与真实对话。未来 12 个月的竞争焦点将集中在"全模态 Agent"——一个模型统一处理所有输入模态，直接从感知到行动。

### 参考来源
- [Qwen3-VL — Ollama Blog](https://ollama.com/blog/qwen3-vl)
- [MiniMax M2 — Ollama Blog](https://ollama.com/blog/minimax-m2)
- [GPT-4o System Card — OpenAI](https://openai.com/index/gpt-4o-system-card/)
- [Gemini 2.5 Pro — Google AI](https://ai.google.dev/gemini-api/docs/models)

---

---

## 10. 视觉语言模型架构详解（基于 HuggingFace 官方指南）

**来源：** [视觉语言模型详解 — HuggingFace Blog (2024-04-11)](https://huggingface.co/blog/zh/vlms)

### 8.1 什么是视觉语言模型？

视觉语言模型（Vision Language Model, VLM）是可以**同时从图像和文本中学习**的多模态生成模型，输入为图像和文本，输出为文本。大视觉语言模型具有良好的零样本能力，广泛适用于：
- 基于图像的对话
- 视觉问答（VQA）
- 文档理解
- 图像描述
- 目标检测与分割（部分模型可输出边界框/分割掩模）

### 8.2 主流架构：三组件堆叠

最常见且表现最好的 VLM 架构由以下三个部分组成：

```
图像 → [图像编码器] → [嵌入投影子模型] → [文本解码器] → 文本输出
                                          ↑
文本 → [文本嵌入] ─────────────────────────┘
```

| 组件 | 作用 | 典型选择 |
|------|------|---------|
| **图像编码器** | 将图像转化为结构化数值表示 | CLIP 视觉塔、ViT |
| **投影子模型** | 将图像特征映射到文本嵌入空间 | 小型 MLP / 稠密神经网络 |
| **文本解码器** | 自回归生成文本输出 | Vicuna、LLaMA 等 LLM |

### 8.3 训练策略

不同的 VLM 采用不同的训练方法：

| 模型 | 训练策略 | 特点 |
|------|---------|------|
| **LLaVA** | 冻结图像编码器 + 文本解码器，先训练投影层，再解冻解码器微调 | 经典预训练+微调范式 |
| **KOSMOS-2** | 端到端完全训练 | 计算成本高，对齐效果好 |
| **Fuyu-8B** | 无图像编码器，图像块直接送投影层 | 架构极简 |

### 8.4 开源模型选型指南

HuggingFace Hub 上的主要开源 VLM：

| 模型 | 可商用 | 规模 | 分辨率 | 特色 |
|------|-------|------|--------|------|
| LLaVA 1.6 (Hermes 34B) | ✅ | 34B | 672×672 | - |
| DeepSeek-VL-Chat | ✅ | 7B | 384×384 | 对话优化 |
| CogVLM-Chat | ✅ | 17B | 490×490 | 接地+对话 |
| Qwen-VL-Chat | ✅ | 4B | 448×448 | 零样本目标检测 |
| Yi-VL-34B | ✅ | 34B | 448×448 | 中英双语 |
| moondream2 | ✅ | ~2B | 378×378 | 超轻量 |

### 8.5 如何选择 VLM

两种主流评估途径：

1. **视觉竞技场（Vision Arena）**：基于匿名投票的排行榜，两个模型对同一提示生成输出，用户选择偏好
2. **开放 VLM 排行榜**：基于 VLMEvalKit 的多指标自动化评估

常用基准：
- **MMMU**：11.5K 多模态问题，需要大学水平学科知识
- **MMBench**：3000 道单选题覆盖 20+ 技能（OCR、定位等）
- **MathVista**：视觉数学推理
- **OCRBench**：文档理解

**参考来源：**
- [视觉语言模型详解 — HuggingFace Blog](https://huggingface.co/blog/zh/vlms)

---

## 11. 多模态模型训练与评估方法论

### 11.1 训练范式演进：从两阶段到端到端

多模态模型的训练方法在 2024-2026 年间经历了显著演进：

| 范式 | 训练方式 | 代表模型 | 特点 |
|------|---------|---------|------|
| **两阶段微调** | 特征对齐预训练 → 指令微调 | LLaVA 1.5, Qwen-VL | 训练稳定，数据需求低 |
| **端到端训练** | 全部参数联合训练 | KOSMOS-2, GPT-4o | 对齐效果好，计算成本高 |
| **交错预训练** | 图文交错数据预训练 → 任务微调 | Flamingo, IDEFICS | 零样本能力强 |
| **连续预训练** | 在已训练 LLM 上继续预训练视觉 token | LLaMA 3.2 Vision | 保留 LLM 原始能力 |

### 11.2 关键评估基准全景

2026 年多模态模型评估已形成完整的基准体系：

| 基准 | 任务类型 | 样本量 | 难度 | 2026 SOTA |
|------|---------|--------|------|-----------|
| **MMMU** | 大学级多学科问答 | 11.5K | ⭐⭐⭐⭐⭐ | GPT-4o / Gemini 2.5 |
| **MMBench** | 20+ 视觉技能单选题 | 3K | ⭐⭐⭐ | Qwen3-VL 235B |
| **MathVista** | 视觉数学推理 | 6K | ⭐⭐⭐⭐ | GPT-4o |
| **OCRBench** | 文档/场景文字理解 | 1K | ⭐⭐⭐ | Qwen3-VL 235B |
| **BLINK** | 视觉感知核心任务 | 1K | ⭐⭐ | GPT-4o |
| **SEED-Bench** | 多模态理解+生成 | 19K | ⭐⭐⭐ | Gemini 2.5 |
| **Video-MME** | 长视频理解 | 3K | ⭐⭐⭐⭐ | Gemini 2.5 Pro |
| **ChartQA** | 图表问答 | 2K | ⭐⭐⭐ | Qwen2.5-VL |

### 11.3 2026 评估新趋势

**趋势 1：从感知到推理**
2025 年的评估重点还是「模型能否识别图像内容」（感知层面），2026 年的前沿评估已转向「模型能否基于视觉输入进行多步推理」。MMMU 和 MathVista 的区分度大幅提升，而传统的 VQA、Caption 基准已接近饱和。

**趋势 2：视觉 Agent 评估**
新涌现的评估基准专门测试模型的 GUI 操作能力（如 ScreenSpot、WebArena）。这些基准要求模型理解界面布局、识別交互元素、规划多步操作序列——而非仅回答关于图像的问题。

**趋势 3：长视频理解**
随着 Gemini 2.5 Pro 的 1M+ 上下文和 Qwen3-VL 的视频理解能力，Video-MME 等长视频基准的竞争加剧。评估重点从「关键帧分析」转向「跨帧时间推理」。

### 11.4 训练数据关键策略

多模态模型的训练数据设计直接影响最终性能：

| 数据类型 | 用途 | 典型规模 | 来源 |
|----------|------|---------|------|
| 图文对 | 特征对齐预训练 | 数百万-数亿 | LAION, CC12M, DataComp |
| 交错图文 | 上下文学习 | 数千万 | MMC4, OBELICS |
| 视觉指令 | 指令微调 | 10万-100万 | LLaVA-Instruct, ShareGPT4V |
| 视频-文本对 | 视频理解 | 数十万-数百万 | WebVid, HowTo100M |
| 文档-文本对 | 文档理解 | 数百万 | DocVQA, SynthDoG |

> **2026 关键洞察：** 多模态训练数据质量比数量更重要。Qwen3-VL 和 LLaVA-NeXT 的实验表明，精心筛选的 100 万视觉指令数据在 MMMU 上的表现优于 500 万未筛选数据。数据去重、难度分层和多样性控制是构建高效训练集的关键。

**来源：**
- [MMMU Benchmark — arXiv 2024](https://arxiv.org/abs/2311.09785)
- [MMBench — arXiv 2024](https://arxiv.org/abs/2307.06281)
- [HuggingFace Open VLM Leaderboard](https://huggingface.co/spaces/opencompass/open_vlm_leaderboard)
- [Visual Instruction Tuning — LLaVA (NeurIPS 2023)](https://arxiv.org/abs/2304.08485)

---

## 2026 最新进展：原生多模态与统一架构

### 概述

2025-2026 年，多模态模型正从「拼接式」（视觉编码器 + LLM）向**原生多模态统一架构**演进。以 GPT-4o、Gemini 2.0 为代表，模型在预训练阶段就同时处理文本、图像、音频等多种模态，而非事后拼接视觉模块。这带来了更低的延迟、更强的跨模态推理能力，以及更自然的交互体验。

### 核心趋势

**1. 原生多模态 vs. 拼接架构**

传统 VLM（如 LLaVA）采用「视觉编码器 → 投影层 → LLM」的拼接架构，优势是复用已有的强大 LLM，但存在模态对齐损失和信息瓶颈。2025 年起，OpenAI 和 Google 率先在 GPT-4o 和 Gemini 中实现原生多模态——模型在预训练时直接从混合模态数据中学习，无需单独的视觉编码器。

- **GPT-4o**：单一模型端到端处理文本、视觉和音频，平均响应时间 320ms，接近人类对话速度
- **Gemini 2.0**：Google 的下一代多模态模型，支持原生图像/视频/音频输入输出，在 MMMU（大规模多学科多模态理解基准）上取得领先成绩

**2. 开源 VLM 持续追赶**

开源社区在 2025-2026 年取得显著进展：

- **LLaVA-NeXT（LLaVA 1.6）**：引入动态高分辨率策略，将图像分割为多个 patch 分别编码，在 DocVQA、ChartQA 等需要细粒度理解的基准上大幅提升
- **Qwen2-VL / Qwen3-VL**：通义千问团队的多模态版本，原生支持动态分辨率和视频理解，在 MMBench、MME 等中文多模态基准上表现优异
- **InternVL 2.5**：商汤团队的多模态模型，通过渐进式对齐策略实现 78B 规模的强大 VLM

**3. 关键能力突破**

| 能力维度 | 2023-2024 水平 | 2025-2026 进展 |
|---------|--------------|---------------|
| 视觉推理 | 简单物体识别 | 复杂图表理解、数学推理、空间关系 |
| 视频理解 | 抽帧分析 | 原生时序建模、长视频问答（>1小时） |
| 音频模态 | 独立模型处理 | 端到端语音对话、音乐理解 |
| 跨模态生成 | 图→文为主 | 任意模态→任意模态（Any-to-Any） |
| 多语言 | 英文为主 | 100+ 语言图文联合理解 |

**4. 训练数据演进**

2026 年多模态训练数据的核心洞察：**质量 > 数量**。Qwen3-VL 和 LLaVA-NeXT 的实验表明，精心筛选的 100 万视觉指令数据在 MMMU 上的表现优于 500 万未筛选数据。关键策略包括：

- **数据去重**：跨模态语义去重，避免训练集中相似图文对的过度拟合
- **难度分层**：按任务复杂度分层采样（OCR → 场景理解 → 数学推理）
- **多样性控制**：确保覆盖不同领域（科学图表、文档、自然场景、医学影像）

### 参考来源

- [GPT-4o System Card — OpenAI](https://openai.com/index/hello-gpt-4o/)
- [Gemini: A Family of Highly Capable Multimodal Models — arXiv 2312.11805](https://arxiv.org/abs/2312.11805)
- [LLaVA: Large Language and Vision Assistant — arXiv 2304.08485](https://arxiv.org/abs/2304.08485)
- [Multimodal Learning — Wikipedia](https://en.wikipedia.org/wiki/Multimodal_learning)
- [MMMU Benchmark — arXiv 2311.09785](https://arxiv.org/abs/2311.09785)

---

## 12. 多模态模型在生产环境中的部署与成本优化

> 实际生产环境中，多模态模型的部署成本（延迟、吞吐、显存）往往是比模型精度更紧迫的约束。本节总结 2026 年多模态推理的优化策略和选型建议。

### 12.1 多模态推理的成本构成

与纯文本 LLM 不同，多模态推理的成本构成更为复杂：

| 成本项 | 纯文本 LLM | 多模态 VLM | 差异倍数 |
|--------|-----------|-----------|---------|
| **输入 Token 数** | 1 token ≈ 1 个词 | 1 张 672×672 图像 ≈ **1,024-2,048 tokens** | 1K-2K× |
| **KV Cache 占用** | 与序列长度线性相关 | 图像 token 的 KV Cache 占主导 | 10-50× |
| **预填充 (Prefill)** | 文本嵌入 | 图像编码 + 投影 + 文本嵌入 | 5-10× |
| **显存占用** | ~2 GB/10B 参数 | ~4-8 GB/10B 参数（含视觉编码器） | 2-4× |

**典型案例**：一个含 10 张截图的分析请求（每张图 ≈ 1,024 tokens），输入总 token 数轻松超过 10K——其中 95%+ 来自图像 token。这意味着多模态 API 调用的成本可能比同等文本请求高 10-50 倍。

### 12.2 图像 Token 压缩技术

2026 年，业界提出了多种减少图像 token 数量的方法：

| 技术 | 原理 | Token 减少 | 精度损失 | 代表实现 |
|------|------|-----------|---------|---------|
| **Token 池化 (Token Pooling)** | 将邻近 image patch 合并 | 2-4× | <1% | LLaVA-NeXT, InternVL |
| **FrameFusion** | 跨帧融合，减少视频 token | 70% | <3% | Qwen3-VL |
| **动态分辨率** | 根据图像内容分配 token | 1.5-3× | 0% | Qwen2.5-VL |
| **Perceiver Resampler** | 用可学习查询向量压缩视觉 token | 8-16× | 1-3% | Flamingo, IDEFICS |
| **视觉总结器** | 先用 VL 模型总结图像，再传文本 | 64-256× | 5-10% | 自定义管道 |

**选择建议**：精度优先场景优先选择 Token 池化或动态分辨率（精度损失 <1%），成本敏感场景可考虑 Perceiver Resampler（8-16× 压缩）或视觉总结器管道（64-256× 压缩但精度下降明显）。

### 12.3 多模态推理的延迟优化策略

**策略 1：视觉编码预缓存（Pre-cache Visual Embeddings）**

如果同一批图像被多次查询（如同一份文档被多个用户提问），可以预计算并缓存视觉嵌入：

```python
# 预计算并缓存
cache = {}
def get_image_embedding(image_path: str) -> torch.Tensor:
    if image_path not in cache:
        image = load_image(image_path)
        cache[image_path] = vision_encoder(image)  # 仅计算一次
    return cache[image_path]
```

在文档分析、看图评标等「同一图像多轮问答」场景中，缓存可将首次调用后的推理延迟降低 **40-60%**。

**策略 2：视觉计算与文本生成流水线并行**

将视觉编码和语言模型推理拆分为两个阶段，重叠执行：
- GPU 处理视觉编码时，CPU 准备文本输入
- 视觉嵌入就绪后，直接送入 LLM 的嵌入层
- 在批处理场景中，一期 batch 的 LLM 推理与下一期 batch 的视觉编码重叠

**策略 3：按需降级（Graceful Degradation）**

当系统负载高或延迟预算紧张时，自动降级：
- **高负载 → 降低图像分辨率**（如从 672×672 降至 336×336，token 减少 4×）
- **极高负载 → 替换为文本描述**（用专用 captioning 模型生成文本替代图像）
- **边缘部署 → 跳过视频帧**（每秒抽 1 帧而非全帧率分析）

### 12.4 多模态 API 的成本优化指南

| 场景 | 推荐方案 | 估计成本/1000 次调用 | 延迟 |
|------|---------|--------------------|------|
| 轻量文档 OCR | Qwen2.5-VL 7B（本地 Ollama） | $0（自有硬件） | 500ms-2s |
| 通用图像理解 | GPT-4o mini（低分辨率） | ~$0.15 | 1-3s |
| 高精度图表分析 | GPT-4o / Gemini 2.5 | ~$1.50 | 2-5s |
| 长视频分析 | Gemini 2.5 Pro（1M 上下文） | ~$5.00 | 10-30s |
| 批量文档处理 | 本地 Qwen3-VL + 预缓存 | $0（自有硬件） | 批处理 |

**核心优化原则**：

1. **按需降低图像分辨率**：不是所有任务都需要 4K 分辨率。对于 OCR，672×672 足够；对于场景理解，可能需要更高分辨率。
2. **压缩图像格式**：使用 WebP（比 PNG 小 30-50%）或 JPEG（质量 85%）而非无损格式
3. **减少不必要的图像**：分析用户是否真的需要同时传 5 张图——多模态调用中 80% 的成本来自图像 token
4. **利用长上下文优势**：如果使用 Gemini 2.5 Pro 的 1M 上下文，可以将 20-50 页文档一次性上传，避免多轮交互
5. **本地混合部署**：将高频、低复杂度任务（文档 OCR、简单图表分析）分流到本地部署的开源模型，仅将复杂推理（多步推理、专业领域分析）路由到云端 API

### 12.5 多模态模型的工程选型框架

```
输入类型：
├── 文本+单张图像
│   ├── 通用理解 → GPT-4o / Qwen3-VL（云端），Qwen2.5-VL（本地）
│   ├── 文档/OCR → Qwen3-VL 235B（32 语言 OCR）
│   ├── 图表/数据 → GPT-4o / Gemini 2.5
│   └── 编程/Agent → MiniMax M2（低延迟 10B 激活）
├── 文本+多张图像
│   ├── 文档对比 → GPT-4o / Gemini 2.5
│   └── 多图推理 → Qwen3-VL（1M 上下文）
├── 文本+视频
│   ├── 短视频 (<5分钟) → GPT-4o / Gemini 2.5
│   └── 长视频 (>30分钟) → Gemini 2.5 Pro（1M 上下文）
└── 文本+音频
    └── 全模态 → GPT-4o（原生音频）

成本约束：
├── 低成本 (本地部署) → Qwen2.5-VL / Gemma 3
├── 中等成本 → GPT-4o mini / Qwen3-VL API
└── 无约束 → GPT-4o / Gemini 2.5 Pro
```

> **2026 核心建议**：生产环境不要用"一个模型解决所有问题"。按场景选择最优模型组合，建立多模态路由层（判断输入类型→分派到不同模型），在精度、成本和延迟之间取得最佳平衡。

**来源：**
- [视觉语言模型详解 — HuggingFace Blog (2024-04-11)](https://huggingface.co/blog/zh/vlms)
- [Ollama Multimodal Models Blog (2025-05-15)](https://ollama.com/blog/multimodal-models)
- [GPT-4o System Card — OpenAI](https://openai.com/index/gpt-4o-system-card/)
- [Gemini API Pricing](https://ai.google.dev/pricing)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-21 00:08:07*
