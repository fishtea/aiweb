#!/usr/bin/env python3
"""Render curated resource blocks from data/resources.json into docs pages."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from content_config import CATEGORIES, RESOURCE_LIMIT_PER_TOPIC

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "resources.json"
START = "<!-- RESOURCES_START -->"
END = "<!-- RESOURCES_END -->"
tz = timezone(timedelta(hours=8))


def clean_markdown_text(text: str) -> str:
    text = text or ""
    while "![" in text:
        start = text.find("![")
        end = text.find(")", start)
        if end < 0:
            text = text[:start]
            break
        text = f"{text[:start]} {text[end + 1:]}"
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def escape_link_label(text: str) -> str:
    return clean_markdown_text(text).replace("[", "\\[").replace("]", "\\]")


def load_resources() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def select_resources(resources: list[dict], category: str, topic: str) -> list[dict]:
    matched = [r for r in resources if r.get("category") == category and r.get("topic") == topic]
    matched.sort(key=lambda r: (r.get("score", 0), r.get("first_seen", "")), reverse=True)
    return matched[:RESOURCE_LIMIT_PER_TOPIC]


def render_block(resources: list[dict]) -> str:
    lines = [
        "## 资料整理状态",
        "",
        "> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。",
        "",
        START,
        "",
    ]
    if not resources:
        lines.extend([
            "*暂无候选资料。后续采集会先进入 `data/resources.json`，不会直接改写正文。*",
            "",
        ])
    else:
        source_count = len({item.get("source_domain", "unknown") for item in resources})
        latest_seen = max((item.get("last_seen") or item.get("first_seen") or "" for item in resources), default="")
        lines.extend([
            f"- 后台候选资料：{len(resources)} 条，覆盖 {source_count} 个来源域名。",
            f"- 最近采集日期：{latest_seen or '未知'}。",
            "- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。",
            "",
        ])
    lines.extend([
        END,
        "",
        f"*资源区块更新时间：{datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])
    return "\n".join(lines)


def replace_resource_block(content: str, block: str) -> str:
    if START in content and END in content:
        before = content[:content.index(START)]
        after = content[content.index(END) + len(END):]
        before = before.rstrip()
        resource_heading_positions = [
            before.find("\n## 精选资源"),
            before.find("\n## 资源列表"),
            before.find("\n## 资料整理状态"),
        ]
        valid_positions = [pos for pos in resource_heading_positions if pos >= 0]
        if valid_positions:
            heading_pos = min(valid_positions)
            before = before[:heading_pos].rstrip()
        after = re.sub(r"^\s*(\*资源区块更新时间：.*\*\s*)+", "", after.lstrip())
        return f"{before}\n\n{block}{after}"
    return f"{content.rstrip()}\n\n---\n\n{block}"


def main() -> None:
    resources = load_resources()
    updated = 0
    for category, category_info in CATEGORIES.items():
        for topic in category_info["subs"]:
            page = PROJECT_ROOT / "docs" / category / topic / "index.md"
            if not page.exists():
                continue
            block = render_block(select_resources(resources, category, topic))
            content = page.read_text(encoding="utf-8")
            next_content = replace_resource_block(content, block)
            if next_content != content:
                page.write_text(next_content, encoding="utf-8")
                updated += 1
    print(f"Rendered resource blocks: {updated}")


if __name__ == "__main__":
    main()
