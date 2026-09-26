"""生成中文 PDF 样本（基于 reportlab）。

按 AGENTS.md：
- 通过 reportlab 显式注册 OFL 子集字体，禁止依赖系统字体
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：标题 + 自编段落 + 古籍原文
"""
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    SUBSET_FONT,
    chinese_paragraphs,
    classics_text,
    ensure_sample_dir,
    sample_name,
)

# 字体注册键（reportlab 内部引用）
FONT_REG_NAME = "SourceHanSansCN"
FONT_REG_BOLD = FONT_REG_NAME + "-Bold"

# 段落样式
BODY_STYLE = ParagraphStyle(
    name="Body",
    fontName=FONT_REG_NAME,
    fontSize=11,
    leading=18,
    textColor=(40, 40, 40),
    spaceAfter=6 * mm,
)
TITLE_STYLE = ParagraphStyle(
    name="Title",
    fontName=FONT_REG_NAME,
    fontSize=22,
    leading=30,
    textColor=(20, 60, 120),
    spaceAfter=12 * mm,
)
CLASSICS_STYLE = ParagraphStyle(
    name="Classics",
    fontName=FONT_REG_NAME,
    fontSize=10,
    leading=16,
    textColor=(80, 80, 80),
    spaceAfter=3 * mm,
    leftIndent=8 * mm,
)
HEADING2_STYLE = ParagraphStyle(
    name="Heading2",
    fontName=FONT_REG_NAME,
    fontSize=16,
    leading=22,
    textColor=(20, 60, 120),
    spaceBefore=10 * mm,
    spaceAfter=6 * mm,
)


def register_fonts() -> None:
    """注册项目自带 OFL 字体到 reportlab（幂等）。"""
    try:
        pdfmetrics.getFont(FONT_REG_NAME)
        return  # 已注册
    except KeyError:
        pass
    pdfmetrics.registerFont(TTFont(FONT_REG_NAME, str(SUBSET_FONT)))
    # 同一字体作为"加粗"使用（子集字体只含 Regular，无独立 Bold）


def escape_xml(text: str) -> str:
    """转义 XML 特殊字符，供 Paragraph 安全渲染。"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_pdf(path: Path, title: str, paragraphs: list[str], classics: str) -> int:
    """构造 PDF 并保存到 path，返回字节数。"""
    register_fonts()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=title,
    )
    story: list = []
    story.append(Paragraph(escape_xml(title), TITLE_STYLE))
    for para in paragraphs:
        story.append(Paragraph(escape_xml(para), BODY_STYLE))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("古籍原文节选", HEADING2_STYLE))
    for line in classics.split("\n"):
        if line.strip():
            story.append(Paragraph(escape_xml(line), CLASSICS_STYLE))
    doc.build(story)
    return path.stat().st_size


def main() -> int:
    ext = "pdf"
    out_dir = ensure_sample_dir(ext)
    title = "中文样本 PDF"

    # 小文件：5 段 + 500 字古籍 ≈ 10–30 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_pdf(
        small_path, title, chinese_paragraphs(5), classics_text(500)
    )

    # 中等文件：100 段（循环）+ 20000 字古籍 ≈ 150–400 KB
    medium_paragraphs = (chinese_paragraphs(10) * 15)[:100]
    medium_classics = classics_text(20000)
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_pdf(
        medium_path, title, medium_paragraphs, medium_classics
    )

    print(f"[pdf] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[pdf] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
