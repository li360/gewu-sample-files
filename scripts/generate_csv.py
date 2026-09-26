"""生成 UTF-8 with BOM 的中文 csv 样本。

按 AGENTS.md：
- 编码：UTF-8 with BOM（兼容 Windows Excel 直接打开不乱码）
- 内容：Faker zh_CN 生成的虚构人物数据
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    ensure_sample_dir,
    faker_person_rows,
    sample_name,
)

# Faker 字段顺序（与 _content.faker_person_rows 返回的 dict 键一致）
CSV_FIELDS = ["姓名", "性别", "年龄", "城市", "邮箱", "电话", "职位", "公司"]

# UTF-8 BOM：让 Windows Excel 直接识别为 UTF-8 而非 GBK
UTF8_BOM = "\ufeff"


def write_csv(path: Path, rows: list[dict[str, str]]) -> int:
    """写入 UTF-8 with BOM 的 CSV 文件，返回字节数。"""
    # csv 模块要求文件以 newline="" 打开，避免行尾被二次转换
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path.stat().st_size


def main() -> int:
    ext = "csv"
    out_dir = ensure_sample_dir(ext)

    # 小文件：30 行虚构人物 ≈ 3–5 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = write_csv(small_path, faker_person_rows(30))

    # 中等文件：2000 行虚构人物 ≈ 200–400 KB
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = write_csv(medium_path, faker_person_rows(2000))

    print(f"[csv] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[csv] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
