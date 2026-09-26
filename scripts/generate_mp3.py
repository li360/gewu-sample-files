"""生成中文 mp3 音频样本（基于 ffmpeg libmp3lame 转码 wav）。

按 AGENTS.md：
- 复用 generate_wav 的合成音频作为输入源
- 用 libmp3lame 编码器转码
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 不引用外部音乐，无版权风险
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    ensure_sample_dir,
    sample_name,
)


def find_ffmpeg() -> str:
    """定位 ffmpeg 可执行文件路径，找不到则抛错。"""
    exe = shutil.which("ffmpeg")
    if not exe:
        raise RuntimeError("未找到 ffmpeg，请安装并加入 PATH")
    return exe


def run_ffmpeg(args: list[str]) -> None:
    """执行 ffmpeg 命令，失败抛错。"""
    cmd = [find_ffmpeg(), "-y", *args]
    print(f"  $ {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        raise RuntimeError(f"ffmpeg 失败：{res.returncode}")


def build_mp3(path: Path, duration: float, frequency: int, sample_rate: int, bitrate_k: int) -> int:
    """合成单声道 mp3 文件，返回字节数。

    用 sine 滤镜生成纯音正弦波 → libmp3lame 编码。
    """
    src = f"sine=frequency={frequency}:duration={duration}:sample_rate={sample_rate}"
    run_ffmpeg([
        "-f", "lavfi", "-i", src,
        "-c:a", "libmp3lame",
        "-b:a", f"{bitrate_k}k",
        "-ar", str(sample_rate),
        "-ac", "1",  # 单声道
        str(path),
    ])
    return path.stat().st_size


def main() -> int:
    ext = "mp3"
    out_dir = ensure_sample_dir(ext)

    # 小文件：3 秒单声道 8kHz 64kbps，A4 440Hz ≈ 20–30 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_mp3(
        small_path, duration=3.0, frequency=440, sample_rate=8000, bitrate_k=64
    )

    # 中等文件：10 秒单声道 44.1kHz 192kbps，A3 220Hz ≈ 200–300 KB
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_mp3(
        medium_path, duration=10.0, frequency=220, sample_rate=44100, bitrate_k=192
    )

    print(f"[mp3] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[mp3] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
