#!/usr/bin/env python3
"""
AI 学习资源每日采集脚本
功能：
  1. 搜索各分类最新AI学习资源
  2. 将英文资源翻译成中文
  3. 按分类归档到 docs/ 目录
  4. 生成每日更新报告
"""

import os
import sys
import json
import hashlib
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 如果timezone为naive，设置中国时区
try:
    tz = timezone(timedelta(hours=8))
except Exception:
    tz = None

TODAY = datetime.now(tz).strftime("%Y-%m-%d")
NOW_STR = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

# ============================================================
# 分类体系 - 每个子分类对应搜索关键词
# ============================================================
CATEGORIES = {
    "初级知识": {
        "人工智能入门": {
            "queries": [
                "AI beginner tutorial 2025",
                "人工智能入门教程 2025",
            ],
            "tags": ["入门", "AI基础", "教程"],
        },
        "机器学习基础": {
            "queries": [
                "machine learning basics tutorial",
                "机器学习基础教程",
            ],
            "tags": ["机器学习", "基础", "算法"],
        },
        "深度学习入门": {
            "queries": [
                "deep learning tutorial beginners",
                "深度学习入门教程",
            ],
            "tags": ["深度学习", "神经网络", "入门"],
        },
        "大语言模型基础": {
            "queries": [
                "large language model beginner guide",
                "大语言模型入门教程",
            ],
            "tags": ["LLM", "大语言模型", "Transformer"],
        },
    },
    "进阶学习": {
        "模型微调技术": {
            "queries": [
                "LLM fine-tuning tutorial 2025",
                "大模型微调教程",
            ],
            "tags": ["微调", "LoRA", "PEFT", "Fine-tuning"],
        },
        "RAG检索增强": {
            "queries": [
                "RAG retrieval augmented generation tutorial",
                "RAG架构教程 2025",
            ],
            "tags": ["RAG", "检索增强", "向量数据库"],
        },
        "Agent智能体": {
            "queries": [
                "LLM agent tutorial 2025",
                "多Agent系统教程",
            ],
            "tags": ["Agent", "智能体", "AI代理"],
        },
        "提示词工程": {
            "queries": [
                "prompt engineering guide 2025",
                "提示词工程教程",
            ],
            "tags": ["提示词", "Prompt", "工程"],
        },
        "模型评估与基准": {
            "queries": [
                "LLM evaluation benchmark 2025",
                "大模型评测基准",
            ],
            "tags": ["评测", "基准", "Benchmark"],
        },
    },
    "高级知识": {
        "模型训练与优化": {
            "queries": [
                "distributed LLM training guide",
                "分布式训练教程 GPU",
            ],
            "tags": ["训练", "分布式", "量化", "优化"],
        },
        "AI安全与对齐": {
            "queries": [
                "AI safety alignment research 2025",
                "AI安全对齐 教程",
            ],
            "tags": ["安全", "对齐", "RLHF", "红队"],
        },
        "多模态模型": {
            "queries": [
                "multimodal AI tutorial 2025",
                "多模态模型教程 CLIP LLaVA",
            ],
            "tags": ["多模态", "视觉", "CLIP", "LLaVA"],
        },
        "模型架构研究": {
            "queries": [
                "Mixture of Experts architecture explained",
                "前沿模型架构研究",
            ],
            "tags": ["MoE", "Mamba", "架构", "前沿"],
        },
    },
    "模型专区": {
        "GPT系列": {
            "queries": [
                "GPT-4o tutorial guide 2025",
                "ChatGPT advanced usage tips",
            ],
            "tags": ["GPT", "OpenAI", "ChatGPT"],
        },
        "Claude系列": {
            "queries": [
                "Claude tutorial guide 2025",
                "Anthropic Claude API tutorial",
            ],
            "tags": ["Claude", "Anthropic"],
        },
        "LLaMA系列": {
            "queries": [
                "LLaMA 3 tutorial guide 2025",
                "LLaMA部署教程 本地运行",
            ],
            "tags": ["LLaMA", "Meta", "开源"],
        },
        "DeepSeek": {
            "queries": [
                "DeepSeek V3 tutorial guide",
                "DeepSeek API使用教程",
            ],
            "tags": ["DeepSeek", "深度求索"],
        },
        "Gemini系列": {
            "queries": [
                "Google Gemini tutorial 2025",
                "Gemini API tutorial Python",
            ],
            "tags": ["Gemini", "Google"],
        },
        "Qwen系列": {
            "queries": [
                "Qwen model tutorial 2025",
                "通义千问Qwen教程",
            ],
            "tags": ["Qwen", "通义千问", "阿里"],
        },
        "StableDiffusion": {
            "queries": [
                "Stable Diffusion tutorial 2025",
                "ComfyUI workflow tutorial",
            ],
            "tags": ["Stable Diffusion", "图像生成", "ComfyUI"],
        },
        "Mixtral系列": {
            "queries": [
                "Mixtral 8x22B tutorial",
                "Mistral AI model guide",
            ],
            "tags": ["Mixtral", "Mistral", "MoE"],
        },
    },
    "工具专区": {
        "LangChain": {
            "queries": [
                "LangChain tutorial 2025",
                "LangChain RAG agent tutorial",
            ],
            "tags": ["LangChain", "框架", "Agent"],
        },
        "AutoGPT": {
            "queries": [
                "AutoGPT tutorial 2025",
                "自主AI Agent搭建教程",
            ],
            "tags": ["AutoGPT", "自主Agent"],
        },
        "ComfyUI": {
            "queries": [
                "ComfyUI tutorial beginner 2025",
                "ComfyUI节点教程 工作流",
            ],
            "tags": ["ComfyUI", "工作流", "图像生成"],
        },
        "vLLM": {
            "queries": [
                "vLLM deployment tutorial 2025",
                "vLLM模型部署教程",
            ],
            "tags": ["vLLM", "推理", "部署"],
        },
        "HuggingFace": {
            "queries": [
                "HuggingFace tutorial 2025",
                "HuggingFace模型使用教程",
            ],
            "tags": ["HuggingFace", "Transformers", "模型库"],
        },
        "PyTorch": {
            "queries": [
                "PyTorch tutorial 2025",
                "PyTorch深度学习教程",
            ],
            "tags": ["PyTorch", "深度学习框架"],
        },
        "TensorFlow": {
            "queries": [
                "TensorFlow tutorial 2025",
                "TensorFlow模型部署 TensorFlow Serving",
            ],
            "tags": ["TensorFlow", "Keras", "ML框架"],
        },
        "Ollama": {
            "queries": [
                "Ollama tutorial 2025",
                "Ollama本地部署大模型教程",
            ],
            "tags": ["Ollama", "本地部署", "LLM"],
        },
    },
}

