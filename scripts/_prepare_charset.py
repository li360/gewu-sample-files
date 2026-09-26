"""生成 GB 2312 一级字符集文本，供 fonttools subset CLI 使用。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "fonts" / "_source" / "charset.txt"


def build_gb2312_charset() -> set[str]:
    """构建 GB 2312 一级常用字 + ASCII + 中文常用标点的字符集。"""
    chars: set[str] = set()
    for c in range(0x20, 0x7F):
        chars.add(chr(c))
    for high in range(0xB0, 0xD8):
        for low in range(0xA1, 0xFF):
            try:
                ch = bytes([high, low]).decode("gb2312")
                chars.add(ch)
            except (UnicodeDecodeError, ValueError):
                continue
    chars.update("，。、；：？！""''《》（）【】—…·～")
    chars.update("ⅠⅡⅢⅣⅤ①②③④⑤⑥⑦⑧⑨⑩")
    return chars


def main() -> int:
    chars = build_gb2312_charset()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(sorted(chars)), encoding="utf-8")
    print(f"[charset] {len(chars)} chars -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
