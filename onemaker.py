"""
OneMaker 游戏项目管理工具
一人利用AI完成游戏全流程制作的项目管理CLI
"""

import os
import sys
import json
import shutil
import datetime
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).parent
PROJECTS_DIR = BASE_DIR / "projects"
TEMPLATES_DIR = BASE_DIR / "templates"
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
REGISTRY_FILE = BASE_DIR / "projects.json"

STAGES = [
    "concept",
    "prototype",
    "vertical_slice",
    "production",
    "alpha",
    "beta",
    "rc",
    "launched",
]

STAGE_LABELS = {
    "concept": "概念期",
    "prototype": "原型期",
    "vertical_slice": "垂直切片",
    "production": "量产期",
    "alpha": "Alpha",
    "beta": "Beta",
    "rc": "发布候选(RC)",
    "launched": "已发布",
}

STAGE_ORDER = {s: i for i, s in enumerate(STAGES)}


def load_registry():
    """加载项目注册表"""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"projects": {}}


def save_registry(reg):
    """保存项目注册表"""
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)


def slugify(name):
    """将项目名转为目录安全的slug"""
    return name.lower().replace(" ", "_").replace("-", "_")


def get_project_dir(slug):
    """获取项目目录路径"""
    return PROJECTS_DIR / slug


def get_current_week(created_date_str):
    """计算当前是第几周"""
    created = datetime.datetime.fromisoformat(created_date_str).date()
    today = datetime.date.today()
    delta = (today - created).days
    return max(1, delta // 7 + 1)


def fill_template(template_path, project_name, stage):
    """填充模板中的占位符"""
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("{{PROJECT_NAME}}", project_name)
    content = content.replace("{{DATE}}", datetime.date.today().isoformat())
    content = content.replace("{{STAGE}}", STAGE_LABELS.get(stage, stage))
    content = content.replace("{{STATUS}}", "进行中")
    return content


def cmd_new(args):
    """创建新游戏项目"""
    if len(args) < 1:
        print("用法: python onemaker.py new <项目名称> [中文名]")
        return
    slug = slugify(args[0])
    cn_name = args[1] if len(args) > 1 else args[0]

    reg = load_registry()
    if slug in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 已存在")
        return

    proj_dir = get_project_dir(slug)
    proj_dir.mkdir(parents=True, exist_ok=True)

    stage = "concept"
    now = datetime.datetime.now().isoformat()

    for subdir in ["design", "art", "audio", "dev", "marketing", "weekly"]:
        (proj_dir / subdir).mkdir(exist_ok=True)

    doc_map = {
        "design/concept_doc.md": TEMPLATES_DIR / "concept_doc.md",
        "design/gdd.md": TEMPLATES_DIR / "gdd.md",
        "art/art_bible.md": TEMPLATES_DIR / "art_bible.md",
        "audio/audio_spec.md": TEMPLATES_DIR / "audio_spec.md",
        "checklist.md": TEMPLATES_DIR / "checklist.md",
    }

    for rel_path, tmpl_path in doc_map.items():
        if tmpl_path.exists():
            content = fill_template(tmpl_path, cn_name, stage)
            (proj_dir / rel_path).write_text(content, encoding="utf-8")

    reg["projects"][slug] = {
        "name": cn_name,
        "slug": slug,
        "stage": stage,
        "created": now,
        "updated": now,
        "engine": "",
        "genre": "",
        "platform": "",
    }
    save_registry(reg)

    print(f"\n[成功] 项目 '{cn_name}' 已创建!")
    print(f"  目录: {proj_dir}")
    print(f"  阶段: {STAGE_LABELS[stage]}")
    print(f"\n下一步:")
    print(f"  1. 编辑 design/concept_doc.md 完善概念文档")
    print(f"  2. 运行 'python onemaker.py status {slug}' 查看项目状态")
    print(f"  3. 运行 'python onemaker.py guide {slug}' 查看当前阶段指南")


def cmd_list(args):
    """列出所有项目"""
    reg = load_registry()
    projects = reg.get("projects", {})
    if not projects:
        print("[信息] 暂无项目，运行 'python onemaker.py new <名称>' 创建")
        return

    print("\n" + "=" * 70)
    print(f"{'项目名称':<16} {'阶段':<12} {'周数':<6} {'创建日期':<12} {'引擎':<10}")
    print("-" * 70)
    for slug, info in projects.items():
        week = get_current_week(info["created"])
        print(
            f"{info['name']:<16} "
            f"{STAGE_LABELS.get(info['stage'], info['stage']):<12} "
            f"第{week:>2}周   "
            f"{info['created'][:10]:<12} "
            f"{info.get('engine', '-'):<10}"
        )
    print("=" * 70 + "\n")


def cmd_status(args):
    """查看项目详细状态"""
    if len(args) < 1:
        print("用法: python onemaker.py status <项目slug>")
        return
    slug = slugify(args[0])
    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    info = reg["projects"][slug]
    proj_dir = get_project_dir(slug)
    week = get_current_week(info["created"])
    stage_idx = STAGE_ORDER.get(info["stage"], 0)

    print(f"\n{'='*50}")
    print(f"  项目: {info['name']}")
    print(f"  Slug: {slug}")
    print(f"  阶段: {STAGE_LABELS.get(info['stage'], info['stage'])}")
    print(f"  周数: 第{week}周")
    print(f"  引擎: {info.get('engine', '未设定')}")
    print(f"  类型: {info.get('genre', '未设定')}")
    print(f"  平台: {info.get('platform', '未设定')}")
    print(f"  创建: {info['created'][:10]}")
    print(f"  目录: {proj_dir}")
    print(f"{'='*50}")

    print(f"\n阶段进度:")
    for i, s in enumerate(STAGES):
        marker = "✓" if i <= stage_idx else "○"
        current = " ← 当前" if s == info["stage"] else ""
        print(f"  {marker} {STAGE_LABELS[s]}{current}")

    checklist_path = proj_dir / "checklist.md"
    if checklist_path.exists():
        content = checklist_path.read_text(encoding="utf-8")
        checked = content.count("[x]")
        total = content.count("[ ]") + checked
        if total > 0:
            pct = checked / total * 100
            bar_len = 20
            filled = int(bar_len * checked / total)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\n总检查清单进度: [{bar}] {pct:.0f}% ({checked}/{total})")

    print()


def cmd_stage(args):
    """推进项目阶段"""
    if len(args) < 2:
        print("用法: python onemaker.py stage <项目slug> <新阶段>")
        print(f"可选阶段: {', '.join(STAGES)}")
        return
    slug = slugify(args[0])
    new_stage = args[1].lower()

    if new_stage not in STAGE_LABELS:
        print(f"[错误] 无效阶段 '{new_stage}'")
        print(f"可选: {', '.join(STAGES)}")
        return

    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    info = reg["projects"][slug]
    old_stage = info["stage"]
    info["stage"] = new_stage
    info["updated"] = datetime.datetime.now().isoformat()
    save_registry(reg)

    checklist_path = get_project_dir(slug) / "checklist.md"
    if checklist_path.exists():
        content = checklist_path.read_text(encoding="utf-8")
        line = f"| {datetime.date.today()} | {STAGE_LABELS[old_stage]} | {STAGE_LABELS[new_stage]} | 阶段推进 |"
        content += "\n" + line + "\n"
        checklist_path.write_text(content, encoding="utf-8")

    print(f"\n[成功] '{info['name']}' 阶段已更新:")
    print(f"  {STAGE_LABELS[old_stage]} → {STAGE_LABELS[new_stage]}")
    print(f"\n运行 'python onemaker.py guide {slug}' 查看新阶段指南\n")


def cmd_guide(args):
    """显示当前阶段的工作指南"""
    if len(args) < 1:
        print("用法: python onemaker.py guide <项目slug> [阶段]")
        return
    slug = slugify(args[0])
    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    info = reg["projects"][slug]
    stage = args[1].lower() if len(args) > 1 else info["stage"]

    if stage not in STAGE_LABELS:
        print(f"[错误] 无效阶段 '{stage}'")
        return

    guides = {
        "concept": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 概念期（Concept）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：确定游戏核心概念，验证方向可行性

  📝 必做任务：
    1. 撰写电梯演讲（一句话描述你的游戏）
    2. 完成 concept_doc.md 所有填空
    3. 收集参考图，制作Moodboard
    4. 确定核心循环（玩家做什么→获得什么→如何成长）
    5. 列出3-5款参考游戏和差异化分析

  🤖 AI协助建议：
    → 用ChatGPT/Claude头脑风暴，输入：
      "我想做一款[类型]游戏，核心体验是[关键词]，请帮我生成5个概念方向"
    → 用Midjourney生成概念参考图
    → 让AI帮你写竞品分析

  ✅ 完成标准：
    □ concept_doc.md 已填写完整
    □ 至少有3张概念参考图
    □ 核心循环已描述清楚
    □ 你能用1分钟向朋友解释这个游戏

  ⏭ 下一阶段：原型期（prototype）
    推进命令：python onemaker.py stage {slug} prototype
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "prototype": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔧 原型期（Prototype）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：验证核心玩法是否有趣

  📝 必做任务：
    1. 选择游戏引擎，创建工程
    2. 实现角色基础控制（移动/跳跃/攻击）
    3. 实现核心循环的最小版本
    4. 用白盒（简单几何体）测试玩法
    5. 开始撰写GDD初稿

  🤖 AI协助建议：
    → 让AI推荐引擎选型：python onemaker.py guide {slug}
    → 用Trae/Cursor辅助编码
    → 让AI帮你搭建项目架构
    → 白盒阶段不需要美术，用纯色方块即可

  ⚠️ 关键决策点：
    核心玩法好玩吗？如果不好玩，在此阶段修改成本最低！
    不要急着加美术，先确保好玩。

  ✅ 完成标准：
    □ 核心循环可运行可操作
    □ 你自己愿意反复玩这个原型
    □ gdd.md 初稿已完成
    □ 技术选型已确定

  ⏭ 下一阶段：垂直切片（vertical_slice）
    推进命令：python onemaker.py stage {slug} vertical_slice
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "vertical_slice": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎨 垂直切片（Vertical Slice）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：完成一个完整关卡的全品质体验

  📝 必做任务：
    1. 确定美术风格，完成 art_bible.md
    2. 制作主角全套资产（模型/动画/UI）
    3. 完成第一个完整关卡（白盒→正式美术）
    4. 搭建UI系统（HUD/菜单）
    5. 制作第一首BGM和关键音效
    6. 完善GDD到详细版本

  🤖 AI协助建议：
    → Midjourney/SD生成概念图和材质
    → 训练LoRA保持美术风格一致
    → Suno/Udio生成BGM
    → ElevenLabs生成音效
    → 让AI编写UI代码

  ✅ 完成标准：
    □ art_bible.md 已完成
    □ 主角资产全套完成
    □ 第一个关卡可完整体验
    □ UI系统可用
    □ BGM和关键音效已集成
    □ 垂直切片可以给别人试玩

  ⏭ 下一阶段：量产期（production）
    推进命令：python onemaker.py stage {slug} production
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "production": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏗️ 量产期（Production）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：批量制作所有内容，完成全部功能和资产

  📝 必做任务：
    1. 批量制作所有关卡
    2. 实现所有游戏系统（经济/成长/任务等）
    3. 制作全部美术资产
    4. 完成全部BGM和音效
    5. 实现全部UI界面
    6. 完成叙事内容

  🤖 AI协助建议：
    → 用模块化策略批量生成资产变体
    → AI辅助批量编写系统代码
    → AI生成批量音效和音乐
    → 让AI帮你做数值平衡

  ⚠️ 注意事项：
    严格控制scope！不要在量产期加新功能。
    使用timebox管理每个任务。

  ✅ 完成标准：
    □ 所有关卡完成
    □ 所有系统完成
    □ 所有美术资产完成
    □ 所有音频完成
    □ 游戏可从头玩到尾

  ⏭ 下一阶段：Alpha
    推进命令：python onemaker.py stage {slug} alpha
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "alpha": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧪 Alpha 工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：功能完整，开始内部测试

  📝 必做任务：
    1. 全面功能测试，记录所有Bug
    2. 修复所有P0（阻断性）Bug
    3. 性能基准测试
    4. 开始准备商店页面素材
    5. 邀请小范围内部测试者

  🤖 AI协助建议：
    → AI生成测试用例
    → AI辅助分析Bug原因
    → AI审查代码质量
    → AI撰写商店描述文案

  ✅ 完成标准：
    □ 无P0 Bug
    □ 游戏可完整通关
    □ 性能基线达标
    □ 内部测试反馈已收集

  ⏭ 下一阶段：Beta
    推进命令：python onemaker.py stage {slug} beta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "beta": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔨 Beta 工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：内容完整，修复Bug，开始外部测试

  📝 必做任务：
    1. 修复所有P1 Bug
    2. 进行外部测试（找真实玩家试玩）
    3. 创建商店页面（Steam/itch.io等）
    4. 制作Trailer
    5. 开始营销推广

  ✅ 完成标准：
    □ P1 Bug全部修复
    □ 外部测试完成
    □ 商店页面已创建
    □ Trailer已制作

  ⏭ 下一阶段：RC
    推进命令：python onemaker.py stage {slug} rc
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "rc": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚀 发布候选（RC）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：最终打磨，准备发布

  📝 必做任务：
    1. 修复P2 Bug
    2. 最终性能优化
    3. 商店素材全部上传
    4. 营销活动执行
    5. 准备发布日计划

  ✅ 完成标准：
    □ 所有已知Bug已修复
    □ 商店页面已完善
    □ 营销素材已准备
    □ 准备好发布

  ⏭ 下一阶段：Launched!
    推进命令：python onemaker.py stage {slug} launched
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        "launched": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎉 已发布（Launched）工作指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 本阶段目标：运营维护，收集反馈，规划更新

  📝 持续任务：
    1. 监控社区反馈和Bug报告
    2. 发布热修复补丁
    3. 社区运营（Discord/B站/微博）
    4. 数据分析（销量/Wishlist/留存）
    5. 规划后续更新/DLC

  恭喜你完成了游戏发布！🎊
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
    }

    guide = guides.get(stage, "暂无该阶段指南")
    print(guide.replace("{slug}", slug))


def cmd_weekly(args):
    """创建本周周报"""
    if len(args) < 1:
        print("用法: python onemaker.py weekly <项目slug>")
        return
    slug = slugify(args[0])
    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    info = reg["projects"][slug]
    week = get_current_week(info["created"])
    proj_dir = get_project_dir(slug)
    weekly_dir = proj_dir / "weekly"
    weekly_dir.mkdir(exist_ok=True)

    filename = f"week_{week:03d}.md"
    filepath = weekly_dir / filename

    if filepath.exists():
        print(f"[信息] 第{week}周周报已存在: {filepath}")
        return

    tmpl_path = TEMPLATES_DIR / "weekly_review.md"
    if tmpl_path.exists():
        content = fill_template(tmpl_path, info["name"], info["stage"])
        content = content.replace("{{WEEK}}", f"第{week}周")
        filepath.write_text(content, encoding="utf-8")
        print(f"[成功] 第{week}周周报已创建: {filepath}")
    else:
        print("[错误] 周报模板不存在")


def cmd_set(args):
    """设置项目属性"""
    if len(args) < 3:
        print("用法: python onemaker.py set <项目slug> <属性> <值>")
        print("属性: engine | genre | platform | name")
        return
    slug = slugify(args[0])
    key = args[1]
    value = " ".join(args[2:])

    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    valid_keys = ["engine", "genre", "platform", "name"]
    if key not in valid_keys:
        print(f"[错误] 无效属性 '{key}'，可选: {', '.join(valid_keys)}")
        return

    reg["projects"][slug][key] = value
    reg["projects"][slug]["updated"] = datetime.datetime.now().isoformat()
    save_registry(reg)
    print(f"[成功] '{reg['projects'][slug]['name']}' 的 {key} 已设置为: {value}")


def cmd_delete(args):
    """删除项目"""
    if len(args) < 1:
        print("用法: python onemaker.py delete <项目slug>")
        return
    slug = slugify(args[0])
    reg = load_registry()
    if slug not in reg["projects"]:
        print(f"[错误] 项目 '{slug}' 不存在")
        return

    name = reg["projects"][slug]["name"]
    confirm = input(f"确认删除项目 '{name}'({slug})？此操作不可恢复 (y/N): ")
    if confirm.lower() != "y":
        print("[取消] 已取消删除")
        return

    proj_dir = get_project_dir(slug)
    if proj_dir.exists():
        shutil.rmtree(proj_dir)
    del reg["projects"][slug]
    save_registry(reg)
    print(f"[成功] 项目 '{name}' 已删除")


def cmd_help(args):
    """显示帮助信息"""
    print(
        """
╔══════════════════════════════════════════════════════════╗
║            OneMaker 游戏项目管理工具 v1.0                ║
║        一人利用AI完成游戏全流程制作的管理系统              ║
╚══════════════════════════════════════════════════════════╝

用法: python onemaker.py <命令> [参数]

命令列表:
  new <名称> [中文名]        创建新游戏项目
  list                       列出所有项目
  status <slug>              查看项目详细状态
  stage <slug> <阶段>        推进项目阶段
  guide <slug> [阶段]        显示当前/指定阶段工作指南
  weekly <slug>              创建本周周报
  set <slug> <属性> <值>     设置项目属性
  delete <slug>              删除项目
  help                       显示此帮助

阶段列表:
  concept        概念期
  prototype      原型期
  vertical_slice 垂直切片
  production     量产期
  alpha          Alpha
  beta           Beta
  rc             发布候选
  launched       已发布

示例:
  python onemaker.py new my_rpg 我的RPG
  python onemaker.py list
  python onemaker.py status my_rpg
  python onemaker.py stage my_rpg prototype
  python onemaker.py guide my_rpg
  python onemaker.py weekly my_rpg
  python onemaker.py set my_rpg engine Unity
"""
    )


COMMANDS = {
    "new": cmd_new,
    "list": cmd_list,
    "status": cmd_status,
    "stage": cmd_stage,
    "guide": cmd_guide,
    "weekly": cmd_weekly,
    "set": cmd_set,
    "delete": cmd_delete,
    "help": cmd_help,
}


def main():
    if len(sys.argv) < 2:
        cmd_help([])
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd in COMMANDS:
        COMMANDS[cmd](args)
    else:
        print(f"[错误] 未知命令 '{cmd}'，运行 'python onemaker.py help' 查看帮助")


if __name__ == "__main__":
    main()
