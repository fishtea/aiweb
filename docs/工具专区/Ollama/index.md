# Ollama

> Ollama 是一个让本地运行大语言模型变得极其简单的工具。只需一条命令，就能在个人电脑上运行各种主流开源模型。

---

## 为什么选择 Ollama？

在 Ollama 出现之前，本地运行大模型需要：

- 配置 Python 环境
- 处理各种依赖冲突
- 下载并转换模型格式
- 编写推理代码

Ollama 将这些全部封装为 **一条命令**：

```bash
ollama run llama3.1
```

---

## 快速开始

### 安装

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 https://ollama.com 下载安装包
```

### 运行模型

```bash
# 运行 LLaMA 3.1
ollama run llama3.1:8b

# 运行其他模型
ollama run qwen2.5:7b
ollama run deepseek-r1:7b
ollama run mistral
ollama run gemma2:9b
```

首次运行会自动下载模型，后续直接使用。

---

## 模型管理

### 查看已下载的模型

```bash
ollama list
```

### 拉取/更新模型

```bash
ollama pull llama3.1:70b  # 下载但不运行
ollama pull qwen2.5:72b
```

### 删除模型

```bash
ollama rm llama3.1:8b
```

---

## 支持的模型

Ollama 支持几乎所有主流开源模型：

| 模型家族 | 推荐规格 | 适用场景 |
|---------|---------|---------|
| **LLaMA 3.1** | 8B, 70B | 通用对话、英文 |
| **Qwen 2.5** | 0.5B-72B | 中文、数学、编程 |
| **DeepSeek-R1** | 7B-70B (蒸馏版) | 推理、编程 |
| **Mistral/Mixtral** | 7B, 8x7B, 8x22B | 多语言、高效推理 |
| **Gemma 2** | 2B, 9B, 27B | Google 轻量模型 |
| **Phi-3** | 3.8B, 14B | 微软小型高效模型 |
| **CodeGemma/CodeQwen** | 代码专项 | 代码生成 |
| **LLaVA** | 7B, 13B | 多模态(视觉) |

---

## API 使用

Ollama 提供兼容 OpenAI 的 HTTP API，适合集成到应用中：

### 启动服务

Ollama 安装后默认在 `http://localhost:11434` 运行 API 服务。

### 调用 API

```python
# 使用 OpenAI 兼容 API
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不验证 key
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "用 Python 写一个斐波那契数列函数"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 流式响应

```python
# 流式生成
stream = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "写一首关于秋天的诗"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## Modelfile（模型定制）

Ollama 允许通过 Modelfile 自定义模型行为：

### 创建自定义模型

```text
# Modelfile
FROM llama3.1:8b

# 设置系统提示
SYSTEM """
你是专业的 Python 编程导师。
用中文回答，给出代码示例。
"""

# 设置参数
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# 设置模板
TEMPLATE """{{ .System }}
用户: {{ .Prompt }}
助手: """
```

```bash
ollama create python-tutor -f Modelfile
ollama run python-tutor
```

### 常用 Modelfile 参数

| 参数 | 默认值 | 说明 |
|-----|-------|------|
| `temperature` | 0.8 | 随机性控制 (0-2) |
| `top_p` | 0.9 | 核采样 |
| `num_ctx` | 2048 | 上下文窗口大小 |
| `num_predict` | 128 | 最大生成 token 数 |
| `stop` | — | 停止词列表 |
| `mirostat` | 0 | 重复控制算法 |

---

## 优势

- **极简体验**：一条命令运行大模型
- **生态丰富**：支持几乎所有主流开源模型
- **OpenAI 兼容 API**：方便集成到现有应用
- **跨平台**：macOS、Linux、Windows 全支持
- **GPU 加速**：自动检测并利用 GPU
- **模型定制**：Modelfile 灵活调整模型行为
- **轻量高效**：基于 llama.cpp，资源占用少

## 局限

- **推理速度**：相比 vLLM 等专业引擎吞吐量较低
- **批量处理**：不擅长大规模批处理推理
- **高级功能缺失**：不支持分布式推理、PagedAttention 等
- **模型限制**：大模型（70B+）需要大内存，消费级硬件受限
- **并发能力**：不适合高并发生产环境

---

## 应用场景

| 场景 | 使用方式 | 推荐模型 |
|-----|---------|---------|
| **个人学习** | `ollama run` 交互 | LLaMA 3.1 8B, Qwen 2.5 7B |
| **本地开发** | API 集成到应用 | 按任务选择 |
| **离线使用** | 完全本地运行 | 小模型优先 |
| **模型实验** | Modelfile 定制 | 各种模型对比 |
| **笔记本硬件** | 8GB 内存可运行 | 7B 模型 (4bit) |

---

## 最佳实践

1. **选择合适的模型大小**：8B 模型适合日常使用，70B 需要 32GB+ 内存
2. **利用 Modelfile**：为不同任务定制专属模型
3. **管理显存**：运行大模型时关闭其他 GPU 应用
4. **使用量化版本**：更低的资源占用，几乎无质量损失
5. **API 集成**：在代码中通过 API 调用，而非直接 CLI

---

## 下一步

- 安装 Ollama 并运行 `ollama run llama3.1:8b`
- 尝试运行不同模型，比较效果
- 创建自定义 Modelfile
- 将 Ollama 集成到你的项目中
- 探索 Ollama 支持的模型库，找到最合适的模型
