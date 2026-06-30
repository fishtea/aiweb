# Ollama — 本地 LLM 管理工具

> Ollama 是当前最流行的**本地 LLM（大语言模型）运行工具**。它以"一键运行"为设计理念，让任何人都能在自己的电脑上轻松下载、管理和运行各种开源 LLM，无需复杂的配置和昂贵的 GPU。

---

## 工具概述

| 属性 | 详情 |
|------|------|
| **开发者** | Ollama Inc. |
| **首次发布** | 2023 年 |
| **当前版本** | 持续更新（2025 活跃） |
| **许可** | MIT |
| **核心语言** | Go + C++ (llama.cpp 后端) |
| **官方网站** | [ollama.com](https://ollama.com) |
| **GitHub** | [ollama/ollama](https://github.com/ollama/ollama) |
| **平台支持** | macOS, Linux, Windows |

---

## 为什么选择 Ollama？

根据 [Tech With Tim 的 Ollama 教程](https://www.youtube.com/watch?v=UtSSMs6ObqY) 和 [SitePoint 的本地 LLM 指南](https://www.sitepoint.com/local-llms-complete-guide)：

### 核心优势

- **一键安装:** 下载 → 安装 → `ollama run` 即可使用
- **模型库丰富:** 支持 LLaMA、Mistral、Qwen、DeepSeek、Gemma 等主流模型
- **本地隐私:** 所有数据在本地处理，无需联网上传
- **零成本:** 完全免费，无 API 费用
- **OpenAI 兼容 API:** 内置 HTTP 服务，可无缝替换 OpenAI

### 与 vLLM 的对比

| 维度 | Ollama | vLLM |
|------|--------|------|
| **定位** | 个人开发/实验 | 生产级高吞吐部署 |
| **易用性** | ⭐⭐⭐⭐⭐ 极简 | ⭐⭐⭐ 中等 |
| **吞吐量** | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 顶尖 |
| **硬件需求** | 低（消费级） | 中高（服务器级） |
| **批量处理** | 有限 | 强大 |

---

## 如何开始

### 安装

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 ollama.com/download 下载安装包
```

### 运行第一个模型

```bash
# 下载并运行 LLaMA 3.1 8B
ollama run llama3.1:8b

# 其他常用模型
ollama run mistral
ollama run qwen2.5:7b
ollama run deepseek-r1:7b
ollama run gemma2:9b
```

第一次运行会自动下载模型，之后可以直接使用。

### 交互示例

```
>>> 解释一下什么是大语言模型
大语言模型（Large Language Model, LLM）是一种...
```

---

## 高级用法

### HTTP API 服务

Ollama 内置 OpenAI 兼容的 API 服务器：

```bash
# 启动 API 服务（默认端口 11434）
ollama serve
```

```python
# 像调用 OpenAI 一样调用 Ollama
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # 任何值均可
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "请用中文介绍 Ollama。"}
    ]
)

print(response.choices[0].message.content)
```

### Ollama Python 库

```bash
pip install ollama
```

```python
import ollama

response = ollama.chat(model='llama3.1:8b', messages=[
    {'role': 'user', 'content': 'Ollama 的工作原理是什么？'}
])

print(response['message']['content'])
```

### 自定义模型

```bash
# 创建自定义模型配置
ollama create mymodel -f Modelfile
# 其中 Modelfile 可指定系统提示、参数等

# Modelfile 示例:
# FROM llama3.1:8b
# SYSTEM "You are a helpful assistant that speaks Chinese."
# PARAMETER temperature 0.7
# PARAMETER top_p 0.9
```

### 与 Agent 框架集成

Ollama 的 OpenAI 兼容 API 让本地模型能无缝接入 Agent 生态：

- **LangChain / LangGraph**：用 `ChatOpenAI(base_url="http://localhost:11434/v1")` 即可替换云端模型。
- **函数调用**：Ollama 已支持工具调用（tool calling），可构建本地 Agent。
- **RAG**：配合 Chroma/Qdrant 等本地向量库，实现完全离线的知识库问答。
- **隐私场景**：医疗、法律、金融等敏感数据全程不出本机。

> 适合本地 Agent 的模型：Qwen3（思考模式可控）、Llama 3.1/4、DeepSeek-R1 蒸馏版（推理）。注意本地模型的函数调用稳定性弱于 GPT/Claude，需加强参数校验和重试。

---

## 模型管理与硬件需求

根据 [n8n 本地 LLM 指南](https://blog.n8n.io/local-llm) 和 [Ollama 模型库](https://ollama.com/library)：

### 推荐模型按硬件配置

| 硬件 | 推荐模型 | 说明 |
|------|---------|------|
| **8GB RAM / 无 GPU** | Qwen2.5-1.5B, Gemma-2B | 较慢但可用 |
| **16GB RAM / 4-6GB GPU** | LLaMA 3.1-8B, Qwen2.5-7B | 通用推理没问题 |
| **32GB RAM / 8-12GB GPU** | Mistral Nemo 12B, Gemma-9B | 更高质量 |
| **64GB RAM / 24GB GPU** | Qwen2.5-32B, Mixtral 8x7B | 专业级推理 |
| **多 GPU / 128GB+ RAM** | LLaMA 3.1-70B, Qwen2.5-72B | 接近闭源水平 |

### 常用命令

```bash
# 列出本地模型
ollama list

# 查看模型详情
ollama show llama3.1:8b

# 删除模型
ollama rm llama3.1:8b

# 复制/重命名模型
ollama cp llama3.1:8b mymodel
```

---

## 搭建 Web UI (OpenWebUI)

推荐搭配 [OpenWebUI](https://github.com/open-webui/open-webui) 使用，获得类似 ChatGPT 的界面体验：

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

---

## 优势与局限

**优势:**
- **极低的入门门槛:** 几分钟内即可运行 LLM
- **数据隐私:** 所有处理在本地完成
- **零成本:** 无需 API 费用
- **丰富的模型库:** 支持主流开源模型
- **OpenAI API 兼容:** 可无缝替换 GPT 调用

**局限:**
- **吞吐量有限:** 不适合高并发生产环境
- **依赖本地硬件:** 大模型仍需高端 GPU
- **模型格式局限:** 主要支持 GGUF 格式
- **无内置监控:** 缺少 vLLM 的详细性能指标
- **批量推理能力有限**

---

**参考资料：**
- [Ollama 官方网站](https://ollama.com)
- [Learn Ollama in 15 Minutes (Tech With Tim)](https://www.youtube.com/watch?v=UtSSMs6ObqY)
- [Complete Guide to Running LLMs Locally (SitePoint)](https://www.sitepoint.com/local-llms-complete-guide)
- [How to Run a Local LLM (n8n Blog)](https://blog.n8n.io/local-llm)
- [Install LLM Locally with Ollama (Adventures in CRE)](https://www.adventuresincre.com/how-to-install-llm-locally)
- [Getting Started with Ollama (Mistwire)](https://mistwire.com/getting-started-running-local-llms-with-ollama)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*

<!-- RESOURCES_END -->

*资源区块更新时间：2026-06-30 11:37:40*
