"""生成中文 dxf 样本（基于 ezdxf，MIT 许可）。

按 AGENTS.md：
- 用 ezdxf 绘制几何图形（线、圆、矩形、多边形）+ 中文文字标注
- 文字样式指定字体名 Source Han Sans CN（与 docx/pptx 一致）
- 内容：示例化标注（示例公司、示例市等），无版权风险
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
- dxf 是 AutoCAD 的开源交换格式，dwg 是专有格式（不支持）
"""
from __future__ import annotations

import sys
from pathlib import Path

import ezdxf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import ensure_sample_dir, sample_name  # noqa: E402

# 字体名：与 docx/pptx 保持一致，dxf 文字样式引用此名称
FONT_NAME = "Source Han Sans CN"


def build_dxf(
    path: Path,
    title: str,
    shapes_count: int,
    include_table: bool = False,
) -> int:
    """生成 dxf 文件，返回字节数。

    title: 图纸标题（中文）
    shapes_count: 绘制的几何图形组数（控制文件大小）
    include_table: 是否包含示例数据表格
    """
    doc = ezdxf.new("R2010")

    # 添加文字样式，指定中文字体名
    # dxf 文字样式通过 font 属性引用字体，实际渲染依赖查看器
    doc.styles.add("ZH_STYLE", font=FONT_NAME + ".ttf")
    doc.header["$TEXTSTYLE"] = "ZH_STYLE"

    msp = doc.modelspace()

    # 图层定义（颜色按 AutoCAD 索引）
    doc.layers.add("标题", color=1)      # 红
    doc.layers.add("图形", color=3)      # 绿
    doc.layers.add("标注", color=5)      # 蓝
    if include_table:
        doc.layers.add("表格", color=7)  # 白

    # 顶部标题
    msp.add_text(
        title,
        dxfattribs={"layer": "标题", "height": 5, "style": "ZH_STYLE"},
    ).set_placement((0, 30))

    # 绘制几何图形组（每组包含线、圆、矩形）
    import math
    for i in range(shapes_count):
        x_offset = (i % 5) * 30
        y_offset = (i // 5) * -20

        # 矩形（四条线）
        x1, y1 = x_offset, y_offset
        x2, y2 = x_offset + 15, y_offset + 10
        msp.add_line((x1, y1), (x2, y1), dxfattribs={"layer": "图形"})
        msp.add_line((x2, y1), (x2, y2), dxfattribs={"layer": "图形"})
        msp.add_line((x2, y2), (x1, y2), dxfattribs={"layer": "图形"})
        msp.add_line((x1, y2), (x1, y1), dxfattribs={"layer": "图形"})

        # 圆
        center = (x_offset + 7.5, y_offset + 5)
        msp.add_circle(center, 4, dxfattribs={"layer": "图形"})

        # 标注文字（示例化）
        msp.add_text(
            f"示例图形{i + 1:03d}",
            dxfattribs={"layer": "标注", "height": 2, "style": "ZH_STYLE"},
        ).set_placement((x_offset, y_offset - 2))

    # 可选：示例数据表格（MTEXT 多行文字模拟）
    if include_table:
        table_y = -40
        # 表头
        headers = ["序号", "示例公司", "示例市", "邮箱"]
        col_widths = [10, 25, 20, 30]
        x = 0
        for h, w in zip(headers, col_widths):
            msp.add_text(
                h,
                dxfattribs={"layer": "表格", "height": 3, "style": "ZH_STYLE"},
            ).set_placement((x, table_y))
            x += w
        # 表格行（示例化数据）
        for row in range(20):
            y = table_y - (row + 1) * 5
            cells = [
                f"{row + 1:03d}",
                f"示例公司{row + 1:03d}",
                f"示例市{row + 1:03d}",
                f"user{row + 1:03d}@example.com",
            ]
            x = 0
            for cell, w in zip(cells, col_widths):
                msp.add_text(
                    cell,
                    dxfattribs={"layer": "表格", "height": 2.5, "style": "ZH_STYLE"},
                ).set_placement((x, y))
                x += w

    doc.saveas(path)
    return path.stat().st_size


def main() -> int:
    ext = "dxf"
    out_dir = ensure_sample_dir(ext)

    # 小文件：5 组图形 + 标题，无表格
    small_path = out_dir / sample_name(ext, 1)
    small_size = build_dxf(
        small_path,
        title="中文样本图纸 DXF",
        shapes_count=5,
        include_table=False,
    )

    # 中等文件：100 组图形 + 20 行表格
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = build_dxf(
        medium_path,
        title="中文样本文件库 · DXF 格式测试 · 示例化数据",
        shapes_count=100,
        include_table=True,
    )

    print(f"[dxf] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[dxf] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
