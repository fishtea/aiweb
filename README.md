# AI 学习路径导航

AI 学习路径导航是一个基于 VitePress 构建、部署在 Vercel 的中文 AI 学习知识库网站。项目把 AI 入门、进阶实践、高级专题、主流模型、开发工具和 AI Agent 实战内容整理成结构化文档，适合按学习路线查阅，也适合通过站内搜索快速定位知识点。

站点内容以 `docs/` 目录中的 Markdown 文档为核心，由 VitePress 生成静态网站。项目包含资源采集、候选资料入库、中文整理状态渲染、更新报告和文档体检脚本。采集结果不会直接作为站外链接列表发布到教程页。

## 内容覆盖

- 初级知识：AI 学习路线图、人工智能入门、数学基础、Python 与数据处理、机器学习、深度学习、NLP、计算机视觉、生成式 AI、大语言模型、提示词入门、AI 伦理安全与隐私。
- 进阶学习：模型微调、RAG 检索增强、Agent 智能体、提示词工程、模型评估、Embedding 与向量数据库、LLM 应用架构。
- 高级知识：模型训练与优化、AI 安全与对齐、多模态模型、模型架构研究、数据工程与合成数据。
- 模型专区：GPT、Claude、LLaMA、DeepSeek、Gemini、Qwen、Stable Diffusion、Mixtral、开源模型部署选型。
- 工具专区：LangChain、LlamaIndex、AutoGPT、ComfyUI、vLLM、Hugging Face、PyTorch、TensorFlow、Ollama、部署运维、GitHub 热门项目。
- AI Agent 实践：函数调用 Agent、RAG Agent 实战、多 Agent 协作、Agent 评估与可观测性、实际应用案例。
- 知识库：使用指南、内容治理与采集规划、更新报告、文档体检报告。

## 项目结构

```text
.
├── docs/                         # VitePress 文档源目录
│   ├── index.md                  # 网站首页
│   ├── .vitepress/
│   │   ├── config.mts            # VitePress 配置、导航、侧边栏、搜索、页脚
│   │   └── theme/                # 自定义主题入口与样式
│   ├── assets/                   # 文档资源
│   ├── public/                   # 静态资源，例如 logo.svg
│   ├── 初级知识/                 # 入门学习路径与基础知识
│   ├── 进阶学习/                 # RAG、Agent、微调、评估等进阶主题
│   ├── 高级知识/                 # 训练优化、安全对齐、多模态、架构研究等高级主题
│   ├── 模型专区/                 # 主流模型系列与开源模型部署选型
│   ├── 工具专区/                 # AI 开发工具、框架、部署与热门项目
│   ├── AIAgent实践/              # Agent 工程实践与应用案例
│   └── 知识库/                   # 使用指南、治理规划、更新和体检报告
├── data/
│   └── resources.json            # 外部学习资源数据
├── scripts/                      # 内容采集、资源渲染、审计、构建和部署脚本
├── website/                      # 静态站点构建产物副本
├── .github/workflows/            # GitHub Pages 自动部署工作流
├── package.json                  # npm 脚本与 VitePress 依赖
├── package-lock.json             # npm 锁文件
├── pyproject.toml                # Python 脚本依赖配置
├── vercel.json                   # Vercel 构建配置
└── README.md
```

## docs 知识分类

```text
docs/
├── 初级知识/
│   ├── AI学习路线图/
│   ├── 人工智能入门/
│   ├── 数学基础/
│   ├── Python与数据处理基础/
│   ├── 数据与特征工程/
│   ├── 机器学习基础/
│   ├── 模型训练与评估基础/
│   ├── 深度学习入门/
│   ├── 自然语言处理基础/
│   ├── 计算机视觉基础/
│   ├── 生成式AI基础/
│   ├── 大语言模型基础/
│   ├── 提示词入门/
│   └── AI伦理安全与隐私/
├── 进阶学习/
│   ├── 模型微调技术/
│   ├── RAG检索增强/
│   ├── Agent智能体/
│   ├── 提示词工程/
│   ├── 模型评估与基准/
│   ├── Embedding与向量数据库/
│   └── LLM应用架构/
├── 高级知识/
│   ├── 模型训练与优化/
│   ├── AI安全与对齐/
│   ├── 多模态模型/
│   ├── 模型架构研究/
│   └── 数据工程与合成数据/
├── 模型专区/
│   ├── GPT系列/
│   ├── Claude系列/
│   ├── LLaMA系列/
│   ├── DeepSeek/
│   ├── Gemini系列/
│   ├── Qwen系列/
│   ├── StableDiffusion/
│   ├── Mixtral系列/
│   └── 开源模型部署选型/
├── 工具专区/
│   ├── LangChain/
│   ├── LlamaIndex/
│   ├── AutoGPT/
│   ├── ComfyUI/
│   ├── vLLM/
│   ├── HuggingFace/
│   ├── PyTorch/
│   ├── TensorFlow/
│   ├── Ollama/
│   ├── 部署运维/
│   └── GitHub热门项目/
├── AIAgent实践/
│   ├── 函数调用Agent/
│   ├── RAGAgent实战/
│   ├── 多Agent协作/
│   ├── Agent评估与可观测性/
│   └── 实际应用案例/
└── 知识库/
    ├── 内容治理与采集规划.md
    ├── 文档体检报告.md
    └── 更新报告/
```

## 技术栈

- VitePress：静态文档站点生成、导航、侧边栏、本地搜索、主题配置。
- Markdown：知识库正文内容格式。
- Vercel：静态网站构建与部署平台。
- Node.js / npm：依赖安装、本地开发、站点构建。
- Python：资源采集、资源渲染、文档审计和部署辅助脚本。

## 本地运行

安装依赖：

```bash
npm install
```

启动本地开发服务：

```bash
npm run dev
```

构建静态站点：

```bash
npm run build
```

预览构建结果：

```bash
npm run preview
```

默认构建产物目录：

```text
docs/.vitepress/dist/
```

## 部署到 Vercel

项目已通过 `vercel.json` 配置 Vercel 构建方式：

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "docs/.vitepress/dist",
  "installCommand": "npm install",
  "framework": "vitepress"
}
```

推荐部署流程：

1. 将项目推送到 GitHub 仓库。
2. 在 Vercel 中导入该仓库。
3. 确认构建命令为 `npm run build`。
4. 确认输出目录为 `docs/.vitepress/dist`。
5. 部署后，后续推送会触发 Vercel 自动构建。

也可以使用项目中的部署脚本：

```bash
python scripts/deploy.py
```

## 常用维护命令

采集候选学习资料：

```bash
python scripts/collect.py
```

重新渲染专题页中的资料整理状态区块：

```bash
python scripts/render_resources.py
```

检查文档结构与资料整理状态区块：

```bash
python scripts/audit_docs.py
```

补齐配置中定义但缺失的栏目页或专题页：

```bash
python scripts/create_index_pages.py
```

## 维护说明

- `docs/` 是网站内容源，新增或修改知识内容应优先编辑这里的 Markdown 文件。
- `docs/.vitepress/config.mts` 维护站点标题、导航、侧边栏、搜索、页脚和 GitHub 编辑入口。
- `data/resources.json` 保存采集到的外部资源数据。
- `scripts/` 中的脚本负责采集、渲染、审计和部署辅助。
- `website/` 是构建产物副本，不是主要内容源。
