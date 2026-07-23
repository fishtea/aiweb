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
| Qwen | Qwen3 / Qwen3-Coder 适合中文、代码、多模态和工具调用 |
| DeepSeek | V3 / R1 / DeepSeek-OCR 适合代码、推理、文档理解和性价比场景 |
| Mixtral/Mistral | Medium 3.1、Devstral、Magistral、Voxtral 与 Mixtral，覆盖企业、代码、推理和语音 |
| Stable Diffusion / FLUX | 图像生成与工作流生态，通常与 ComfyUI 配合使用 |

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

## 推理框架格局

开源部署不再只有 Transformers 一条路。实际选型通常从开发便利性、吞吐、结构化输出、量化、硬件兼容和运维成本出发。

| 框架 | 2026 定位 |
|------|-----------|
| vLLM | 高吞吐服务、PagedAttention、OpenAI 兼容 API、批处理和多模型服务 |
| SGLang | 高性能推理、结构化生成、前缀缓存和 Agent / RAG 场景 |
| llama.cpp | CPU/边缘推理首选，量化生态最丰富 |
| Ollama | 个人开发者和本地实验首选 |
| TGI (HuggingFace) | 企业级服务，HF 生态深度集成 |
| TensorRT-LLM | NVIDIA GPU 上的极致性能优化 |
| LM Studio | 桌面本地实验和非工程用户体验好 |

## 模型与框架匹配

| 需求 | 建议组合 |
|------|----------|
| 快速本地试用 | Ollama / LM Studio + GGUF 或官方模型仓库 |
| 单机 GPU 高吞吐 API | vLLM / SGLang + AWQ / GPTQ / FP8 量化 |
| CPU、Mac、边缘设备 | llama.cpp / Ollama + GGUF 量化 |
| 结构化输出和 Agent 工具调用 | SGLang / vLLM + JSON schema / constrained decoding |
| NVIDIA 企业生产 | TensorRT-LLM、TGI 或 vLLM，配合监控和灰度发布 |
| 多模态模型 | 优先确认框架是否支持对应模型结构、视觉编码器和输入格式 |

## 2026 选型补充

- **闭源 API 与开源模型混合使用**：GPT-5.6、Claude Fable 5、Gemini 3 Pro 等闭源模型适合高价值步骤；Qwen3、DeepSeek、Llama 4、Mistral 等适合私有化和成本控制。
- **2026 开源默认候选**：中文与代码优先看 Qwen3 / DeepSeek-R1；超长上下文和开放权重多模态看 Llama 4 Scout / Maverick；欧洲合规和企业部署看 Mistral Medium 3.1 / Devstral。
- **不要只看参数量**：MoE 模型要同时看总参数、激活参数、专家路由稳定性和实际吞吐。
- **长上下文要测 KV cache**：128K 以上上下文的显存主要消耗常常来自 KV cache，并发越高越明显。
- **量化必须复测业务任务**：4-bit / 8-bit 量化可能对抽取、代码和数学造成不同程度损失。
- **推理模型要单独估算成本**：R1、o 系列、Qwen thinking 等模型会产生额外推理 token 或更长延迟。
- **许可证先于性能**：Llama、Qwen、Mistral、DeepSeek 等许可证细节不同，商用、再分发、服务化都要单独确认。
- **模型路由是常态**：生产系统常用小模型做分类、抽取和路由，用大模型或推理模型处理少量关键请求。

## 2026 部署技术前沿

### vLLM v1 引擎重构

vLLM 在 2025-2026 年推出了 **v1 引擎**（V1 Engine），对核心推理架构进行了重大重构，不是简单的版本升级，而是架构层面的重新设计：

