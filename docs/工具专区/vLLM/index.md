# vLLM

> vLLM 是一个高性能的大语言模型推理引擎，通过 PagedAttention 等创新技术，实现了业界领先的推理吞吐量。

---

## 为什么需要 vLLM？

将大模型部署为生产服务时，面临的关键挑战：

- **显存瓶颈**：KV 缓存占用大量显存，限制并发数
- **吞吐量低**：传统实现无法充分利用 GPU 算力
- **请求管理**：批量处理和调度难度大
- **延迟波动**：长序列推理的延迟不稳定

vLLM 通过一系列技术创新解决了这些问题。

---

## 核心技术

### PagedAttention

vLLM 最核心的创新是 **PagedAttention**，灵感来自操作系统的虚拟内存管理：

**传统注意力**：KV 缓存按最大序列长度分配连续显存
- 碎片化严重，实际使用率仅 20-40%

**PagedAttention**：KV 缓存按页分配非连续显存
- 类似虚拟内存的页表机制
- 显存利用率接近 100%
- 支持动态增长和回收

```
传统方式: |████████░░░░░░░░████████░░░░|  (50% 浪费)
PagedAttention: |████████████████████████|  (接近 100% 利用)
```

### 连续批处理（Continuous Batching）

传统批处理：等一批请求全部完成后再处理下一批
vLLM：请求到达后立即加入当前批次，完成即移除

```
传统批处理:
[Req1] [Req2] [Req3] ──全部完成── [Req4] [Req5]

连续批处理:
[Req1] → [Req1 Req2] → [Req1 Req2 Req3] → [Req2 Req3] → [Req3]
```

---

## 性能对比

| 指标 | HuggingFace Transformers | vLLM |
|-----|------------------------|------|
| 吞吐量 | 1x（基准） | **10-23x** |
| 显存效率 | 20-40% | **95-100%** |
| 请求调度 | FIFO | **连续批处理** |
| KV 缓存管理 | 连续分配 | **分页管理** |
| 并行解码 | 不支持 | **支持** |

---

## 快速开始

### 安装

```bash
pip install vllm
```

### 基本使用

```python
from vllm import LLM, SamplingParams

# 加载模型
llm = LLM(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    tensor_parallel_size=1,    # 单卡
    dtype="auto",
    max_model_len=8192         # 最大上下文长度
)

# 采样参数
params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=1024,
    presence_penalty=0.1
)

# 批量生成
prompts = [
    "解释什么是量子计算。",
    "用 Python 写一个快速排序。",
    "太阳系有几颗行星？"
]
outputs = llm.generate(prompts, params)

for output in outputs:
    print(f"提示: {output.prompt}")
    print(f"生成: {output.outputs[0].text}\n")
```

---

## 部署为 API 服务

### 启动服务

```bash
# 启动兼容 OpenAI API 的服务
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.9
```

### 调用服务

```python
from openai import OpenAI

# 完全兼容 OpenAI API
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # vLLM 不验证 key
)

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    messages=[
        {"role": "user", "content": "什么是强化学习？"}
    ],
    temperature=0.7,
    max_tokens=512
)

print(response.choices[0].message.content)
```

---

## 高级配置

### 多 GPU 部署

```bash
# 张量并行（多卡分摊模型）
vllm serve meta-llama/Meta-Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4

# 流水线并行
vllm serve meta-llama/Meta-Llama-3.1-70B-Instruct \
    --pipeline-parallel-size 2
```

### 量化支持

```bash
# AWQ 量化
vllm serve TheBloke/Llama-2-7B-AWQ --quantization awq

# GPTQ 量化
vllm serve TheBloke/Llama-2-7B-GPTQ --quantization gptq
```

---

## 生产环境最佳实践

| 配置项 | 推荐值 | 说明 |
|-------|-------|------|
| `gpu-memory-utilization` | 0.85-0.95 | GPU 显存利用率 |
| `max-num-seqs` | 256 | 最大并发请求数 |
| `max-model-len` | 8192-32768 | 模型最大上下文 |
| `enable-prefix-caching` | True | 前缀缓存加速 |
| `enforce-eager` | False | 使用 CUDA 图加速 |

---

## 优势

- **超高吞吐**：比 HuggingFace 实现快 10-20 倍
- **显存高效**：PagedAttention 接近零浪费
- **兼容 OpenAI API**：即插即用，生态兼容
- **支持多种模型**：LLaMA、Mistral、Qwen、DeepSeek 等
- **高级功能**：前缀缓存、多模态支持、LoRA 服务

## 局限

- **部署复杂度**：多 GPU 配置需要专业运维知识
- **仅限推理**：不支持训练和微调
- **模型兼容性**：部分模型需额外适配
- **首次加载慢**：大模型首次加载需要时间

---

## 应用场景

- **生产推理服务**：高并发 LLM API
- **批量离线推理**：大规模数据处理
- **模型评测**：需要高效运行大量测试用例
- **多租户服务**：为多个应用提供模型服务

---

## 下一步

- 安装 vLLM 并运行一个小模型测试
- 启动 OpenAI 兼容 API 服务
- 对比 vLLM 与原始 Transformers 的吞吐量差异
- 学习张量并行和流水线并行的配置
- 了解 PagedAttention 的技术细节论文
