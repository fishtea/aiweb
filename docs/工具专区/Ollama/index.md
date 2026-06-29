# Ollama：一条命令运行任何大模型

> 2023 年 9 月之前，在本地跑大模型是一个"折腾"的过程：
> 下载权重、装各种 Python 库、处理 CUDA 版本冲突、写推理代码……
>
> Ollama 改变了这一切。只需要两行命令：
> ```
> ollama pull llama3.1
> ollama run llama3.1
> ```

---

## 为什么 Ollama 如此重要？

Ollama 的定位：**大模型的 Docker**。

| 对比 | Docker | Ollama |
|------|--------|--------|
| 核心概念 | 容器化应用 | 容器化模型 |
| 仓库 | Docker Hub | Ollama Library |
| 拉取 | `docker pull nginx` | `ollama pull llama3.1` |
| 运行 | `docker run nginx` | `ollama run llama3.1` |
| 配置文件 | Dockerfile | Modelfile |
| 自定义 | 构建镜像 | 创建模型 |

**Ollama 解决的核心痛点**：模型格式的混乱。GGUF、SafeTensors、PyTorch、ONNX……Ollama 统一使用 GGUF 格式，底层用 llama.cpp 做推理引擎。

---

## 快速入门：5 分钟从零开始

### 安装

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 ollama.com 下载安装包
```

**安装后自动启动服务**，监听 `localhost:11434`。

### 拉取并运行模型

```bash
# 查看可用模型列表
ollama list

# 拉取模型（自动下载 + 量化）
ollama pull llama3.1:8b         # LLaMA 3.1 8B（约 4.7GB）
ollama pull qwen2.5:7b          # Qwen 2.5 7B
ollama pull deepseek-r1:7b      # DeepSeek R1 7B

# 直接运行（如果未拉取则自动下载）
ollama run llama3.1:70b         # 如果只有 24GB VRAM → 自动用 Q4 量化
```

**输入提示词后交互**，`Ctrl+D` 退出，`/help` 查看内置命令。

### 常用命令

```bash
ollama pull <model>              # 下载模型
ollama run <model>               # 运行模型（交互式）
ollama run <model> "你好"        # 单次对话
ollama list                      # 列出已下载的模型
ollama rm <model>                # 删除模型
ollama cp <src> <dst>            # 复制模型
ollama show <model>              # 查看模型详情
ollama stop <model>              # 停止运行中的模型
ollama serve                     # 只启动服务（不交互）
```

---

## 模型库导览

Ollama 官方维护的模型库：https://ollama.com/library

### 最流行的模型

| 模型 | 命令 | 大小 | 适合场景 |
|------|------|------|---------|
| **LLaMA 3.1** | `ollama run llama3.1` | 8B / 70B / 405B | 通用最强开源 |
| **Qwen 2.5** | `ollama run qwen2.5` | 0.5B-72B | 中文任务 |
| **DeepSeek R1** | `ollama run deepseek-r1` | 1.5B-70B | 数学推理 |
| **Mistral** | `ollama run mistral` | 7B | 轻量级通用 |
| **Mixtral** | `ollama run mixtral` | 8x7B / 8x22B | MoE，性价比高 |
| **Gemma 2** | `ollama run gemma2` | 2B-27B | Google 出品 |
| **Phi-3** | `ollama run phi3` | 3.8B-14B | 小模型奇迹 |
| **Llama 3.2-Vision** | `ollama run llama3.2-vision` | 11B / 90B | 多模态 |

### 社区模型

Ollama 支持从 HuggingFace 导出自定义模型：

```bash
# 从 HuggingFace GGUF 模型创建
ollama create mymodel -f ./Modelfile
```

```dockerfile
# Modelfile 示例
FROM ./qwen2.5-7b-instruct-q4_k_m.gguf
TEMPLATE """{{ .Prompt }}"""
PARAMETER temperature 0.7
PARAMETER top_p 0.9
```

---

## Modelfile 定制

Ollama 的"配置文件"是 Modelfile，类似 Dockerfile。

### 基础配置

```dockerfile
FROM llama3.1:8b                           # 基础模型
TEMPLATE "System: {{ .System }}\nUser: {{ .Prompt }}"  # 模板格式
PARAMETER temperature 0.8                  # 温度
PARAMETER top_k 40                         # Top-K 采样
PARAMETER top_p 0.9                        # Top-P 采样
PARAMETER stop "<|im_end|>"                # 停止标记
```

### 完整示例：创建中文助手

```dockerfile
FROM qwen2.5:7b

