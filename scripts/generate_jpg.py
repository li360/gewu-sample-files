"""生成中文 JPG 图片样本（基于 Pillow）。

按 AGENTS.md：
- 复用 generate_png 的渲染逻辑（标题 + 自编段落 + 思源字体）
- 仅输出格式为 JPEG（无 alpha 通道，无透明背景）
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
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
from generate_png import wrap_text  # 复用 png 的换行工具函数

# 调色板：与 png 保持一致；JPEG 无 alpha，背景必须实色
BG_COLOR = (245, 245, 240)  # 米白
TEXT_COLOR = (40, 40, 40)    # 深炭
TITLE_COLOR = (20, 60, 120)  # 藏青


def render_jpg(path: Path, title: str, paragraphs: list[str], size: tuple[int, int], quality: int = 88) -> int:
    """渲染指定尺寸的中文 JPG，返回字节数。

    quality: JPEG 压缩质量（1–95），默认 88 兼顾体积与清晰度。
    """
    width, height = size
    img = Image.new("RGB", size, BG_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(str(SUBSET_FONT), 36)
    body_font = ImageFont.truetype(str(SUBSET_FONT), 22)

    margin_x, margin_y = 40, 40
    draw.text((margin_x, margin_y), title, fill=TITLE_COLOR, font=title_font)
    margin_y += 60

    max_x = width - margin_x * 2
    for para in paragraphs:
        wrapped = wrap_text(para, body_font, max_x, draw)
        for line in wrapped:
            draw.text((margin_x, margin_y), line, fill=TEXT_COLOR, font=body_font)
            margin_y += 32
        margin_y += 16  # 段间距

    # JPEG 优化：quality + optimize=True
    img.save(path, format="JPEG", quality=quality, optimize=True, progressive=True)
    return path.stat().st_size


def main() -> int:
    ext = "jpg"
    out_dir = ensure_sample_dir(ext)
    title = "中文样本图片"

    # 小文件：600×400，3 段（复用 png 的内容/尺寸）
    small_path = out_dir / sample_name(ext, 1)
    small_size = render_jpg(
        small_path, title, chinese_paragraphs(3), (600, 400)
    )

    # 中等文件：1600×1200，30 段（复用 png 的内容/尺寸）
    medium_paragraphs = (chinese_paragraphs(10) * 3)[:30]
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = render_jpg(
        medium_path, title, medium_paragraphs, (1600, 1200)
    )

    print(f"[jpg] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[jpg] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
