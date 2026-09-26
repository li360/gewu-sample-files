"""生成中文 mp4 视频样本（基于 ffmpeg lavfi + drawtext 叠加中文字体）。

按 AGENTS.md：
- 用 ffmpeg lavfi 生成测试图样（testsrc / smptebars），不引用外部视频
- 通过 drawtext 滤镜叠加中文文本，使用项目自带 OFL 子集字体
- 大小档位：小 < 100 KB（受限于此处不可能，mp4 容器最小约 50–200 KB，按"小"目标尽量压），
  中等 100 KB–1 MB
- 视频编码：libx264，yuv420p，无音频流（减少体积）
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    SUBSET_FONT,
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


def build_mp4(path: Path, duration: float, size: tuple[int, int], fps: int, pattern: str, text_overlay: str, crf: int, audio_freq: int | None = None) -> int:
    """生成 mp4 文件，返回字节数。

    pattern: lavfi 视频源（testsrc2 / smptebars / gradients 等）
    text_overlay: 叠加的中文文本（使用项目自带字体避免 Linux/CI 方块）
    crf: x264 质量（18-28，越大越压缩）
    audio_freq: 若非 None，叠加 sine 纯音音轨（无版权风险）
    """
    width, height = size
    font_path_escaped = str(SUBSET_FONT).replace("\\", "/").replace(":", r"\:")
    # drawtext 文本用单引号包裹；中文需 UTF-8；fontfile 用 Windows 路径转义
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
        # 叠加 sine 纯音音轨
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
        cmd += [
            "-c:a", "aac", "-b:a", "96k",  # AAC 96kbps 音轨
            "-shortest",
        ]
    cmd += ["-movflags", "+faststart", str(path)]  # web 友好：moov atom 前置

    run_ffmpeg(cmd)
    return path.stat().st_size


def main() -> int:
    ext = "mp4"
    out_dir = ensure_sample_dir(ext)

    # 小文件：5 秒 320×180 15fps，testsrc2 + 标题，无音轨（极致压缩）
    # mp4 容器最小体积限制：< 100 KB 不现实，目标 100–300 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_mp4(
        small_path,
        duration=5.0,
        size=(320, 180),
        fps=15,
        pattern="testsrc2",
        text_overlay="中文样本视频",
        crf=30,
        audio_freq=None,
    )

    # 中等文件：15 秒 960×540 30fps，动态测试图 + 标题 + 220Hz 纯音轨
    # 目标：3–5 MB（在 AGENTS.md 5 MB 上限内）
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_mp4(
        medium_path,
        duration=15.0,
        size=(960, 540),
        fps=30,
        pattern="testsrc2",
        text_overlay="中文样本文件库 · 思源黑体渲染测试 · 含音轨",
        crf=25,
        audio_freq=220,
    )

    print(f"[mp4] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[mp4] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