# 设置系统提示词
SYSTEM """你是中文助手，用简洁准确的中文回答问题。"""

# 调整推理参数
PARAMETER temperature 0.6
PARAMETER num_ctx 8192       # 上下文长度

# 嵌入许可证信息
LICENSE MIT
```

然后构建：

```bash
ollama create my-chinese-assistant -f ./Modelfile
ollama run my-chinese-assistant
```

---

## OpenAI 兼容 API

Ollama 启动后自动提供 OpenAI 兼容的 API 端点。

```bash
# 默认端点
http://localhost:11434/v1/chat/completions
http://localhost:11434/v1/embeddings
http://localhost:11434/v1/models
```

**用任何 OpenAI SDK 调用 Ollama**：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不验证 API Key
)

# 跟调用 GPT-4 一样
response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

**这意味着**：
- Cursor、Continue.dev、LangChain 等工具可以直接指向 Ollama
- 一键把 AI 工作流从云端切换到本地
- 不修改代码，只改 base_url

---

## Mac vs Linux vs Windows 部署

### Apple Silicon (M1/M2/M3/M4)

**这是 Ollama 最流畅的体验**。

```bash
# Mac 的优势：统一内存
# M2 Ultra (192GB) → 可以跑 LLaMA 70B (Q4)
# M3 Max (128GB)  → 可以跑 70B (Q4)
# M1 (8GB)        → 只能跑 3B 以下
```

**性能对比**（M2 Max 96GB）：
| 模型 | 量化 | 生成速度 | 能否运行 |
|------|------|---------|---------|
| Qwen 2.5 7B | Q4 | 35 t/s | ✅ |
| LLaMA 3.1 8B | Q4 | 38 t/s | ✅ |
| Qwen 2.5 72B | Q4 | 6 t/s | ✅ (96GB) |
| LLaMA 3.1 70B | Q3 | 4 t/s | ❌ (96GB 不够) |

### Linux + NVIDIA GPU

**最佳性能**。Ollama 自动使用 NVIDIA GPU（CUDA）加速。

```bash
# 确认 GPU 可用
ollama run llama3.1:8b --verbose
# 输出中会显示：llm_load_tensors: using CUDA for GPU acceleration
```

### Windows

- 原生 Windows 版本（不是 WSL）
- 自动使用 NVIDIA GPU
- 如果没有 NVIDIA GPU → 用 CPU（慢很多）

---

## 量化级别（Q4 vs Q8 等等）

Ollama 使用 GGUF 量化格式。同样的模型可以有多个量化版本：

```
量化级别  精度损失  显存节省  推荐场景
q8_0     ~0%      ~50%     最大质量，大显存
q6_K     ~1%      ~55%     质量敏感场景
q5_K_M   ~2%      ~60%     质量/速度平衡（推荐）
q4_K_M   ~3%      ~70%     质量/显存平衡（最常用）
q4_0     ~5%      ~72%     快速测试
q3_K_M   ~8%      ~78%     显存紧张时使用
q2_K     ~15%     ~83%     极限节省
```

**经验法则**：
- 8B 模型：Q4_K_M（~4.7GB）在 8GB 显存设备上流畅运行
- 70B 模型：Q4_K_M（~41GB）需要 2×24GB 或 1×48GB 专业卡
- 默认选择 Q4_K_M，质量损失约 3%，显存节省 70%

---

## 什么时候用 Ollama？

### ✅ 适合的场景

- 个人学习、实验、开发调试
- 需要离线/本地运行的场景
- 不想折腾 GPU 环境配置
- 想一条命令尝试各种模型
- 隐私敏感（数据不出本地）

### ❌ 不适合的场景

- 生产环境高并发（vLLM 更高效）
- 需要自定义推理优化
- 多 GPU 复杂部署
- 超过 70B 的大模型

---

> **一句话总结**：Ollama 是大模型领域的"门把手"——门槛最低的上手方式。对于个人开发者、研究者和爱好者来说，它是"在本地跑大模型"的最简单方案。对于生产环境，请用 vLLM。
