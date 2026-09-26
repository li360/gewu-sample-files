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

## P0 + P1a + P1b 格式（已实现）

| 格式 | 编码 | 小文件 | 中等文件 | 字体 | 内容来源 | 测试场景 |
|------|------|--------|----------|------|----------|----------|
| txt  | UTF-8（无 BOM） | 2.6 KB | 193.3 KB | 否 | 自编段落 + 古籍原文 | 编码检测、文本预览、行尾处理 |
| csv  | UTF-8 with BOM | 2.8 KB | 185.6 KB | 否 | 示例化占位数据（姓氏+X、示例市、example.com、示例公司） | Excel 中文导入、CSV 解析、表头识别 |
| docx | — | 37.2 KB | 141.5 KB | 是（指定字体名） | Faker 段落 + 古籍原文 | Office 在线预览、文档解析、中文字体替换 |
| pdf  | — | 70.7 KB | 149.3 KB | 是（reportlab 注册） | 自编段落 + 古籍原文 | PDF 阅读器渲染、文本抽取、字体嵌入验证 |
| png  | — | 56.9 KB | 338.6 KB | 是（Pillow truetype） | Pillow 自绘中文段落 | 图片预览、缩略图生成、中文字体渲染 |
| zip  | — | 370.9 KB | 1633.2 KB | — | 打包各格式小文件 + 非音视频中等文件（按子目录组织） | 压缩包解压、目录结构还原、跨格式批量测试 |
| xlsx | — | 7.0 KB | 115.2 KB | 是（openpyxl Font 指定字体名） | 示例化占位表格（姓氏+X、示例市、example.com、示例公司） | Excel 解析、单元格样式、中文字体替换 |
| pptx | — | 31.7 KB | 163.9 KB | 是（python-pptx 指定字体名） | Faker 段落 + 自编段落 | 幻灯片解析、版式渲染、中文字体替换 |
| jpg  | — | 45.0 KB | 277.2 KB | 是（Pillow truetype） | Pillow 自绘中文段落（JPEG 压缩） | 图片预览、缩略图生成、有损压缩测试 |
| xml  | UTF-8（无 BOM） | 7.3 KB | 486.0 KB | 否 | ElementTree + 示例化占位数据序列化 | XML 解析、命名空间处理、编码声明验证 |
| ini  | UTF-8（无 BOM） | 4.1 KB | 258.0 KB | 否 | configparser + 示例化占位数据 | 配置文件解析、节段读取、键值对提取 |
| cfg  | UTF-8（无 BOM） | 4.1 KB | 258.0 KB | 否 | 同 ini（仅扩展名不同，内容字节级一致） | 配置文件解析、扩展名兼容性测试 |
| wav  | — | 47.0 KB | 861.4 KB | 否 | ffmpeg sine 滤镜合成正弦波（A4 440Hz / A3 220Hz） | 音频解析、PCM 解码、采样率测试 |
| mp3  | — | 25.4 KB | 235.8 KB | 否 | ffmpeg libmp3lame 编码正弦波（同 wav 内容） | MP3 解码、ID3 标签、比特率测试 |
| mp4  | — | 61.8 KB | 2551.3 KB | 是（drawtext 加载子集字体） | ffmpeg testsrc2 测试图 + drawtext 中文叠加 + 可选 sine 音轨 | 视频解析、H.264 解码、字幕渲染、音视频同步 |
| mkv  | — | 63.5 KB | 2557.6 KB | 是（drawtext 加载子集字体） | ffmpeg testsrc2 测试图 + drawtext 中文叠加 + libopus 音轨（MKV 容器） | MKV 容器解析、H.264/Opus 解码、字幕渲染 |
| dxf  | ASCII（dxf 规范默认） | 23.0 KB | 122.8 KB | 是（文字样式引用 Source Han Sans CN） | ezdxf 几何图形（线/圆/矩形）+ 中文标注 + 示例化数据表格 | CAD 图纸解析、图层管理、文字样式渲染 |
| 7z   | — | 365.6 KB | 1388.1 KB | 否 | py7zr 打包各格式小文件 + 非音视频中等文件（LZMA2） | 7z 解压、LZMA2 解码、目录结构还原 |

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
  - mp4/mkv：ffmpeg `drawtext` 滤镜 `fontfile` 参数加载子集字体
  - dxf：ezdxf 文字样式引用字体名 `Source Han Sans CN`（dxf 文件本身用 ASCII 编码，中文用 \U+XXXX 转义）

### 大小档位说明

- 小档位目标 < 100 KB：14 个格式符合；zip/7z 因打包所有格式"小文件"组合，体积 376/366 KB，属结构性偏离；mp4/mkv 受视频流最小体积限制，需 320×180/15fps/crf=30 才能压到 62/64 KB
- 中等档位目标 100 KB–1 MB：12 个格式符合；mp4/mkv 因视频流本质特性，15 秒 960×540 即 2.5 MB，超 1 MB 但在 5 MB 上限内；zip/7z 中等 1.6/1.4 MB，因打包多格式组合，超 1 MB 但在 5 MB 上限内
- 其余格式均符合档位区间

### ffmpeg 依赖说明

- wav/mp3/mp4/mkv 需要 ffmpeg 系统预装并加入 PATH（按 AGENTS.md 不进 pyproject）
- 验证版本：ffmpeg 7.1-full_build（gyan.dev）启用 libmp3lame、libx264、libfreetype、libharfbuzz、libopus
- 所有音频/视频内容均为 ffmpeg lavfi 滤镜合成（sine 正弦波 / testsrc2 测试图 + drawtext 中文叠加），无版权风险

### py7zr 依赖说明

- 7z 格式使用 py7zr（MIT 许可，开源 LZMA2 压缩格式，替代专有许可的 RAR）
- 已加入 pyproject.toml，通过 `uv sync` 安装

### 示例化数据策略

csv / xlsx / xml / ini / cfg 中的人物数据采用"一看就是示例"的占位格式，避免撞上真实信息：

| 字段 | 格式 | 示例 |
|------|------|------|
| 姓名 | 常见姓氏 + 1~2 个 X | `李X`、`王XX`、`张X` |
| 城市 | `示例市` + 3 位序号 | `示例市001`、`示例市002` |
| 邮箱 | `user` + 3 位序号 + `@example.com` | `user001@example.com`（RFC 2606 保留域名） |
| 电话 | 固定假号码 | `0000-00000000`（非真实号码格式） |
| 公司 | `示例公司` + 3 位序号 | `示例公司001`、`示例公司002` |
| 性别 | 随机 `男`/`女` | — |
| 年龄 | 随机 18~65 | — |
| 职位 | Faker 生成通用职业名 | `软件工程师`（无撞真实风险） |

实现位于 `scripts/_content.py` 的 `faker_person_rows()` 函数。

## P2（待评估）

rar（暂缓，可改用 7z）、mkv、cad/dwg/dxf
