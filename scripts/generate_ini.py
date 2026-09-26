"""生成中文 INI / CFG 文本样本（基于标准库 configparser）。

按 AGENTS.md：
- 编码：UTF-8（无 BOM）
- ini 与 cfg 内容完全一致，仅扩展名不同（同一 configparser 文本）
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：应用配置节段 + Faker zh_CN 虚构人物作为占位数据
"""
from __future__ import annotations

import configparser
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    ensure_sample_dir,
    faker,
    faker_person_rows,
)

# 同时输出 ini 和 cfg 两个目录
TARGET_EXTS = ["ini", "cfg"]


def build_config(rows: list[dict[str, str]]) -> str:
    """构造 configparser 文本，返回字符串。

    结构：
        [app]
        name = 中文样本文件库
        version = 0.1.0
        language = zh-CN

        [users]
        count = N
        sample_0_name = 张三
        sample_0_email = ...
        ...

        [runtime]
        timeout_seconds = 30
        log_level = INFO
    """
    cp = configparser.ConfigParser()
    # 保持键大小写，避免 lower-case 默认行为影响示例展示
    cp.optionxform = str

    cp["app"] = {
        "name": "中文样本文件库",
        "version": "0.1.0",
        "language": "zh-CN",
        "description": "用于文件上传/下载/预览/转换的测试样本",
    }
    cp["runtime"] = {
        "timeout_seconds": "30",
        "log_level": "INFO",
        "max_workers": "4",
        "data_dir": "samples/ini",
    }

    # 用户数据作为键值对写入（小文件用前 N 行，大文件用全部）
    cp["users"] = {
        "count": str(len(rows)),
    }
    for i, row in enumerate(rows):
        for field in ("姓名", "邮箱", "城市", "公司"):
            # 键名用 ASCII + 序号，值用中文，便于阅读与编码测试
            cp["users"][f"user_{i:04d}_{field}"] = row[field]

    # 用 StringIO 写出，避免 configparser 写文件时的 newline 默认行为
    import io
    buf = io.StringIO()
    cp.write(buf)
    return buf.getvalue()


def write_sample(path: Path, content: str) -> int:
    """写文本到指定路径，UTF-8 无 BOM，返回字节数。"""
    # newline="" 让 configparser 自己的 \n 不被系统转为 \r\n
    data = content.encode("utf-8")  # 默认无 BOM
    path.write_bytes(data)
    return path.stat().st_size


def make_sample_name(ext: str, idx: int) -> str:
    """构造样本文件名：中文示例_<ext>_<idx>.<ext>。"""
    return f"中文示例_{ext}_{idx:02d}.{ext}"


def main() -> int:
    # 小：30 行；中：2000 行
    small_rows = faker_person_rows(30)
    medium_rows = faker_person_rows(2000)

    for ext in TARGET_EXTS:
        out_dir = ensure_sample_dir(ext)

        small_name = make_sample_name(ext, 1)
        small_path = out_dir / small_name
        small_content = build_config(small_rows)
        small_size = write_sample(small_path, small_content)

        medium_name = make_sample_name(ext, 2)
        medium_path = out_dir / medium_name
        medium_content = build_config(medium_rows)
        medium_size = write_sample(medium_path, medium_content)

        print(f"[{ext}] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
        print(f"[{ext}] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
