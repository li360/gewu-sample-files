"""生成中文 docx 样本（基于 python-docx）。

按 AGENTS.md：
- 使用项目自带 OFL 子集字体（思源黑体）
- 通过库 API 指定字体名，跨平台显示一致
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：标题 + 自编段落 + 古籍原文
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    chinese_paragraphs,
    classics_text,
    ensure_sample_dir,
    faker,
    sample_name,
)

# 字体名：思源黑体 CN Regular（不嵌字体文件，仅指定名称，
# 依赖阅读器/字体替换；与 AGENTS.md “文档内嵌字体策略后续讨论”一致）
FONT_NAME = "Source Han Sans CN"


def set_run_font(run, font_name: str = FONT_NAME, size_pt: int = 12) -> None:
    """设置 run 的字体与字号，同时指定 east-asia 字体（中文渲染关键）。"""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    # 中文 East Asian 字体必须单独设置，否则会用默认宋体
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        from docx.oxml import OxmlElement
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:eastAsia"), font_name)


def add_paragraph_with_font(doc: Document, text: str, font_name: str = FONT_NAME, size_pt: int = 12) -> None:
    """向 doc 添加一段中文文本并应用字体。"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, font_name, size_pt)


def build_doc(path: Path, title: str, paragraphs: list[str], classics: str) -> int:
    """构造 docx 并保存到 path，返回字节数。"""
    doc = Document()

    # 文档默认字体也设置为思源黑体
    style = doc.styles["Normal"]
    style.font.name = FONT_NAME
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        from docx.oxml import OxmlElement
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:eastAsia"), FONT_NAME)

    # 标题（用 Heading 1，字号稍大）
    h = doc.add_heading(level=1)
    title_run = h.add_run(title)
    set_run_font(title_run, FONT_NAME, size_pt=20)

    # 正文段落
    for para in paragraphs:
        add_paragraph_with_font(doc, para, FONT_NAME, 12)

    # 古籍原文作为引用块（斜体）
    doc.add_paragraph()  # 空行
    classics_heading = doc.add_heading(level=2)
    classics_run = classics_heading.add_run("古籍原文节选")
    set_run_font(classics_run, FONT_NAME, size_pt=16)
    for line in classics.split("\n"):
        add_paragraph_with_font(doc, line, FONT_NAME, 11)

    doc.save(path)
    return path.stat().st_size


def main() -> int:
    ext = "docx"
    out_dir = ensure_sample_dir(ext)
    title = "中文样本文档"

    # 小文件：5 段 + 500 字古籍 ≈ 10–20 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_doc(
        small_path, title, chinese_paragraphs(5), classics_text(500)
    )

    # 中等文件：800 段 Faker 段落（独特内容，降低 ZIP 压缩率）+ 古籍 ≈ 150–300 KB
    medium_paragraphs = [faker.paragraph(nb_sentences=10) for _ in range(800)]
    medium_classics = classics_text(150000)
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_doc(
        medium_path, title, medium_paragraphs, medium_classics
    )

    print(f"[docx] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[docx] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
