"""生成 UTF-8（无 BOM）中文 txt 样本。

按 AGENTS.md：
- 编码：UTF-8（无 BOM）
- 内容：自编段落 + 古籍原文
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    chinese_paragraphs,
    classics_text,
    ensure_sample_dir,
    sample_name,
)


def write_txt(path: Path, paragraphs: list[str], classics: str) -> int:
    """写入 UTF-8 无 BOM 文本文件，返回字节数。"""
    body = "\n\n".join(paragraphs) + "\n\n----\n\n" + classics + "\n"
    # encoding="utf-8" 默认不写 BOM；newline="\n" 保证 LF 行尾
    path.write_text(body, encoding="utf-8", newline="\n")
    return path.stat().st_size


def main() -> int:
    ext = "txt"
    out_dir = ensure_sample_dir(ext)

    # 小文件：5 段自编 + 500 字古籍 ≈ 2–5 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = write_txt(
        small_path,
        chinese_paragraphs(5),
        classics_text(500),
    )

    # 中等文件：循环填充至 200–300 KB
    medium_paragraphs = (chinese_paragraphs(10) * 50)[:200]
    medium_classics = classics_text(50000)
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = write_txt(medium_path, medium_paragraphs, medium_classics)

    print(f"[txt] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[txt] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
