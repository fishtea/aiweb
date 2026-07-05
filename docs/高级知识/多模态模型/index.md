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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