# ============================================================
# 翻译模块
# ============================================================
_translator = None

def get_translator():
    global _translator
    if _translator is None:
        try:
            from deep_translator import GoogleTranslator
            _translator = GoogleTranslator(source='en', target='zh-CN')
        except Exception as e:
            print(f"[WARN] deep-translator import failed: {e}", file=sys.stderr)
            _translator = None
    return _translator

def needs_translation(text):
    """检测文本是否包含较多英文"""
    if not text:
        return False
    # 如果英文字母比例超过40%，认为需要翻译
    total_chars = len(text.strip())
    if total_chars == 0:
        return False
    en_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    # 如果有大量中文，不需要翻译
    if cn_chars > total_chars * 0.3:
        return False
    return en_chars > total_chars * 0.4

def translate_text(text, dest="zh-cn"):
    """翻译英文文本到中文，带重试"""
    if not text or not text.strip():
        return text
    if not needs_translation(text):
        return text
    
    translator = get_translator()
    if not translator:
        return text
    
    try:
        result = translator.translate(text[:3000])
        if result:
            return str(result)
    except Exception as e:
        print(f"[WARN] Translation failed: {e}", file=sys.stderr)
    return text

def translate_batch(texts):
    """批量翻译"""
    results = []
    for t in texts:
        results.append(translate_text(t))
    return results

# ============================================================
# 搜索模块
# ============================================================
def search_resources(query, max_results=3):
    """使用 DuckDuckGo 搜索资源"""
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "body": r.get("body", ""),
                })
        return results
    except Exception as e:
        print(f"[WARN] Search failed for '{query}': {e}", file=sys.stderr)
        return []

def classify_resource(title, body, tags):
    """判断资源是否匹配分类"""
    title_body = (title + " " + body).lower()
    keywords = [t.lower() for t in tags]
    # 简单匹配：如果标题包含任一关键词，判定为匹配
    for k in keywords:
        if k in title_body:
            return True
    return False

def deduplicate(existing_urls, new_results):
    """去重：基于URL去重"""
    deduped = []
    for r in new_results:
        url = r.get("url", "")
        if url and url not in existing_urls:
            deduped.append(r)
    return deduped

# ============================================================
# 文档生成
# ============================================================
def load_existing_urls(cat_dir):
    """读取已有资源列表中的URL"""
    urls = set()
    index_file = cat_dir / "index.md"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        # 提取所有URL
        for line in content.split("\n"):
            match = re.search(r'\((https?://[^)]+)\)', line)
            if match:
                urls.add(match.group(1))
    return urls

def format_resource_markdown(title, url, body, translated=False):
    """格式化单个资源为markdown条目"""
    status = "🌐" if not translated else "🌏"
    return f"- **[{title}]({url})**\n  - {body[:200]}{'...' if len(body) > 200 else ''}\n"

