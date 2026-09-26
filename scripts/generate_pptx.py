"""生成中文 pptx 样本（基于 python-pptx）。

按 AGENTS.md：
- 通过 python-pptx 指定字体名（思源黑体 CN），跨平台显示一致
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：标题幻灯片 + 多张内容幻灯片（自编段落 + Faker 段落）
"""
from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    chinese_paragraphs,
    ensure_sample_dir,
    faker,
    sample_name,
)

# 字体名：思源黑体 CN（不嵌字体文件，仅指定名称）
FONT_NAME = "Source Han Sans CN"

# 主题色
TITLE_COLOR = RGBColor(0x14, 0x3C, 0x78)  # 藏青
BODY_COLOR = RGBColor(0x28, 0x28, 0x28)   # 深炭


def set_run_font(run, size_pt: int = 18, bold: bool = False, color: RGBColor = BODY_COLOR) -> None:
    """给 run 应用思源黑体、字号、加粗、颜色。"""
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color
    # 中文字体也需 ea 字段，python-pptx 通过 name 即可，部分阅读器需 east_asia
    # 这里设置字体名通常已足够，python-pptx 1.0+ 会写入 rFonts.ea


def add_title_slide(prs: Presentation, title: str, subtitle: str) -> None:
    """添加标题幻灯片：使用 layout[0]（标题幻灯片版式）。"""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title_placeholder = slide.shapes.title
    subtitle_placeholder = slide.placeholders[1] if len(slide.placeholders) > 1 else None

    if title_placeholder:
        title_placeholder.text = title
        for para in title_placeholder.text_frame.paragraphs:
            for run in para.runs:
                set_run_font(run, size_pt=36, bold=True, color=TITLE_COLOR)
    if subtitle_placeholder:
        subtitle_placeholder.text = subtitle
        for para in subtitle_placeholder.text_frame.paragraphs:
            for run in para.runs:
                set_run_font(run, size_pt=20, color=BODY_COLOR)


def add_content_slide(prs: Presentation, heading: str, paragraphs: list[str]) -> None:
    """添加内容幻灯片：标题 + 多段正文。"""
    slide_layout = prs.slide_layouts[1]  # 标题+内容版式
    slide = prs.slides.add_slide(slide_layout)
    title_placeholder = slide.shapes.title
    content_placeholder = slide.placeholders[1] if len(slide.placeholders) > 1 else None

    if title_placeholder:
        title_placeholder.text = heading
        for para in title_placeholder.text_frame.paragraphs:
            for run in para.runs:
                set_run_font(run, size_pt=28, bold=True, color=TITLE_COLOR)

    if content_placeholder:
        tf = content_placeholder.text_frame
        # 第一段已有占位
        first = True
        for para_text in paragraphs:
            if first:
                p = tf.paragraphs[0]
                first = False
            else:
                p = tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = para_text
            set_run_font(run, size_pt=18, color=BODY_COLOR)


def build_pptx(path: Path, title: str, content_slides: list[tuple[str, list[str]]]) -> int:
    """构造 pptx 并保存到 path，返回字节数。"""
    prs = Presentation()
    add_title_slide(prs, title, "中文样本文件库 · 思源黑体渲染")

    for heading, paragraphs in content_slides:
        add_content_slide(prs, heading, paragraphs)

    prs.save(path)
    return path.stat().st_size


def main() -> int:
    ext = "pptx"
    out_dir = ensure_sample_dir(ext)
    title = "中文样本演示"

    # 小文件：3 张内容幻灯片（每张 2 段自编段落）≈ 30–60 KB
    small_slides = [
        (f"主题 {i}", chinese_paragraphs(2)) for i in range(1, 4)
    ]
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_pptx(small_path, title, small_slides)

    # 中等文件：30 张幻灯片，每张 12 段 × 20 句 Faker 段落 ≈ 130–250 KB
    medium_slides = [
        (f"Faker 段落集 {i}", [faker.paragraph(nb_sentences=20) for _ in range(12)])
        for i in range(1, 31)
    ]
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_pptx(medium_path, title, medium_slides)

    print(f"[pptx] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[pptx] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
