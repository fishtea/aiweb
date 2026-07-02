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

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[LLAVA 系列论文精读 - 稀土掘金](https://juejin.cn/post/7475877205257928739)**
  - 来源：`juejin.cn` · 质量分：11 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 通过连接CLIP 的开源视觉编码器和语言解码器LLaMA 组成多模态模型LLaVA，并在生成的视觉- 语言指令数据上进行端到端微调。 公布两个多模态基准测试。作者

- **[吹爆！VIT/BLIP/CLIP/Lora/LLaVA/LLama大模型六大基础模型详解！大模型入门必学！_哔哩哔哩_bilibili](https://bilibili.com/video/BV1g47nzTEAY)**
  - 来源：`bilibili.com` · 质量分：11 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # 吹爆！VIT/BLIP/CLIP/Lora/LLaVA/LLama大模型六大基础模型详解！大模型入门必学！. 【2026最新版】一口气学完VIT/BLIP/CLIP/Lora/LLaVA/LLama大模型六大基础模型详解！大模型入门必学！. 【源码级拆解】一文看懂Qwen3、LLama4.0和DeepSeek V3 三大顶流AI大模型核心技术！llm 大模型原理 大模型零基础入门教程. 多模态论文精读：CLIP、ViLT、ALBEF...

- **[【LLM多模态】LLava模型架构和训练过程| CLIP模型原创 - CSDN博客](https://blog.csdn.net/qq_35812205/article/details/136586853)**
  - 来源：`blog.csdn.net` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - LLaVA的模型结构非常简单，就是CLIP+LLM(Vicuna，LLaMA结构)，利用Vison Encoder将图片转换为[N=1, grid_H x grid_W, hide_dim]的特征图，然后接一个

- **[LLM大模型：LLaVa多模态图片检索原理 - 博客园](https://cnblogs.com/theseventhson/p/18343089)**
  - 来源：`cnblogs.com` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - clip模型一旦训练完成，就具备zero-shot能力了；被集成到其他下游任务中后，本身是不需要再次微调的（训练数据400Million对，见多识广啦）！ 3、clip

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