| 维度 | v0 引擎 | v1 引擎 |
|------|---------|---------|
| 调度模型 | 同步式，按 step 调度 | 异步事件驱动，更灵活 |
| 内存管理 | PagedAttention v1 | PagedAttention v2 + 更细粒度内存复用 |
| 多模态 | 后期添加，支持有限 | 原生多模态支持，统一 encoder/decoder 管线 |
| 推测解码 | 有限支持 | EAGLE3、DFlash、DSpark、MTP 等多种推测策略 |
| 分页服务 | — | 原生 disaggregated prefill/decode/encode |
| 结构化输出 | 基础 xgrammar | xgrammar + guidance，支持复杂 JSON schema |
| 批处理策略 | 固定调度窗口 | 动态批处理 + 前缀缓存感知调度 |

**迁移建议：** v1 引擎已在 2025 年下半年进入稳定阶段，新项目应直接使用 v1。对于已有 v0 部署，建议在测试环境验证业务兼容性后逐步迁移。v0 将继续获得安全更新但不再有架构级新特性。

### Disaggregated Serving（分离式服务）

Disaggregated serving 是 2026 年推理架构的最大变化之一，将传统的单一服务节点拆分为 **prefill 节点（预填充）** 和 **decode 节点（解码）**：

- **Prefill 节点**：专门处理 prompt 的并行预填充，对计算密度要求高，适合用 H100/B200 等高性能 GPU
- **Decode 节点**：专门处理自回归解码，KV cache 占用大但计算密度低，适合用显存大但计算能力中等的 GPU
- **跨节点 KV cache 传输**：prefill 完成后通过高速网络（NVLink/InfiniBand/RoCE）将 KV cache 传输到 decode 节点

**适用场景：**
- 长上下文推理（128K+ tokens）：prefill 阶段计算量大，分离后可按需分配 GPU
- 高并发在线服务：decode 节点可独立扩缩容，应对流量波动
- 混合负载：不同 prompt 长度可路由到不同 prefill 节点

**2026 实现状态：** vLLM、SGLang 均已支持 disaggregated serving 生产部署。DeepSeek-V4 等最新模型也针对分离式服务做了优化。

### SGLang 结构化生成与 Agent 路由

SGLang 在 2026 年已成为结构化生成和 Agent 工作负载的重要选择：

- **Constrained Decoding（约束解码）**：原生支持 JSON schema、正则表达式和 CFG（上下文无关文法）约束，无需后处理即可保证输出格式
- **RadixAttention（前缀缓存）**：自动缓存和复用公共前缀的 KV cache，在多轮对话和 RAG 场景中显著降低延迟
- **Agent 路由**：支持根据 prompt 内容自动路由到不同模型，适合多模型 Agent 系统中的任务分发
- **Multi-Turn 性能**：在 Agent 多轮工具调用的场景中，RadixAttention 的优势尤为明显

**选型建议：** 如果你的核心场景是结构化输出、Agent 工具调用和多轮对话，SGLang 的约束解码和前缀缓存机制比 vLLM 天然更适合；如果主要是高吞吐通用对话和批处理，vLLM 的调度和批处理生态更成熟。

### 2026 推理框架决策树

```
你的场景是什么？
├── 本地实验/学习
│   └── Ollama / LM Studio（零配置、体验友好）
├── 单 GPU 低延迟服务
│   └── llama.cpp / Ollama（CPU/边缘）+ GGUF 量化
├── 单机多 GPU 高吞吐
│   ├── 通用对话 → vLLM（生态最成熟）
│   ├── Agent + 结构化输出 → SGLang（约束解码优势）
│   └── 多模态 → 优先确认框架支持（vLLM v1 / SGLang）
├── 集群生产环境
│   ├── 高并发 → vLLM + K8s + 自动扩缩容
│   ├── 长上下文 + 高 QPS → Disaggregated serving
│   └── 多模型路由 → 考虑模型网关（vLLM / SGLang 多模型服务）
└── NVIDIA 极致性能
    └── TensorRT-LLM（深度优化，但开发和运维成本最高）
```

## 2026 开源模型实战排名

