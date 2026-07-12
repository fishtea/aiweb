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

## 2026 年生态概览：模型推荐与工具对比

2026 年本地 LLM 生态已高度成熟，参考 [SegmentFault 选型指南](https://segmentfault.com/a/1190000047650440) 和 [Pinggy 2026 工具排行](https://pinggy.io/blog/top_5_local_llm_tools_and_models)：

### 2026 年 Ollama 关键数据

- **GitHub Stars**：165k+（截至 2026 年 3 月），40,000+ 社区集成
- **开发者用户**：890 万+ 活跃开发者
- **融资里程碑**：累计融资 $8,800 万（Benchmark、Theory Ventures、8VC、Y Combinator）
- **模型库**：200+ 模型，涵盖 Llama 4、Qwen 3.5、DeepSeek-R1/V3、Gemma 4、Kimi K2.6、GPT-OSS 等全部主流开源模型
- **新能力**：原生 `ollama launch kimi` 命令支持 Kimi Agent 工作流；MLX 优化大幅提升 Apple Silicon 推理速度
- **版本迭代**：约每两周一次更新，v0.17.x 系列（2026年3月）

### 2026 年本地 Agent 任务模型推荐（OpenClaw 社区验证）

| 推荐优先级 | 模型 | 优势 | 拉取命令 |
|-----------|------|------|----------|
| ⭐ 首推 | **Qwen3-Coder:32B** | 工具调用稳定性最佳，中文顶级，推理连贯 | `ollama pull qwen3-coder:32b` |
| ⭐ 高性价比 | **GLM-4.7-Flash** | 30B 级中工具调用精度最高，"比同级 Qwen 更听话" | `ollama pull glm-4.7-flash` |
| Agent 专用 | **GPT-OSS:20B** | OpenAI 首个开源模型，Agent 场景优化 | `ollama pull gpt-oss:20b` |
| 通用标杆 | **Llama 3.3:70B** | Meta SOTA，通用性极强（需 48GB+ VRAM） | `ollama pull llama3.3:70b` |
| 推理编码 | **DeepSeek-R1:32B** | 逻辑推理 + 编码专项 | `ollama pull deepseek-r1:32b` |

### 2026 年本地 LLM 工具生态对比

| 工具 | 定位 | 界面 | 适用人群 | 亮点 |
|------|------|------|----------|------|
| **Ollama** | 命令行 + REST API | CLI | 开发者/工程师 | 200+ 模型，OpenAI 兼容 API，165k Stars |
| **LM Studio** | 图形界面 | GUI | 非技术用户 | 内置模型搜索，可视化参数调优 |
| **text-generation-webui** | 功能丰富的 Web UI | Web | 高级用户 | 支持 GGUF/GPTQ/AWQ，插件扩展 |
| **GPT4All** | 桌面应用 | Desktop | 入门用户 | 开箱即用，预配置模型 |
| **Jan** | 离线 ChatGPT 替代 | GUI | 普通用户 | 100% 离线，Cortex 引擎 |
| **LocalAI** | OpenAI API 替代 | REST API | DevOps/后端 | Docker 原生，多架构支持 |

### 硬件选择建议

| 显存/内存 | 推荐模型 | 体验评价 |
|-----------|---------|---------|
| 8–16GB | qwen3-coder:14b / glm-4.7-flash | 勉强可用，需优化 prompt |
| 24–32GB | qwen3-coder:32b / glm-4.7 | **"甜蜜点"**，性能与资源消耗最佳平衡 |
| 48GB+ | llama3.3:70b / qwen3:72b | 通用性顶级，接近闭源模型水平 |
| Apple Silicon (M1 Max+) | Qwen / GLM 系列 | 对 Apple Silicon 优化优秀 |

> **结论**：2026 年 Ollama 仍是本地 LLM 的事实标准。对 Agent 任务，Qwen3-Coder 和 GLM-4.7-Flash 是性价比最高的选择。如需图形界面，LM Studio 是首选补充。

### 参考来源

- [Ollama 选型指南：本地大模型运行工具全面解析（2026）— SegmentFault](https://segmentfault.com/a/1190000047650440)
- [Top 5 Local LLM Tools and Models in 2026 — Pinggy](https://pinggy.io/blog/top_5_local_llm_tools_and_models)
- [2026 年 OpenClaw 最佳 Ollama 本地模型推荐 — CSDN](https://aicoding.csdn.net/6a23e6b610ee7a33f278ab72.html)
- [不想数据上传云端？2026年本地部署AI大模型完全指南 — 知乎](https://zhuanlan.zhihu.com/p/2015729095867138141)

### v0.31.2: 稳定性增强与引擎更新 (2026年7月6日)

2026年7月6日，Ollama 发布 **v0.31.2**，这是在 v0.31.1 重大加速更新（Gemma 4 MTP Apple Silicon ~90% 提升）之后的稳定性补丁。

**关键变更：**

| 变更 | 说明 |
|------|------|
| **老 GPU Flash Attention 支持** | 计算能力 6.x（Pascal 架构，如 GTX 1080/Titan Xp）的 NVIDIA GPU 现在可启用 Flash Attention |
| **iGPU 视觉模型卸载** | 集成显卡可通过填充（padding）将视觉模型适配到可用显存，降低入门门槛 |
| **思考模型结构化输出修复** | 当思考（thinking）被禁用时，结构化输出现在正常工作 |
| **GGUF 模型创建加固** | 增强 GGUF 模型文件创建的健壮性 |
| **Claude Code 遥测默认关闭** | `ollama launch` 启动 Claude Code 时默认禁用遥测 |
| **非 UTF-8 路径修复** | 修复在含非 UTF-8 字符路径上加载模型的问题 |
| **MLX + llama.cpp 引擎更新** | 同步上游最新优化 |

> 这是一个典型的"稳定性版本"——在 v0.31.1 大胆的性能突破之后，v0.31.2 专注于边缘场景修复和引擎同步，为下一步功能突破铺路。

### 版本演进总览

| 版本 | 日期 | 关键变化 |
|------|------|---------|
| v0.30.11 | 6月25日 | `ollama launch` 支持 Claude Code/openCode 自动安装；Vulkan 混合显卡修复 |
| v0.30.12-rc0 | 6月29日 | 工具调用 JSON 解析增强；MLX 依赖更新 |
| v0.31.1 | 6月30日 | Gemma 4 MTP Apple Silicon 加速 ~90%；MLX + llama.cpp 引擎更新 |
| **v0.31.2** | **7月6日** | **Flash Attention 老 GPU 兼容；iGPU 视觉卸载；Claude Code 遥测关闭** |

### 参考来源

**多 Token 预测（MTP）自动调优：**

- Ollama 利用 Gemma 4 原生的多 token 预测能力，在 Apple Silicon 上自动调优草稿 token 数量（无需任何配置）。
- 在编程 Agent 基准测试中，**tokens/秒生成速度平均提升约 90%**，且不改变模型输出质量。
- 默认开启，对用户完全透明。

**MLX 引擎更新：**

- 收紧 Gemma 4 MoE 模型加载流程
- 更新至最新 MLX 版本，新增小批量矩阵乘法内核
- llama.cpp 后端更新至 build 9840
- 统一并调优推测解码（speculative decoding）在 MLX runner 中的行为

### 参考来源
- [Ollama v0.31.2 Release Notes](https://github.com/ollama/ollama/releases/tag/v0.31.2)
- [Ollama v0.31.1 Release Notes](https://github.com/ollama/ollama/releases/tag/v0.31.1)
- [Ollama 官方博客](https://ollama.com/blog)
- [Ollama 选型指南：本地大模型运行工具全面解析（2026） — SegmentFault](https://segmentfault.com/a/1190000047650440)
- [Top 5 Local LLM Tools and Models in 2026 — Pinggy](https://pinggy.io/blog/top_5_local_llm_tools_and_models)
- [2026 年 OpenClaw 最佳 Ollama 本地模型推荐 — CSDN](https://aicoding.csdn.net/6a23e6b610ee7a33f278ab72.html)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-12 05:04:02*
