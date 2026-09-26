"""准备 OFL 中文字体：下载思源黑体并子集化到常用字符集。

子集化策略：保留 GB 2312 一级常用 3755 字 + ASCII + 常用标点，
输出文件控制在 1–2 MB 之间，便于直接入 git（< 5 MB）。

可重复运行：源字体已存在则跳过下载，子集已存在则跳过子集。
"""
from __future__ import annotations

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

# 项目根目录（脚本在 scripts/ 下，根是上一级）
ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "fonts" / "_source"
OUTPUT_DIR = ROOT / "assets" / "fonts"
SOURCE_OTF = SOURCE_DIR / "SourceHanSansCN-VF.ttf"
# 子集输出为 TTF（glyf outlines），reportlab TTFont 必需
SUBSET_OTF = OUTPUT_DIR / "SourceHanSansSC-Regular-subset.ttf"
LICENSE_FILE = OUTPUT_DIR / "LICENSE-OFL.txt"

# Adobe 官方 Variable TTF 子集（约 17.7 MB，glyf 格式），reportlab 直接可用
# 优先 jsdelivr CDN 镜像（国内访问更稳定），失败时自动回退 raw.githubusercontent
SOURCE_URL_PRIMARY = (
    "https://cdn.jsdelivr.net/gh/adobe-fonts/source-han-sans"
    "@release/Variable/TTF/Subset/SourceHanSansCN-VF.ttf"
)
SOURCE_URL_FALLBACK = (
    "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/"
    "release/Variable/TTF/Subset/SourceHanSansCN-VF.ttf"
)

# OFL-1.1 许可证全文（取自 Adobe source-han-sans 仓库 LICENSE.txt）
OFL_LICENSE_URLS = [
    "https://cdn.jsdelivr.net/gh/adobe-fonts/source-han-sans@release/LICENSE.txt",
    "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/release/LICENSE.txt",
]


def download_source_font() -> None:
    """下载思源黑体 CN Regular 子集 OTF 到 _source/ 目录。

    幂等：文件已存在则跳过。优先 jsdelivr CDN，失败回退 GitHub raw。
    """
    if SOURCE_OTF.exists() and SOURCE_OTF.stat().st_size > 1024 * 1024:
        print(f"[skip] 源字体已存在: {SOURCE_OTF}")
        return
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [SOURCE_URL_PRIMARY, SOURCE_URL_FALLBACK]
    last_err: Exception | None = None
    for url in candidates:
        print(f"[download] {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "zh-sample-files/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp, SOURCE_OTF.open("wb") as f:
                f.write(resp.read())
            print(f"[done] {SOURCE_OTF.stat().st_size / 1024 / 1024:.2f} MB -> {SOURCE_OTF}")
            return
        except Exception as e:
            print(f"[warn] 失败: {e}")
            last_err = e
            if SOURCE_OTF.exists():
                SOURCE_OTF.unlink()
    raise RuntimeError(f"所有下载源均失败，最后错误：{last_err}")


def write_ofl_license() -> None:
    """写入 OFL-1.1 许可证文本到 assets/fonts/LICENSE-OFL.txt。

    幂等：已存在则跳过。优先 jsdelivr，失败回退 GitHub raw。
    """
    if LICENSE_FILE.exists() and LICENSE_FILE.stat().st_size > 1000:
        print(f"[skip] 许可证已存在: {LICENSE_FILE}")
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    last_err: Exception | None = None
    for url in OFL_LICENSE_URLS:
        print(f"[download] OFL license <- {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "zh-sample-files/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                LICENSE_FILE.write_text(resp.read().decode("utf-8"), encoding="utf-8")
            print(f"[done] {LICENSE_FILE}")
            return
        except Exception as e:
            print(f"[warn] 失败: {e}")
            last_err = e
    raise RuntimeError(f"OFL 许可证下载失败，最后错误：{last_err}")


def build_gb2312_charset() -> set[str]:
    """构建 GB 2312 一级常用字 + ASCII + 中文常用标点的字符集。

    GB 2312 一级字（共 3755 字）覆盖 99% 中文日常文本，
    子集后字体大小可控制在 1–2 MB。
    """
    chars: set[str] = set()
    # ASCII 可见字符
    for c in range(0x20, 0x7F):
        chars.add(chr(c))
    # GB 2312 一级字（0xB0A1 - 0xD7F9）
    # 通过 cp936 编码遍历构造
    for high in range(0xB0, 0xD8):
        for low in range(0xA1, 0xFF):
            try:
                ch = bytes([high, low]).decode("gb2312")
                chars.add(ch)
            except (UnicodeDecodeError, ValueError):
                continue
    # 常用中文标点（全角）
    chars.update("，。、；：？！""''《》（）【】—…·～")
    # 数字与罗马字母补充
    chars.update("ⅠⅡⅢⅣⅤ①②③④⑤⑥⑦⑧⑨⑩")
    return chars


def subset_font() -> None:
    """用 fonttools pyftsubset 子集化字体到常用字符集。

    幂等：子集已存在则跳过。
    """
    if SUBSET_OTF.exists() and SUBSET_OTF.stat().st_size > 100 * 1024:
        print(f"[skip] 子集字体已存在: {SUBSET_OTF}")
        return
    from fontTools import subset

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chars = build_gb2312_charset()
    print(f"[subset] 字符集大小: {len(chars)}")

    # 使用 fonttools subset API
    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.recalc_bounds = True
    options.recalc_timestamp = False
    options.drop_tables = ["DSIG"]
    # 源是 Variable TTF（glyf outlines），保留 VF 结构；reportlab 用默认实例
    options.flavor = None
    options.with_zopfli = True

    font = subset.load_font(str(SOURCE_OTF), options, lazy=False)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text="".join(sorted(chars)))
    subsetter.subset(font)
    buffer = io.BytesIO()
    font.save(buffer, options)
    SUBSET_OTF.write_bytes(buffer.getvalue())
    print(f"[done] {SUBSET_OTF.stat().st_size / 1024:.1f} KB -> {SUBSET_OTF}")


def main() -> int:
    """主流程：下载 → 写入许可证 → 子集化。"""
    try:
        download_source_font()
    except Exception as e:
        print(f"[error] 下载源字体失败: {e}", file=sys.stderr)
        print("请检查网络或手动放置思源黑体到 assets/fonts/_source/", file=sys.stderr)
        return 1
    try:
        write_ofl_license()
    except Exception as e:
        print(f"[warn] 写入 OFL 许可证失败: {e}", file=sys.stderr)
    try:
        subset_font()
    except Exception as e:
        print(f"[error] 子集化字体失败: {e}", file=sys.stderr)
        return 2
    print("\n[ok] 字体准备完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
