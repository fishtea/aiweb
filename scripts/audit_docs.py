#!/usr/bin/env python3
"""Audit docs structure against the shared taxonomy and VitePress expectations."""

from __future__ import annotations

import re
from pathlib import Path

from content_config import CATEGORIES

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS = PROJECT_ROOT / "docs"
REPORT = DOCS / "知识库" / "文档体检报告.md"
RESOURCE_START = "<!-- RESOURCES_START -->"
RESOURCE_END = "<!-- RESOURCES_END -->"


def iter_markdown_pages() -> list[Path]:
    ignored_parts = {".vitepress"}
    pages = []
    for path in DOCS.rglob("*.md"):
        if any(part in ignored_parts for part in path.parts):
            continue
        pages.append(path)
    return sorted(pages)


def expected_topic_pages() -> set[Path]:
    pages = set()
    for category, category_info in CATEGORIES.items():
        pages.add(DOCS / category / "index.md")
        for topic in category_info["subs"]:
            pages.add(DOCS / category / topic / "index.md")
    pages.add(DOCS / "index.md")
    pages.add(DOCS / "知识库" / "index.md")
    pages.add(DOCS / "知识库" / "内容治理与采集规划.md")
    return pages


def extract_links(content: str) -> list[str]:
    md_links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    html_links = re.findall(r'href="([^"]+)"', content)
    return md_links + html_links


def local_link_exists(link: str, current_page: Path) -> bool:
    if not link or link.startswith(("http://", "https://", "mailto:", "#")):
        return True
    link = link.split("#", 1)[0]
    if not link:
        return True
    if link.startswith("/"):
        target = DOCS / link.lstrip("/")
    else:
        target = current_page.parent / link
    if target.suffix == ".md":
        return target.exists()
    if target.is_dir():
        return (target / "index.md").exists()
    if target.exists():
        return True
    return (Path(str(target).rstrip("/")) / "index.md").exists()


def heading_count(content: str) -> int:
    return len(re.findall(r"^##\s+", content, re.M))


def audit() -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    suggestions: list[str] = []
    pages = iter_markdown_pages()
    expected = expected_topic_pages()
    actual = set(pages)

    for missing in sorted(expected - actual):
        warnings.append(f"缺少配置中的页面：`{missing.relative_to(PROJECT_ROOT)}`")

    for extra in sorted(actual - expected):
        rel = extra.relative_to(PROJECT_ROOT)
        if "更新报告" not in str(rel) and rel.name != "文档体检报告.md":
            suggestions.append(f"页面未纳入统一分类配置：`{rel}`")

    for page in pages:
        content = page.read_text(encoding="utf-8")
        rel = page.relative_to(PROJECT_ROOT)
        is_audit_report = page == REPORT
        is_home = page == DOCS / "index.md" and content.lstrip().startswith("---")
        is_category_index = page.name == "index.md" and page.parent.parent == DOCS
        is_topic_index = page.name == "index.md" and page.parent.parent.parent == DOCS
        if not is_home and not content.lstrip().startswith("#"):
            warnings.append(f"缺少一级标题：`{rel}`")
        if len(content.strip()) < 800 and not is_audit_report:
            suggestions.append(f"正文偏短，建议补充概念、步骤和误区：`{rel}`")
        if "TODO" in content or "待补充" in content:
            warnings.append(f"存在未完成标记：`{rel}`")
        if is_topic_index:
            if RESOURCE_START not in content or RESOURCE_END not in content:
                suggestions.append(f"专题页缺少精选资源区块：`{rel}`")
        if RESOURCE_START in content and RESOURCE_END not in content:
            warnings.append(f"资源区块结束标记缺失：`{rel}`")
        if RESOURCE_END in content and RESOURCE_START not in content:
            warnings.append(f"资源区块开始标记缺失：`{rel}`")
        if heading_count(content) < 2 and not is_home and not is_audit_report:
            suggestions.append(f"二级标题偏少，阅读结构可能不足：`{rel}`")
        for link in extract_links(content):
            if not local_link_exists(link, page):
                warnings.append(f"本地链接可能失效：`{rel}` -> `{link}`")

    return warnings, suggestions


def write_report(warnings: list[str], suggestions: list[str]) -> None:
    lines = [
        "# 文档体检报告",
        "",
        "该报告由 `python scripts/audit_docs.py` 生成，用于检查文档结构、统一分类配置和本地链接。",
        "",
        "## 严重问题",
        "",
    ]
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- 未发现严重问题。")
    lines.extend(["", "## 优化建议", ""])
    if suggestions:
        lines.extend(f"- {item}" for item in suggestions)
    else:
        lines.append("- 暂无优化建议。")
    lines.extend([
        "",
        "## 后续处理",
        "",
        "- 严重问题应优先修复，尤其是缺页、未完成标记和失效本地链接。",
        "- 优化建议可按栏目逐步处理，不要求一次性清空。",
        "- 资源区块由 `scripts/render_resources.py` 统一重建，正文内容应人工整理。",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    warnings, suggestions = audit()
    write_report(warnings, suggestions)
    print(f"Warnings: {len(warnings)}")
    print(f"Suggestions: {len(suggestions)}")
    print(f"Report: {REPORT}")
    if warnings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
