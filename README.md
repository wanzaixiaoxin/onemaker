# OneMaker - 独立游戏AI全流程制作工具

> 一个人 + AI = 一个游戏团队

## 快速开始

```bash
# 查看帮助
python onemaker.py help

# 创建新游戏项目
python onemaker.py new my_game 我的游戏

# 查看所有项目
python onemaker.py list

# 查看项目状态
python onemaker.py status my_game

# 查看当前阶段工作指南
python onemaker.py guide my_game

# 推进到下一阶段
python onemaker.py stage my_game prototype

# 创建周报
python onemaker.py weekly my_game

# 设置项目属性
python onemaker.py set my_game engine Unity
python onemaker.py set my_game genre ARPG
python onemaker.py set my_game platform Steam
```

## 项目结构

```
onemaker/
├── onemaker.py              # 项目管理CLI工具
├── projects.json            # 项目注册表（自动生成）
├── projects/                # 游戏项目目录（可管理多个）
│   └── my_game/
│       ├── design/          # 设计文档
│       │   ├── concept_doc.md
│       │   └── gdd.md
│       ├── art/             # 美术资产与文档
│       │   └── art_bible.md
│       ├── audio/           # 音频资产与文档
│       │   └── audio_spec.md
│       ├── dev/             # 代码/工程
│       ├── marketing/       # 营销素材
│       ├── weekly/          # 周报
│       │   └── week_001.md
│       └── checklist.md     # 阶段检查清单
├── templates/               # 文档模板
│   ├── concept_doc.md
│   ├── gdd.md
│   ├── art_bible.md
│   ├── audio_spec.md
│   ├── checklist.md
│   └── weekly_review.md
└── knowledge_base/          # 知识库（参考资料）
    ├── 01_game_design.md
    ├── 02_programming.md
    ├── 03_art.md
    ├── 04_audio.md
    ├── 05_pm_and_publish.md
    └── 06_ai_toolchain.md
```

## 开发阶段

| 阶段 | 名称 | 目标 |
|------|------|------|
| concept | 概念期 | 确定核心概念，验证方向 |
| prototype | 原型期 | 验证核心玩法是否有趣 |
| vertical_slice | 垂直切片 | 完成一个完整关卡的全品质体验 |
| production | 量产期 | 批量制作所有内容 |
| alpha | Alpha | 功能完整，内部测试 |
| beta | Beta | 内容完整，外部测试 |
| rc | 发布候选 | 最终打磨，准备发布 |
| launched | 已发布 | 正式上架，持续运营 |

## 多游戏管理

OneMaker 支持同时管理多个游戏项目，每个项目有独立的设计文档、资产目录、周报和进度追踪。

```bash
# 同时管理多个项目
python onemaker.py new rpg_game 冒险传说
python onemaker.py new puzzle_game 谜之迷宫
python onemaker.py new casual_game 休闲农场

# 查看所有项目进度
python onemaker.py list

# 分别查看各项目状态
python onemaker.py status rpg_game
python onemaker.py status puzzle_game
```

## AI工具链

每个阶段都提供AI协作建议和Prompt模板，详见各阶段工作指南（`python onemaker.py guide <项目>`）。

完整的AI工具链参考：[knowledge_base/06_ai_toolchain.md](knowledge_base/06_ai_toolchain.md)
