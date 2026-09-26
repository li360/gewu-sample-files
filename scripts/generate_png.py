"""生成中文 PNG 图片样本。

按 AGENTS.md：
- 用 Pillow 在画布上绘制中文段落，使用项目自带 OFL 子集字体
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：自编段落 + 标题
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    SUBSET_FONT,
    chinese_paragraphs,
    ensure_sample_dir,
    sample_name,
)

# 调色板：浅背景 + 深字色，符合中文文档审美
BG_COLOR = (245, 245, 240)  # 米白
TEXT_COLOR = (40, 40, 40)    # 深炭
TITLE_COLOR = (20, 60, 120)  # 藏青


def render_png(path: Path, title: str, paragraphs: list[str], size: tuple[int, int]) -> int:
    """渲染指定尺寸的中文 PNG，返回字节数。"""
    width, height = size
    img = Image.new("RGB", size, BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 标题字体（稍大）
    title_font = ImageFont.truetype(str(SUBSET_FONT), 36)
    body_font = ImageFont.truetype(str(SUBSET_FONT), 22)

    # 顶部留白
    margin_x, margin_y = 40, 40

    # 绘制标题
    draw.text((margin_x, margin_y), title, fill=TITLE_COLOR, font=title_font)
    margin_y += 60

    # 绘制段落（自动换行）
    max_x = width - margin_x * 2
    for para in paragraphs:
        wrapped = wrap_text(para, body_font, max_x, draw)
        for line in wrapped:
            draw.text((margin_x, margin_y), line, fill=TEXT_COLOR, font=body_font)
            margin_y += 32
        margin_y += 16  # 段间距

    img.save(path, format="PNG", optimize=True)
    return path.stat().st_size


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """按像素宽度将文本换行为多行（中文按字断行）。"""
    lines: list[str] = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width:
            if current:
                lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def main() -> int:
    ext = "png"
    out_dir = ensure_sample_dir(ext)

    title = "中文样本图片"

    # 小文件：600×400，3 段
    small_path = out_dir / sample_name(ext, 1)
    small_size = render_png(
        small_path, title, chinese_paragraphs(3), (600, 400)
    )

    # 中等文件：1600×1200，10 段（循环填充）
    medium_paragraphs = (chinese_paragraphs(10) * 3)[:30]
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = render_png(
        medium_path, title, medium_paragraphs, (1600, 1200)
    )

    print(f"[png] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[png] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
