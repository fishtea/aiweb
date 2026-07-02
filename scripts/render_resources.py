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
        "## 精选资源",
        "",
        "> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。",
        "",
        START,
        "",
    ]
    if not resources:
        lines.extend([
            "*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*",
            "",
        ])
    else:
        for item in resources:
            title = escape_link_label(item.get("title_cn") or item.get("title") or "未命名资源")
            summary = clean_markdown_text(item.get("summary_cn") or item.get("summary") or "暂无摘要。")
            url = item.get("url", "")
            source = item.get("source_domain", "unknown")
            score = item.get("score", 0)
            first_seen = item.get("first_seen", "")
            provider = item.get("provider") or ", ".join(item.get("providers") or [])
            verified_at = item.get("verified_at", "")
            lines.append(f"- **[{title}]({url})**")
            meta = f"来源：`{source}` · 质量分：{score} · 首次采集：{first_seen}"
            if provider:
                meta += f" · 信息源：`{provider}`"
            if verified_at:
                meta += f" · 已验证：{verified_at[:10]}"
            lines.append(f"  - {meta}")
            lines.append(f"  - {summary[:220]}{'...' if len(summary) > 220 else ''}")
            lines.append("")
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
