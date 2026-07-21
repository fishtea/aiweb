# 计算机视觉基础

计算机视觉（Computer Vision，CV）研究如何让计算机理解图像和视频。它广泛用于人脸识别、医学影像、自动驾驶、工业质检、OCR 和图像生成。

## 常见任务

| 任务 | 目标 | 示例 |
|------|------|------|
| 图像分类 | 判断整张图属于哪一类 | 猫/狗、良品/缺陷 |
| 目标检测 | 找出图中物体位置和类别 | 行人、车辆、商品 |
| 图像分割 | 给每个像素分类 | 医学病灶、道路区域 |
| OCR | 识别图片中的文字 | 发票、截图、证件 |
| 人脸识别 | 判断身份或相似度 | 门禁、相册聚类 |
| 姿态估计 | 识别人身体关键点 | 运动分析、动作识别 |
| 图像生成 | 根据文本或条件生成图像 | Stable Diffusion |

## 图像如何表示

图像本质上是数字矩阵。彩色图片通常包含 RGB 三个通道：

```text
高度 × 宽度 × 通道数
例如：224 × 224 × 3
```

深度学习模型会从像素中逐层提取边缘、纹理、形状和高级语义。

## CNN 的直觉

卷积神经网络（CNN）是视觉任务中的经典架构。

| 组件 | 作用 |
|------|------|
| 卷积层 | 提取局部特征 |
| 激活函数 | 引入非线性能力 |
| 池化层 | 降低尺寸，保留重要信息 |
| 全连接层 | 汇总特征并输出分类 |

Transformer 也已经大量用于视觉任务，但理解 CNN 仍有助于建立基础直觉。

## 数据增强

视觉模型很容易受数据规模和拍摄条件影响。数据增强可以提高泛化能力：

- 随机裁剪
- 翻转
- 旋转
- 色彩扰动
- 加噪声
- MixUp、CutMix

增强要符合业务常识。比如医学影像不能随意做会改变病灶含义的变换。

## 评估指标

| 任务 | 常见指标 |
|------|----------|
| 分类 | Accuracy、Precision、Recall、F1 |
| 检测 | mAP、IoU |
| 分割 | IoU、Dice |
| OCR | 字符准确率、字段准确率 |

视觉任务要特别重视错误样本可视化。只看平均指标，容易忽略某些关键场景失败。

## 2025-2026 最新进展

### 视觉 Transformer（ViT）成为主流

传统上 CNN 是视觉任务的默认选择，但 Vision Transformer（ViT）在 2025-2026 年已经全面进入生产环境。ViT 将图像切分为固定大小的 patch，用 Transformer 的注意力机制（Attention）建模 patch 之间的全局关系。

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| ViT（原版） | 纯 Transformer，需要大量数据预训练 | 大规模分类 |
| Swin Transformer | 分层窗口注意力，计算量更小 | 检测、分割 |
| DINOv2 | 自监督学习，无需标注 | 通用特征提取 |
| EfficientViT | 轻量高效，适合移动端 | 边缘设备部署 |

CNN 并未消失——许多最新架构采用 **CNN + Transformer 混合设计**（如 ConvNeXt V2），在速度和精度之间取得平衡。

### YOLO 和实时检测

目标检测领域 YOLO 系列持续迭代：

- **YOLOv10** / **YOLO11**：无 NMS（非极大值抑制）设计，推理速度更快
- **YOLO-World**：开放词汇检测，结合 CLIP 实现零样本目标检测
- 工业场景中 YOLO 仍然是性价比最高的选择，配合 TensorRT 或 ONNX 在边缘设备上可达实时性能

### 多模态融合

2025-2026 年最大的趋势是视觉与语言模型的深度融合：
- **LLaVA** / **LLaVA-NeXT**：语言模型接入视觉编码器，实现看图问答
- **CLIP** 和 **SigLIP**：图文对比学习，广泛用于搜索和检索
- **Florence-2**：统一视觉任务的序列到序列模型
- 多模态 API（GPT-4V/4o、Gemini、Claude 3.5）使得开发者无需自己训练模型，直接调用即可完成图像理解

### 合成数据与数据增强

高质量标注数据稀缺是视觉项目的主要瓶颈：
- **合成数据生成**：用 Unity/Unreal 等引擎渲染带精确标注的虚拟场景
- **扩散模型增强**：用 Stable Diffusion 从文字描述生成训练图像
- **CutMix / MixUp** 等增强方法结合自监督学习（SimCLR、MAE）显著降低标注需求

### 工业落地进展

计算机视觉在 2026 年已广泛应用于：
- **医学影像**：X 光、CT、病理切片辅助诊断（FDA 已批准 200+ AI 医疗设备）
- **自动驾驶**：BEV（鸟瞰图）感知 + 端到端模型成为主流方案
- **工业质检**：小样本学习和异常检测方案替代传统人工检测
- **零售与安防**：人体姿态估计、动作识别、人流密度分析

