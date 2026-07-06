# vLLM — 高性能 LLM 推理引擎

> vLLM 是 UC Berkeley Sky Computing Lab 开发的高性能 LLM（大语言模型）推理和部署引擎。凭借革命性的 **PagedAttention** 算法，vLLM 成为生产环境中部署 LLM 的首选工具之一。

---

## 工具概述

| 属性 | 详情 |
|------|------|
| **开发者** | UC Berkeley Sky Computing Lab → 社区 |
| **首次发布** | 2023 年 6 月 |
| **当前版本** | V1 (2025) |
| **许可** | Apache 2.0 |
| **核心语言** | Python + CUDA |
| **GitHub** | [vllm-project/vllm](https://github.com/vllm-project/vllm) |
| **贡献者** | 2000+ |

---

## PagedAttention — 核心创新

根据 [vLLM 官方文档](https://docs.vllm.ai) 和 [vLLM 宣布博客](https://blog.vllm.ai/2023/06/20/vllm.html)：

### 传统 KV 缓存问题

大模型的推理瓶颈在于 KV 缓存（Key-Value Cache）管理：
- 每个序列的 KV 缓存巨大（GPT-3 约 1.7GB/序列）
- 显存碎片化严重（最多浪费 60-80%）
- 无法有效共享和调度

### PagedAttention 解决方案

借鉴操作系统**虚拟内存分页**的思想：

- 将 KV 缓存划分为固定大小的**块（Blocks/Pages）**
- 非连续存储在物理显存中
- 通过块表（Block Table）实现逻辑到物理的映射
- **减少显存碎片 60%+**
- 支持**跨序列共享**（如并行采样时共享前缀）

**效果:** 相比传统方案，vLLM 实现 **14-24× 更高的吞吐量**。

---

## vLLM V1 — 架构升级

根据 [vLLM 优化文档](https://docs.vllm.ai/en/stable/configuration/optimization) 和 [PagedAttention PDF](https://llmsystem.github.io/llmsystem2025spring/assets/files/llmsys-22-vLLM_woosuk_kwon-1f34697dbb1a1fb5b798daf6eff14b67.pdf)：

### V1 关键改进

| 特性 | V0 | V1 |
|------|-----|-----|
| 输入张量管理 | 每步重建 | **增量 diff 更新** |
| CUDA Graph | 全模型单图 | **Piecewise CUDA Graph** |
| 预处理 | 单进程 | **双进程**（前端+引擎分离） |

### V1 性能提升

- Piecewise CUDA Graph 减少了 Python/PyTorch 开销（可占推理延迟的 50%）
- 增量输入准备：每步仅处理新加入/完成的请求差异
- 双进程架构：确保 GPU 不被预处理/后处理/HTTP 请求阻塞

---

## 支持的模型

vLLM 支持 **200+ 模型架构**，包括：

| 类型 | 示例 |
|------|------|
| Decoder-only LLMs | LLaMA, Qwen, Gemma, GPT |
| MoE LLMs | Mixtral, DeepSeek-V3, Qwen-MoE |
| 多模态 | LLaVA, Qwen-VL, Pixtral |
| Embedding | E5-Mistral, GTE, ColBERT |
| 混合注意力 | Mamba, Qwen3.5 |

---

## 量化支持

- **FP8, MXFP8/MXFP4, NVFP4**
- **INT8, INT4**
- **GPTQ/AWQ**
- **GGUF**
- 以及更多压缩格式

---

## 如何开始

### 安装

```bash
pip install vllm
```

### 运行模型

```python
from vllm import LLM, SamplingParams

# 加载模型
llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")

# 设置采样参数
sampling_params = SamplingParams(temperature=0.7, max_tokens=512)

# 推理
outputs = llm.generate(["请解释 vLLM 的 PagedAttention 原理。"], sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

### 启动 OpenAI 兼容 API 服务器

```bash
vllm serve meta-llama/Meta-Llama-3-8B-Instruct --port 8000
```

```python
# 然后像调用 OpenAI 一样调用
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")
```

---

## 高级特性

| 特性 | 说明 |
|------|------|
| **Continuous Batching** | 动态添加/移除请求，最大化 GPU 利用率 |
| **Chunked Prefill** | 将长预填充分块后与解码批处理 |
| **Prefix Caching** | 缓存公共前缀的计算结果 |
| **Speculative Decoding** | 使用草稿模型加速推理 |
| **Disaggregated Prefill/Decode** | 分离预填充和解码阶段 |
| **Multi-LoRA** | 同时服务多个 LoRA 适配器 |
| **Structured Output** | xgrammar / guidance 支持 |
| **Reasoning Model 支持** | DeepSeek-R1、Qwen3 等思考模型的原生支持与 `reasoning_tokens` 计费 |
| **MCP / Agent 工具调用** | 配合 OpenAI 兼容 API 暴露函数调用能力 |

### 推理加速技术对比

理解 vLLM 的加速原理，有助于在不同场景选对优化手段：

| 技术 | 解决的瓶颈 | 效果 | 代价 |
|------|-----------|------|------|
| PagedAttention | KV 缓存显存碎片 | 吞吐 14-24× | 实现复杂 |
| Continuous Batching | 请求间 GPU 空闲 | 提升并发吞吐 | 调度开销 |
| Prefix Caching | 重复前缀重复计算 | 降低 TTFT、省 token | 额外显存 |
| Chunked Prefill | 长上下文阻塞解码 | 降低排队延迟 | 实现复杂 |
| Speculative Decoding | 自回归逐 token 生成慢 | 2-3× 解码加速 | 需草稿模型 |
| Disaggregated Prefill | Prefill 与 Decode 抢资源 | 资源隔离、吞吐提升 | 多节点部署 |

> 选型提示：单机低并发优先 Prefix Caching + Chunked Prefill；高并发服务化优先 Continuous Batching + PagedAttention；对延迟极敏感可叠加 Speculative Decoding。

---

## 优势与局限

**优势:**
- **吞吐量顶尖:** PagedAttention 带来 14-24× 提升
- **模型支持广泛:** 200+ 架构，持续更新
- **硬件支持广:** NVIDIA、AMD、Intel、Google TPU 等
- **与 HuggingFace 无缝集成**
- **生产级可靠:** 2000+ 贡献者，企业广泛采用

**局限:**
- 本地/单用户场景过重（更适合 Ollama 或 llama.cpp）
- 调试和配置较复杂
- CPU 推理性能不如 llama.cpp
- 新硬件支持有时滞后

---

**参考资料：**
- [vLLM 官方文档](https://docs.vllm.ai)
- [PagedAttention & vLLM (PDF)](https://llmsystem.github.io/llmsystem2025spring/assets/files/llmsys-22-vLLM_woosuk_kwon-1f34697dbb1a1fb5b798daf6eff14b67.pdf)
- [vLLM Quickstart Guide (Glukhov)](https://www.glukhov.org/llm-hosting/vllm/vllm-quickstart)
- [vLLM Optimization Documentation](https://docs.vllm.ai/en/stable/configuration/optimization)
- [vLLM Announcing Blog](https://blog.vllm.ai/2023/06/20/vllm.html)

---

## 2026 最新进展

### vLLM V1 进入稳定阶段

vLLM V1 在 0.6.0+ 版本中成为默认引擎，V0 已废弃。V1 的核心改进聚焦于**多模态推理**和**架构分离**：

**多模态推理专属优化：**
- **Encoder Cache（编码器缓存）**：多模态嵌入直接在 GPU 上计算并存储，避免重复执行编码器。例如 Pixtral 单张 1024×1024 图像产生 4096 个嵌入向量，缓存后显著降低延迟。
- **Encoder-Aware Scheduler（编码感知调度器）**：跟踪多模态嵌入位置，合并文本嵌入时直接检索缓存数据。
- **增强 Prefix Caching**：引入图像/音频哈希作为元数据，解决 V0 中占位符 token（如 `<image>`）引起的缓存冲突问题。
- **解耦 CPU/GPU 进程**：将输入处理（CPU）与前向推理（GPU）分离为独立进程，异步流水线防止 CPU 阻塞 GPU。

**基准测试结果：**
- 在线服务（Qwen2-VL 7B）：高并发场景下 V1 显著优于 V0
- 离线推理（Molmo-72B, 4×H100）：V1 吞吐量提升约 **40%**；启用 Prefix + Feature Caching 后，重复请求场景获得数倍提升

### 生产部署最佳实践（2026）

根据 SitePoint 和 Spheron 的部署指南，vLLM 生产环境部署要点：

**Docker 单 GPU 部署：**
```bash
docker run -d \
  --name vllm-server \
  --gpus '"device=0"' \
  --shm-size=4g \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env-file .env \
  vllm/vllm-openai:<tag> \
  --model hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 \
  --served-model-name llama-3.1-8b \
  --max-model-len 8192 \
  --quantization awq \
  --dtype auto \
  --gpu-memory-utilization 0.90 \
  --enable-prefix-caching \
  --port 8000
```

**关键优化参数：**
- `--max-model-len`：限制 KV 缓存预留量，调低可腾出显存给更大批次
- `--gpu-memory-utilization 0.90`：为 CUDA context 预留 10% 头寸
- `--enable-prefix-caching`：对共享 System Prompt 场景显著降低首 token 延迟（TTFT）
- 多 GPU 场景使用 `--tensor-parallel-size N` + `--ipc=host` 确保 NCCL 通信

**量化选型建议：**
| 量化方式 | 精度 | 适用场景 | 吞吐提升 |
|---------|------|---------|---------|
| AWQ | 4-bit | 最广泛兼容 | 5-15% vs GPTQ |
| FP8 | 8-bit | H100 Hopper | ~2× vs FP16 |
| GGUF | 可变 | CPU 卸载 | 不推荐 GPU 优先场景 |

**生产架构组件：** Nginx 反向代理（TLS 终止 + 速率限制）+ Docker Compose 编排 + Healthcheck 探针 + KEDA 自动伸缩。

### 社区与生态里程碑

- GitHub Stars 突破 **66,000+**，贡献者 **2000+**
- 与 deeplearning.ai 合作推出免费课程《Fast & Efficient LLM Inference with vLLM》（2026 年 6 月）
- Simon Mo（vLLM 联合负责人）在 Ray Summit 分享 State of vLLM 2025，涵盖 RLHF 后训练与推理集成
- 支持 200+ 模型架构，从 LLaMA 到 DeepSeek-R1 的推理优化均已覆盖

### Disaggregated Prefill/Decode（分离式 P/D）

vLLM V1 引入**分离式预填充与解码**：将计算密集的 Prefill 阶段与显存带宽密集的 Decode 阶段部署到不同节点。这使得：
- Prefill 节点专注高计算吞吐，Decode 节点专注低延迟连续生成
- 资源隔离避免"长上下文阻塞解码"问题
- 适合离线批处理 + 在线推理混合场景

### 参考来源
- [Red Hat: vLLM V1 Accelerating Multimodal Inference](https://developers.redhat.com/articles/2025/02/27/vllm-v1-accelerating-multimodal-inference-large-language-models)
- [Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)
- [vLLM Production Deployment: Complete 2026 Guide - SitePoint](https://www.sitepoint.com/vllm-production-deployment-guide-2026)
- [The Rise of vLLM: Building an Open Source LLM Inference Engine (YouTube)](https://www.youtube.com/watch?v=WLl8D1nyaW8)
- [deeplearning.ai: Fast & Efficient LLM Inference with vLLM](https://vllm.ai/blog/2026-06-03-deeplearning-ai-vllm-course)

### v0.24.0 发布 (2026年6月)

2026年6月29日，vLLM 发布 **v0.24.0**，571 个提交、256 位贡献者（77 位新加入），是近期最大的一次版本更新。

**新模型支持：**

- **MiniMax-M3**：新增对 MiniMax 新一代多模态模型 M3 的完整支持，包括 BF16/FP8 indexer（通过 MSA）、MXFP4 量化、FP8 稀疏 GQA，以及 AMD ROCm（MI300X FP8 per-channel、gfx950 mxfp8 MoE）和 XPU 后端适配。
- **DeepSeek-V4 持续成熟**：自 v0.22.0 首次引入后，V4 经历了最大规模优化——FlashInfer 稀疏索引缓存（TTFT 2-4% 提升）、prefill chunk-planning 优化（端到端吞吐 4% 提升）、集群协作 topK 内核（低延迟）、连续 per-block KV 分配、共享专家的 block-FP8 TEP=16。已启用 **SM120（Blackwell 下一代）** 支持，同步覆盖 XPU 和 ROCm 的 attention/MoE 路径。

**Model Runner V2 (MRv2) 扩展：**

- MRv2 在 Llama 和 Mistral 密集模型上已成为默认引擎（继 Qwen3 之后），新增 FlashInfer 采样器、可打断 CUDA Graph、流水线并行气泡消除等特性。
- 标志着 vLLM 推理引擎架构从 V1 向 MRv2 的全面迁移已进入成熟阶段，覆盖主流模型家族。

**硬件生态里程碑：**

- **SM120**：vLLM 成为首批支持 NVIDIA 下一代 Blackwell Ultra 架构的推理框架之一，DeepSeek-V4 和 GLM-5.1 均已在 SM120 上启用。
- Intel XPU 和 AMD ROCm 持续追赶——MoE 模型的多后端覆盖已接近 CUDA 水平。
- AMD Zen CPU 推理路径新增 zentorch 加速量化线性推理（W8A8/W4A16）。

### v0.23.0 → v0.24.0 版本演进要点

| 版本 | 日期 | 关键变化 |
|------|------|---------|
| v0.22.0 | 5月底 | DeepSeek-V4 首次引入 |
| v0.22.1 | 6月5日 | 补丁版：Mellum v2 编码模型、Zen CPU 加速 |
| v0.23.0 | 6月15日 | DeepSeek-V4 多后端固化、MRv2 默认 Llama/Mistral、408 commits |
| v0.24.0 | 6月29日 | MiniMax-M3、SM120 支持、MRv2 扩展、571 commits |

> **趋势**：vLLM 正以每两周一个大版本的节奏迭代，核心方向是**多后端（CUDA/ROCm/XPU/CPU）统一** + **新模型（MiniMax/DeepSeek/GLM）快速接入** + **MRv2 引擎全面替换 V1**。

### 参考来源
- [vLLM v0.24.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.24.0)
- [vLLM v0.23.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.23.0)
- [vLLM v0.22.1 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.22.1)
- [vLLM 官方文档](https://docs.vllm.ai/en/latest/)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-07 00:14:39*
