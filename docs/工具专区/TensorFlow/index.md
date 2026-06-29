# TensorFlow

## 为什么 TensorFlow 还活着

2019 年 PyTorch 在学术界超越 TensorFlow 时，很多人以为 TF 要死了。但事实是：**TensorFlow 没死，它转型了**。

### 它的位置

PyTorch 赢了研究，TF 赢了部署：

| 场景 | 赢家 |
|------|------|
| 学术论文、快速原型 | PyTorch |
| 移动端/嵌入式 | **TensorFlow Lite** |
| 浏览器推理 | **TensorFlow.js** |
| 大规模生产部署 | **TF Serving / TFX** |
| TPU 训练 | **TensorFlow**（独家） |
| Keras 快速上手 | 平手（Keras 3 已支持多后端） |

### TensorFlow 2.x 的改变

TF 1.x 的计算图模式（先定义图再执行）让无数人弃坑。2.x 引入 Eager Execution，体验接近 PyTorch：

```python
# TF 2.x 和 PyTorch 一样即时执行
import tensorflow as tf
x = tf.constant([1, 2, 3])
print(x * 2)  # tf.Tensor([2 4 6], shape=(3,), ...)
```

### 谁在用

- **Google 全家桶**：搜索、广告、Gmail 的 ML 基础设施
- **制造业/物联网**：TF Lite 在树莓派和手机上的部署生态没有对手
- **TPU 用户**：想用 Google TPU，只能用 TF（JAX 也可以，但生态不同）
- **Keras 用户**：很多人不知道 Keras 可以用 TF 以外的后端了

### 一句话

> PyTorch 是研究者的选择，TensorFlow 是工程师的归宿。

如果你是学生或研究者，主学 PyTorch。如果你是做端侧部署或要用 Google 的云 TPU，TensorFlow 绕不开。
