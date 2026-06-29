# AI 学习路径导航

一个基于 VitePress 的中文 AI 学习资料站点。项目会把 AI 教程、模型资料、工具指南和 Agent 实践内容整理到 `docs/`，并支持本地预览、静态构建、资源采集、GitHub Pages 部署和 Vercel 部署。

## 网站功能

- 中文 AI 学习路径首页：提供入门、应用、工程等推荐学习路线。
- 分类导航：覆盖初级知识、进阶学习、高级知识、模型专区、工具专区、AI Agent 实践、知识库指南。
- 本地全文搜索：使用 VitePress local search，可在站内检索文档内容。
- 侧边栏目录：在 `docs/.vitepress/config.mts` 中维护导航和栏目结构。
- 最后更新时间：启用 VitePress `lastUpdated`，文档页展示最近更新时间。
- GitHub 编辑入口：文档页支持跳转到 GitHub 编辑对应页面。
- 自定义主题样式：`docs/.vitepress/theme/style.css` 优化首页、卡片、文章、表格、暗色模式和移动端布局。
- 自动更新内容承载：采集脚本会向各分类文档中的 `<!-- RESOURCES_START -->` 与 `<!-- RESOURCES_END -->` 之间追加资源。

## 内容结构

```text
docs/
  index.md                         # 首页
  知识库/                           # 知识库指南
  初级知识/                         # AI、机器学习、深度学习、LLM 基础
  进阶学习/                         # 微调、RAG、Agent、提示词、评估等
  高级知识/                         # 训练优化、安全对齐、多模态、架构等
  模型专区/                         # GPT、Claude、LLaMA、DeepSeek、Gemini、Qwen 等
  工具专区/                         # LangChain、ComfyUI、vLLM、Hugging Face、PyTorch 等
  AIAgent实践/                      # 函数调用、RAG Agent、多 Agent、可观测性等实践
  .vitepress/config.mts             # VitePress 站点配置
  .vitepress/theme/                 # 自定义主题入口与样式
```

## 常用命令

```bash
npm install
npm run dev
npm run build
npm run preview
```

- `npm run dev`：启动 VitePress 本地开发服务，默认监听 `0.0.0.0`。
- `npm run build`：构建静态站点到 `docs/.vitepress/dist/`。
- `npm run preview`：预览已构建的静态站点。

## 脚本说明

| 脚本 | 功能 | 典型用途 |
| --- | --- | --- |
| `scripts/collect.py` | 按预设分类和关键词搜索 AI 学习资源，去重、翻译英文标题/摘要，并追加到对应 `docs/` 分类页。 | 每日内容采集、自动补充资源列表。 |
| `scripts/create_index_pages.py` | 根据内置分类结构批量生成分类首页和子分类 `index.md` 模板。 | 初始化或重建文档分类页。注意会覆盖对应索引页。 |
| `scripts/build.sh` | 执行 `npm run build`，并把 `docs/.vitepress/dist/` 同步到 `website/`。 | 生成可直接托管的静态产物副本。 |
| `scripts/deploy.sh` | 串联采集、构建、同步、Vercel 部署、Git 提交和推送。 | 完整的一键更新发布流程。 |
| `scripts/deploy.py` | 使用 Vercel API 上传 `docs/.vitepress/dist/`，等待部署就绪，并分配 `aiweb-lemon.vercel.app` 别名。 | 本机或自动任务直接部署到 Vercel。 |
| `scripts/vercel_deploy.py` | 从环境变量读取 `VERCEL_TOKEN`，使用 Vercel API 部署构建产物。 | GitHub Actions 或 CI 环境部署到 Vercel。 |
| `scripts/deploy_vercel.py` | 从 `/tmp/vercel_token.txt` 读取 token，部署 `~/aiweb/docs/.vitepress/dist`。 | 旧版或特定机器路径的 Vercel 部署脚本。 |
| `scripts/github_push.py` | 验证 GitHub 仓库权限，配置凭据并推送 `master` 分支。 | 旧版自动推送脚本。 |

## 网站更新流程

### 1. 更新或新增文档

在 `docs/` 下按栏目新增或编辑 `index.md`。如果新增栏目，需要同步更新：

- `docs/.vitepress/config.mts` 的 `nav`
- `docs/.vitepress/config.mts` 的 `sidebar`
- 首页 `docs/index.md` 中的入口、统计或最新更新记录

### 2. 自动采集资源

```bash
python scripts/collect.py
```

采集脚本会：

- 根据 `CATEGORIES` 中的分类、子分类、搜索关键词执行搜索。
- 用 URL 归一化和已有链接扫描做去重。
- 对英文标题和摘要做中文翻译。
- 将新资源追加到对应专题页的资源列表标记区间。
- 更新专题页中的最后更新时间。

如果要调整采集方向，修改 `scripts/collect.py` 里的 `CATEGORIES`。

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
- `pyproject.toml`：Python 项目信息，当前未声明额外依赖。
- `.github/workflows/deploy.yml`：GitHub Pages 自动构建部署流程。

## 维护注意事项

- `scripts/create_index_pages.py` 会覆盖分类页和子分类页，运行前应确认是否需要保留已有内容。
- 部分旧部署脚本包含固定本机路径或硬编码 token，建议后续统一改为环境变量。
- `collect.py` 依赖 `ddgs` 和 `deep_translator`，但 `pyproject.toml` 当前未声明这些依赖；新环境运行采集前需要手动安装。
- `website/` 是构建产物副本，主要用于静态托管或直接预览，不是主要内容源。
- 主要内容源是 `docs/`，站点配置源是 `docs/.vitepress/`。
