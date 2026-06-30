#!/usr/bin/env python3
"""
AI learning resource collection pipeline.

Design goals:
  1. Keep tutorial pages structured and readable.
  2. Store collected links in data/resources.json as the source of truth.
  3. Rebuild bounded "精选资源" blocks instead of endlessly appending links.
  4. Prefer official docs, papers, reputable courses, and maintained open-source docs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from content_config import BLOCKED_DOMAINS, CATEGORIES, TRUSTED_DOMAINS
from render_resources import main as render_resources

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "resources.json"
REPORT_DIR = PROJECT_ROOT / "docs" / "知识库" / "更新报告"
tz = timezone(timedelta(hours=8))
NOW = datetime.now(tz)
TODAY = NOW.strftime("%Y-%m-%d")
NOW_STR = NOW.strftime("%Y-%m-%d %H:%M:%S")


@dataclass(frozen=True)
class SearchTask:
    category: str
    topic: str
    query: str
    tags: list[str]
    level: str


def normalize_domain(netloc: str) -> str:
    domain = netloc.lower().split(":")[0]
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def normalize_url(url: str) -> str:
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return ""
        tracking_params = {
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "ref",
            "source",
            "source_url",
            "si",
            "mc_cid",
            "mc_eid",
            "fbclid",
            "gclid",
            "gclsrc",
            "dclid",
        }
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        clean_params = {k: v for k, v in query_params.items() if k.lower() not in tracking_params}
        clean_query = urlencode(clean_params, doseq=True)
        path = parsed.path.rstrip("/") or "/"
        return urlunparse((parsed.scheme.lower(), normalize_domain(parsed.netloc), path, "", clean_query, ""))
    except Exception:
        return ""


def source_domain(url: str) -> str:
    return normalize_domain(urlparse(url).netloc)


def load_resources() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {DATA_FILE}: {exc}") from exc


def save_resources(resources: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    resources.sort(key=lambda r: (r.get("category", ""), r.get("topic", ""), r.get("score", 0), r.get("first_seen", "")), reverse=True)
    DATA_FILE.write_text(json.dumps(resources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def needs_translation(text: str) -> bool:
    if not text or not text.strip():
        return False
    total = len(text.strip())
    en_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    cn_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    return cn_chars <= total * 0.3 and en_chars > total * 0.4


_translator = None


def translate_text(text: str) -> str:
    if not needs_translation(text):
        return text
    global _translator
    if _translator is None:
        try:
            from deep_translator import GoogleTranslator

            _translator = GoogleTranslator(source="en", target="zh-CN")
        except Exception as exc:
            print(f"[WARN] deep-translator unavailable: {exc}", file=sys.stderr)
            return text
    try:
        return str(_translator.translate(text[:3000]) or text)
    except Exception as exc:
        print(f"[WARN] translation failed: {exc}", file=sys.stderr)
        return text


def search_resources(query: str, max_results: int) -> list[dict]:
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            return [
                {
                    "title": r.get("title", "").strip(),
                    "url": r.get("href", "").strip(),
                    "summary": r.get("body", "").strip(),
                }
                for r in ddgs.text(query, max_results=max_results)
            ]
    except Exception as exc:
        print(f"[WARN] search failed for {query!r}: {exc}", file=sys.stderr)
        return []


def keyword_score(title: str, summary: str, tags: list[str]) -> int:
    text = f"{title} {summary}".lower()
    score = 0
    for tag in tags:
        if tag.lower() in text:
            score += 2
    if re.search(r"\b(tutorial|guide|course|docs|documentation|paper|论文|教程|指南|课程|官方|文档)\b", text, re.I):
        score += 2
    if re.search(r"\b(2025|2026|latest|最新)\b", text, re.I):
        score += 1
    return score


def quality_score(url: str, title: str, summary: str, tags: list[str]) -> int:
    domain = source_domain(url)
    score = TRUSTED_DOMAINS.get(domain, 0)
    if any(domain == d or domain.endswith(f".{d}") for d in TRUSTED_DOMAINS):
        score = max(score, 4)
    score += keyword_score(title, summary, tags)
    if len(summary) >= 80:
        score += 1
    if len(title) < 8:
        score -= 2
    return max(score, 0)


def is_blocked(url: str) -> bool:
    domain = source_domain(url)
    return any(domain == d or domain.endswith(f".{d}") for d in BLOCKED_DOMAINS)


def build_tasks(categories: list[str] | None, topics: list[str] | None) -> list[SearchTask]:
    tasks: list[SearchTask] = []
    topic_filter = set(topics or [])
    category_filter = set(categories or [])
    for category, category_info in CATEGORIES.items():
        if category_filter and category not in category_filter:
            continue
        for topic, topic_info in category_info["subs"].items():
            if topic_filter and topic not in topic_filter:
                continue
            for query in topic_info.get("queries", []):
                tasks.append(
                    SearchTask(
                        category=category,
                        topic=topic,
                        query=query,
                        tags=topic_info.get("tags", []),
                        level=topic_info.get("level", ""),
                    )
                )
    return tasks


def merge_candidate(existing: dict | None, task: SearchTask, candidate: dict) -> tuple[dict, bool]:
    url = normalize_url(candidate.get("url", ""))
    if not url or is_blocked(url):
        return {}, False
    title = candidate.get("title", "").strip()
    summary = candidate.get("summary", "").strip()
    if not title:
        return {}, False
    score = quality_score(url, title, summary, task.tags)
    if score < 2:
        return {}, False

    if existing:
        existing["last_seen"] = TODAY
        existing["seen_count"] = int(existing.get("seen_count", 1)) + 1
        existing["score"] = max(int(existing.get("score", 0)), score)
        if len(summary) > len(existing.get("summary", "")):
            existing["summary"] = summary
            existing["summary_cn"] = translate_text(summary)
        return existing, False

    item = {
        "url": url,
        "source_domain": source_domain(url),
        "title": title,
        "title_cn": translate_text(title),
        "summary": summary,
        "summary_cn": translate_text(summary),
        "category": task.category,
        "topic": task.topic,
        "tags": task.tags,
        "level": task.level,
        "score": score,
        "first_seen": TODAY,
        "last_seen": TODAY,
        "seen_count": 1,
        "query": task.query,
    }
    return item, True


def write_report(added: list[dict], total_seen: int, task_count: int) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"{TODAY}.md"
    by_topic: dict[tuple[str, str], list[dict]] = {}
    for item in added:
        by_topic.setdefault((item["category"], item["topic"]), []).append(item)

    lines = [
        f"# {TODAY} 采集更新报告",
        "",
        f"- 运行时间：{NOW_STR}",
        f"- 搜索任务：{task_count}",
        f"- 搜索结果：{total_seen}",
        f"- 新增资源：{len(added)}",
        f"- 资源库：`data/resources.json`",
        "",
        "## 新增资源",
        "",
    ]
    if not added:
        lines.append("本次没有新增资源。")
    else:
        for (category, topic), items in sorted(by_topic.items()):
            lines.append(f"### {category} / {topic}")
            lines.append("")
            for item in sorted(items, key=lambda r: r.get("score", 0), reverse=True):
                title = item.get("title_cn") or item.get("title")
                lines.append(f"- **[{title}]({item['url']})**")
                lines.append(f"  - 来源：`{item['source_domain']}` · 质量分：{item['score']}")
            lines.append("")
    report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Report: {report}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect AI learning resources into a curated resource database.")
    parser.add_argument("--category", action="append", help="Limit collection to a category. Can be repeated.")
    parser.add_argument("--topic", action="append", help="Limit collection to a topic. Can be repeated.")
    parser.add_argument("--max-results", type=int, default=5, help="Search results per query.")
    parser.add_argument("--workers", type=int, default=8, help="Parallel search workers.")
    parser.add_argument("--no-render", action="store_true", help="Only update data/resources.json, do not render docs blocks.")
    args = parser.parse_args()

    tasks = build_tasks(args.category, args.topic)
    resources = load_resources()
    by_url = {r.get("url"): r for r in resources if r.get("url")}
    added: list[dict] = []
    total_seen = 0

    print(f"=== AI 学习资源采集 [{NOW_STR}] ===")
    print(f"任务数: {len(tasks)}")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {executor.submit(search_resources, task.query, args.max_results): task for task in tasks}
        for future in as_completed(future_map):
            task = future_map[future]
            results = future.result()
            total_seen += len(results)
            print(f"  [{task.category}/{task.topic}] {task.query[:48]} -> {len(results)}")
            for raw in results:
                url = normalize_url(raw.get("url", ""))
                existing = by_url.get(url)
                item, is_new = merge_candidate(existing, task, raw)
                if not item:
                    continue
                by_url[item["url"]] = item
                if is_new:
                    resources.append(item)
                    added.append(item)

    save_resources(resources)
    write_report(added, total_seen, len(tasks))
    if not args.no_render:
        render_resources()

    print("=== 采集完成 ===")
    print(f"搜索结果: {total_seen}")
    print(f"新增资源: {len(added)}")
    print(f"资源总数: {len(resources)}")


if __name__ == "__main__":
    main()