根据 [Ryz Labs 2026 年 6 月开源 LLM 部署选型报告](https://learn.ryzlabs.com/llm-development/best-open-source-llms-for-deployment-in-2026)及社区实践共识，2026 年生产级开源模型的推荐排序如下：

| 排名 | 模型 | 核心优势 | 最佳场景 | 注意事项 |
|------|------|---------|---------|---------|
| 1 | **LLaMA 4** (Meta) | GLUE/SuperGLUE SOTA，生态最丰富 | 研究应用、复杂 NLP | 微调需要大量计算资源 |
| 2 | **DeepSeek-V3/R1** | 推理+代码双优，MoE 高性价比 | 代码生成、推理、中文 | MoE 路由需关注稳定性 |
| 3 | **Qwen3** (阿里) | 中文能力顶尖，工具调用原生支持 | 中文应用、Agent、代码 | 部分版本许可证需确认 |
| 4 | **Mistral Medium 3.1** | 企业合规，欧洲部署首选 | 企业内部应用、合规场景 | 生态不如 LLaMA 丰富 |
| 5 | **GPT-NeoX 20B** (EleutherAI) | 20B 参数，社区驱动改进 | 文本生成、对话 Agent | 推理需 ≥40GB GPU 显存 |
| 6 | **BLOOM** (BigScience) | 46 种语言多语言模型 | 多语言应用 | 推理速度较慢 |

### ollama、vLLM、llama.cpp 场景化选型

根据 [CSDN 2026 年本地部署对比](https://blog.csdn.net/weixin_64358901/article/details/161665173)及社区实践：

| 维度 | Ollama | vLLM | llama.cpp |
|------|--------|------|-----------|
| **上手难度** | ★☆☆☆☆ 零配置 | ★★★☆☆ 需了解 GPU 和模型格式 | ★★☆☆☆ 需了解量化格式 |
| **推理吞吐** | 中等（单请求友好） | 极高（PagedAttention） | 中低（CPU 场景） |
| **量化支持** | GGUF（自动管理） | AWQ/GPTQ/FP8 | GGUF（格式最丰富） |
| **并发能力** | 有限（社区版） | 企业级（continuous batching） | 有限 |
| **API 兼容** | OpenAI 兼容 | OpenAI 兼容 + 多模型服务 | server 模式提供基础 API |
| **硬件要求** | Apple Silicon 友好 | NVIDIA GPU 优先 | CPU/Apple Silicon/边缘设备 |
| **适用规模** | 个人 ~ 小团队 | 团队 ~ 企业生产 | 个人 ~ 嵌入式 |

**选型口诀：**
- 🏠 想省事 → **Ollama**（一行命令跑模型）
- ⚡ 要高吞吐 → **vLLM**（生产环境首选）
- 💻 没显卡 → **llama.cpp**（CPU 也能跑 7B）
- 🔧 Agent + 结构化输出 → **SGLang**（约束解码天然优势）

## 2026 年 7 月推理框架最新动态

### vLLM v0.25.0：Model Runner V2 成为默认引擎

[vLLM v0.25.0](https://github.com/vllm-project/vllm/releases/tag/v0.25.0)（2026-07-11）是一个重大里程碑版本，**558 个 commits、232 位贡献者**参与：

- **Model Runner V2 成为所有 Dense 模型的默认引擎**（#44443）。这意味着所有非 MoE 模型将自动使用新一代推理管线，无需手动配置
- 性能提升：更高效的 KV cache 管理、更好的批处理调度
- 迁移建议：现有 v0.x 部署可直接升级，v1 引擎用户需关注兼容性变更

同时 [v0.24.0](https://github.com/vllm-project/vllm/releases/tag/v0.24.0)（2026-06-29）新增了：
- **MiniMax-M3** 模型支持（#45381）
- **DSpark 推测解码**支持，与 DeepSeek-V4 原生推测解码配合可提升推理吞吐

### Ollama v0.32.3 与本地推理生态

[Ollama v0.32.3](https://github.com/ollama/ollama/releases)（2026-07-23，今天发布）包含 MLX 框架更新，优化了 Apple Silicon 上的推理性能。近期版本的关键更新：

| 版本 | 日期 | 关键更新 |
|------|------|---------|
| v0.32.3 | 2026-07-23 | MLX 更新（Apple Silicon 优化） |
| v0.32.2 | 2026-07-20 | Claude Code 通道保持可用；移除废弃的 Agent prompt wrappers |
| v0.32.1 | 2026-07-16 | Gemma 4 工具调用改进；修复 MLX 缓存泄漏 |

> **趋势**：Ollama 正在向 Agent 场景靠拢——v0.32.2 专门为 Claude Code 保留了通道，v0.32.1 改进了 Gemma 4 的工具调用能力。本地 Agent 开发栈（Ollama + Claude Code / OpenCode）正在成为 2026 年开发者的重要选择。

### llama.cpp 的持续进化

llama.cpp 项目在 2026 年持续高频更新，保持 **CPU 推理和边缘部署的事实标准**地位。其 GGUF 量化生态仍然是格式最丰富、社区最活跃的选择，尤其在以下场景：
- Apple Silicon Mac 上的本地推理（MLX 和 llama.cpp 双轨支持）
- 嵌入式和边缘设备（Raspberry Pi、Android）
- 低成本 CPU-only 服务（无需 GPU）

### 2026 下半年部署趋势预判

| 趋势 | 说明 |
|------|------|
| **模型路由常态化** | 生产系统不再单一模型，而是小模型做分类→中模型做抽取→大模型做推理的路由管线 |
| **vLLM vs SGLang 双雄格局** | vLLM 主导通用高吞吐，SGLang 主导 Agent + 结构化输出，各有阵地 |
| **本地 Agent 开发栈兴起** | Ollama + Claude Code / OpenCode 的组合让本地 Agent 开发门槛大幅降低 |
| **量化即默认** | FP4/FP8 量化正在成为推理部署的默认选项，而非可选项——DeepSeek-V4 证明了 4-bit 量化在推理质量上的可行性 |
| **端侧推理加速** | Apple MLX、Qualcomm AI Engine、Intel OpenVINO 等端侧推理框架的成熟使 MacBook/手机上的模型运行体验接近 GPU 服务器 |

## 2026 年硬件选型快速参考

| 模型规模 | 推荐硬件 | 推理框架 | 预估成本 |
|---------|---------|---------|---------|
| 1B-7B 量化 | MacBook M4 / RTX 3060+ | Ollama / llama.cpp | $0（已有硬件） |
| 7B-13B 量化 | RTX 3090/4090 24GB | Ollama / vLLM | $800-$2000 |
| 13B-70B 量化 | A6000 48GB / 2× RTX 3090 | vLLM / SGLang | $4000-$8000 |
| MoE（如 DeepSeek-V4-Flash） | A100 80GB / H100 | vLLM / SGLang | $10K-$30K |
| 集群生产 | 多节点 H100/B200 | vLLM + K8s | 按需 |

## 参考来源

- [vLLM 文档](https://docs.vllm.ai/)
- [SGLang 文档](https://docs.sglang.ai/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Ollama 文档](https://github.com/ollama/ollama)
- [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference/index)
- [vLLM Blog — v1 Engine](https://blog.vllm.ai/)
- [SGLang — Structured Generation](https://docs.sglang.ai/)
- [Best Open Source LLMs for Deployment in 2026 — Ryz Labs](https://learn.ryzlabs.com/llm-development/best-open-source-llms-for-deployment-in-2026)
- [2026 本地部署大模型深度对比 — CSDN](https://blog.csdn.net/weixin_64358901/article/details/161665173)
- [vLLM v0.25.0 Release](https://github.com/vllm-project/vllm/releases/tag/v0.25.0)
- [Ollama v0.32.3 Release](https://github.com/ollama/ollama/releases)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-24 00:15:31*
