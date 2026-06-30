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

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:11:39*
*资源区块更新时间：2026-06-30 11:11:09*
*资源区块更新时间：2026-06-30 10:42:21*
*资源区块更新时间：2026-06-30 10:25:06*
