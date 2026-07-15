# LLM 应用架构

LLM 应用不是简单地把用户输入转发给模型。稳定的生产系统通常包含上下文管理、工具调用、检索、缓存、评估、权限、监控和降级策略。

## 架构分层

| 层级 | 主要职责 |
|------|----------|
| 交互层 | Web、移动端、聊天入口、IDE 插件、客服系统等用户触点 |
| 编排层 | Prompt 模板、消息状态、工具路由、Agent 循环、工作流控制 |
| 知识层 | 文档解析、Embedding、向量库、关键词索引、知识图谱和引用管理 |
| 模型层 | 商业 API、开源模型、本地推理、路由、重试、限流和成本控制 |
| 安全层 | 身份认证、权限过滤、输入输出审查、敏感信息处理 |
| 评估层 | 离线测试集、线上反馈、A/B 实验、质量指标和回归检测 |
| 运维层 | 日志、追踪、告警、缓存、队列、灰度发布和故障降级 |

## 常见模式

### Prompt 驱动应用

适合摘要、改写、分类、结构化抽取等边界清晰的任务。关键在于模板版本管理、输出格式约束、错误重试和样例覆盖。

### RAG 应用

适合企业知识库、产品问答、法规查询和技术支持。核心难点不是“能否检索”，而是文档治理、权限过滤、召回评估和引用可信度。

### 工具调用应用

适合订单查询、表单填写、代码执行、日程管理等需要外部动作的场景。必须把工具 schema、参数校验、幂等性、审计日志和人工确认设计清楚。

### Agent 工作流

适合多步骤任务、研究分析、自动化运营和复杂排障。不要让 Agent 无限制循环，应明确最大步数、失败策略、状态存储和可观察轨迹。

## 设计原则

- 先做窄任务闭环，再扩展多能力助手。
- 将 Prompt、检索、工具、模型参数都版本化。
- 对高风险动作加入确认、权限和回滚机制。
- 用结构化日志记录输入摘要、检索结果、工具调用、模型输出和用户反馈。
- 将“模型回答错误”拆成可定位的问题：需求理解、检索召回、上下文组织、推理生成、工具执行或权限控制。

## 最小生产闭环

1. 定义目标任务、成功标准和不可接受输出。
2. 准备 30 到 100 条真实样例作为初始评估集。
3. 构建最小链路：输入处理、模型调用、输出解析、错误处理。
4. 接入日志和人工反馈，记录失败案例。
5. 将高频失败归类，决定是改 Prompt、改检索、加工具、换模型还是补数据。
6. 上线灰度流量，监控质量、延迟、成本和异常率。

## 技术选型提示

| 需求 | 优先考虑 |
|------|----------|
| 快速原型 | 直接调用模型 API，少量模板和轻量日志即可 |
| 企业知识库 | RAG、权限过滤、引用返回、检索评估和数据更新流程 |
| 自动化执行 | 函数调用、工作流引擎、审计日志、人工确认 |
| 成本敏感 | 模型路由、缓存、小模型预处理、批处理和离线任务 |
| 数据敏感 | 私有化部署、脱敏、访问控制和日志最小化 |

## 相关文档

### 2026年生产实践趋势

2026年，LLM应用的架构设计从"能不能跑起来"转向"如何跑得稳、省、快"。LLMOps（大模型运维）成为独立工程领域，与传统的MLOps有显著差异。

> **核心趋势：** 生产级LLM应用的架构重心从"模型选型"转向"系统设计"——缓存、路由、可观测性、降级策略比换更大的模型更有效。

#### LLMOps与MLOps的关键区别

| 维度 | MLOps | LLMOps |
|------|-------|--------|
| 训练成本 | 数月数据准备+训练 | 微调预训练模型，快速 |
| 主要工件 | 模型权重 | Prompt模板、检索库、护栏配置 |
| 成本模型 | 高前期训练+低推理 | 低训练+高持续推理（按Token计费） |
| 监控重点 | 统计漂移、模型准确率 | 幻觉率、Prompt有效性、每次请求成本 |

