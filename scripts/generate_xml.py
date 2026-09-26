"""生成中文 XML 样本（基于标准库 xml.etree.ElementTree）。

按 AGENTS.md：
- 编码：UTF-8（无 BOM），XML 首行声明 `encoding="UTF-8"`
- 内容：Faker zh_CN 虚构人物数据序列化为层级 XML
- 大小档位：小 < 100 KB，中等 100 KB–1 MB
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _content import (  # noqa: E402
    ensure_sample_dir,
    faker_person_rows,
    sample_name,
)


def build_xml_bytes(rows: list[dict[str, str]]) -> bytes:
    """将虚构人物行数据序列化为 UTF-8 XML 字节串。

    结构：
        <?xml version='1.0' encoding='UTF-8'?>
        <persons count="N">
          <person id="1">
            <姓名>...</姓名>
            <性别>...</性别>
            ...
          </person>
          ...
        </persons>
    """
    root = ET.Element("persons")
    root.set("count", str(len(rows)))
    for idx, row in enumerate(rows, start=1):
        person = ET.SubElement(root, "person")
        person.set("id", str(idx))
        for field, value in row.items():
            elem = ET.SubElement(person, field)
            elem.text = value

    # XML 声明：encoding="UTF-8"，无 BOM；xml_declaration=True 才能输出声明
    # ET.tostring 默认 short_empty_elements=True，自闭合空标签会丢内容
    xml_bytes = ET.tostring(
        root,
        encoding="utf-8",
        method="xml",
        xml_declaration=True,
    )
    # ET 在 encoding="utf-8" 时声明写 encoding='utf-8'，按 AGENTS.md 改为大写
    # XML 规范不区分大小写但项目风格要求大写
    return xml_bytes.replace(b"encoding='utf-8'", b"encoding='UTF-8'")


def write_xml(path: Path, rows: list[dict[str, str]]) -> int:
    """写 XML 文件到 path，返回字节数。"""
    data = build_xml_bytes(rows)
    # 直接写 bytes，避免 open() 默认编码与 BOM 干扰
    path.write_bytes(data)
    return path.stat().st_size


def main() -> int:
    ext = "xml"
    out_dir = ensure_sample_dir(ext)

    # 小文件：30 行虚构人物 ≈ 5–8 KB
    small_path = out_dir / sample_name(ext, 1)
    small_size = write_xml(small_path, faker_person_rows(30))

    # 中等文件：2000 行虚构人物 ≈ 350–500 KB
    medium_path = out_dir / sample_name(ext, 2)
    medium_size = write_xml(medium_path, faker_person_rows(2000))

    print(f"[xml] 小: {small_path.name} ({small_size / 1024:.1f} KB)")
    print(f"[xml] 中: {medium_path.name} ({medium_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
