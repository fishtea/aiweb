# Stable Diffusion — Stability AI

> Stable Diffusion（稳定扩散）是由 Stability AI 主导开发的开源文本到图像生成模型系列。从 2022 年的 SD 1.0 发展到 2024 年的 SD3，Stable Diffusion 系列是开源图像生成领域的标杆。

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
| FLUX.2 | 2025.07 | Flow Matching | 12B+ | 多模态提示，更强调文本渲染 |

### 扩散模型演进要点

| 趋势 | 说明 |
|------|------|
| 从 U-Net 到 DiT | SD3/FLUX 用 Transformer 替代 U-Net，扩展性更强 |
| Rectified Flow / Flow Matching | 更直的采样路径，更少步数即可出图 |
| 文本渲染突破 | FLUX.2、Ideogram 等大幅改善图中文字准确性 |
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

## FLUX.1 — Black Forest Labs 的崛起

根据 [FLUX 架构解析 (arXiv:2507.09595)](https://arxiv.org/html/2507.09595v1)：

- 由原 Stability AI 核心团队（Black Forest Labs）开发
- 采用 **Flow Matching** 架构，基于 Diffusion Transformer
- 12B 参数，在提示遵循、图像质量和多样性上超越 SD3
- 与 Midjourney、DALL·E 3 竞争

### FLUX 模型规格

| 版本 | 特点 | 许可 |
|------|------|------|
| FLUX.1 Pro | 完整版，最高质量 | 商业 |
| FLUX.1 Dev | 开源版，蒸馏得到 | 开源 |
| FLUX.1 Schnell | 极速版，4 步生成 | 开源 |
| FLUX.2 | 升级版，2025 年发布 | — |

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

**参考资料：**
- [Stable Diffusion 3 Research Paper (Stability AI)](https://stability.ai/news-updates/stable-diffusion-3-research-paper)
- [Demystifying Flux Architecture (arXiv:2507.09595)](https://arxiv.org/html/2507.09595v1)
- [Flux vs SD3 Comparison (YouTube)](https://www.youtube.com/watch?v=hSnepsdGzdo)
- [SDXL vs Flux Comparison (Facebook)](https://www.facebook.com/groups/stablediffusion/posts/1433531040645700)
- [Diffusion Models Overview (Medium)](https://medium.com/diffusion-doodles/the-myriad-of-diffusion-models-f0907ee6cc6b)

---

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[ComfyUI 中的稳定 Diffusion 3.5 工作流程教程 |维基百科](https://comfyui-wiki.com/en/tutorial/advanced/stable-diffusion-3-5-comfyui-workflow)**
  - 来源：`comfyui-wiki.com` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # ComfyUI 中的稳定扩散 3.5 工作流程教程。 Stable Diffusion 3.5是最新的AI图像生成模型，提供多种强大的模型变体。本教程整理了以下资源，主要是关于如何在ComfyUI中使用Stable Diffusion 3.5：。 * 稳定的Diffusion 3.5 FP16版本ComfyUI相关工作流程。 * 稳定的 Diffusion 3.5 FP8 版本 ComfyUI 相关工作流程（低 VRAM 解决方案）...

- **[解锁令人惊叹的视觉效果：稳定扩散工作流程的分步指南 - ComfyUI.org](https://comfyui.org/en/stable-diffusion-workflow-guide)**
  - 来源：`comfyui.org` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - ### 工作流程。解锁令人惊叹的图像：基于 Flux.1 的文本到图像生成的分步指南。转变您的图像：SUPIR-8K 壁纸级升级分步指南。让您的图像栩栩如生：利用声波扩散和 NTCosyVoice 进行人工智能驱动的视频生成。 “释放艺术潜力：深入探讨 Flux.1 和 Florence-2 工作流程”。从脚本到屏幕：宫崎风格故事板的分步指南。通过稳定的 Cascade 和 CLIP Vision 解锁高质量图像生成。剪切变得简单：Co...

- **[稳定扩散教程 2026：10 分钟内免费制作 AI 艺术（分步）](https://aitoolranked.com/blog/stable-diffusion-tutorial)**
  - 来源：`aitoolranked.com` · 质量分：8 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # 稳定扩散教程 2026：免费 AI 图像生成 [指南]。学习安装、快速工程、模型微调以及创造令人惊叹的人工智能艺术的先进技术。 。 Stable Diffusion 是一款开源 AI 图像生成器，可根据文本提示创建图像。 3.5 版本采用具有 25 亿个参数的 MMDiT-X 架构，而 SDXL 和 SD1.5 因其广泛的模型生态系统和较低的硬件要求而仍然受欢迎。 ### 稳定扩散 3.5 有哪些新功能？ **Stable Diff...

- **[Stable Diffusion 2026：型号规格和 VRAM 硬件指南](https://aitoolsdevpro.com/ai-tools/stable-diffusion-guide)**
  - 来源：`aitoolsdevpro.com` · 质量分：8 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - # Stable Diffusion 2026：型号规格和 VRAM 硬件指南。在快速发展的生成人工智能领域，**稳定扩散**仍然是开放权重视觉合成无可争议的王者。当我们步入 2026 年时，Stability AI 和开源社区已经突破了可能的界限，从简单的文本到图像生成转变为复杂的视频工作流程、3D 资产创建和实时企业渲染。本综合指南涵盖了 2026 年 Stable Diffusion 的状态，包括最新模型 (SD4 / SDXL ...

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