**来源：** [Redis Blog - LLMOps Guide 2026](https://redis.io/blog/large-language-model-operations-guide)

#### 2026年三大核心优化技术

##### 1. 智能模型路由

将简单查询路由到廉价模型，复杂推理留给强大模型。

- **效果：** RouterBench证明多LLM路由器的质量可匹敌或超越最佳单模型，同时大幅降低推理成本
- **开销：** 路由决策仅增加5-20ms延迟
- **注意：** 安全关键型场景中，单个精心调优的模型更安全

##### 2. 语义缓存

使用向量Embedding识别语义相似的查询（如"今天天气怎么样？"和"告诉我今天的温度"）。

- **缓存命中率：** 60–85%（FAQ、文档查询等高重复场景）
- **API调用减少：** 最多68.8%（正确阈值下97%+准确率）
- **成本降低：** 最高73%
- **延迟降低：** 从~1.67s降至**0.052s**每次缓存命中（降幅96.9%）
- **架构：** 精确匹配层 → 语义层（向量Embedding）→ 阈值动态调整

##### 3. 批量处理优化

| 方案 | 原理 | 适用场景 |
|------|------|---------|
| 静态批处理 | 固定大小分组 | 离线文档处理 |
| 连续批处理 | 迭代级调度，运行时添加请求 | 实时聊天机器人 |
| 多桶批处理 | 按序列长度分组 | 吞吐量优先（提升70%） |

#### 2026年LLM应用架构参考

**来源：** [InfraSketch - LLM System Design Architecture](https://infrasketch.net/blog/llm-system-design-architecture)（2026年2月）

```
┌─────────────────────────────────────────┐
│ 交互层 (UI/Client)                       │
│ Web应用、移动端、API消费者               │
│ SS E/WebSocket 流式响应（必须）          │
├─────────────────────────────────────────┤
│ 编排层 (Orchestration)                   │
│ LangGraph / 状态机                       │
│ Prompt管理、工具路由、护栏、错误处理     │
├─────────────────────────────────────────┤
│ 模型层 (Model Layer)                     │
│ Claude/GPT-4o/Gemini/开源               │
│ Prompt缓存、模型路由、降级、重试         │
├─────────────────────────────────────────┤
│ 数据层 (Data Layer)                      │
│ 向量数据库、文档存储、对话历史           │
│ 外部知识、用户上下文、缓存               │
└─────────────────────────────────────────┘
```

**各层关键设计决策：**

**交互层：**
- 流式响应（SSE/WebSocket）是2026年的标配——用户等待时间超过2秒即流失
- 考虑多模态输出（文本+图表+代码+数据表格）

**编排层：**
- **LangGraph**成为Agent编排的主流选择，支持有状态工作流
- 护栏（Guardrails）是必要组件——输入过滤、输出校验、敏感内容检测
- 错误处理策略：重试→降级→人工转接

**模型层：**
- **路由策略**：简单查询→小模型/快模型；复杂推理→大模型
- **缓存策略**：多层级（精确→语义），FAQ场景成本降低73%
- **降级策略**：缓存降级→模型降级→静态回复→断路器

**数据层：**
- 向量数据库选型见[Embedding与向量数据库](/进阶学习/Embedding与向量数据库/)的2026年指南
- 对话历史和用户上下文需要**持久化存储**（Redis等）
- **实时数据**：考虑Web搜索/API调用补充静态知识库

#### 端到端可观测性基础设施

2026年生产级LLM应用的可观测性至少需要覆盖：
1. **按用户、按功能、按模型的Token使用和成本追踪**
2. **延迟分解**：Prompt构建→LLM推理→后处理的每个环节
3. **质量指标**：自动评估 + 人工反馈
4. **降级架构**：
   - 缓存降级：模型失败时返回语义相似的历史缓存
   - 模型降级：不同提供商/版本的备用端点
   - 静态降级：关键路径的预定义回复
   - 断路器：防止级联故障

#### 从Vibe Coding到Agentic Engineering

2026年LLM应用架构的一个核心转变是：**从"AI辅助编码"到"自主Agent工程"**。

| 维度 | Vibe Coding（2024-2025） | Agentic Engineering（2026） |
|------|-------------------------|---------------------------|
| 角色 | 人类写代码，AI补全 | AI自主写代码，人类审核 |
| 架构 | 简单API调用 | 多Agent协作、工具调用、自我修正 |
| 可靠性 | 偶发可用 | 系统化测试、评估集、回归检测 |
| 监控 | 无 | 全链路可观测、成本控制、质量指标 |

GLM-5（2026年2月）等模型已原生支持Agent工程模式，Nemotron 3等混合架构（Mamba-Transformer）正在改变推理效率范式。

**来源：**
- [Redis LLMOps Guide 2026](https://redis.io/blog/large-language-model-operations-guide)
- [InfraSketch LLM System Design Architecture](https://infrasketch.net/blog/llm-system-design-architecture)
- [a16z Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications)

---

## 可扩展 LLM 服务集成五大模式

**来源：** [5 Patterns for Scalable LLM Service Integration - Latitude](https://latitude.so/blog/5-patterns-for-scalable-llm-service-integration)

构建可扩展的 LLM 服务集成需要解决流量波动、成本控制和第三方服务连接三大挑战。以下是 2025 年实践中总结的五大模式：

| 模式 | 核心思想 | 最佳场景 | 成本效率 |
|------|---------|----------|---------|
| **混合架构** (Hybrid) | 单体 LLM 推理 + 微服务辅助 | 混合负载、敏感数据 | 高 |
| **管道工作流** (Pipeline) | 顺序独立阶段，可独立扩展 | 批处理、多步骤任务 | 高 |
| **适配器集成** (Adapter) | 包装器/转换器桥接遗留系统 | 渐进式 AI 采纳 | 中 |
| **并行化与路由** (Parallel + Routing) | 并发处理 + 动态路由到最优模型 | 高吞吐量、多样化查询 | 极高 |
| **编排器-工作者** (Orchestrator-Worker) | 集中管理 + 分布式执行 | 复杂工作流、容错 | 高 |

### 混合架构

- **工作负载分配**：本地部署处理敏感数据，云端处理非关键负载，运营成本降低最多 **35%**
- **应用场景**：美国银行使用 LLM 进行实时欺诈检测和客户更新

### 管道工作流

- **独立扩展**：每个阶段可独立扩容，支持批处理和并行任务
- **真实案例**：Uber QueryGPT 每月处理 **120 万次查询**，使用 RAG + LLM + 向量数据库管道，节省 **14 万小时/月**
- **缓存层**：阶段间缓存防止重复 LLM 调用，显著降低成本

### 适配器集成

- **桥接遗留系统**：无需大改现有架构即可增加 AI 能力
- **动态切换**：统一管理多个适配器，根据可用性和性能动态切换提供商

### 并行化与路由

- **智能路由**：Amazon Bedrock 智能 Prompt 路由降低成本最高 **30%**
- **效果数据**：动态模型路由减少 LLM 使用量 **37-46%**，简单查询延迟降低 **32-38%**，AI 处理成本降低 **39%**
- **语义路由**：使用 Embedding + 向量数据库进行基于语义的任务分类和路由

### 编排器-工作者

- **集中管理与协调**：单个编排器管理多个工作者 Agent，处理任务分解、结果聚合、错误重试
- **容错机制**：工作者失败时，编排器自动重新分配任务
- **参考框架**：LangGraph（图编排）、CrewAI（角色编排）

---

## LLM 系统开发的七种模式

**来源：** [Patterns for Building LLM-based Systems & Products - Eugene Yan](https://eugeneyan.com/writing/llm-patterns)

从"性能提升"到"成本/风险降低"的谱系中，七个关键模式共同构成了生产级 LLM 应用的完整工具链：

| 模式 | 目的 | 关键方法 |
|------|------|---------|
| **评估 (Evals)** | 测量性能，检测回归 | Eval-driven development (EDD)，LLM-as-a-Judge |
| **RAG** | 注入外部知识 | 混合检索 (BM25 + 语义)、HyDE、元数据过滤 |
| **微调 (Fine-tuning)** | 提升特定任务能力 | LoRA/QLoRA、指令微调、领域自适应 |
| **缓存 (Caching)** | 降低延迟与成本 | 语义缓存 (向量 Embedding)、精确匹配+语义两层级 |
| **护栏 (Guardrails)** | 确保输出质量与安全 | 输入过滤、输出校验、敏感内容检测 |
| **防御性 UX** | 优雅处理错误 | 降级策略、重试机制、人工转接 |
| **用户反馈闭环** | 构建数据飞轮 | 展示即反馈、隐式信号收集 |

### 评估 (Evals) — 关键模式

> "Eval 的重要性是区分仓促出垃圾和认真做产品的主要分水岭。" — HackerNews

- **MMLU**：57 个任务（数学、历史、CS、法律等）
- **LLM-as-a-Judge**：使用 GPT-4 等模型作为评估者
  - G-Eval：GPT-4 + Chain-of-Thought 评分，与人类 Spearman 相关性 0.514
  - Vicuna：GPT-4 与人类评分一致率 85%（人类之间一致率 81%）
- **注意偏差**：位置偏差、冗长偏差、自我增强偏差
- **最小评估集**：50-200 个真实查询即可检测主要回归

### 缓存 — 成本优化核心

- **语义缓存**：使用向量 Embedding 识别语义相似查询
- **缓存命中率**：60-85%（FAQ、文档查询等高重复场景）
- **API 调用减少**：最多 68.8%
- **成本降低**：最高 73%
- **延迟降低**：从 ~1.67s 降至 0.052s（降低 96.9%）

---

## 🔗 参考资料（补充）

- [5 Patterns for Scalable LLM Service Integration - Latitude](https://latitude.so/blog/5-patterns-for-scalable-llm-service-integration)
- [Patterns for Building LLM-based Systems & Products - Eugene Yan](https://eugeneyan.com/writing/llm-patterns)
- [Top 10 security architecture patterns for LLM applications - Red Hat](https://www.redhat.com/en/blog/top-10-security-architecture-patterns-llm-applications)
- [LLM System Design Architecture - InfraSketch](https://infrasketch.net/blog/llm-system-design-architecture)

---

- [提示词工程](/进阶学习/提示词工程/)
- [RAG 检索增强](/进阶学习/RAG检索增强/)
- [函数调用 Agent](/AIAgent实践/函数调用Agent/)
- [Agent 评估与可观测性](/AIAgent实践/Agent评估与可观测性/)

## LLM 推理优化：KV Cache 深度解析

**来源：** [KV Caching Explained: Optimizing Transformer Inference Efficiency - HuggingFace Blog (2025-01-31)](https://huggingface.co/blog/not-lain/kv-caching)

### KV Cache 是什么？

KV Cache（键值缓存）是 Transformer 推理中最核心的优化技术之一。在自回归生成（autoregressive generation）过程中，模型每次预测下一个 token 都需要重新计算所有已生成 token 的注意力——这导致大量重复计算。KV Cache 通过缓存已计算过的 Key 和 Value 矩阵，避免每个生成步骤都从头计算。

### 工作原理

```
Token 1: [K1, V1] → Cache: [K1, V1]
Token 2: [K2, V2] → Cache: [K1, K2], [V1, V2]
...
Token n: [Kn, Vn] → Cache: [K1, K2, ..., Kn], [V1, V2, ..., Vn]
```

每次生成新 token 时：
1. 只计算新 token 的 Query、Key、Value
2. 从缓存中取出之前所有 token 的 K、V
3. 拼接后计算注意力
4. 将新 token 的 K、V 追加到缓存

### KV Cache vs 标准推理对比

| 维度 | 标准推理 | KV Cache |
|------|---------|----------|
| 计算模式 | 每个 token 重新计算全部历史 | 复用历史，只算新 token |
| 显存使用 | 每步较低但总开销大 | 额外存储，但避免重复计算 |
| 长文本速度 | 随文本变长急剧下降 | 保持稳定 |
| 长文本适用性 | 差 | **优秀** |

### 实践中的 KV Cache

HuggingFace Transformers 默认启用 KV Cache（`use_cache=True`）。在 T4 GPU 上的基准测试显示：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('HuggingFaceTB/SmolLM2-1.7B')
model = AutoModelForCausalLM.from_pretrained('HuggingFaceTB/SmolLM2-1.7B')

tokens = tokenizer.encode("Once upon a time")
output = model.generate(tokens, max_new_tokens=100)  # use_cache=True 默认
```

可以通过 `cache_implementation` 参数选择不同的缓存策略（如 `"quantized"` 量化缓存以节省显存）。

### 关键要点

1. **每个 Transformer 层独立缓存**：不同层的注意力头有不同的表示，KV Cache 在每一层分别维护
2. **仅适用于自回归模型**：扩散模型（如图像生成）不使用此机制
3. **显存与序列长度成正比**：长序列生成时 KV Cache 可能成为显存瓶颈，催生了 Multi-Query Attention（MQA）、Grouped-Query Attention（GQA）等优化架构
4. **量化 KV Cache**：使用 FP8/INT8 存储缓存的 K、V 可以显著降低长上下文推理的显存压力

> 来源参考：[KV Caching Explained - HuggingFace Blog](https://huggingface.co/blog/not-lain/kv-caching)

---

## 2026 年 LLM 路由器架构：从单模型到智能路由

当 LLM 应用从实验阶段进入生产环境后，单一模型调用所有请求的模式迅速暴露出成本和质量问题。智能模型路由（Model Router）成为 2026 年 LLM 应用架构的关键组件。

> 核心趋势：不再用最强模型回答所有问题，而是为每类请求匹配最合适的模型——将简单查询路由到廉价模型，复杂推理留给强大模型，可降低 60-85% 的推理成本。

### 三种路由策略

| 策略 | 原理 | 适用场景 |
|------|------|---------|
| **规则路由** | 基于关键词、长度、标签等硬规则 | 边界清晰、变化少的高频场景 |
| **语义路由** | 用 Embedding 匹配查询与路由意图 | 表述多样但意图集中的场景 |
| **预测路由** | 训练模型预估"哪个模型性价比最高" | 有标注偏好数据、查询分布稳定 |

- **语义+规则互补**：语义路由作为快速通路，低于阈值的查询回退到 LLM 判断
- **预测路由效果惊人**：RouteLLM MT-Bench 基准测试中，矩阵分解路由器保留了 GPT-4 95% 的分数，但仅将 14% 的查询发送给强模型

### 语义缓存：第一次就省钱

语义缓存是比路由更优先的优化手段——如果回答已缓存，连路由都不需要走。

- **精确匹配 vs 语义匹配**：用户对话中约 31% 的查询与历史相似但完全相同的情况极为罕见，精确匹配基本无效
- **效果数据**：FAQ 场景下缓存命中率 60-85%，API 调用减少最高 68.8%，成本降低最高 73%
- **延迟对比**：缓存命中 ~0.052s vs 正常调用 ~1.67s（降幅 96.9%）

### 容错与降级

生产环境必须处理多种失败模式，而不是统一重试：

| 失败类型 | 处理策略 |
|---------|---------|
| 5xx 错误 | 即时切换 Provider |
| 429 限流 | 按 Retry-After 延迟退避 |
| 延迟升高 | 逐步转移流量 |
| 内容过滤拒绝 | 走策略修复，不重试 |
| 流式中断 | 恢复/重试该请求，不切换模型 |

**关键模式**：
- **断路器（Circuit Breaker）**：连续失败超过阈值后暂停发送请求，冷却期后恢复
- **多 Provider 故障切换**：一个 Provider 不可用时自动切换到另一个

> 来源参考：[LLM Router Architecture: Best Practices for 2026 - Redis Blog](https://redis.io/en/blog/llm-router-architecture-best-practices/)（2026年7月1日发布）

### 从 Workflow 到 Agent：Anthropic 的架构建议

Anthropic 在 2024年底发布的《Building Effective Agents》指南中给出了清晰的架构抉择框架——至今仍是业界参考标准：

- **Workflow（工作流）**：LLM 和工具通过预定义的代码路径编排，适合边界清晰、可重复的任务
- **Agent（智能体）**：LLM 动态控制自己的流程和工具使用，适合需要灵活性和模型决策的场景

**核心建议**：
1. **从最简单方案开始**：单次 LLM 调用 + 检索 + 上下文示例通常就够了
2. **Workflow 优先于 Agent**：可预测的任务先用 Workflow，只有当 Workflow 不够灵活时才用 Agent
3. **避免过度框架化**：很多模式十几行代码就能实现，直接调 API 比用框架更容易调试
4. **Agent 必须有边界**：最大步数、失败策略、人工确认、状态存储和可观察轨迹缺一不可

> 来源参考：[Building Effective Agents - Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-effective-agents)（2024年12月19日发布）

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-16 00:08:55*
