#!/usr/bin/env python3
"""Create missing category/topic index pages from the shared taxonomy.

This script is intentionally conservative: it does not overwrite existing
tutorial pages. Use it when adding new topics to scripts/content_config.py.
"""

from pathlib import Path

from content_config import CATEGORIES

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS = PROJECT_ROOT / "docs"


def create_category_page(category: str, info: dict) -> bool:
    path = DOCS / category
    path.mkdir(parents=True, exist_ok=True)
    page = path / "index.md"
    if page.exists():
        return False
    lines = [
        f"# {category}",
        "",
        f"> {info['desc']}",
        "",
        "## 子分类",
        "",
    ]
    for topic, topic_info in info["subs"].items():
        lines.append(f"- **[{topic}]({topic}/)** — {topic_info['desc']}")
    lines.extend(["", "---", "", "*该分类下的资源会通过采集脚本持续更新。*", ""])
    page.write_text("\n".join(lines), encoding="utf-8")
    return True


def create_topic_page(category: str, topic: str, info: dict) -> bool:
    path = DOCS / category / topic
    path.mkdir(parents=True, exist_ok=True)
    page = path / "index.md"
    if page.exists():
        return False
    lines = [
        f"# {topic}",
        "",
        info["desc"],
        "",
        "## 适合读者",
        "",
        "- 正在系统学习该主题的读者",
        "- 需要快速建立概念框架的开发者、产品经理或研究者",
        "",
        "## 核心概念",
        "",
        "TODO: 补充该主题的概念解释、工作机制、适用场景和常见误区。",
        "",
        "## 实践建议",
        "",
        "TODO: 补充最小可运行实践、验证方法和延伸学习路径。",
        "",
        "---",
        "",
        "## 精选资源",
        "",
        "<!-- RESOURCES_START -->",
        "",
        "*暂无采集资源。后续运行 `python scripts/collect.py` 后会自动补充。*",
        "",
        "<!-- RESOURCES_END -->",
        "",
        "*资源区块更新时间：待首次采集*",
        "",
    ]
    page.write_text("\n".join(lines), encoding="utf-8")
    return True


def main() -> None:
    created = 0
    for category, category_info in CATEGORIES.items():
        created += int(create_category_page(category, category_info))
        for topic, topic_info in category_info["subs"].items():
            created += int(create_topic_page(category, topic, topic_info))
    print(f"Created pages: {created}")


if __name__ == "__main__":
    main()
