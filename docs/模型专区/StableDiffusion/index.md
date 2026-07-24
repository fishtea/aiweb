# Stable Diffusion — Stability AI

> Stable Diffusion（稳定扩散）是由 Stability AI 主导开发的开源文本到图像生成模型系列。从 SD 1.5、SDXL 到 Stable Diffusion 3 / 3.5，它仍是本地可控图像工作流的重要基础。按 2026-07-06 可核验的图像模型生态，生产选型还应把 Black Forest Labs 的 FLUX.2 / FLUX.1、Google 的图像生成模型和闭源图像模型纳入对比。

---

## 模型演进

| 模型 | 发布时间 | 架构 | 参数规模 | 特点 |
|------|---------|------|---------|------|
| SD 1.0 | 2022.08 | Latent Diffusion + U-Net | ~1B | 首个开源文生图模型 |
| SD 1.5 | 2022.10 | Latent Diffusion + U-Net | ~1B | 社区最广泛采用 |
| SD 2.0 | 2022.11 | Latent Diffusion + U-Net | ~1B | 改进文本生成 |
| SDXL 1.0 | 2023.07 | Latent Diffusion + U-Net | ~3.5B | 大幅提升图像质量 |
| SD 3.0 | 2024.03 | **MMDiT** | 800M-8B | 架构转型为 Diffusion Transformer |
| SD 3.5 | 2024.10 | MMDiT | 8B | 改进版 |
| FLUX.1 | 2024.08 | Diffusion Transformer | 12B | Black Forest Labs 开发，社区新宠 |
| SD 3.5 Large Turbo | 2024.10 | MMDiT | 8B | 4 步快速生成 |
| FLUX.2 | 2026 | Flow Matching / DiT | 未公开 | BFL 2026 图像生成与编辑主线 |

### 扩散模型演进要点

| 趋势 | 说明 |
|------|------|
| 从 U-Net 到 DiT | SD3/FLUX 用 Transformer 替代 U-Net，扩展性更强 |
| Rectified Flow / Flow Matching | 更直的采样路径，更少步数即可出图 |
| 文本渲染突破 | FLUX.2、FLUX.1、Ideogram 等显著改善图中文字准确性 |
| 速度优化 | Turbo/Lightning 蒸馏版 4-8 步出图，接近实时 |
| ControlNet / IPAdapter | 精确控制构图、姿态、风格、角色一致性 |

---

## SD3 — MMDiT 架构革命

