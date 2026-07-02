# LlamaIndex

LlamaIndex 是面向 LLM 数据接入、索引、检索和 Agent 工作流的开发框架。它常用于把文档、数据库、API 和业务数据连接到大语言模型应用中。

## 核心能力

| 能力 | 说明 |
|------|------|
| 数据连接器 | 读取文件、网页、数据库、对象存储、协作平台和第三方系统 |
| 文档解析 | 将原始内容转换为节点，保留元数据和层级关系 |
| 索引构建 | 支持向量索引、列表索引、树索引、知识图谱等组织方式 |
| 查询引擎 | 将用户问题转换为检索、聚合、重排和生成流程 |
| Agent 工具 | 将查询引擎、函数和外部 API 暴露给 Agent 使用 |
| 评估工具 | 支持检索质量、回答质量和忠实度评估 |

## 适合场景

- 企业文档问答、知识库搜索和多源数据整合。
- 需要快速搭建 RAG 原型，并逐步替换底层向量库、模型和解析器。
- 需要把结构化数据和非结构化文档统一接入 LLM。
- 需要对检索和生成链路做可解释分析。

## 与 LangChain 的区别

| 维度 | LlamaIndex | LangChain |
|------|------------|-----------|
| 重点 | 数据接入、索引、检索和查询 | 模型编排、链、工具调用和 Agent |
| RAG 体验 | 内置抽象更集中，适合知识库场景 | 更通用，可组合能力更广 |
| 学习曲线 | 从文档索引开始较直观 | 生态庞大，需要选择合适模块 |
| 常见组合 | LlamaIndex 做数据层，LangChain 或自研服务做业务编排 | LangChain 做统一应用框架 |

两者不是非此即彼。生产系统中也可以只采用其中一部分能力，避免被框架抽象绑死。

### LlamaIndex 的演进：Workflow 与 Agent

2024-2025 年，LlamaIndex 从"RAG 框架"扩展为"Agent + 数据"框架：

- **LlamaIndex Workflow**：事件驱动的工作流引擎，用"事件 + 步骤"替代线性链，支持循环、并发和人工干预，对标 LangGraph。
- **LlamaAgents**：多 Agent 编排能力，支持 Agent 间消息传递和任务分发。
- **Agentic RAG**：把检索器封装为 Agent 工具，让模型自主决定何时检索、检索什么、是否追问，超越固定 RAG 管道。
- **LlamaParse**：高质量文档解析（PDF、表格、复杂版式），解决 RAG 的"文档摄入"难题。
- **LlamaCloud**：托管索引与解析服务，降低运维负担。

> 选型建议：以"文档知识库问答"为核心 → LlamaIndex 上手快；以"多工具 Agent 编排"为核心 → LangGraph 更成熟；两者可在数据层和编排层互补使用。

## 最小实践流程

1. 选择数据源，加载文档并保留来源元数据。
2. 设置切分策略和 Embedding 模型。
3. 选择向量库或本地索引，构建可查询索引。
4. 配置 retriever、reranker 和 response synthesizer。
5. 用真实问题测试召回片段和最终答案。
6. 接入日志、反馈和评估样例，持续改进索引策略。

## 工程注意事项

- 不要只依赖默认切分器，文档结构复杂时应自定义解析。
- 元数据要从第一天设计好，后续权限过滤和引用返回都依赖它。
- 框架示例通常省略鉴权、租户隔离、错误处理和成本控制，生产环境需要补齐。
- 对大规模文档要设计增量索引、删除重建和索引版本管理。

## 相关文档

- [RAG 检索增强](/进阶学习/RAG检索增强/)
- [Embedding 与向量数据库](/进阶学习/Embedding与向量数据库/)
- [LangChain](/工具专区/LangChain/)
- [Agent 评估与可观测性](/AIAgent实践/Agent评估与可观测性/)

---

## 2026年LlamaIndex最新进展

### LlamaCloud 更名为 LlamaParse

2026 年 2 月，LlamaIndex 宣布将其企业平台 **LlamaCloud** 更名为 **LlamaParse**，标志着产品战略从通用云平台转向以文档解析为核心的 Agent 工作流自动化。官方声明称："过去一年，我们的企业平台已演变为真正意义上的 Agent 文档处理平台，LlamaParse 是核心。更名反映了这一演进，并聚焦于我们最擅长的领域：强大的文档解析和以文档为中心的 Agent 工作流。"

### LlamaAgents Builder 新增文件上传

LlamaAgents Builder（自然语言驱动的 Agent 文档工作流构建器）现已支持**文件上传**功能。用户可以提供示例文档作为上下文，创建更贴合实际场景的应用。这意味着非开发者可以通过上传 PDF、发票、合同等文件，直接向 Builder 描述需求，自动构建定制化的文档处理 Agent。

**LlamaAgents 竞赛**同期举办：使用 LlamaParse 的 Agent 标签页构建处理杂乱 PDF、发票或监管文件的文档 Agent，最佳作品获 $200 奖金。

### AgentWorkflow：事件驱动的多 Agent 编排

LlamaIndex 推出了 **AgentWorkflow**——一个事件驱动的多 Agent 编排系统，核心特性：

- **灵活 Agent 类型**：FunctionAgent（函数式）、ReActAgent（推理-行动循环）
- **内置状态管理**：自动管理 Agent 间的状态传递和上下文
- **实时监控**：可视化工作流执行过程
- **Human-in-the-Loop**：人工审核和干预能力
- 从简单助手到复杂多 Agent 系统均可构建

### 2026年 LlamaIndex vs LangChain 定位

两个框架在 2026 年的功能已大幅趋同，但设计哲学仍截然不同：

| 维度 | LlamaIndex | LangChain |
|------|-----------|-----------|
| **核心定位** | 数据图书馆员——为模型连接私有数据 | 编排者——构建 Agent 工作流 |
| **2026 年最强项** | 高级 RAG & 数据索引（精度手术刀） | Agent 工作流 & 工具调用（瑞士军刀） |
| **编排风格** | 事件驱动（Workflows API） | 声明式/命令式（LCEL）+ 图（LangGraph） |
| **学习曲线** | 中等（聚焦数据场景） | 陡峭（抽象层次多、生态庞大） |
| **企业级能力** | LlamaParse 文档解析 + Agentic RAG | LangSmith 可观测性 + Deep Agents 长运行 |

**2026 年"高手"模式**：大部分资深开发者**不选边站**——用 LlamaIndex 做检索层（找到事实），用 LangChain/LangGraph 做编排层（决定拿事实做什么）。两者互补使用是最佳实践。

### 推荐学习路径

1. **入门**：从 LlamaIndex 开始——"Chat with PDF"场景直觉、见效快
2. **进阶/求职导向**：掌握 LangChain + LangGraph——$150k+ AI 工程岗位的核心要求
3. **三月路线**：第 1 月 LlamaIndex RAG → 第 2 月 LangChain 基础 → 第 3 月 LangGraph 深度

### 参考来源

- [LlamaIndex Newsletter 2026-02-24](https://www.llamaindex.ai/blog/llamaindex-newsletter-2026-02-24)
- [LangChain vs LlamaIndex: Which One Should You Learn in 2026?](https://medium.com/codetodeploy/langchain-vs-llamaindex-which-one-should-you-learn-in-2026-62f18aa1a66f)
- [Introducing AgentWorkflow (YouTube)](https://www.youtube.com/watch?v=MmiveeGxfX0)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-03 00:15:41*
