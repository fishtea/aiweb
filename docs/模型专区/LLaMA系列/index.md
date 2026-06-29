# LLaMA 系列

> Meta 发布的 LLaMA（Large Language Model Meta AI）系列是开源大模型的标杆，带动了全球开源 AI 生态的繁荣。

---

## 发展历程

| 版本 | 发布时间 | 参数量 | 关键创新 |
|-----|---------|-------|---------|
| LLaMA 1 | 2023.02 | 7B, 13B, 33B, 65B | 高质量数据、小模型强性能 |
| LLaMA 2 | 2023.07 | 7B, 13B, 70B | 开源商用许可、Chat 版本 |
| Code LLaMA | 2023.08 | 7B, 13B, 34B | 代码专项优化 |
| LLaMA 3 | 2024.04 | 8B, 70B | 全新 tokenizer、更强性能 |
| LLaMA 3.1 | 2024.07 | 8B, 70B, **405B** | 首个 400B+ 开源模型、工具调用 |
| LLaMA 3.2 | 2024.09 | 1B, 3B, 11B, 90B | 多模态（视觉+文本）、轻量端侧 |

---

## LLaMA 3.1 模型规格

| 规格 | 8B | 70B | 405B |
|-----|-----|-----|------|
| 适用硬件 | 消费级 GPU | 多卡服务器 | 集群部署 |
| 推理内存 | ~16GB | ~140GB | ~800GB |
| 量化运行 | 8GB（4bit） | 40GB（4bit） | 200GB（4bit） |
| 推理速度 | 快速 | 中等 | 较慢 |
| 智能水平 | 良好 | 优秀 | 卓越 |

---

## 如何本地使用 LLaMA

### 使用 Ollama（推荐入门）

```bash
# 一键安装后运行
ollama run llama3.1:8b
ollama run llama3.1:70b  # 需足够显存
```

### 使用 Hugging Face Transformers

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": "你是一个有用的助手。"},
    {"role": "user", "content": "什么是注意力机制？"}
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

outputs = model.generate(
    inputs,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True
)

response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
print(response)
```

---

## 微调生态

### 微调方法

| 方法 | 工具 | 适用场景 | 显存需求 |
|-----|------|---------|---------|
| **全参数微调** | PyTorch + FSDP | 大规模定制 | 极高 |
| **LoRA** | PEFT | 高效适配单任务 | 低 |
| **QLoRA** | PEFT + bitsandbytes | 单卡微调 70B | 极低（48GB） |
| **DPO** | TRL | 偏好对齐 | 中等 |

### LoRA 微调示例

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 仅训练 ~0.5% 的参数
```

---

## 社区生态系统

LLaMA 的开源属性催生了庞大的社区生态：

- **推理引擎**：llama.cpp、vLLM、TensorRT-LLM
- **量化工具**：GPTQ、AWQ、GGUF
- **微调框架**：Axolotl、Unsloth、LLaMA-Factory
- **应用层**：Ollama、LocalAI、Text Generation WebUI
- **衍生模型**：Vicuna、Alpaca、WizardLM、Yi 等

---

## 优势

- **完全开源**：权重开源，商用许可（LLaMA 2+）
- **性能出众**：405B 模型在多项基准上接近 GPT-4
- **生态丰富**：社区工具、教程、衍生模型众多
- **可定制**：支持微调、量化、蒸馏等定制
- **数据隐私**：可完全本地部署，数据不外泄

## 局限

- **部署门槛**：405B 模型需要专业基础设施
- **中文能力**：原生中文不及 Qwen 等专注中文的模型
- **需要技术能力**：微调和部署需要一定技术背景
- **社区版本不一**：衍生模型质量参差不齐

---

## 应用场景

- **私有化部署**：企业内部 AI 助手
- **学术研究**：模型架构研究、对齐研究
- **微调定制**：特定领域模型训练
- **边缘计算**：1B/3B 模型在手机和 IoT 设备运行

---

## 下一步

- 下载 LLaMA 模型（需申请访问权限）
- 使用 Ollama 体验 8B 模型
- 学习使用 Unsloth 进行高效微调
- 探索社区生态中的优秀衍生模型
