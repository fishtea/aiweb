#!/bin/bash
# AI 学习路径导航 - 完全部署脚本
# 1. 采集资源 → 2. 构建网站 → 3. 推送 Git
set -e

cd "$(dirname "$0")/.."

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "=========================================="
echo "  AI 学习资源库 - 自动部署"
echo "  时间: $TIMESTAMP"
echo "=========================================="
echo ""

# 第1步：采集资源
echo "=== 第1步：采集AI学习资源 ==="
python3 scripts/collect.py
echo ""
echo "✅ 采集完成"
echo ""

# 第2步：构建网站
echo "=== 第2步：构建静态网站 ==="
npm run build
rm -rf website/*
cp -r docs/.vitepress/dist/* website/
echo "✅ 网站构建完成"
echo ""

# 第3步：推送到 Git
echo "=== 第3步：推送到 Git ==="
git add -A
git commit -m "每日更新 ${TIMESTAMP}"
git push origin master
echo "✅ 推送完成"
echo ""

echo "=========================================="
echo "  部署完成！"
echo "  Vercel: https://aiweb-lemon.vercel.app/"
echo "=========================================="