根据 [Stability AI 的 SD3 研究论文公告](https://stability.ai/news-updates/stable-diffusion-3-research-paper)：

### 核心创新：MMDiT

**Multimodal Diffusion Transformer (MMDiT)** 是 SD3 最大的架构变革：

- 从传统的 **U-Net** 架构转型为 **Diffusion Transformer (DiT)** 架构
- **两套独立的权重**分别处理图像和语言表示
- **联合序列进行注意力计算**：允许跨模态信息流动，同时保持各模态的独立空间
- 从 450M 到 8B 参数的扩展实验显示**没有饱和迹象**

### 文本编码器

SD3 使用三个文本编码器：
- **两个 CLIP 模型**：处理通用文本理解
- **一个 T5 (4.7B 参数)**：处理复杂文本理解（推理时可移除以节省内存）
  - 移除 T5：视觉美学 50% 胜率（无影响），文字遵循 46%（轻微下降），排版 38%（显著下降）

### Rectified Flow 改进

- 使用 Rectified Flow (RF) 公式
- 引入**新的轨迹采样调度**，更重视轨迹中间部分（更具挑战性的预测任务）
- Reweighted RF 变体在所有步数范围内持续提升性能

---

## 性能对比

根据 SD3 论文的人类偏好评估：

| 模型 | 提示遵循 | 排版 | 视觉美学 |
|------|---------|------|---------|
| **SD3 8B** | **最佳** | **最佳** | **最佳** |
| DALL·E 3 | 竞争 | 竞争 | 竞争 |
| Midjourney v6 | 竞争 | 较弱 | 较强 |
| Ideogram v1 | 竞争 | 竞争 | 竞争 |
| SDXL | — | — | — |

---

## FLUX.2 与 Black Forest Labs

根据 Black Forest Labs 官方文档与发布资料：

- 由原 Stability AI 核心团队（Black Forest Labs）开发
- 采用 **Flow Matching** 架构，基于 Diffusion Transformer
- FLUX.1 以 12B 参数打开高质量开源图像生成生态；FLUX.2 是 2026 需要重点评估的新主线
- 与 Midjourney、DALL·E 3 竞争

### FLUX 模型规格

| 版本 | 特点 | 许可 |
|------|------|------|
| FLUX.1 Pro | 完整版，最高质量 | 商业 |
| FLUX.1 Dev | 开源版，蒸馏得到 | 开源 |
| FLUX.1 Schnell | 极速版，4 步生成 | 开源 |
| FLUX.2 | 2026 主线，图像生成与编辑 | 商业/API 与生态实现并存 |

### 2026 选型建议

| 场景 | 推荐 |
|------|------|
| 社区资源和 LoRA 最丰富 | SD 1.5 / SDXL |
| 更高提示遵循和文字能力 | FLUX.2、SD3.5 Large、FLUX.1 Dev / Pro |
| 快速草图与低步数生成 | SD3.5 Turbo、FLUX.1 Schnell |
| 精确控制姿态、构图、角色 | SDXL / SD3.5 + ControlNet / IPAdapter / LoRA |
| 商业闭源质量对比 | Midjourney、DALL·E、Ideogram、FLUX Pro |

### FLUX.2 系列详解（2026 更新）

根据 Black Forest Labs 官方网站（bfl.ai，2026-07 访问）及 BFL 博客，FLUX.2 系列已发展为一个完整的产品家族：

| 模型 | 定位 | 关键特性 |
|------|------|---------|
| **FLUX.2** | 旗舰模型 | 多参考图像控制（Multi-Reference Control）、专业级场景一致性、产品植入与光照自适应 |
| **FLUX.2 [klein]** | 快速推理 | 亚秒级推理，生产质量不妥协，开放权重可本地运行 |
| **FLUX.2 [max]** | 极致质量 | 最高编辑一致性、世界知识最丰富、提示遵循最强 |
| **FLUX.1 Kontext** | 上下文感知 | 基于 Flow Matching 的图像生成与编辑，支持 BFL Playground |

**核心能力升级：**

- **多参考控制（Multi-Reference Control）**：支持多张参考图像统一风格或角色身份，实现批量资产生成的风格一致性。同一角色可生成数百张图片，角色身份保持一致。
- **产品植入（Products In Any Context）**：自动适应光照、透视和材质，将产品自然融入场景，光线自动适配，物理效果真实。
- **FLUX Erase（2026.06 发布）**：一键擦除任意图像元素，不留痕迹，类似 Photoshop 的生成式填充但更精准。
- **FLUX VTO（2026.05 发布）**：虚拟试穿（Virtual Try-On），支持在电商目录规模上进行服装试穿展示，BFL 已与多家零售商合作落地。

**开放生态：**

- **API 服务**：通过 docs.bfl.ai 接入，提供 Premium Quality、Ease of Use、Built for Scale 三个层级
- **开放权重**：FLUX.2 [klein] 开放权重，可在 Hugging Face 下载（black-forest-labs 组织）
- **Playground**：bfl.ai 提供免费在线试用
- **企业许可证**：SOC 2 + ISO 27001 认证，适合企业生产部署
- **Azure AI Foundry 集成**：FLUX 模型已在 Microsoft Azure 上线

**生态影响：** Martin Scorsese（马丁·斯科塞斯）于 2026 年 6 月加入 BFL 担任顾问，标志着 BFL 在影视创作领域的战略布局。BFL 已完成 3 亿美元的 B 轮融资（2025.12），估值 32.5 亿美元。

### BFL API 快速使用

```python
# 通过 BFL API 生成图像
import requests

response = requests.post(
    "https://api.bfl.ai/v1/image",
    headers={"Authorization": f"Bearer YOUR_API_KEY"},
    json={
        "model": "flux.2",
        "prompt": "A cat wearing a hat, cinematic lighting, photorealistic",
        "width": 1024,
        "height": 1024,
        "steps": 50
    }
)
print(response.json())
```

---

## 如何使用

### 本地运行 ComfyUI

ComfyUI 是最流行的 SD 工作流管理工具：

1. 安装 ComfyUI
2. 下载模型权重（SD3 / FLUX）
3. 搭建工作流

### 通过 API (Stability AI)

```python
import requests
import base64

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": f"Bearer your-api-key",
        "accept": "image/*"
    },
    files={
        "prompt": "A beautiful landscape with mountains and sunset, cinematic lighting",
        "output_format": "png"
    }
)
```

### 通过 Hugging Face

```python
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    torch_dtype=torch.float16
).to("cuda")

image = pipe("A cat wearing a hat, digital art").images[0]
image.save("cat.png")
```

---

## 优势与局限

**优势:**
- **开源生态:** 完全开源，社区活跃
- **灵活部署:** 可在消费级 GPU 运行
- **丰富的社区资源:** 数千种 LoRA、ControlNet 扩展
- **ComfyUI 工作流:** 可视化节点编辑，无限定制
- **成本低廉:** 相比 Midjourney/DALL·E，本地运行成本极低

**局限:**
- 人体结构（特别是手部）有时不正确
- 复杂提示遵循仍有局限
- 需要 GPU 才能获得合理速度
- FLUX 等更优模型需要更高硬件配置

---

---

## 2026 年图像生成生态最新进展

### FLUX.2 — 2025 年底的视觉智能革命

**Black Forest Labs**（BFL）于 **2025 年 11 月 25 日** 发布 FLUX.2，定位为"前沿视觉智能"模型。由 Stable Diffusion 原论文作者团队创立，BFL 在短短一年多内从 FLUX.1（2024 年 8 月）快速进化到 FLUX.2。

**FLUX.2 核心能力：**
- **4MP 超高清输出：** 生成和编辑可达 400 万像素，保持细节和一致性
- **多参考图控制：** 支持多张参考图，保持角色和风格一致性
- **文本渲染突破：** 准确生成图中文字，支持品牌指南、Logo 等
- **子秒级生成：** 相比 FLUX.1 显著加速
- **图像编辑：** 支持高达 4MP 的编辑，保留细节和连贯性
- **生产级工作流：** 专为实际创意工作流设计，非演示 demo

**产品线：**

| 变体 | 说明 |
|------|------|
| FLUX.2 [pro] | 生产级 API，面向 Adobe、Meta 等企业客户 |
| FLUX.2 [flex] | 灵活版 API，适合开发者和中小团队 |
| FLUX.2 [dev] | 开源权重版（开放核心），社区可自由使用和研究 |
| FLUX.2 [schnell] | 快速版，极速推理 |

### 2026 图像生成格局对比

| 模型 | 架构 | 参数量 | 生成速度 | 文字渲染 | 成本 |
|------|------|--------|---------|---------|------|
| **FLUX.2** | Flow Matching + DiT | 未公开 | 子秒级 | ⭐⭐⭐⭐⭐ | API/开源 |
| **SD 3.5 Large** | MMDiT | 8B | 中等 | ⭐⭐⭐⭐ | 开源免费 |
| **FLUX.1** | DiT | 12B | 中等 | ⭐⭐⭐⭐ | 开源免费 |
| **Midjourney v7** | 闭源 DiT | 未公开 | 快 | ⭐⭐⭐⭐ | 订阅 $30-60/月 |
| **GPT Image** | 闭源 | 未公开 | 快 | ⭐⭐⭐⭐ | API 按量计费 |

### 开源 vs 闭源 — BFL 的"开放核心"路线

Black Forest Labs 采用 **开放核心（Open Core）** 策略：
- 发布可审计、可组合的开源权重模型（FLUX.2 [dev]）
- 同时提供专业级生产 API（FLUX.2 [pro]）
- 支持社区创新，同时维持商业可持续性

这使得 BFL 成为 Stability AI 之后的"第二代"开源图像生成领导者。

### 对 Stable Diffusion 生态的影响

- **SD 3.5** 仍然是重要的开源选择，尤其适合 8B 以下硬件
- **FLUX.2** 在质量、速度和文字渲染方面全面领先，但需要更高硬件配置
- **ComfyUI** 已原生支持 FLUX.2 工作流
- **ControlNet / IP-Adapter** 等控制工具正在适配 FLUX 生态
- 实际选型建议：硬件受限用 SD 3.5，追求品质用 FLUX.2

**资料来源：**
- [FLUX.2: Frontier Visual Intelligence (BFL Official Blog)](https://bfl.ai/blog/flux-2)
- [FLUX.2 Model Page (BFL)](https://bfl.ai/models/flux-2)
- [BFL Flux vs Stable Diffusion 2026: AI Showdown](https://resource.digen.ai/black-forest-labs-flux-vs-stable-diffusion-2026/)
- [FLUX.2 and the Future of AI Image Generation in 2026](https://ropewalk.ai/blog/flux-2-ai-image-generation-2026)
- [Stable Diffusion vs Flux in 2026 — Which Model Should You Use?](https://willitrunai.com/blog/stable-diffusion-vs-flux-2026)

---

**参考资料：**
- [Stable Diffusion 3 Research Paper (Stability AI)](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Stable Diffusion 3.5 发布公告](https://stability.ai/news/introducing-stable-diffusion-3-5)
- [Black Forest Labs FLUX.1](https://blackforestlabs.ai/announcing-black-forest-labs/)
- [Black Forest Labs 官网 — FLUX.2](https://blackforestlabs.ai/)
- [BFL API 文档](https://docs.bfl.ai/)
- [BFL Hugging Face 组织](https://huggingface.co/black-forest-labs)
- [Diffusers Stable Diffusion 3 文档](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3)

---

## 2026 最新进展

### FLUX.2：Black Forest Labs 的全能图像引擎

2026 年，图像生成领域的话语权已从 Stability AI 转移到 Black Forest Labs（BFL）。BFL 由 Stable Diffusion 原始团队创立，其 FLUX 系列已成为开源图像生成的事实标准。

#### FLUX.2 Klein（2026.01）：实时图像生成与编辑

根据 [StableDiffusionTutorials 评测](https://www.stablediffusiontutorials.com/2026/01/flux2-klein.html)，FLUX.2 Klein 将文本生成图像、图像编辑和**多参考图工作流**统一到单一紧凑架构中，无需切换模型：

| 变体 | 参数量 | 许可 | 硬件需求 | 核心用法 |
|------|--------|------|---------|---------|
| FLUX.2 Klein 4B | 4B | **Apache 2.0** | RTX 3090/4070 (~13GB VRAM) | 图像编辑 + 多参考图生成 |
| FLUX.2 Klein 9B | 9B | BFL 非商用 | ~20GB VRAM | 旗舰文生图，4 步出图 |

**核心特性**：

- **实时推理**：9B 蒸馏版仅需 **4 步采样**，在 **0.5 秒内**生成质量媲美 5 倍参数量模型的结果。
- **统一架构**：文生图 + 图像编辑 + 多参考图在同一个模型中完成，无需串联多个模型。
- **8B Qwen3 文本编码器**：9B 版采用 Qwen3-8B 作为文本编码器，大幅提升提示词遵循能力。
- **ComfyUI 原生支持**：GGUF 量化版本由 Unsloth 提供，可在 8GB 显存消费卡上运行。

**工作流要点**：

- 基础版：20-50 步、CFG=4、Euler 采样器
- 蒸馏版：4 步、CFG=1、Euler 采样器，速度优先
- 提示词结构推荐：主体 → 场景 → 细节 → 光照 → 氛围（模型不会自动增强提示词）

> 来源：[Flux.2 Klein Guide](https://www.stablediffusiontutorials.com/2026/01/flux2-klein.html)、[BFL HuggingFace](https://huggingface.co/black-forest-labs)

#### FLUX.2 Pro / Kontext：专业级图像编辑

BFL 还推出了 **FLUX.2 Pro** 和 **Kontext** 系列（通过 [Replicate](https://replicate.com/collections/flux) 和 BFL API 提供）：

- **Kontext Pro/Max**：支持自然语言图像编辑——"把衬衫换成蓝色"、"改变背景为海滩"等指令直接执行。
- **多图参考**：可同时参考多张图片的风格/内容进行生成。
- **4MP 分辨率**：原生支持高分辨率输出，真实感极强。

### 2026 年图像生成生态格局

| 阵营 | 代表模型 | 定位 |
|------|---------|------|
| **Black Forest Labs** | FLUX.2 Pro / Klein / Kontext | 开源图像生成领导者，全栈覆盖 |
| **Stability AI** | SD 3.5 | 仍在使用但已退居二线 |
| **Midjourney** | V7 | 闭源，艺术品质最高 |
| **Ideogram** | 3.0 | 文字渲染最强 |
| **Google** | Imagen 系列 | 闭源，集成 Gemini 生态 |
| **OpenAI** | DALL·E 4 | 闭源，集成 ChatGPT |

**关键趋势**：

- **速度革命**：Turbo/Lightning 蒸馏 + 4 步采样成为标配，实时交互成为可能。
- **文字渲染突破**：FLUX.2、Ideogram 3.0 已能准确渲染英文文本，中文渲染仍有差距。
- **多参考图工作流**：不再局限于单图生成，多参考图引导成为专业工作流标准。
- **本地化 + 开源**：FLUX.2 Klein 4B 的 Apache 2.0 许可 + GGUF 量化，使消费级 GPU 也能运行生产级图像模型。

> 来源：[BFL 官网](https://bfl.ai/)、[StableDiffusionTutorials](https://www.stablediffusiontutorials.com/2026/01/flux2-klein.html)、[Replicate FLUX Collection](https://replicate.com/collections/flux)

---

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-25 00:09:45*
