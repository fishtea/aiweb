#!/bin/bash
# AI 学习路径导航 - VitePress 构建
set -e

cd "$(dirname "$0")/.."

echo "=== 构建静态网站 ==="
echo "项目目录: $(pwd)"
echo ""

echo "→ 生成静态站点..."
npm run build
echo "  ✅ 站点生成完成: docs/.vitepress/dist/"

echo "→ 同步到 website/..."
rm -rf website/*
cp -r docs/.vitepress/dist/* website/
echo "  ✅ 同步完成"

echo ""
echo "=== 构建完成 ==="
echo "站点路径: $(pwd)/website/"
echo "可以直接打开 website/index.html 预览"
