"""生成中文 xlsx 样本（基于 openpyxl）。

按 AGENTS.md：
- 使用 Faker zh_CN 虚构人物数据
- 通过 openpyxl 设置字体名（思源黑体 CN），跨平台显示一致
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- 内容：表头 + 行数据
"""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    ensure_sample_dir,
    faker_person_rows,
    sample_name,
)

# 字体名：思源黑体 CN（不嵌字体文件，仅指定名称）
FONT_NAME = "Source Han Sans CN"

# 表头字段顺序（与 _content.faker_person_rows 返回的 dict 键一致）
XLSX_FIELDS = ["姓名", "性别", "年龄", "城市", "邮箱", "电话", "职位", "公司"]


def apply_header_style(cell) -> None:
    """给表头单元格应用：思源黑体、加粗、浅色底色、居中。"""
    cell.font = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="2C5AA0")
    cell.alignment = Alignment(horizontal="center", vertical="center")


def apply_body_style(cell) -> None:
    """给正文单元格应用：思源黑体、常规、左对齐。"""
    cell.font = Font(name=FONT_NAME, size=10)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def build_xlsx(path: Path, rows: list[dict[str, str]]) -> int:
    """构造 xlsx 并保存到 path，返回字节数。"""
    wb = Workbook()
    ws = wb.active
    ws.title = "虚构人物样本"

    # 写表头
    for col_idx, field in enumerate(XLSX_FIELDS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=field)
        apply_header_style(cell)

    # 写数据行
    for row_idx, row in enumerate(rows, start=2):
        for col_idx, field in enumerate(XLSX_FIELDS, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=row[field])
            apply_body_style(cell)

    # 自适应列宽：按字段名长度估算
    for col_idx, field in enumerate(XLSX_FIELDS, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = max(
            len(field) * 2 + 4, 12
        )

    # 冻结首行
    ws.freeze_panes = "A2"

    wb.save(path)
    return path.stat().st_size


def main() -> int:
    ext = "xlsx"
    out_dir = ensure_sample_dir(ext)

    # 小文件：30 行虚构人物 ≈ 4–6 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_xlsx(small_path, faker_person_rows(30))

    # 中等文件：2000 行虚构人物 ≈ 200–400 KB
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_xlsx(medium_path, faker_person_rows(2000))

    print(f"[xlsx] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[xlsx] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
