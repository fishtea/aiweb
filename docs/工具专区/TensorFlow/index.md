# TensorFlow

> **深度学习框架的老牌劲旅，Google 出品的生产级 ML 平台**

## 概述

TensorFlow 由 Google Brain 团队于 2015 年开源，是最早被广泛采用的深度学习框架之一。TensorFlow 2.x 引入的 **Eager Execution** 和 **Keras** 高层 API 大幅降低了使用门槛，使其在工业界和学术界都拥有庞大的生态系统。

## 核心概念

### Tensor（张量）
TensorFlow 的核心数据单元，是多维数组的泛化：

| 维度 | 名称 | 示例 |
|------|------|------|
| 0 | 标量 (Scalar) | `1`, `3.14` |
| 1 | 向量 (Vector) | `[1, 2, 3]` |
| 2 | 矩阵 (Matrix) | `[[1,2],[3,4]]` |
| 3+ | 高维张量 | 图像 (H×W×C)、视频 (T×H×W×C) |

### Eager Execution（即时执行模式）
TensorFlow 2.x 默认启用，每行代码立即执行并返回结果，无需构建计算图再运行。

```python
import tensorflow as tf
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
c = tf.matmul(a, b)
print(c.numpy())  # 立即得到结果
```

### Keras API
TensorFlow 的高层 API，5 步完成模型训练：

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))
model.evaluate(x_test, y_test)
```

## 主要组件

| 组件 | 用途 |
|------|------|
| **tf.data** | 高性能数据流水线，支持并行加载和预处理 |
| **tf.keras** | 高层模型构建 API（推荐入口） |
| **tf.function** | 将 Python 函数编译为高效计算图 |
| **tf.distribute** | 分布式训练策略（MirroredStrategy、TPUStrategy） |
| **tf.lite** | 模型轻量化，部署到移动端/嵌入式设备 |
| **tf.js** | 在浏览器中运行 TensorFlow 模型 |
| **TensorBoard** | 可视化训练过程（Loss 曲线、计算图、嵌入向量） |
| **TF Hub** | 预训练模型仓库 |
| **TF Serving** | 生产级模型部署服务 |
| **TFX** | 完整 ML 生产流水线 |

## TensorFlow vs PyTorch

| 维度 | TensorFlow | PyTorch |
|------|-----------|---------|
| 发布 | 2015 (Google) | 2016 (Meta) |
| 调试 | `tf.function` 可能隐藏错误 | Pythonic，天然易调试 |
| 部署 | **TF Serving / TF Lite** 丰富 | TorchServe / ONNX |
| 移动端 | TF Lite 成熟 | 相对较弱 |
| 学术界 | 逐渐减少 | **占主导** |
| 工业界 | **Google / 大厂广泛使用** | 增长迅速 |
| 分布式 | 开箱即用 | 需要配置 |
| 动态图 | Eager Execution | 原生支持 |

## 实践指南

### 安装
```bash
pip install tensorflow  # CPU 版本
pip install tensorflow-gpu  # GPU 版本（TF < 2.10）
# TF >= 2.10 已集成 GPU 支持
```

### 学习路径
1. **入门**：Keras Sequential API → 训练简单的分类/回归模型
2. **进阶**：Functional API → 自定义层/损失函数 → tf.data 流水线
3. **高级**：分布式训练 → TF Serving 部署 → TF Lite 移动端
4. **专业**：TFX 流水线 → 自定义训练循环 → TPU 训练

### 调试技巧
- 使用 `tf.debugging.assert_*` 检查张量值
- TensorBoard 实时监控训练过程
- `tf.config.run_functions_eagerly(True)` 关闭 @tf.function 编译

## 生态系统对比

| 场景 | 推荐工具 |
|------|---------|
| 快速原型 | Keras + TensorFlow |
| 工业部署 | TF Serving + TF Lite |
| 研究实验 | PyTorch（更灵活） |
| 移动端 | TensorFlow Lite |
| 浏览器 | TensorFlow.js |
| 大规模分布式 | TensorFlow + TPU |

## 下一步

完成基础学习后，你可以：

- 学习使用 [PyTorch](../PyTorch/index.md)（另一个主流框架）
- 探索 [HuggingFace Transformers](../HuggingFace/index.md)（基于 TensorFlow/PyTorch 的高层库）
- 深入 [模型训练与优化](../../高级知识/模型训练与优化/index.md)（分布式训练策略）
- 了解 [vLLM](../vLLM/index.md)（推理优化，与 TensorFlow Serving 互补）
