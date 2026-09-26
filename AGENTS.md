# AGENTS.md

## 项目使命

本项目是“中文示例文件库（zh-sample-files）”，目标是为开发者提供：
- 中文内容
- 无版权或明确 CC0/MIT 许可
- 覆盖多种格式
- 可直接下载或通过脚本生成
- 用于文件管理、上传下载、预览、格式转换等测试场景

## 许可证

- 代码、脚本、配置：MIT
- `AGENTS.md`、`README.md`、`docs/` 等项目级文档：MIT
- `samples/` 下由本项目生成的样本文件：CC0-1.0
- `assets/fonts/` 下的字体（思源黑体 CN 子集 `SourceHanSansSC-Regular-subset.ttf` + `LICENSE-OFL.txt`）按 OFL-1.1 许可，单独标注；OFL 不可与 MIT 合并为单一许可证
- 第三方来源文件必须单独标注来源和许可证，且只能使用 CC0、MIT、公共领域等宽松许可

## 版权红线

严禁使用以下内容作为样本内容：
- 新闻、小说、歌词、论文、教材、维基百科、博客文章等受版权保护的文本
- 真实个人姓名、电话、地址、身份证号、邮箱等隐私数据
- 未明确授权的图片、音频、视频、CAD 模型
- 任何需要署名、非商业、禁止演绎等限制的素材

允许使用：
- Faker `zh_CN` 生成的虚构数据（仅用于样本展示，不代表真实人物或号码）
- 古籍**原文**（如《论语》《道德经》原文）；**不包含**现代整理本的标点、校勘、白话翻译、注释，这些有独立版权
- 项目自编中文段落
- 明确 CC0/MIT 的素材

## 技术栈

- Python 3.11+
- 依赖管理：uv 优先，兼容 pip；提交 `uv.lock` 以保证可复现
- 主要库：faker、faker-file、Pillow、openpyxl、python-docx、python-pptx、reportlab
- 音视频处理：ffmpeg（需系统预装并加入 PATH，不在 pyproject 中）
- 压缩：zip 标准库；RAR 暂缓，因格式专有且工具许可复杂，必要时改用 7z 替代

## 字体策略

中文样本在跨平台渲染时差异巨大（Windows 雅黑/宋体、Linux Noto、macOS PingFang），必须统一字体来源，避免在 CI 或 Linux 服务器上出现方块字。

- 项目自带字体放入 `assets/fonts/`，使用 OFL-1.1 许可字体（思源黑体 CN）
- **子集格式必须是 TTF（glyf outlines），不能是 OTF（CFF outlines）**：reportlab 的 TTFont 只支持 TrueType outlines，CFF OTF 会报 "postscript outlines are not supported"
- 子集化输出 `SourceHanSansSC-Regular-subset.ttf`（约 1.93 MB，< 5 MB 可直接入 git）
- 字符集：GB 2312 一级常用字 3755 + ASCII + 常用中文标点（共 3882 字）
- 源字体（17 MB 的 Variable TTF）不入 git，放入 `assets/fonts/_source/`（已 .gitignore）
- OFL 许可证单独保存为 `assets/fonts/LICENSE-OFL.txt`，OFL 不可与 MIT 合并为单一许可证
- 生成 PDF 时通过 reportlab `TTFont` 显式注册子集字体，禁止依赖系统字体
- 生成 docx/pptx 时通过库 API 指定字体名 `Source Han Sans CN`，文档内嵌字体策略后续讨论
- 生成 PNG 时通过 Pillow `ImageFont.truetype` 加载同一子集字体
- 字体文件不放入 `samples/`，避免污染样本许可
- 子集化脚本：`scripts/prepare_fonts.py`，可重复运行（已存在子集则跳过）

## 目录结构

```text
zh-sample-files/
├── AGENTS.md
├── LICENSE
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .gitattributes     # Git LFS 规则
├── .editorconfig       # 中文项目编码与缩进规范
├── assets/
│   └── fonts/
│       └── LICENSE-OFL.txt  # OFL 字体许可证
├── scripts/
│   ├── generate.py
│   ├── generate_docx.py
│   ├── generate_pdf.py
│   └── ...
├── samples/
│   ├── docx/
│   ├── xlsx/
│   ├── pdf/
│   ├── csv/
│   ├── txt/
│   ├── png/
│   ├── jpg/
│   ├── wav/
│   ├── mp3/
│   ├── mp4/
│   ├── xml/
│   ├── ini/
│   ├── cfg/
│   └── zip/
└── docs/
    └── formats.md
```

## 生成规则

- 所有样本内容优先使用中文。
- 文件名使用中文或中英混合，但避免特殊字符和空格。
- 每个格式至少生成 1 个小文件、1 个中等文件。文件大小档位：
  - 小：< 100 KB
  - 中等：100 KB–1 MB
  - 大（可选）：1–5 MB
- 单个样本文件默认不超过 5 MB；超过 5 MB 使用 Git LFS 或 GitHub Release。
- 字符编码：
  - txt：UTF-8（无 BOM）
  - csv：UTF-8 with BOM（兼容 Windows Excel 直接打开）
  - xml/ini/cfg：UTF-8（无 BOM），XML 首行声明 `encoding="UTF-8"`
  - 其他二进制格式按格式规范处理
- 生成脚本必须可重复运行，输出到固定目录。
- 每次新增格式，必须同时更新 README 和 docs/formats.md，并在 formats.md 记录编码、大小、字体等元数据。

## 命名规范

- 脚本：`generate_<format>.py`（format 用扩展名，如 `generate_csv.py`、`generate_docx.py`）
- 样本：`中文示例_<ext>_<序号>.<ext>`（ext 用扩展名作为格式标识，避免 png/jpg 都叫"图片"等歧义）
- 例如：
  - `中文示例_docx_01.docx`
  - `中文示例_xlsx_01.xlsx`
  - `中文示例_png_01.png`
  - `中文示例_jpg_01.jpg`

## AI 行为约束

- 每次开始任务前，先阅读本文件。
- 不要一次性实现所有格式。先完成 MVP，再扩展。
- 不要擅自添加未确认的依赖；新增依赖前必须先加入 pyproject.toml 并运行 `uv lock`。
- 不要生成或提交受版权保护的内容。
- 不要提交超过 5 MB 的二进制文件，除非已配置 Git LFS 或 Release。
- 不要自动创建 GitHub 仓库、修改许可证、公开仓库；这些操作必须由人类确认。
- 修改代码后，运行生成脚本验证，并报告生成的文件路径和大小。
- 遇到不确定的版权、格式、依赖问题，先停下来询问。

## 当前优先级

P0：
- txt、csv、docx、pdf、png、zip

P1：
- xlsx、pptx、jpg、wav、mp3、mp4、xml、ini、cfg

P2：
- rar、mkv、cad/dwg/dxf

## 工作流

1. 读 AGENTS.md
2. 检查当前目录和已有文件
3. 提出 MVP 简短计划（含本次新增的格式、依赖、字体）
4. 确认 Python 环境与依赖（pyproject.toml + uv 虚拟环境 + 字体就位）
5. 等人类确认后执行
6. 运行脚本生成样本
7. 检查文件大小、编码、字体渲染
8. 更新 README 和 docs/formats.md
9. 报告结果和下一步建议