### 入门项目（2026 版）

- 用预训练模型做图像分类（HuggingFace `transformers` 一行代码）
- 用 YOLOv11 训练自定义目标检测器
- 用 CLIP 做零样本图像搜索
- 用 LLaVA 做图片问答
- 用 OpenCV + 传统方法做 OCR（用于理解基础图像处理）

### SAM 2：图像与视频分割的基础模型

根据 [SAM 2 GitHub 仓库](https://github.com/facebookresearch/sam2) 和 [Meta 官方发布博客](https://ai.meta.com/blog/segment-anything-2)：

**Segment Anything Model 2（SAM 2）** 是 Meta FAIR 团队推出的分割基础模型，将 SAM 从静态图像扩展到**视频领域**。

#### 核心创新

| 特性 | 说明 |
|------|------|
| **图像+视频统一分割** | 图像视为单帧视频，无需单独模型 |
| **流式记忆（Streaming Memory）** | Transformer 架构 + 流式记忆实现实时视频处理 |
| **可提示交互** | 点击、框选、涂抹等方式指定分割目标 |
| **多目标跟踪** | SAM2VideoPredictor 支持多对象独立推理 |
| **模型内循环数据引擎** | 通过用户交互持续改进模型和数据 |

#### SAM 2.1（2024年9月发布）

- **改进的模型检查点**：SAM 2.1 系列（tiny / small / base_plus / large）
- **开放训练代码**：支持微调和自定义训练（`training/README.md`）
- **Web Demo 开源**：前后端完整代码均开源
- **torch.compile 支持**（2024年12月）：全模型编译，视频对象分割（VOS）推理大幅加速

#### 使用方式

```python
# 图像分割
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

checkpoint = "./checkpoints/sam2.1_hiera_large.pt"
predictor = SAM2ImagePredictor(build_sam2("configs/sam2.1/sam2.1_hiera_l.yaml", checkpoint))

with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    predictor.set_image(image)
    masks, _, _ = predictor.predict(prompts)  # 点击/框选即可
```

```python
# 视频分割与追踪
from sam2.build_sam import build_sam2_video_predictor

predictor = build_sam2_video_predictor(model_cfg, checkpoint)
with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    state = predictor.init_state(video_frames)
    # 在第一帧添加提示，自动传播到所有帧
    frame_idx, object_ids, masks = predictor.add_new_points_or_box(state, prompts)
    for frame_idx, object_ids, masks in predictor.propagate_in_video(state):
        ...  # 获取每一帧的分割结果
```

#### SA-V 数据集

SAM 2 配套发布了 **SA-V（Segment Anything Video）** 数据集——目前最大的视频分割数据集，通过模型内循环数据引擎收集，覆盖广泛的任务和视觉领域。

> SAM 2 的意义在于让「分割一切」从图像走进了视频，且延续了 SAM 的开放精神。它在视频编辑、自动驾驶感知、医学影像分析等领域有巨大潜力。

- **参考来源**：[SAM 2 GitHub](https://github.com/facebookresearch/sam2) | [SAM 2 论文](https://ai.meta.com/research/publications/sam-2-segment-anything-in-images-and-videos/) | [SAM 2 博客](https://ai.meta.com/blog/segment-anything-2)

## 2026 年 CV 关键突破深度解读

### 概述

计算机视觉市场在 2026 年预计达到 **328.8 亿美元**，到 2031 年增长至 683.8 亿美元。更重要的是，驱动增长的技术栈已发生根本性转变——从"特定任务模型"转向"通用视觉理解"，从"检测"转向"行动"。以下基于 viso.ai、Robotocist、discoverinai 等平台的最新报告整理。

> 综合来源：viso.ai, "Computer Vision Trends We're Observing in 2026", https://viso.ai/deep-learning/computer-vision-trends-2026/（2026-07-13）；Robotocist, "Computer Vision Breakthroughs of 2026", https://robotocist.com/articles/computer-vision-2026（2026-02-22）；discoverinai.com, "Computer Vision: 5 Key 2026 Trends to Watch", https://discoverinai.com/computer-vision-5-key-2026-trends-to-watch/（2026-06-04）

### 1. 视觉通用智能（VGI）：从概念到产品

**Visual General Intelligence** 是 2026 年 CV 领域最重要的突破。VGI 系统能理解任意物理环境、跨领域推理、用自然语言描述观察结果，无需为每个任务单独训练模型。viso.ai 在 2025 年初发布 VGI 白皮书并推出 Viso Now 平台后，2026 年 VGI 已从概念走向生产部署——制造业、物流、建筑等行业的实际生产环境中已在运行基于 VGI 架构的视觉系统。

**关键区别**：传统 CV 需要标注大量数据训练专用模型，VGI 只需用自然语言描述任务，系统即能理解环境并回答问题。

### 2. 自主计算机视觉（Agentic CV）：检测→行动

传统 CV 系统只做检测，产生告警后需要人工处理。**Agentic CV** 系统则能：检测安全违规 → 自动将告警路由至相关负责人 → 附带视觉证据 → 更新 EHS 系统 → 创建整改工单——全过程无需人工介入。

Gartner 预测到 2028 年，33% 的企业软件将包含 Agentic AI。CV 作为 Agentic AI 在物理世界的核心感知层，正在从"检测端点"转型为"行动起点"。

### 3. 基础模型取代任务特定模型

过去构建 CV 系统需要收集标注数据 → 训练专用模型 → 部署。2026 年，**视觉基础模型**（如 GPT-4o、Gemini 2.5 Pro、InternVL3、Qwen3-VL）经过海量视觉数据训练后，开箱即可理解几乎任何场景。

**实际影响**：以前需要数月深度学习和大量标注数据的工作，现在数分钟即可完成。对于大多数监控和智能分析场景，基础模型是更快、更便宜、更灵活的选择。不过高精度检测（如微米级公差质检）仍需专用模型。

### 4. 合成数据达到与真实数据同等的训练效果

2026 年关键进展是：生成式 AI 产出的合成数据在**模型训练效果上已与真实数据无法区分**。照片级渲染、程序化光照和角度调整、AI 生成的边缘案例，覆盖了真实数据集常遗漏的长尾情况。

discoverinai 的数据显示，合成数据可将训练数据采集成本降低约 40%。对于目标检测、缺陷识别和安全监控等应用，传统标注密集型管线已变得非必需。

### 5. Vision Transformer 成为默认架构

Vision Transformer（ViT）在 2026 年已全面成为目标检测、图像分割、深度估计和多模态推理的默认骨干网络。高效 ViT 变体（YOLO26、InternVL 系列）在边缘硬件上已达到此前云端模型的性能——这使得架构选择不再是 CV 系统设计时的关键决策点。

### 6. 3D 场景理解主流化与 Physical AI

**3D Gaussian Splatting** 技术快速成熟——从 30 秒手机视频中 1 分钟内重建完整 3D 场景。应用场景包括房地产虚拟看房、机器人环境建图、游戏/VR 内容创作。同时，**Physical AI**（物理 AI）——能感知、推理物理环境并采取行动的系统——正在从研究走向商业部署，Tesla Optimus 人形机器人已于 2026 年 1 月开始量产。

> 来源：Robotocist, "Computer Vision Breakthroughs of 2026", https://robotocist.com/articles/computer-vision-2026（2026-02-22）；viso.ai（同上）

### 7. 边缘计算成熟与语义视频智能

EU AI Act 等法规对数据跨境传输的限制推动边缘部署以 17.29% CAGR 增长。2026 年，NVIDIA Jetson、Intel 等芯片已能在边缘运行最先进的深度学习推理。

**语义视频搜索**则让用户能用自然语言对监控视频提问——无需预先配置、无需标注、无需人工观看——底层是大视觉模型与视频嵌入语义搜索的结合。

### 8. CV 学习路径建议（2026 更新）

根据 Scaler 的 2026 CV 路线图：

| 阶段 | 内容 | 时长 |
|------|------|:----:|
| 基础 | Python、线性代数、概率统计、图像处理基础 | 1-2 月 |
| 机器学习 | 监督/无监督学习、模型评估、Scikit-learn | 1 月 |
| 深度学习 | 神经网络、CNN、迁移学习、PyTorch/TensorFlow | 1-2 月 |
| 现代 CV 架构 | Vision Transformer、YOLO、图像分割 | 1 月 |
| 目标检测与跟踪 | 检测算法、跟踪算法、视频理解 | 1 月 |
| 高级主题 | 3D 视觉、生成式 CV、MLOps 部署、模型量化 | 持续 |

> 来源：Scaler, "Computer Vision Roadmap 2026", https://www.scaler.com/blog/computer-vision-roadmap/（2026-07-16）

### 参考来源

- viso.ai, "Computer Vision Trends We're Observing in 2026", https://viso.ai/deep-learning/computer-vision-trends-2026/（2026-07-13）
- Robotocist, "Computer Vision Breakthroughs of 2026", https://robotocist.com/articles/computer-vision-2026（2026-02-22）
- discoverinai.com, "Computer Vision: 5 Key 2026 Trends", https://discoverinai.com/computer-vision-5-key-2026-trends-to-watch/（2026-06-04）
- Scaler, "Computer Vision Roadmap 2026", https://www.scaler.com/blog/computer-vision-roadmap/（2026-07-16）

---

## 延伸阅读

- [深度学习入门](../深度学习入门/)
- [多模态模型](/高级知识/多模态模型/)
- [Stable Diffusion](/模型专区/StableDiffusion/)
- [HuggingFace Transformers 教程](/工具专区/HuggingFace/)

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 4 个来源域名。
- 最近采集日期：2026-07-04。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-22 00:08:01*
