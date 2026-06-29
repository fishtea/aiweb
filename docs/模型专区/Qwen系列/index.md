# Qwen 系列（通义千问）

> 阿里巴巴通义千问（Qwen）系列是中文大模型的开源标杆，在中文理解、数学推理和代码生成方面表现卓越。

---

## 发展历程

| 版本 | 发布时间 | 参数量 | 关键特性 |
|-----|---------|-------|---------|
| Qwen | 2023.08 | 7B, 14B, 72B | 初代，中文能力突出 |
| Qwen 1.5 | 2024.02 | 0.5B-72B | 全系列、多尺寸覆盖 |
| Qwen 2 | 2024.06 | 0.5B-72B | MoE 版本、更强推理 |
| Qwen 2.5 | 2024.09 | 0.5B-72B | **最强开源中文模型** |
| Qwen 2.5-Coder | 2024.11 | 1.5B-32B | 代码专项优化 |
| Qwen 2.5-Math | 2024.11 | 1.5B-72B | 数学推理增强 |
| Qwen 2.5-VL | 2025.01 | 3B-72B | 视觉语言多模态 |
| Qwen 3 | 2025.04 | 0.6B-235B | 思考模式、全面升级 |

---

## 模型规格（Qwen 2.5）

| 规格 | 0.5B | 1.5B | 7B | 14B | 32B | 72B |
|-----|------|------|-----|-----|-----|-----|
| 硬件要求 | 手机/CPU | 低端GPU | 消费级 | 中端GPU | 多卡 | 服务器 |
| 推理显存 | 1GB | 3GB | 14GB | 28GB | 64GB | 144GB |
| 量化 4bit | 0.5GB | 1GB | 4GB | 8GB | 16GB | 40GB |
| 智能水平 | 基础 | 基础 | 良好 | 优秀 | 优秀 | 卓越 |

**适合各种场景，从手机端到服务器全覆盖。**

---

## 核心优势

### 1. 中文能力行业领先

Qwen 系列在中文理解与生成方面达到开源模型的最佳水平：

- **中文写作**：符合中文表达习惯，成语、俗语运用自然
- **中文知识**：对中国文化、历史、社会有深入理解
- **中英翻译**：高质量的中英互译能力

### 2. 数学推理

Qwen2.5-Math 在数学基准测试中表现突出：

| 基准 | Qwen2.5-Math-72B | GPT-4o | Claude 3.5 |
|-----|-----------------|--------|------------|
| GSM8K | 96.8% | 95.9% | 96.4% |
| MATH | 85.8% | 76.9% | 79.1% |
| 中国高考数学 | 92.5% | — | — |

### 3. 代码能力

Qwen2.5-Coder 在代码生成任务上表现优异：

- 支持 Python、Java、C++、JavaScript 等主流语言
- 代码补全、调试、重构均表现良好

---

## 本地使用

### 使用 Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-7B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

prompt = "用 Python 实现一个二叉树的中序遍历"
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer([text], return_tensors="pt").to(model.device)

outputs = model.generate(**inputs, max_new_tokens=512)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

### 使用 Ollama

```bash
ollama run qwen2.5:7b
ollama run qwen2.5:72b  # 需大显存
```

### 使用 vLLM 部署

```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen2.5-72B-Instruct", tensor_parallel_size=4)
params = SamplingParams(temperature=0.7, max_tokens=1024)

outputs = llm.generate(["解释一下反向传播算法"], params)
print(outputs[0].outputs[0].text)
```

---

## API 访问

通过阿里云通义千问 API 调用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen2.5-72b-instruct",
    messages=[{"role": "user", "content": "什么是注意力机制？"}]
)
print(response.choices[0].message.content)
```

---

## 优势

- **中文能力最强**：开源模型中的中文水平天花板
- **模型尺寸齐全**：从 0.5B 到 235B，覆盖一切场景
- **开源彻底**：权重、代码、技术报告全公开
- **数学推理强**：数学基准测试表现顶尖
- **社区活跃**：中文社区支持充分，教程丰富
- **商用友好**：开源许可允许商业使用

## 局限

- **英文能力**：在纯英文任务上不如 LLaMA-3
- **创意生成**：创意写作略逊于 GPT-4o 和 Claude
- **开源版本滞后**：API 版本更新快于开源版

---

## 应用场景

- **中文 NLP 任务**：文本分类、信息抽取、内容审核
- **企业知识库**：中文企业内部问答系统
- **教育辅助**：数学题讲解、作文批改
- **代码生成**：中文注释的代码开发
- **本地部署**：数据安全要求高的场景

---

## 下一步

- 访问 [通义千问官网](https://tongyi.aliyun.com) 在线体验
- 从 Hugging Face 下载 Qwen2.5 模型
- 使用 LLaMA-Factory 对 Qwen 进行微调
- 关注 Qwen 3 的新特性更新
