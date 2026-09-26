"""生成中文 mkv 视频样本（基于 ffmpeg lavfi + drawtext 叠加中文字体）。

按 AGENTS.md：
- 用 ffmpeg lavfi 生成测试图样（testsrc2），不引用外部视频
- 通过 drawtext 滤镜叠加中文文本，使用项目自带 OFL 子集字体
- 大小档位：小 < 100 KB（mkv 容器最小体积限制，目标 100–300 KB），
  中等 100 KB–1 MB
- 视频编码：libx264，yuv420p
- 音频编码：libopus（MKV 容器的现代开源编码，无许可风险）
- MKV 不需要 mp4 的 +faststart movflags
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import SUBSET_FONT, ensure_sample_dir, sample_name  # noqa: E402
from generate_mp4 import find_ffmpeg, run_ffmpeg  # 复用 ffmpeg 辅助函数


def build_mkv(
    path: Path,
    duration: float,
    size: tuple[int, int],
    fps: int,
    pattern: str,
    text_overlay: str,
    crf: int,
    audio_freq: int | None = None,
) -> int:
    """生成 mkv 文件，返回字节数。

    pattern: lavfi 视频源（testsrc2 / smptebars 等）
    text_overlay: 叠加的中文文本（使用项目自带字体避免 Linux/CI 方块）
    crf: x264 质量（18-28，越大越压缩）
    audio_freq: 若非 None，叠加 sine 纯音音轨（libopus 编码，无版权风险）
    """
    width, height = size
    font_path_escaped = str(SUBSET_FONT).replace("\\", "/").replace(":", r"\:")
    vf = (
        f"drawtext="
        f"fontfile='{font_path_escaped}':"
        f"text='{text_overlay}':"
        f"fontsize={max(24, height // 20)}:"
        f"fontcolor=white:"
        f"borderw=2:bordercolor=black:"
        f"x=(w-text_w)/2:y=h-60"
    )

    cmd: list[str] = [
        "-f", "lavfi", "-i", f"{pattern}=size={width}x{height}:rate={fps}",
    ]
    if audio_freq is not None:
        cmd += ["-f", "lavfi", "-i", f"sine=frequency={audio_freq}:duration={duration}:sample_rate=44100"]

    cmd += [
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", str(crf),
    ]
    if audio_freq is not None:
        # libopus：MKV 容器推荐的现代开源音频编码
        cmd += ["-c:a", "libopus", "-b:a", "96k", "-shortest"]
    cmd += [str(path)]  # MKV 不需要 +faststart

    run_ffmpeg(cmd)
    return path.stat().st_size


def main() -> int:
    ext = "mkv"
    out_dir = ensure_sample_dir(ext)

    # 小文件：5 秒 320×180 15fps，testsrc2 + 标题，无音轨
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_mkv(
        small_path,
        duration=5.0,
        size=(320, 180),
        fps=15,
        pattern="testsrc2",
        text_overlay="中文样本视频 MKV",
        crf=30,
        audio_freq=None,
    )

    # 中等文件：15 秒 960×540 30fps，动态测试图 + 标题 + 220Hz 纯音轨
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_mkv(
        medium_path,
        duration=15.0,
        size=(960, 540),
        fps=30,
        pattern="testsrc2",
        text_overlay="中文样本文件库 · MKV 容器测试 · 思源黑体 · 含音轨",
        crf=25,
        audio_freq=220,
    )

    print(f"[mkv] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[mkv] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
