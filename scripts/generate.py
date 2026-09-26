"""P0 + P1a 总入口：依次运行所有格式生成脚本（zip 必须最后运行）。

用法：
    uv run python scripts/generate.py

按 AGENTS.md 工作流，运行后应检查生成文件的大小、编码、字体渲染。
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# 模块顺序：zip 依赖其他格式已生成，放在最后
# jpg 复用 generate_png 的工具函数，需在 png 之后
# ini/cfg 在 zip 之前
MODULES = [
    "generate_txt",
    "generate_csv",
    "generate_png",
    "generate_docx",
    "generate_pdf",
    "generate_xlsx",
    "generate_pptx",
    "generate_jpg",
    "generate_xml",
    "generate_ini",
    "generate_zip",
]


def main() -> int:
    sys.path.insert(0, str(SCRIPTS_DIR))
    t0 = time.time()
    failures: list[tuple[str, str]] = []
    for mod_name in MODULES:
        print(f"\n=== {mod_name} ===")
        try:
            mod = importlib.import_module(mod_name)
            rc = mod.main()
            if rc != 0:
                failures.append((mod_name, f"exit code {rc}"))
        except Exception as e:
            failures.append((mod_name, f"{type(e).__name__}: {e}"))
    elapsed = time.time() - t0
    print(f"\n=== 汇总 ===")
    print(f"耗时 {elapsed:.1f}s")
    if failures:
        print(f"失败 {len(failures)} 个：")
        for m, err in failures:
            print(f"  - {m}: {err}")
        return 1
    print("全部成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
