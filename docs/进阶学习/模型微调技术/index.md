# 模型微调技术

> 本页面总结了大型语言模型（LLM）的主流微调技术，重点涵盖 LoRA、QLoRA 及 Hugging Face 生态下的实践方法。

---

## 1. 概述

微调（Fine-tuning）是指在预训练模型基础上，使用特定领域数据进一步训练，以提升模型在目标任务上的表现。对于 LLM，微调可以在不改变模型架构的前提下，显著提升其在特定任务（如 Text-to-SQL、代码生成、文档摘要）上的质量。

> *"Not all use cases require fine-tuning – evaluate existing models/APIs first."* — [Philschmid 微调指南](https://www.philschmid.de/fine-tune-llms-in-2024-with-trl)

---

## 2. 核心技术

### 2.1 LoRA（Low-Rank Adaptation）

**来源：** [Databricks Blog - Efficient Fine-Tuning with LoRA](https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms)

LoRA 的核心思想是：**不直接更新完整的权重矩阵，而是训练两个低秩矩阵（LoRA Adapter）来近似权重更新**。训练完成后，Adapter 可以合并回原模型或在推理时动态加载。

**关键超参数：**

| 参数 | 描述 | 推荐值 |
|------|------|--------|
| `r` | 低秩矩阵的秩，决定可训练参数量 | 8-256 |
| `lora_alpha` | 缩放因子 | 16-128 |
| `lora_dropout` | Dropout 率 | 0.05-0.1 |
| `target_modules` | 应用 LoRA 的目标层 | 建议覆盖所有线性层 |

**关键实验发现（Databricks）：**

| r | target_modules | 输出质量 | 可训练参数量 |
|---|----------------|----------|-------------|
| 8 | 仅 Attention 层 | **低** | 2.66M |
| 16 | 仅 Attention 层 | **低** | 5.32M |
| **8** | **所有线性层** | **高** | **12.99M** |
| 8 | 所有线性层 (8-bit) | 高 | 12.99M |

> *"The biggest improvement is observed in targeting all linear layers in the adaptation process, as opposed to just the attention blocks."*

### 2.2 QLoRA（量化 LoRA）

QLoRA 是 LoRA 的内存优化版本，将预训练模型以 **4-bit 量化** 权重加载到 GPU，同时保持与标准 LoRA 几乎相同的效果。通过 `bitsandbytes` + `PEFT` + `TRL` 实现。

**优势：**
- 单张 24GB GPU 即可微调 7B 参数模型
- 微调效果与全精度 LoRA 无显著差异
- 支持双重量化（Double Quantization）进一步节省显存

### 2.3 PEFT（Parameter-Efficient Fine-Tuning）

Hugging Face 的 [PEFT](https://github.com/huggingface/peft) 库统一了多种参数高效微调方法：

- **LoRA / QLoRA** — 低秩适应
- **Adapter** — 在 Transformer 层间插入小型适配层
- **Prefix Tuning** — 在输入前添加可训练的前缀向量
- **IA³** — 通过学习向量对激活进行缩放

---

## 3. 实战：使用 Hugging Face TRL 微调 LLM

**来源：** [How to Fine-Tune LLMs in 2024 with Hugging Face - Philschmid](https://www.philschmid.de/fine-tune-llms-in-2024-with-trl)

### 3.1 环境准备

```bash
pip install "transformers==4.36.2" "datasets==2.16.1" "accelerate==0.26.1"
pip install "bitsandbytes==0.42.0" "peft" "trl"
```

如需 Flash Attention（Ampere GPU 及以上）：
```bash
MAX_JOBS=4 pip install flash-attn --no-build-isolation
```

### 3.2 数据集准备

以 Text-to-SQL 为例，使用 `b-mc2/sql-create-context` 数据集：

```python
def create_conversation(sample):
    return {
        "messages": [
            {"role": "system", "content": f"SCHEMA: {sample['context']}"},
            {"role": "user", "content": sample["question"]},
            {"role": "assistant", "content": sample["answer"]}
        ]
    }
```

### 3.3 4-bit 量化加载模型

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_config,
    attn_implementation="flash_attention_2",
    torch_dtype=torch.bfloat16
)
```

### 3.4 LoRA 配置（推荐全线性层）

```python
from peft import LoraConfig

peft_config = LoraConfig(
    lora_alpha=128,
    lora_dropout=0.05,
    r=256,
    bias="none",
    target_modules="all-linear",
    task_type="CAUSAL_LM",
)
```

### 3.5 训练超参数

```python
from transformers import TrainingArguments

args = TrainingArguments(
    output_dir="my-finetuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=3,
    gradient_accumulation_steps=2,
    gradient_checkpointing=True,
    learning_rate=2e-4,
    bf16=True,
    warmup_ratio=0.03,
    lr_scheduler_type="constant",
)
```

### 3.6 SFTTrainer 训练

```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    args=args,
    train_dataset=dataset,
    peft_config=peft_config,
    max_seq_length=3072,
    tokenizer=tokenizer,
)
trainer.train()
```

> **成本参考：** 在 AWS `g5.2xlarge` (NVIDIA A10G, 24GB VRAM) 上微调 CodeLlama-7B 约需 1.5 小时，费用约 **$1.80**。

---

## 4. LoRA 超参数调优建议

**来源：** [Unsloth - LoRA Fine-tuning Hyperparameters Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)

| 超参数 | 建议 |
|--------|------|
| 学习率 | 标准 LoRA/QLoRA：`2e-4`；强化学习（DPO/GRPO）：`5e-6`；全参数微调：更低 |
| 训练轮数 | 避免过多轮数以防止过拟合 |
| `r` 值 | 从 8-16 开始，复杂任务可提高到 256 |
| `target_modules` | 推荐覆盖所有线性层以获得最佳效果 |

---

## 5. 总结

- **LoRA 可以在使用 4 倍更少显存的情况下达到全参数微调的效果**
- **target_modules 的选择比 rank 值更关键** — 覆盖所有线性层效果显著优于仅覆盖 Attention 层
- QLoRA（4-bit）与标准 LoRA（8-bit）在生成质量上无显著差异
- Hugging Face 的 TRL + PEFT + Transformers 生态提供了开箱即用的微调工具链

---

## 🔗 参考资料

- [How to Fine-Tune LLMs in 2024 with Hugging Face - Philschmid](https://www.philschmid.de/fine-tune-llms-in-2024-with-trl)
- [Efficient Fine-Tuning with LoRA for LLMs - Databricks Blog](https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms)
- [LoRA Hyperparameters Guide - Unsloth](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- [Implementing LoRA From Scratch - Daily Dose of Data Science](https://www.dailydoseofds.com/implementing-lora-from-scratch-for-fine-tuning-llms)
- [A Beginners Guide to Fine Tuning LLM Using LoRA - Zohaib.me](https://zohaib.me/a-beginners-guide-to-fine-tuning-llm-using-lora)
