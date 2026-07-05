# 开源模型部署选型

开源模型部署的目标不是“把模型跑起来”这么简单，而是在能力、延迟、成本、隐私、硬件和维护复杂度之间取得平衡。

## 选型维度

| 维度 | 需要确认的问题 |
|------|----------------|
| 任务类型 | 对话、代码、检索增强、函数调用、长文本、多模态还是嵌入 |
| 模型尺寸 | 参数量、上下文长度、显存需求、量化后质量损失 |
| 推理性能 | 首 token 延迟、吞吐、并发、批处理和流式输出 |
| 部署环境 | 单机 GPU、多机集群、CPU、本地电脑、边缘设备或云服务 |
| 生态支持 | tokenizer、推理引擎、微调框架、模型许可证和社区活跃度 |
| 安全合规 | 私有数据、审计、日志、访问控制和许可证限制 |

## 常见部署路线

### 本地实验

使用 Ollama、LM Studio、llama.cpp 或 Transformers 快速验证模型能力。适合个人学习、Prompt 验证和小规模原型。

### 单机服务

使用 vLLM、TGI、SGLang、llama.cpp server 等提供 OpenAI 兼容接口或 HTTP 服务。适合内部工具、低到中等并发应用。

### 集群推理

面向高并发、长上下文或多模型路由，需要调度、监控、自动扩缩容、缓存和灰度发布。通常还要配合 Kubernetes、网关、队列和成本报表。

## 模型家族对比提示

| 家族 | 常见使用重点 |
|------|--------------|
| LLaMA | 通用开源生态、微调资料丰富、部署工具支持好 |
| Qwen | 中文、代码、多模态和工具调用生态活跃 |
| DeepSeek | 代码、推理和性价比场景常被重点评估 |
| Mixtral/Mistral | MoE 与轻量高效模型路线，适合关注吞吐和部署成本 |
| Stable Diffusion | 图像生成与工作流生态，通常与 ComfyUI 配合使用 |

## 部署前检查清单

- 模型许可证是否允许目标使用场景。
- 是否有代表性评估集，而不是只看排行榜。
- 显存是否覆盖模型权重、KV cache、并发和上下文长度。
- 是否需要量化，量化后是否重新评估关键任务。
- 是否支持流式输出、函数调用、JSON 输出或多模态输入。
- 是否具备限流、鉴权、日志、监控、告警和回滚策略。

## 推荐阅读路径

- 本地快速运行：先看 [Ollama](/工具专区/Ollama/)。
- 高性能推理服务：继续看 [vLLM](/工具专区/vLLM/)。
- 模型能力对比：阅读 [LLaMA 系列](/模型专区/LLaMA系列/)、[Qwen 系列](/模型专区/Qwen系列/)、[DeepSeek](/模型专区/DeepSeek/)。
- 生产应用设计：结合 [LLM 应用架构](/进阶学习/LLM应用架构/)。

## 2026 部署工具最新进展

### vLLM：从推理引擎到全栈平台

vLLM 在 2026 年已从单纯的推理引擎发展为覆盖多模态、路由、强化学习的全栈平台。2026 年 6-7 月发布的关键特性包括：

- **vLLM Semantic Router v0.3 Themis**（2026-06-05）：从信号级路由升级到有状态生产路由，支持多模型动态调度和灰度发布。
- **DiffusionGemma 原生支持**（2026-06-10）：首个在 vLLM 中原生支持的扩散 LLM（dLLM），标志着扩散模型与自回归模型推理的统一。
- **MiniMax M3 Day-0 支持**（2026-06-12）：100 万 token 上下文的多模态推理，展示了超长上下文的工程挑战和解决方案。
- **vLLM-Omni 多阶段模型服务**（2026-07-01）：从 Qwen3-Omni 的多阶段推理中总结的实战经验，解决语音、文本、视觉交替推理的调度难题。

