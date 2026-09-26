"""生成中文 wav 音频样本（基于 ffmpeg sine 滤镜合成正弦波）。

按 AGENTS.md：
- 不引用任何外部音乐，纯合成音频（无版权风险）
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：单频正弦波（sine 滤镜，参数简单可靠）
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


def build_wav(path: Path, duration: float, frequency: int, sample_rate: int) -> int:
    """合成单声道 wav 文件，返回字节数。

    用 sine 滤镜生成纯音正弦波，无表达式解析风险。
    """
    src = f"sine=frequency={frequency}:duration={duration}:sample_rate={sample_rate}"
    run_ffmpeg([
        "-f", "lavfi", "-i", src,
        "-c:a", "pcm_s16le",  # 16-bit PCM，标准 wav 编码
        "-ar", str(sample_rate),
        "-ac", "1",  # 单声道
        str(path),
    ])
    return path.stat().st_size


def main() -> int:
    ext = "wav"
    out_dir = ensure_sample_dir(ext)

    # 小文件：3 秒单声道 8kHz，A4 440Hz 正弦波 ≈ 47 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_wav(small_path, duration=3.0, frequency=440, sample_rate=8000)

    # 中等文件：10 秒单声道 44.1kHz，A3 220Hz 正弦波 ≈ 860 KB
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_wav(medium_path, duration=10.0, frequency=220, sample_rate=44100)

    print(f"[wav] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[wav] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
