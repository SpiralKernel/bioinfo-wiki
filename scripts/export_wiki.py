#!/usr/bin/env python3
"""Export this wiki's Obsidian notes without modifying the source vault."""

import argparse
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import quote


WIKI_URL = "https://github.com/SpiralKernel/bioinfo-wiki/wiki"
FOLDERS = ("学习路线", "术语与概念", "方法与算法", "工具", "数据库", "分析工作流")
FIRST_PAGES = (
    "SNP与基因型是什么", "群体结构是什么", "用PCA探索样本的群体结构",
    "群体结构与GWAS有什么关系",
)
LINK = re.compile(r"(!?)\[\[([^\]]+)\]\]")


def page_url(name):
    return f"{WIKI_URL}/{quote(name, safe='')}"


def strip_properties(text):
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "".join(lines[index + 1:]).lstrip("\n")
        raise ValueError("YAML 属性缺少结束分隔符")
    return text


def render_note(text, path, targets):
    def replace(match):
        if match[1]:
            raise ValueError(f"{path.name}: 请先将 ![[...]] 嵌入改为标准 Markdown 链接")
        target, separator, label = match[2].replace("\\|", "|").partition("|")
        page, anchor, heading = target.partition("#")
        page = page.removesuffix(".md")
        if not page and anchor:
            raise ValueError(f"{path.name}: 请将页内标题链接改为标准 Markdown 锚点")
        if page not in targets:
            raise ValueError(f"{path.name}: 内部链接未纳入发布范围：{target}")
        url = page_url(targets[page])
        if anchor:
            raise ValueError(f"{path.name}: 请将标题锚点链接改为页面链接：{target}")
        return f"[{label if separator else page.rsplit('/', 1)[-1]}]({url})"

    # Leave fenced code and inline code examples unchanged.
    output = []
    fence = None
    for line in strip_properties(text).splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            output.append(line)
            if re.match(rf"^\s{{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$", line):
                fence = None
            continue
        if marker:
            fence = marker[1]
            output.append(line)
            continue
        pieces = re.split(r"(`+[^`\n]*`+)", line)
        output.append("".join(piece if i % 2 else LINK.sub(replace, piece)
                              for i, piece in enumerate(pieces)))
    return "".join(output)


def export(source, output):
    if not source.is_dir():
        raise ValueError(f"原稿目录不存在：{source}")
    if source == output or source in output.parents or output in source.parents:
        raise ValueError("原稿与导出目录必须分开，且不能互相包含")
    notes = sorted(p for folder in FOLDERS for p in (source / folder).rglob("*.md"))
    targets = {"知识库/中文生信Wiki/00-开始写作": "Home", "00-开始写作": "Home"}
    names = set()
    for note in notes:
        if note.stem in names or note.stem in {"Home", "_Sidebar", "_Footer"}:
            raise ValueError(f"重复或保留的页面名称：{note.stem}")
        names.add(note.stem)
        relative = note.relative_to(source).with_suffix("").as_posix()
        for key in (note.stem, relative, f"知识库/中文生信Wiki/{relative}"):
            targets[key] = note.stem
    rendered = {f"{note.stem}.md": render_note(note.read_text(), note, targets)
                for note in notes}
    ordered = [name for name in FIRST_PAGES if name in names]
    ordered += sorted(names - set(ordered))
    links = "\n".join(f"- [{name}]({page_url(name)})" for name in ordered)
    rendered["Home.md"] = (
        "# 中文生信 Wiki\n\n面向入门学生，从群体分析和 GWAS 开始。\n\n"
        "> 当前为试写阶段，标有“待编写”的页面仅提供提纲。\n\n"
        "## 建议阅读顺序\n\n" + links + "\n\n"
        "## 编写方式\n\n原稿在 Obsidian 中维护，导出后同步至本 Wiki。\n\n"
        "[项目与发布工具](https://github.com/SpiralKernel/bioinfo-wiki)\n"
    )
    rendered["_Sidebar.md"] = f"[首页]({page_url('Home')})\n\n" + links + "\n"
    # Finish link validation before updating any published file.
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        for filename, text in rendered.items():
            (staging / filename).write_text(text)
        attachments = source / "附件"
        if attachments.is_dir():
            shutil.copytree(attachments, staging / "附件")
        output.mkdir(parents=True, exist_ok=True)
        for item in staging.iterdir():
            if item.is_dir():
                shutil.copytree(item, output / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, output / item.name)
    print(f"已导出 {len(notes)} 篇文章，以及首页和侧边栏：{output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "wiki")
    args = parser.parse_args()
    try:
        export(args.source.resolve(), args.output.resolve())
    except ValueError as error:
        parser.exit(1, f"导出失败：{error}\n")