> 参考来源：vLLM Blog (https://blog.vllm.ai/)，2026 年 6-7 月系列文章。

### SGLang 崛起与推理框架格局

2026 年推理框架竞争加剧，SGLang 凭借结构化生成（constrained decoding）和 RadixAttention 前缀缓存获得广泛关注。主要变化：

| 框架 | 2026 定位 |
|------|-----------|
| vLLM | 全栈平台：推理 + 路由 + 多模态 + RL |
| SGLang | 高性能推理 + 结构化生成 + 前缀缓存 |
| llama.cpp | CPU/边缘推理首选，量化生态最丰富 |
| Ollama | 个人开发者和本地实验首选 |
| TGI (HuggingFace) | 企业级服务，HF 生态深度集成 |

### 部署新范式：扩散 LLM 与多模态统一推理

2026 年出现了两个值得关注的部署新范式：

1. **扩散 LLM（dLLM）**：不同于传统的自回归逐 token 生成，扩散 LLM 并行生成整个响应，理论上可以实现更低的延迟。vLLM 对 DiffusionGemma 的 Day-0 支持标志着这一范式进入生产可用的阶段。

2. **多阶段模型统一推理**：Qwen3-Omni 等模型需要交替进行语音识别、文本理解和语音合成，传统的一次推理一个模型的模式效率低下。vLLM-Omni 的实践表明，通过阶段间缓存共享和流水线编排，可以在单个框架内处理多阶段推理。

### 部署选型更新建议（2026）

基于 2026 年最新发展，对原有选型维度补充：

- **扩散 LLM 场景**：如需极低延迟的并行生成，关注 dLLM + vLLM 组合。
- **超长上下文场景**：MiniMax M3 和 Gemini 等 100 万+ token 模型需要专门的 KV cache 管理策略。
- **多模态 Agent 场景**：优先考虑支持多阶段推理的框架（vLLM-Omni 等）。
- **语义路由场景**：多模型生产环境考虑 vLLM Semantic Router 等专用路由方案。

### 2026 年 Ollama 性能里程碑

**来源：** [Ollama Blog 2026年6-7月系列文章](https://ollama.com/blog)

Ollama 在 2026 年上半年发布了一系列重大性能更新，重新定义了本地模型部署的性能上限：

#### 多 Token 预测（MTP）：Gemma 4 加速 90%

**来源：** [Faster Gemma 4 on MLX with multi-token prediction (2026-06-29)](https://ollama.com/blog/faster-gemma-4-mlx-mtp)

- Gemma 4 自带一个小型快速"草稿模型"（draft model），与主模型并行运行，同时预测后续多个 token
- 主模型在单次前向传播中验证草稿模型的预测，接受正确的 token
- 代码场景加速效果最显著（代码充满闭合括号、重复标识符和模板代码），对编程 Agent 的响应速度提升尤为明显
- 在 Aider polyglot 基准测试中，Gemma 4 12B 在 M5 Max 上生成速度提升近 90%
- Ollama 自动调优草稿 token 数量，无需手动配置

#### MLX 引擎：Apple Silicon 上的最高性能

**来源：** [Ollama's highest performance on Apple Silicon yet with MLX (2026-06-11)](https://ollama.com/blog/mlx-performance)

- 支持 NVIDIA 模型优化格式 **NVFP4**——量化质量损失约为传统 Q4_K_M 的一半
- 数据中心优化的模型可直接导入本地运行，实现数据中心到桌面的可移植性
- 输出速度提升高达 20%（通过 Metal 内核融合和 JIT 编译优化）
- 更低的内存占用和更快的首 token 时间

#### GGUF 兼容性与 Vulkan 加速

**来源：** [Improved performance and model support with GGUF (2026-06-05)](https://ollama.com/blog/improved-performance-and-model-support-with-gguf)

- Ollama 0.30 在 NVIDIA 硬件上吞吐量提升高达 20%
- **Vulkan 默认启用**：AMD 和 Intel GPU 开箱即用
- 扩展 GGUF 生态兼容性：LFM、Prism 及 Unsloth 微调模型可直接运行
- 支持从 HuggingFace 加载 GGUF 文件，与 Claude Code、Hermes Agent 等编程 Agent 无缝集成

#### Nemotron 3 Ultra：Agent 工作流专用模型

**来源：** [NVIDIA Nemotron 3 Ultra (2026-06-04)](https://ollama.com/blog/nemotron-3-ultra)

- 550B 总参数 / 55B 激活参数 MoE 架构
- 专为长时间运行的 Agent 工作流调优（编程 Agent、深度研究、企业工作流）
- **100 万 token 上下文**：保留整个代码库、长工具调用历史和搜索路径
- 成本效率领先：比同类开源模型节省高达 30% 成本
- 通过 Ollama 一键启动：`ollama launch claude --model nemotron-3-ultra:cloud`

> 💡 **2026 本地部署趋势总结**：本地推理不再是"妥协方案"——MLX + MTP + NVFP4 的组合让 MacBook 上的编程 Agent 体验接近云端；GGUF 生态的扩展让更多模型开箱即用；MoE 架构（如 Nemotron 3 Ultra）让大规模模型也能在消费级硬件上运行。

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-05 05:14:27*
