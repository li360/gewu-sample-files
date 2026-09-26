# 样本格式元数据（formats.md）

本文件记录每种格式样本的元数据：编码、大小、字体、内容来源。
每次新增格式或调整生成规则，必须同步更新本表。

## 字段说明

- **格式**：文件扩展名
- **编码**：文本类文件字符编码；二进制文件标注"—"
- **小文件 / 中等文件**：实际生成的大小（KB）
- **字体**：是否使用项目自带 OFL 字体（思源黑体子集 SourceHanSansSC-Regular-subset.ttf，约 1.93 MB）
- **内容来源**：样本内容的来源（自编 / Faker / 古籍原文）
- **测试场景**：该格式样本适合的常见测试用途

## P0 + P1a 格式（已实现）

| 格式 | 编码 | 小文件 | 中等文件 | 字体 | 内容来源 | 测试场景 |
|------|------|--------|----------|------|----------|----------|
| txt  | UTF-8（无 BOM） | 2.6 KB | 193.3 KB | 否 | 自编段落 + 古籍原文 | 编码检测、文本预览、行尾处理 |
| csv  | UTF-8 with BOM | 3.1 KB | 200.4 KB | 否 | Faker zh_CN 虚构人物 | Excel 中文导入、CSV 解析、表头识别 |
| docx | — | 37.2 KB | 141.5 KB | 是（指定字体名） | Faker 段落 + 古籍原文 | Office 在线预览、文档解析、中文字体替换 |
| pdf  | — | 70.7 KB | 149.3 KB | 是（reportlab 注册） | 自编段落 + 古籍原文 | PDF 阅读器渲染、文本抽取、字体嵌入验证 |
| png  | — | 56.9 KB | 338.6 KB | 是（Pillow truetype） | Pillow 自绘中文段落 | 图片预览、缩略图生成、中文字体渲染 |
| zip  | — | 241.3 KB | 1533.3 KB | — | 打包上述样本（按子目录组织） | 压缩包解压、目录结构还原、跨格式批量测试 |
| xlsx | — | 7.7 KB | 150.8 KB | 是（openpyxl Font 指定字体名） | Faker zh_CN 虚构人物表格 | Excel 解析、单元格样式、中文字体替换 |
| pptx | — | 31.7 KB | 163.5 KB | 是（python-pptx 指定字体名） | Faker 段落 + 自编段落 | 幻灯片解析、版式渲染、中文字体替换 |
| jpg  | — | 45.0 KB | 277.2 KB | 是（Pillow truetype） | Pillow 自绘中文段落（JPEG 压缩） | 图片预览、缩略图生成、有损压缩测试 |
| xml  | UTF-8（无 BOM） | 7.5 KB | 500.5 KB | 否 | ElementTree + Faker 假数据序列化 | XML 解析、命名空间处理、编码声明验证 |
| ini  | UTF-8（无 BOM） | 4.4 KB | 276.1 KB | 否 | configparser + Faker 假数据 | 配置文件解析、节段读取、键值对提取 |
| cfg  | UTF-8（无 BOM） | 4.4 KB | 276.1 KB | 否 | 同 ini（仅扩展名不同，内容字节级一致） | 配置文件解析、扩展名兼容性测试 |

### 字体说明

- 子集字体：`assets/fonts/SourceHanSansSC-Regular-subset.ttf`（1.93 MB，OFL-1.1）
- 字符集：GB 2312 一级常用 3755 字 + ASCII + 常用中文标点（共 3882 字）
- 源字体：Adobe Source Han Sans CN Variable TTF（17 MB，已子集化至 1.93 MB）
- 许可证：`assets/fonts/LICENSE-OFL.txt`
- 源字体不入 git（`.gitignore` 排除 `assets/fonts/_source/`）
- 字体使用方式：
  - PDF：reportlab `TTFont` 显式注册
  - docx/pptx/xlsx：通过库 API 指定字体名 `Source Han Sans CN`（不嵌字体文件）
  - png/jpg：Pillow `ImageFont.truetype` 加载子集字体

### 大小档位说明

- 小档位目标 < 100 KB：zip 因打包 11 个目录的"小文件"组合，体积为 241 KB，属结构性偏离
- 中等档位目标 100 KB–1 MB：zip 因打包全部格式"中等文件"组合，体积为 1.5 MB，仍在 5 MB 上限内（视为可选大档位）
- 其余 11 个格式均符合档位区间

## P1b（待实现）

wav、mp3、mp4（需 ffmpeg 系统预装）

## P2（待评估）

rar（暂缓，可改用 7z）、mkv、cad/dwg/dxf
