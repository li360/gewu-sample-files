"""样本内容生成器：为各格式脚本提供统一的中文内容来源。

内容来源遵循 AGENTS.md 版权红线：
- 自编中文段落（项目原创，无版权风险）
- 古籍原文（公共领域，仅原文，不含现代整理本标点）
- Faker zh_CN 虚构数据（仅用于样本展示，不代表真实人物）
"""
from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

# 项目根目录（脚本在 scripts/ 下，根是上一级）
ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT / "assets" / "fonts"
SUBSET_FONT = FONTS_DIR / "SourceHanSansSC-Regular-subset.ttf"
SAMPLES_DIR = ROOT / "samples"

# 单例 Faker（zh_CN 区域）
faker = Faker("zh_CN")
Faker.seed(0)

# 项目自编段落模板：覆盖不同文体（叙述、说明、列表感）
SELF_PARAGRAPHS = [
    "春日清晨，山间薄雾未散。一条石板小径从村口蜿蜒而上，穿过竹林与溪涧，最终抵达半山腰的旧茶亭。亭中立着一块石碑，字迹已模糊，只余“嘉庆”二字尚可辨认。",
    "现代物流体系的核心在于信息流与实物流的同步。仓库管理系统的每一次库存变动，都会触发订单系统、财务系统、运输调度系统的级联更新。任何环节的延迟都会导致整体吞吐量下降。",
    "数据处理流程通常分为四个阶段：采集、清洗、转换、加载。采集阶段需考虑数据源的异构性；清洗阶段需处理缺失值与异常值；转换阶段需对齐业务语义；加载阶段需保证幂等性。",
    "城市公共交通规划应遵循“最小换乘次数”原则。理想状态下，任意两站点之间不超过一次换乘。这要求公交线路设计兼顾覆盖密度与主干通行效率，避免过度绕行。",
    "夜雨滴答敲打着青瓦。屋内油灯摇曳，映出墙上斑驳的水渍。老人翻动着手中的旧账本，纸张已发黄脆化，墨迹却依然清晰，记录着半个世纪前这场村庄的每一笔进出。",
    "云原生架构强调“不可变基础设施”。容器镜像一旦构建即不可修改，运行时配置通过环境变量注入。这种约束虽然看似死板，却消除了“环境漂移”这一长期困扰运维的顽疾。",
    "良渚遗址的考古发现将中华文明史的起点推前至距今约五千年。玉琮、玉璧、神徽符号体系完备，显示出已存在高度组织化的社会结构与宗教体系。",
    "函数式编程的核心思想是“数据不可变”与“函数是一等公民”。通过纯函数组合替代可变状态，程序的行为更容易推理与测试。但其学习曲线对命令式背景的开发者而言相对陡峭。",
    "海边渔村的清晨总是从潮汐声开始。渔船陆续归来，渔民在码头上分拣渔获。海风带着咸腥，混着柴油与冰块的气味。今夜的市集将整夜营业，直至次日清晨再次出航。",
    "分布式系统的 CAP 定理指出：一致性（Consistency）、可用性（Availability）、分区容错（Partition tolerance）三者不可兼得。工程实践通常在 CP 与 AP 之间取舍。",
]

# 古籍原文片段：公共领域，仅原文，不含现代整理本的标点与校勘
# 出处：《道德经》《论语》《大学》《中庸》《孙子兵法》《诗经》
# 注：此处仅录入原文，不添加现代标点；行末以句读断句，符合古籍体例
CLASSICS_LINES = [
    # 道德经
    "道可道非常道名可名非常名无名天地之始有名万物之母故常无欲以观其妙常有欲以观其徼",
    "上善若水水善利万物而不争处众人之所恶故几于道居善地心善渊与善仁言善信正善治事善能动善时",
    "三十辐共一毂当其无有车之用埏埴以为器当其无有器之用凿户牖以为室当其无有室之用",
    "信言不美美言不信善者不辩辩者不善知者不博博者不知圣人不积既以为人己愈有既以与人己愈多",
    # 论语
    "学而时习之不亦说乎有朋自远方来不亦乐乎人不知而不愠不亦君子乎",
    "吾日三省吾身为人谋而不忠乎与朋友交而不信乎传不习乎",
    "温故而知新可以为师矣",
    "学而不思则罔思而不学则殆",
    # 大学
    "大学之道在明明德在亲民在止于至善知止而后有定定而后能静静而后能安安而后能虑虑而后能得",
    "物格而后知至知至而后意诚意诚而后心正心正而后身修身修而后家齐家齐而后国治国治而后天下平",
    # 中庸
    "天命之谓性率性之谓道修道之谓教道也者不可须臾离也可离非道也",
    # 孙子兵法
    "兵者国之大事死生之地存亡之道不可不察也",
    "知己知彼百战不殆不知彼而知己一胜一负不知彼不知己每战必殆",
    # 诗经
    "关关雎鸠在河之洲窈窕淑女君子好逑",
    "蒹葭苍苍白露为霜所谓伊人在水一方",
    "昔我往矣杨柳依依今我来思雨雪霏霏",
    "桃之夭夭灼灼其华之子于归宜其室家",
]


def chinese_paragraphs(n: int = 5) -> list[str]:
    """返回 n 段自编中文段落（带项目内重复采样）。"""
    rng = random.Random(42)
    return [rng.choice(SELF_PARAGRAPHS) for _ in range(n)]


def classics_text(min_chars: int = 500) -> str:
    """拼接古籍原文至不少于 min_chars 字。"""
    rng = random.Random(7)
    out: list[str] = []
    while sum(len(s) for s in out) < min_chars:
        out.append(rng.choice(CLASSICS_LINES))
    return "\n".join(out)


def faker_person_rows(n: int = 10) -> list[dict[str, str]]:
    """生成 n 行虚构人物数据。返回 dict 列表，键与 CSV 表头一致。

    字段：姓名、性别、年龄、城市、邮箱、电话、职位、公司
    """
    rows: list[dict[str, str]] = []
    for _ in range(n):
        rows.append({
            "姓名": faker.name(),
            "性别": random.choice(["男", "女"]),
            "年龄": str(random.randint(18, 65)),
            "城市": faker.city(),
            "邮箱": faker.email(),
            "电话": faker.phone_number(),
            "职位": faker.job(),
            "公司": faker.company(),
        })
    return rows


def faker_paragraph(n_sentences: int = 5) -> str:
    """生成 n 句 Faker 中文段落（用于测试随机文本渲染）。"""
    return faker.paragraph(nb_sentences=n_sentences)


def ensure_sample_dir(ext: str) -> Path:
    """确保 samples/<ext>/ 目录存在，返回路径。"""
    d = SAMPLES_DIR / ext
    d.mkdir(parents=True, exist_ok=True)
    return d


def sample_name(ext: str, idx: int) -> str:
    """构造样本文件名：中文示例_<ext>_<idx>.<ext>。"""
    return f"中文示例_{ext}_{idx:02d}.{ext}"
