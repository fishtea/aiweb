#!/bin/bash
# AI 学习路径导航 - 构建静态网站
set -e

cd "$(dirname "$0")/.."

echo "=== 构建静态网站 ==="
echo "项目目录: $(pwd)"
echo ""

# 运行MkDocs构建
echo "→ 生成静态站点..."
python3 -m mkdocs build --clean
echo "  ✅ 站点生成完成: site/"

# 复制到 website/ 目录（保留一份额外副本）
echo "→ 同步到 website/..."
rm -rf website/*
cp -r site/* website/
echo "  ✅ 同步完成"

echo ""
echo "=== 构建完成 ==="
echo "站点路径: $(pwd)/website/"
echo "可以直接打开 website/index.html 预览"