def append_to_category(cat, sub, resources):
    """将资源追加到对应分类文件"""
    cat_dir = PROJECT_ROOT / "docs" / cat / sub
    index_file = cat_dir / "index.md"
    
    if not resources:
        return 0
    
    added = 0
    content = index_file.read_text(encoding="utf-8") if index_file.exists() else ""
    
    # 处理翻译
    translated_resources = []
    for r in resources:
        title = r.get("title", "")
        body = r.get("body", "")
        
        title_cn = translate_text(title)
        body_cn = translate_text(body)
        was_translated = (title_cn != title) or (body_cn != body)
        
        translated_resources.append({
            "title": title_cn if title_cn else title,
            "url": r["url"],
            "body": body_cn if body_cn else body,
            "translated": was_translated,
        })
    
    # 生成markdown条目
    new_entries = []
    for r in translated_resources:
        new_entries.append(format_resource_markdown(
            r["title"], r["url"], r["body"], r["translated"]
        ))
    
    # 插入到 RESOURCES_START / RESOURCES_END 标记之间
    if "<!-- RESOURCES_START -->" in content and "<!-- RESOURCES_END -->" in content:
        # 追加到 RESOURCES_START 后面
        start_marker = "<!-- RESOURCES_START -->"
        end_marker = "<!-- RESOURCES_END -->"
        
        start_idx = content.index(start_marker) + len(start_marker)
        end_idx = content.index(end_marker)
        
        # 生成新条目
        new_section = "\n\n" + "\n".join(new_entries)
        
        new_content = content[:start_idx] + new_section + "\n" + content[end_idx:]
        
        # 更新最后更新时间
        new_content = re.sub(
            r'\*最后更新：[^*]+\*',
            f'*最后更新：{NOW_STR}*',
            new_content
        )
        
        index_file.write_text(new_content, encoding="utf-8")
        added = len(new_entries)
    else:
        # 没有标记，追加到末尾
        with open(index_file, "a", encoding="utf-8") as f:
            f.write("\n\n<!-- RESOURCES_START -->\n")
            f.write("\n".join(new_entries))
            f.write("\n<!-- RESOURCES_END -->\n")
            f.write(f"\n*最后更新：{NOW_STR}*\n")
        added = len(new_entries)
    
    return added

# ============================================================
# 主流程
# ============================================================
def main():
    print(f"=== AI 学习资源采集开始 [{NOW_STR}] ===")
    print(f"项目目录: {PROJECT_ROOT}")
    print()
    
    total_searched = 0
    total_new = 0
    total_categories = 0
    
    # 收集所有搜索任务
    search_tasks = []
    for cat, subs in CATEGORIES.items():
        for sub, info in subs.items():
            for query in info["queries"]:
                search_tasks.append((cat, sub, query, info["tags"]))
    
    print(f"总搜索任务: {len(search_tasks)} 个\n")
    
    # 并发搜索
    results_map = {}  # (cat, sub) -> [(query, results)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_map = {}
        for cat, sub, query, tags in search_tasks:
            future = executor.submit(search_resources, query, 3)
            future_map[future] = (cat, sub, query, tags)
        
        for future in as_completed(future_map):
            cat, sub, query, tags = future_map[future]
            try:
                results = future.result()
                key = (cat, sub)
                if key not in results_map:
                    results_map[key] = []
                results_map[key].append((query, results, tags))
                print(f"  ✅ [{cat}/{sub}] \"{query[:40]}...\" → {len(results)} 条", flush=True)
                total_searched += len(results)
            except Exception as e:
                print(f"  ❌ [{cat}/{sub}] 搜索失败: {e}", flush=True)
    
    print(f"\n搜索完成，共 {total_searched} 条结果\n")
    
    # 分类归档
    for (cat, sub), query_results in results_map.items():
        tags = query_results[0][2]  # 取第一个的tags
        cat_dir = PROJECT_ROOT / "docs" / cat / sub
        existing_urls = load_existing_urls(cat_dir)
        
        all_new = []
        for query, results, q_tags in query_results:
            matched = [r for r in results if classify_resource(r.get("title", ""), r.get("body", ""), tags)]
            deduped = deduplicate(existing_urls, matched)
            all_new.extend(deduped)
        
        if all_new:
            added = append_to_category(cat, sub, all_new)
            total_new += added
            total_categories += 1
            print(f"  📝 [{sub}] 新增 {added} 条资源", flush=True)
    
    print()
    print(f"=== 采集完成 ===")
    print(f"总搜索到: {total_searched} 条")
    print(f"新增归档: {total_new} 条")
    print(f"涉及分类: {total_categories} 个")
    print(f"存档位置: {PROJECT_ROOT}/docs/")
    print(f"当前时间: {NOW_STR}")

if __name__ == "__main__":
    main()
