"""生成中文 zip 样本（标准库 zipfile）。

按 AGENTS.md：
- 打包已生成的其他格式样本，让 zip 解压测试同时验证其他格式
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 重复运行覆盖同名文件
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import SAMPLES_DIR, ensure_sample_dir, sample_name  # noqa: E402

# 要打包的源目录（不含 zip 自身）
# 覆盖 P0 + P1a + P1b 已实现格式；新增格式时同步追加
SOURCE_DIRS = ["txt", "csv", "docx", "pdf", "png", "xlsx", "pptx", "jpg", "xml", "ini", "cfg", "wav", "mp3", "mp4", "mkv", "dxf"]


def collect_source_files() -> list[tuple[Path, str]]:
    """收集各格式下的小文件，返回 (绝对路径, zip 内路径) 列表。"""
    files: list[tuple[Path, str]] = []
    for sub in SOURCE_DIRS:
        d = SAMPLES_DIR / sub
        if not d.exists():
            continue
        for f in sorted(d.iterdir()):
            if f.is_file():
                arc = f"{sub}/{f.name}"
                files.append((f, arc))
    return files


def build_zip(path: Path, files: list[tuple[Path, str]]) -> int:
    """打包 files 到 path（ZIP_DEFLATED），返回字节数。"""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for src, arc in files:
            zf.write(src, arc)
    return path.stat().st_size


def main() -> int:
    ext = "zip"
    out_dir = ensure_sample_dir(ext)
    sources = collect_source_files()
    if not sources:
        print("[zip][warn] 未找到源文件，请先运行其他 P0 脚本", file=sys.stderr)
        return 1

    # 小文件：仅打包各格式的小文件（序号 01）
    small_files = [(s, a) for s, a in sources if "_01." in s.name]
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_zip(small_path, small_files)

    # 中等文件：打包所有格式小文件 + 非音视频格式的中等文件
    # 音视频（wav/mp3/mp4/mkv）中等文件本身接近 5MB，打包进 zip 会超 AGENTS.md 5MB 上限
    AV_EXTS = {"wav", "mp3", "mp4", "mkv"}
    medium_files = [
        (s, a) for s, a in sources
        if "_01." in s.name or (s.suffix.lstrip(".").lower() not in AV_EXTS and "_02." in s.name)
    ]
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_zip(medium_path, medium_files)

    print(f"[zip] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[zip] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
