# AI 学习路径导航

一个基于 VitePress 的中文 AI 学习知识库。项目目标不是简单堆积链接，而是把 AI 教程、模型资料、工具指南、Agent 实践和持续采集到的新资源，整理成有学习路径、有专题正文、有精选资源、有更新报告的可维护站点。

## 项目目标

- 建立清晰的 AI 学习路径：从初级知识到进阶应用、高级原理、模型选型、工具使用和 Agent 实践。
- 持续采集高质量外部资源：优先官方文档、论文、课程、主流开源项目和工程实践文章。
- 保持文章结构稳定：教程正文人工维护，自动采集只更新“精选资源”区块，避免页面无限追加成链接列表。
- 支持自动构建与部署：VitePress 本地预览、静态构建、GitHub Pages、Vercel 部署。

## 网站功能

- 中文 AI 学习路径首页：提供入门、应用、工程等推荐学习路线。
- 分类导航：覆盖初级知识、进阶学习、高级知识、模型专区、工具专区、AI Agent 实践、知识库指南。
- 本地全文搜索：使用 VitePress local search，可在站内检索文档内容。
- 侧边栏目录：在 `docs/.vitepress/config.mts` 中维护导航和栏目结构。
- 最后更新时间：启用 VitePress `lastUpdated`，文档页展示最近更新时间。
- GitHub 编辑入口：文档页支持跳转到 GitHub 编辑对应页面。
- 自定义主题样式：`docs/.vitepress/theme/style.css` 优化首页、卡片、文章、表格、暗色模式和移动端布局。
- 结构化资源更新：采集脚本写入 `data/resources.json`，再重建专题页中的 `<!-- RESOURCES_START -->` 与 `<!-- RESOURCES_END -->` 精选资源区块。

## 内容结构

```text
docs/
  index.md                         # 首页
  知识库/                           # 知识库指南、内容治理、更新报告
  初级知识/                         # AI、数学、Python、数据、ML、DL、LLM、提示词、安全基础
  进阶学习/                         # 提示词、Embedding、RAG、Agent、微调、评估、应用架构
  高级知识/                         # 训练优化、安全对齐、多模态、架构、数据工程
  模型专区/                         # GPT、Claude、LLaMA、DeepSeek、Gemini、Qwen、SD、开源部署
  工具专区/                         # LangChain、LlamaIndex、ComfyUI、vLLM、Hugging Face、Ollama 等
  AIAgent实践/                      # 函数调用、RAG Agent、多 Agent、Agent 评估等实践
  .vitepress/config.mts             # VitePress 站点配置
  .vitepress/theme/                 # 自定义主题入口与样式

scripts/
  content_config.py                 # 统一分类、专题、关键词和资源质量配置
  collect.py                        # 搜索、评分、去重、翻译、写入资源库
  render_resources.py               # 从资源库重建专题页精选资源区块
  create_index_pages.py             # 根据分类配置补齐缺失专题页面
  build.sh                          # 构建并同步到 website/
  deploy.sh                         # 采集、构建、部署、提交、推送

data/
  resources.json                    # 自动采集资源库，首次采集后生成
```

## 内容治理模型

本项目把“正文教程”和“外部资源”分开维护：

| 层级 | 维护方式 | 作用 |
| --- | --- | --- |
| 专题正文 | 人工维护 | 保持概念解释、实践步骤、常见误区和学习顺序稳定 |
| 精选资源 | 脚本自动生成 | 展示当前专题最相关的外部资源，数量受控 |
| 资源库 | `data/resources.json` | 保存 URL、来源、标题、摘要、分类、质量分、采集日期 |
| 更新报告 | `docs/知识库/更新报告/` | 记录每日新增了什么，便于人工复盘 |

详细规则见：[docs/知识库/内容治理与采集规划.md](docs/知识库/内容治理与采集规划.md)。

## 环境准备

Node 依赖：

```bash
npm install
```

Python 依赖：

```bash
pip install -e .
```

如果当前环境不支持 editable install，也可以直接安装脚本依赖：

```bash
pip install ddgs deep-translator
```

## 常用命令

```bash
npm run dev
npm run build
npm run preview
```

- `npm run dev`：启动 VitePress 本地开发服务，默认监听 `0.0.0.0`。
- `npm run build`：构建静态站点到 `docs/.vitepress/dist/`。
- `npm run preview`：预览已构建的静态站点。

采集与资源渲染：

```bash
python scripts/collect.py
python scripts/collect.py --category 初级知识
python scripts/collect.py --topic RAG检索增强 --max-results 10
python scripts/collect.py --no-render
python scripts/render_resources.py
```

初始化缺失专题页：

```bash
python scripts/create_index_pages.py
```

## 脚本说明

