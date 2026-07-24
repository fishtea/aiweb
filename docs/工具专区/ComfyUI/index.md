# ComfyUI — 图像生成工作流

> ComfyUI 是一个基于**节点式编辑器**的 AI 图像生成工具。它将 Stable Diffusion 等模型的图像生成过程可视化为可拖拽、可连接的工作流节点，为创作者提供了无与伦比的灵活性和控制力。

---

## 工具概述

| 属性 | 详情 |
|------|------|
| **开发者** | Comfyanonymous (comfyanonymous) |
| **首次发布** | 2023 年初 |
| **最新版本** | 持续更新（2025/2026 活跃） |
| **许可** | GPL-3.0 |
| **核心语言** | Python + JavaScript (Web UI) |
| **GitHub** | [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI) |

---

## 核心概念

根据 [ComfyUI 2025 入门指南](https://weirdwonderfulai.art/comfyui/getting-started-with-comfyui-in-2025) 和 [Sebastian Kamph 的 ComfyUI 教程](https://www.youtube.com/watch?v=23VkGD-4uwk)：

### 节点（Nodes）

ComfyUI 中的每个操作都是一个"节点"。常见的节点类型：

| 节点类型 | 功能 | 示例 |
|---------|------|------|
| **模型加载** | 加载 Checkpoint / LoRA | Load Checkpoint, Load LoRA |
| **输入** | 提示词、图像输入 | CLIP Text Encode, Load Image |
| **采样器** | 生成过程核心 | KSampler（控制步数、CFG、种子） |
| **潜空间处理** | VAE 编解码 | VAE Encode, VAE Decode |
| **输出** | 保存/预览结果 | Save Image, Preview Image |

### 工作流（Workflows）

工作流是节点的连接图。典型的 Text-to-Image 工作流：

```
[Checkpoint Loader] → [CLIP Text Encode (正面)]
                    → [CLIP Text Encode (负面)]
                    → [KSampler] → [VAE Decode] → [Save Image]
```

### 颜色编码

根据 Sebastian Kamph 的教程，ComfyUI 使用颜色标记数据类型：

- **粉色:** 模型权重
- **蓝色:** 潜在空间（Latent）
- **灰色:** 张量/数值数据
- **黄色:** 文本/提示词

---

## 为什么选择 ComfyUI？

对比其他图像生成工具：

| 特性 | ComfyUI | Automatic1111 WebUI | Midjourney |
|------|---------|-------------------|------------|
| 工作流可视化 | ✅ 节点式连接 | ❌ 表单式 | ❌ 封闭 |
| 灵活性 | ✅ 最高 | ⚠️ 中等 | ❌ 低 |
| 内存效率 | ✅ 极高（按需加载） | ⚠️ 中等 | N/A |
| 自定义节点 | ✅ 丰富的社区扩展 | ✅ 扩展插件 | ❌ 无 |
| 学习曲线 | ⚠️ 中等偏高 | ✅ 低 | ✅ 最低 |
| 批量处理 | ✅ 原生支持 | ✅ 支持 | ❌ 有限 |

---

## 如何开始

### 本地安装

**最低硬件要求:**
- GPU 8GB+ VRAM（推荐 12GB+）
- 支持 CUDA 的 NVIDIA 显卡

**安装方式:**

```bash
# 方式 1: 直接 Git 克隆
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
python main.py

# 方式 2: 一键安装器（推荐初学者）
# 下载 ComfyUI 一键安装包
```

安装完成后，浏览器访问 `http://127.0.0.1:8188`

### 基础工作流

1. 加载 Checkpoint 模型（从 HuggingFace 或 CivitAI 下载）
2. 添加 CLIP Text Encode 节点（正面和负面提示词）
3. 添加 KSampler 节点，设置步数（20-50）、CFG（7-10）
4. 添加 VAE Decode 和 Save Image 节点
5. 连接所有节点，点击 Queue Prompt 生成

### 云部署

使用 **RunPod** （$0.40/小时起）等云 GPU 服务部署 ComfyUI，无需本地 GPU。

---

## 自定义节点生态

ComfyUI 拥有庞大的自定义节点社区，推荐值得关注的节点包：

| 节点包 | 功能 |
|--------|------|
| **ComfyUI-Manager** | 节点包管理器（必装） |
| **WAS Node Suite** | 丰富的图像处理节点 |
| **ComfyUI-Impact-Pack** | 增强的工作流节点 |
| **Efficiency Nodes** | 简化和加速工作流 |
| **AnimateDiff** | 视频生成支持 |
| **ControlNet / IPAdapter** | 精确控制构图、姿态、角色一致性 |
| **Flux / SD3 节点包** | 新一代 DiT 模型支持 |

### 工作流设计要点

- **节点复用**：把常用子流程（如"加载模型+编码提示词"）封装成组或自定义节点，避免重复连线。
- **参数可控**：把种子、步数、CFG 设为工作流输入变量，便于批量生成和参数扫描。
- **渐进式生成**：先用低分辨率 + 少步数快速试错，确定构图后再放大精修（Hi-res fix）。
- **资源管理**：大模型按需加载，显存不足时用低显存优化节点或分块生成。
- **版本化**：工作流以 JSON 保存，纳入版本控制，便于回溯和团队共享。

---

## 优势与局限

**优势:**
- **极致灵活:** 可构建任何图像生成工作流
- **内存高效:** 仅加载工作流所需的组件
- **丰富的扩展:** 数千个社区自定义节点
- **支持多模型:** SD1.5、SDXL、SD3、FLUX、MaskGCT 等
- **可复现:** 工作流可以 .json 格式共享和导出

**局限:**
- **学习曲线较陡:** 需要理解节点连接逻辑
- **调试困难:** 工作流错误不易定位
- **UI 直观性不足:** 相比 Automatic1111 不够友好
- **节点碎片化:** 太多选择让人困惑

---

**参考资料：**
- [Getting Started with ComfyUI 2025 (WeirdWonderfulAI)](https://weirdwonderfulai.art/comfyui/getting-started-with-comfyui-in-2025)
- [ComfyUI for Beginners (Sebastian Kamph YouTube)](https://www.youtube.com/watch?v=23VkGD-4uwk)
- [ComfyUI Absolute Beginner Guide (Winbush YouTube)](https://www.youtube.com/watch?v=6dXpgL1-YdM)
- [ComfyUI Reddit Getting Started 2025](https://www.reddit.com/r/StableDiffusion/comments/1icbucd/getting_started_with_comfyui_2025)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)

---

## 2026 最新进展

### ComfyUI v0.21.1（2026年5月发布）

ComfyUI 在 2026 年 5 月 14 日发布了 **v0.21.1 稳定版**，这是一次"功能扩展 + 稳定性修复 + 生态同步"的综合性更新：

**新增伙伴节点：**
| 新节点 | 功能 |
|--------|------|
| Flux2ImageNode | Flux 模型专用图像生成节点 |
| GrokImageEditNodeV2 | 图像编辑专用节点 |
| ByteDanceSeedreamNodeV2 | 支持 DynamicCombo + Autogrow（动态下拉+自适应布局） |
| OpenAI Image | OpenAI 图像 API 集成节点 |
| Claude LLM | 语言模型节点，扩展多模态工作流组合空间 |

**新模型支持：**
- **HiDream-O1-Image**：正式加入 ComfyUI 模型生态
- 修复 HiDream-O1 的 dtype 问题，优化非 dynamic VRAM 场景的内存因子

**保存与格式兼容性：**
- 修复 safetensors 保存 FP8 格式的问题
- 新增对 **anima TE LoRA kohya 格式**的支持
- Save3D 节点扩展为支持保存顶点颜色（Vertex Colors）和纹理（Textures）

**视频与多帧工作流：**
- 修复 LTXV 视频中段多帧引导对齐问题
- "Create Video"入口移入 Essentials 标签页

**稳定性改进：**
- 回退部分破坏性变更（Breaking Changes）
- 修复 VOID 运行时错误（RuntimeError）
- LoadAudio 节点自动创建缺失的输入目录
- 抑制 WebSocket 端点的误报检查

### 视频生成：ComfyUI 的 2026 核心战场

2026 年 ComfyUI 最重要的趋势是**从图像生成全面扩展到视频生成**。当前主流的视频生成模型与推荐配置：

| 模型 | 质量 | 最大时长 | 音频 | 最低 VRAM | LoRA 支持 |
|------|------|---------|------|----------|----------|
| **Wan 2.2 14B** | ★★★★★ | ~5秒 | ❌ | 12GB (GGUF) | 丰富 |
| **LTX 2.3** | ★★★★ | ~5秒 | ✅ 同步音频 | 12GB | 有 |
| **LongCat** | ★★★★ | 无限 | ❌ | 16GB | Wan兼容 |

**Wan 2.2 14B（首选推荐）**：
- 社区公认质量最高的开源视频生成模型
- 使用 GGUF 量化：Q4 适合 12GB，Q5_K_M 适合 16GB，Q8 适合 24GB
- 推荐分辨率：960×960、784×1136、720×1264
- 速度 LoRA 可加速 5-10×（Lightning 4-step、CausVid_v2、Lightx2v）
- ⚠️ 禁用 TeaCache——会降低手部、头发和快速运动质量

**硬件真相：**
- **12GB VRAM 是基线**，8GB 在视频生成中频繁 OOM
- RTX 4060 Ti 16GB 是最佳性价比选择
- 系统 RAM 64GB 配合 **DisTorch**（让模型从 RAM 流式加载）比升级 VRAM 更具性价比
- 非 NVIDIA GPU（AMD ROCm 在 Linux 有瑕疵、Apple Silicon 不支持 Float8）目前不推荐

### 学习路径建议

1. **入门**：从 Text-to-Image 基础工作流开始 → 理解节点连接逻辑 → 使用内置模板
2. **进阶**：学习图像放大（Upscaling）→ ControlNet/IP-Adapter 精确控制 → 自定义节点安装
3. **视频**：迁移到 Wan 2.2 I2V 工作流 → 理解 GGUF 量化 → 尝试速度 LoRA 组合
4. **AI 创客**：用 LoRA 训练工具（Ostris AI Toolkit）制作一致性角色 → 利用 ComfyUI 模板库快速产出

### 2026 年后 ComfyUI 还值得学吗？

答案是**肯定的**。原因：
- **社区生态最强**：400 万+用户、60,000+ 自定义节点、新模型/新功能几乎都有对应节点
- **视频生成红利**：Wan、LTX、Seedance 等模型在 ComfyUI 中第一时间可用
- **零成本生成**：本地运行，无限生成，数据隐私安全
- **3D 扩展**：Save3D 顶点颜色/纹理、3D 纹理工作流正在成熟

### 参考来源
- [ComfyUI v0.21.1 最新版本发布 (腾讯云)](https://cloud.tencent.com/developer/article/2671337)
- [The Complete Guide to AI Video Generation 2026](https://aiimagetovideo.pro/blog/comfyui-image-to-video-2)
- [2026年后 ComfyUI 还值得学吗？(知乎)](https://zhuanlan.zhihu.com/p/2000774799509721190)
- [NVIDIA Studio: Get Started in ComfyUI w/ Max Novak](https://www.youtube.com/watch?v=tuXveeHJpDA)
- [ComfyUI AI Influencer Starter Guide 2026 (smallzero)](https://www.youtube.com/watch?v=QHw5UXLo74M)

---

## 2026年7月最新：v0.27.0 与 v0.28.0 更新

根据 [ComfyUI GitHub Releases](https://github.com/Comfy-Org/ComfyUI/releases)（**注意**：仓库已于 2026 年从 `comfyanonymous/ComfyUI` 迁移至 `Comfy-Org/ComfyUI`），2026 年 6–7 月 ComfyUI 连续发布了三个重要版本，引入了多项新模型支持和核心改进。

### v0.28.0（2026-07-15）— 量化革命 + 视频/音频 + 3D 全面扩展

#### 1. 模型量化：int8 / int4 全面支持

v0.28.0 最重要的底层改进是 **int4 和 int8 量化模型的全面支持**，大幅降低 VRAM 需求：

| 量化精度 | 适用显卡 | 效果 |
|---------|---------|------|
| **FP16**（原始） | 24GB+ | 最高质量 |
| **int8** | 16GB (v0.27 引入) | 质量基本无损，VRAM 减半 |
| **int4** | 12GB 甚至更低 (v0.28 新增) | Turing 显卡优化，黑图问题已修复 |

具体改进：
- **ConvRot int8 模型支持**（v0.27）：支持压缩旋转位置编码的 8-bit 量化模型
- **ConvRot int4 模型支持**（v0.28）：4-bit 量化支持，面向低 VRAM 显卡
- **Turing 架构优化**：修复 GTX 16xx 系列 int4 黑图问题、int8 性能回归
- **PID 1.5 模型支持**：新增对 PID（Position Interpolation Distillation）1.5 模型格式的支持
- **GQA 全注意力后端支持**：Group Query Attention 在所有注意力后端通用
- 放弃 PyTorch 2.4 支持，PyTorch 2.5+ 成为最低要求

#### 2. 视频与音频生成新纪元

| 新功能 | 说明 |
|--------|------|
| **SeedVR2**（CORE-6） | 全新视频超分辨率模型，正式加入核心支持 |
| **Seed Audio 1.0** | 字节跳动音频生成模型，可通过节点直接生成配乐/音效 |
| **Seedream 5 Pro** | 字节跳动最新图像生成模型，新增"思考开关"（Disable Thinking）widget |
| **SeeDance 2.0 4K 支持**（v0.27） | 视频生成分辨率上限提升至 4K |
| **HappyHorse 1.1**（v0.27） | 阿里巴巴新模型，提供完整的图像生成 workflow 模板 |
| **视频容错** | 解码失败的音频流不再导致工作流崩溃 |

#### 3. 3D 工作流扩展

- **Save 3D (Advanced) 节点族**（CORE-329）：支持选择合并方式（Merge Vertices）、重计算法线、应用变换、导出材质
- **FBX 输出恢复**：Tencent3DPartNode 修复 FBX 格式输出
- **Create Bounding Boxes 增强**：新增 bboxes 输入，支持批量生成包围盒

#### 4. 文本与叠加层节点

- **Text Overlay 节点**（CORE-137）：在图像上叠加文字，支持字体、颜色、位置自定义
- **Save Text Node**（CORE-176）：将文本内容保存到文件
- **文本节点保留**：原计划废弃的文本节点被撤销，保持向后兼容

#### 5. AMD ROCm 优化（v0.28）

| 改进 | 说明 |
|------|------|
| **Triton 后端默认启用** | AMD 矩阵核心 GPU 自动启用 comfy-kitchen Triton 后端 |
| **Flash Attention AMD** | 修复相关兼容性问题 |
| **FP8 激活量化** | 修复 >2D 激活的混合精度运算（AMD 贡献） |
| 暂时禁用 AMD Triton 自动启用 | 因稳定性问题后续回退 |

#### 6. 伙伴节点生态调整

| 变更 | 说明 |
|------|------|
| **移除** Ideogram V1/V2 | 旧版本节点下线 |
| **移除** StabilityAI 节点 | 从核心仓库移除 |
| **新增** sync.so sync-3 模型 | 3D 生成新伙伴 |
| **Google Gemini** 图像预览路由至正式版 | 不再使用预览版模型 |
| **Grok Image 1080p** | 分辨率提升支持 |
| **核心版本请求头** | 伙伴节点发送 ComfyUI Core 版本号，便于追踪兼容性 |

#### 7. 工程改进

- **AGENTS.md / CLAUDE.md**：为 AI 辅助开发添加项目级指引文件
- **CLA Assistant**：新增贡献者许可协议检查 CI
- **前端升级**：comfyui-frontend-package 升级至 1.45.21
- **嵌入式文档更新**：v0.5.8
- **安全修复**：修复 4 个安全漏洞（GHSA-779p-m5rp-r4h4）
- **模型目录启动参数**：`--models-directory` 允许自定义模型存放路径
- **API Base 目标**：`--comfy-api-base` 支持指向临时测试环境

### v0.27.0 亮点（2026-06-30）

- **int8 ConvRot 模型支持**（为 v0.28 的 int4 奠定基础）
- **HappyHorse 1.1** 图像生成模型支持
- **Grok Image 1080p** 分辨率
- **SeeDance 2.0 4K** 视频生成
- 工作流模板更新至 v0.10.2

### v0.26.0 亮点（2026-06-23）

- **Qwen3-VL 文本生成**：通义千问 3 视觉语言模型在 ComfyUI 中支持文生文
- **节点分类重构**（CORE-263）：节点菜单重新组织，查找更便捷
- SoniloTextToMusic 降价 50%

### ComfyUI Desktop 应用

ComfyUI 已推出独立的 **Comfy Desktop** 桌面应用（[comfy.org/download](https://comfy.org/download)），支持在本地硬件上运行，提供：
- 超过 5,000 个社区扩展，共 60,000+ 节点
- 零配置安装体验
- 自动 GPU 检测和优化

### 参考来源
- [ComfyUI v0.28.0 Release Notes](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.28.0)
- [ComfyUI v0.27.0 Release Notes](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.27.0)
- [ComfyUI v0.26.0 Release Notes](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.26.0)
- [Comfy Desktop Download](https://comfy.org/download)
- [ComfyUI Official Docs](https://docs.comfy.org/)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
