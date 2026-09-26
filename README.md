# 中文示例文件库（zh-sample-files）

为开发者提供无版权、可脚本生成的中文样本文件，覆盖 txt / csv / docx / pdf / png / zip 等多种格式，适用于文件管理、上传下载、预览、格式转换等测试场景。

## 特性

- **中文优先**：所有样本内容以中文为主
- **无版权风险**：脚本与样本采用 MIT / CC0 双许可，字体采用 OFL-1.1
- **可复现**：通过 `uv` 管理依赖与锁文件，一键重建环境
- **跨平台字体**：项目自带思源黑体子集，避免 Linux/CI 渲染方块

## 快速开始

```powershell
# 1. 安装 uv（如未安装）
# 见 https://docs.astral.sh/uv/

# 2. 同步依赖（uv 会自动安装所需 Python 版本与依赖）
uv sync

# 3. 生成全部 P0 样本（txt/csv/docx/pdf/png/zip）
uv run python scripts/generate.py
```

## 目录结构

```text
zh-sample-files/
├── AGENTS.md          # 项目规范与 AI 行为约束
├── LICENSE            # MIT（代码）+ CC0（样本）+ OFL（字体）
├── README.md
├── pyproject.toml     # 依赖声明
├── uv.lock            # 依赖锁文件（保证可复现）
├── assets/fonts/      # OFL 字体子集
├── scripts/           # 生成脚本（每种格式一个）
├── samples/           # 生成的样本文件（CC0）
└── docs/formats.md    # 各格式样本的元数据
```

## 已支持的格式（P0）

| 格式 | 编码 | 小文件 | 中等文件 | 内容来源 |
|------|------|--------|----------|----------|
| txt  | UTF-8（无 BOM） | 2.6 KB | 193.3 KB | 自编段落 + 古籍原文 |
| csv  | UTF-8 with BOM | 3.1 KB | 200.4 KB | Faker zh_CN 虚构人物 |
| docx | — | 37.2 KB | 140.9 KB | Faker 段落 + 古籍原文 |
| pdf  | — | 70.7 KB | 149.3 KB | 自编段落 + 古籍原文 |
| png  | — | 56.9 KB | 338.6 KB | Pillow + 思源字体 |
| zip  | — | 159.8 KB | 800.2 KB | 打包上述样本 |

完整元数据（字体、测试场景）见 [docs/formats.md](docs/formats.md)。

## 许可证

- 代码、脚本、配置：**MIT**
- `samples/` 下生成的样本文件：**CC0-1.0**
- `assets/fonts/` 下的字体：按其原始许可证（OFL-1.1），见目录内 LICENSE 文件

## 生成规则摘要

- 每个格式至少生成 1 个小文件（<100 KB）和 1 个中等文件（100 KB–1 MB）
- 单个样本文件默认不超过 5 MB
- 生成脚本必须可重复运行（输出到固定目录、覆盖同名文件）
- 命名规范：`中文示例_<ext>_<序号>.<ext>`，例如 `中文示例_csv_01.csv`

详见 [AGENTS.md](AGENTS.md)。
