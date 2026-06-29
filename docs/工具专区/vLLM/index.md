# vLLM：大模型推理的速度革命

> 2023 年 6 月，UC Berkeley 的一篇论文和开源项目改变了 LLM 推理的格局。
> 在此之前，部署一个 70B 模型需要复杂的工程优化。vLLM 之后，一条命令搞定高吞吐推理。

---

## 问题：传统 LLM 推理为什么又慢又贵？

### 显存的"黑洞"

运行一个 70B 模型（FP16）需要 140GB 显存。但问题不止于模型权重——**KV Cache** 才是最大的内存杀手。

**KV Cache 是什么**：
```
用户："法国的首都是什么？"
模型逐 token 生成："巴" → "黎"

生成"巴"时，模型计算了所有注意力头的 Key 和 Value
生成"黎"时，它需要重新计算吗？
不！之前的 Key/Value 被缓存了起来 = KV Cache
```

**KV Cache 有多大**：
```
一个 70B 模型处理 2048 tokens 的请求：
每层 × 每头 × 每 token × 2（Key+Value）× 精度
≈ 每 token 约 5MB
2048 tokens = 10GB+

100 个并发请求 → 1000GB+ KV Cache
```

**传统方案的问题**：显存被"碎片化"。有些 KV Cache 提前完成了但空间被占着，新请求找不到连续的内存块。

### 批处理的浪费

传统批处理（Static Batching）：
```
┌─────────────────────┐
│ 请求A (长)  ████████│
│ 请求B (短)  ██      │  ← 等 B 等 A 完成
│ 请求C (中)  ████    │  ← 等 C 等 A 完成
└─────────────────────┘
所有请求必须一起开始一起结束。
短的请求只能干等长的请求。
```

---

## vLLM 的解决方案

### PagedAttention — 显存的"虚拟内存"

vLLM 把操作系统中的"分页"（Paging）概念引入 KV Cache 管理。

**传统方式**：KV Cache 存在一个连续的内存块。

```
请求A: [KKKKKKKKKKKKKKKK] ← 连续分配
        ↑ 如果内存碎片，分配失败
```

**PagedAttention**：KV Cache 被分成固定的"页"（Block），可以存在不连续的内存位置。

```
请求A: 页[K1]→页[K3]→页[K5]→页[K2]→页[K4]
       ↑ 页表（Page Table）记录映射关系
       ↑ 不连续的物理页，逻辑上连续
```

**效果对比**：显存利用率从 20-40% 提升到 **95%+**。

### Continuous Batching — 动态批处理

不再等所有请求一起结束。

```
时间 →
请求A: ████░░░░░████░░░░░░░████
请求B: ░░████░░░░░░░████
请求C: ░░░░████░░░░░░░░░░░████
       ↑ 新请求可以随时加入
       ↑ 完成的请求立即退出，释放空间
```

**传统 vs 连续批处理**：
```
传统批处理:
[A: 10s] [B: 1s] [C: 3s] → 总时间 = 10s（B 和 C 等 A）

连续批处理:
A: ████████████
B: ██▓▓▓▓▓▓▓▓▓▓  ← B 早完成了，但空间被释放
C: ████████████
总时间 = 10s，但吞吐量提高 2-3 倍
```

---

## 性能基准：vLLM vs 其他方案

### 吞吐量对比

| 方案 | 吞吐量 (tokens/s) | 相对 vLLM | 适用场景 |
|------|-------------------|-----------|---------|
| **vLLM** | **3200** | 1.0× | 生产部署标准 |
| HuggingFace TGI | 2100 | 0.66× | 简单部署 |
| TensorRT-LLM | 3800 | 1.19× | 极致性能（需 NVIDIA）|
| llama.cpp | 1500 | 0.47× | 个人使用 |
| 原生 HF + 自己写 | 500-800 | 0.16-0.25× | 不推荐 |

**测试条件**：LLaMA 70B, 4× A100 80GB, batch=32, input_len=512, output_len=256

### 显存节省对比

| 上下文长度 | 传统方案 | vLLM (PagedAttention) | 节省 |
|-----------|---------|----------------------|------|
| 2K tokens | 8GB | 2.5GB | 69% |
| 4K tokens | 17GB | 5.1GB | 70% |
| 8K tokens | 35GB | 9.8GB | 72% |
| 32K tokens | 142GB | 38GB | 73% |

---

## 实际部署：一条命令起飞

### 基础部署

```bash
pip install vllm

python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-72B-Instruct \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192
```

**参数说明**：
| 参数 | 含义 | 推荐 |
|------|------|------|
| `tensor-parallel-size` | GPU 数量 | N 张卡设 N |
| `gpu-memory-utilization` | 显存占用比例 | 0.85-0.95 |
| `max-model-len` | 最大上下文 | 根据显存调整 |
| `dtype` | 精度 | auto (FP16/BF16) |
| `enforce-eager` | 是否禁用 CUDA 图 | 调试时开启 |

### 与 OpenAI API 完全兼容

启动后，任何用 OpenAI SDK 的代码都可以切换到 vLLM：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct",
    messages=[{"role": "user", "content": "你好"}]
)
```

**这意味着**：所有用 OpenAI API 的工具（LangChain、Cursor、Continue.dev）可以无缝切换到你本地的 vLLM 实例。

---

## 高级功能

### 量化支持

```bash
# AWQ 量化（推荐，质量损失最小）
vllm serve model-path --quantization awq

# GPTQ 量化
vllm serve model-path --quantization gptq

# FP8（H100 原生支持）
vllm serve model-path --dtype float8
```

### Prefix Caching（前缀缓存）

相同的前缀（如 System Prompt）只计算一次 KV Cache：

```python
server_kwargs = {
    "enable_prefix_caching": True
}
```

**效果**：在共享 system prompt 的场景下，首 token 延迟降低 50-80%。

### Speculative Decoding（投机解码）

用小模型生成候选 tokens，大模型验证——加速 2-3×：

```bash
vllm serve Qwen2.5-72B \
  --speculative-model Qwen2.5-7B \
  --num-speculative-tokens 5
```

---

## 什么时候用 vLLM？

### ✅ 适合的场景

- 生产环境需要高吞吐
- 部署 30B+ 大模型
- 需要 OpenAI 兼容 API
- 多个应用共享同一模型
- 需要严格的延迟控制

### ❌ 不适合的场景

- 个人本地调试（Ollama 更简单）
- 只需要单个模型单次调用
- 没有 GPU（vLLM 需要 CUDA）
- 只需要小模型（7B 以下用什么差异不大）

---

> **一句话总结**：vLLM 是目前生产环境中推理部署的"事实标准"。PagedAttention 解决了 LLM 推理的最大瓶颈——显存管理和批处理效率。如果你的应用依赖 LLM，vLLM 应该是你的首选推理后端。