| 脚本 | 功能 | 典型用途 |
| --- | --- | --- |
| `scripts/content_config.py` | 统一维护分类、专题、描述、采集关键词、标签、可信域名、屏蔽域名和资源展示数量。 | 调整知识体系或采集方向。 |
| `scripts/collect.py` | 搜索资源，URL 归一化，跨专题去重，质量评分，标题/摘要翻译，写入 `data/resources.json`，生成更新报告。 | 每日内容采集。 |
| `scripts/render_resources.py` | 从 `data/resources.json` 重建各专题页的“精选资源”区块。 | 控制资源展示数量，保持正文结构清晰。 |
| `scripts/create_index_pages.py` | 根据统一分类结构补齐缺失的分类首页和专题 `index.md`。 | 新增栏目后初始化页面。不会覆盖已有页面。 |
| `scripts/audit_docs.py` | 检查文档缺页、未完成标记、资源区块、本地链接和统一配置覆盖情况。 | 每次批量整理文档后做体检。 |
| `scripts/build.sh` | 执行 `npm run build`，并把 `docs/.vitepress/dist/` 同步到 `website/`。 | 生成可直接托管的静态产物副本。 |
| `scripts/deploy.sh` | 串联采集、构建、同步、Vercel 部署、Git 提交和推送。 | 完整一键更新发布流程。 |
| `scripts/deploy.py` | 使用 Vercel API 上传构建产物，等待部署就绪，并分配 `aiweb-lemon.vercel.app` 别名。 | 本机或自动任务直接部署到 Vercel。 |
| `scripts/vercel_deploy.py` | 从环境变量读取 `VERCEL_TOKEN`，使用 Vercel API 部署构建产物。 | GitHub Actions 或 CI 环境部署到 Vercel。 |
| `scripts/deploy_vercel.py` | 从 `/tmp/vercel_token.txt` 读取 token，部署固定路径构建产物。 | 旧版或特定机器路径部署脚本。 |
| `scripts/github_push.py` | 验证 GitHub 仓库权限，配置凭据并推送 `master` 分支。 | 旧版自动推送脚本。 |

## 自动采集流程

```text
scripts/content_config.py
  ↓
生成搜索任务
  ↓
DuckDuckGo 搜索
  ↓
URL 归一化与屏蔽域名过滤
  ↓
来源域名、关键词、摘要长度、新鲜度评分
  ↓
英文标题/摘要翻译
  ↓
写入 data/resources.json
  ↓
生成 docs/知识库/更新报告/YYYY-MM-DD.md
  ↓
重建专题页精选资源区块
  ↓
npm run build
```

调整采集来源和质量策略时，优先修改：

- `CATEGORIES`：分类、专题、关键词、标签。
- `TRUSTED_DOMAINS`：高质量来源加权。
- `BLOCKED_DOMAINS`：低质量或不适合来源过滤。
- `RESOURCE_LIMIT_PER_TOPIC`：每个专题展示的资源数量上限。

## 网站更新流程

### 1. 更新或新增文档

在 `docs/` 下按栏目新增或编辑 `index.md`。如果新增专题，优先修改 `scripts/content_config.py`，再运行：

```bash
python scripts/create_index_pages.py
python scripts/audit_docs.py
```

如果需要让站点侧边栏出现新专题，同步更新：

- `docs/.vitepress/config.mts` 的 `sidebar`
- 首页 `docs/index.md` 的学习路径、统计或最新更新记录

### 2. 自动采集资源

```bash
python scripts/collect.py
```

采集脚本会：

- 根据 `scripts/content_config.py` 中的分类、专题和关键词执行搜索。
- 用 URL 归一化和 `data/resources.json` 做跨专题去重。
- 按来源域名、关键词匹配、摘要长度等因素做基础质量评分。
- 对英文标题和摘要做中文翻译。
- 将新资源写入 `data/resources.json`。
- 生成 `docs/知识库/更新报告/YYYY-MM-DD.md`。
- 重建各专题页中的“精选资源”区块。

### 3. 构建和本地验证

```bash
npm run build
npm run preview
```

构建产物位于：

```text
docs/.vitepress/dist/
```

如需同步一份静态文件到 `website/`：

```bash
bash scripts/build.sh
```

### 4. 发布部署

GitHub Pages 自动部署配置在 `.github/workflows/deploy.yml`：

- 推送 `master` 分支后触发。
- 安装 Node.js 20。
- 执行 `npm install` 和 `npm run build`。
- 上传 `docs/.vitepress/dist` 并部署到 GitHub Pages。

Vercel 部署可使用：

```bash
python scripts/deploy.py
```

完整自动流程可使用：

```bash
bash scripts/deploy.sh
```

该流程会执行采集、构建、部署、提交和推送。

## 配置文件

- `package.json`：定义 VitePress 开发、构建、预览命令。
- `vercel.json`：指定 Vercel 构建命令、输出目录和框架类型。
- `pyproject.toml`：Python 项目信息和采集脚本依赖。
- `.github/workflows/deploy.yml`：GitHub Pages 自动构建部署流程。
- `docs/.vitepress/config.mts`：站点导航、侧边栏、搜索、页脚和主题配置。

## 维护清单

- 正文教程应人工维护，自动采集只更新“精选资源”区块。
- `data/resources.json` 是采集资源的源数据，页面资源区块可随时由 `scripts/render_resources.py` 重建。
- 新增分类或专题时，先改 `scripts/content_config.py`，再补页面和导航。
- 每周人工浏览 `docs/知识库/更新报告/`，把真正有价值的新资料吸收到正文。
- 每次批量改文档后运行 `python scripts/audit_docs.py`，查看 `docs/知识库/文档体检报告.md`。
- 涉及模型版本、工具 API、价格、排行榜的信息，要标注更新时间并定期复查。
- 部分旧部署脚本包含固定本机路径或硬编码 token，后续建议统一改为环境变量。
- `website/` 是构建产物副本，主要用于静态托管或直接预览，不是主要内容源。
- 主要内容源是 `docs/`，站点配置源是 `docs/.vitepress/`，资源库源是 `data/resources.json`。

## 验证命令

```bash
python -m py_compile scripts/content_config.py scripts/render_resources.py scripts/collect.py scripts/create_index_pages.py
python scripts/audit_docs.py
npm run build
```
