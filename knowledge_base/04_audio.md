# 04 音频（Audio）

## 一、音乐制作（Music Production）

### 职责定义
为游戏创作BGM，包括主题音乐、场景音乐、战斗音乐、菜单音乐等。音乐是游戏情感的灵魂。

### 关键产出物
- **音乐需求表**：每个场景/状态需要的BGM清单
- **BGM文件**：WAV/OGG格式的成品音乐

### 详细操作步骤

#### Step 1: 制作音乐需求表
```
BGM需求表模板：

| ID | 场景/状态 | 情绪 | BPM | 时长 | 循环 | 优先级 |
|----|---------|------|-----|------|------|-------|
| M01 | 主菜单 | 史诗/期待 | 80-100 | 2min | 是 | P0 |
| M02 | 村庄 | 温暖/安宁 | 70-90 | 3min | 是 | P0 |
| M03 | 森林 | 神秘/探索 | 90-110 | 3min | 是 | P0 |
| M04 | 战斗-普通 | 紧张/节奏 | 120-140 | 2min | 是 | P0 |
| M05 | 战斗-Boss | 激烈/史诗 | 140-160 | 3min | 是 | P0 |
| M06 | 地牢 | 阴暗/压迫 | 80-100 | 3min | 是 | P1 |
| M07 | 胜利 | 欢快/成就 | 130 | 30s | 否 | P0 |
| M08 | 失败 | 悲伤/遗憾 | 60-80 | 30s | 否 | P0 |
| M09 | 标题画面 | 悬疑/吸引 | 70 | 1min | 是 | P1 |
```

#### Step 2: 音乐制作流程（AI辅助）
```
制作流程：

1. 确定音乐参数
   - 调性：大调（明亮）/ 小调（阴暗）
   - BPM：根据场景节奏
   - 乐器编制：弦乐+钢琴+打击 等
   - 情绪关键词：3-5个

2. AI生成初稿
   工具选择：
   - Suno AI：快速生成完整曲子
   - Udio：更精细的风格控制
   - AIVA：古典/交响乐风格

   Prompt模板：
   "[风格] [情绪] background music, [BPM] BPM,
    [乐器列表], [调性], loopable,
    video game soundtrack"

3. 人工精修（可选）
   - 用Audacity进行裁剪/淡入淡出
   - 调整EQ/压缩
   - 确保无缝循环

4. 导出规范
   - 格式：OGG Vorbis（游戏内）/ WAV（高品质存档）
   - 采样率：44100Hz
   - 声道：立体声
   - 比特率：OGG 128-192kbps
```

#### Step 3: 音乐循环技术
```
无缝循环制作要点：

1. 采样级精确对齐
   - 起始点和结束点必须在同相位
   - 推荐在零交叉点裁剪
   - Audacity操作：选区 → 编辑 → 剪裁

2. 交叉淡入淡出
   - 在结尾处添加10-50ms的crossfade
   - 消除循环点的"咔嗒"声

3. 和弦进行循环
   推荐使用可循环的和弦进行：
   | 进行 | 情绪 |
   |------|------|
   | I-V-vi-IV | 明亮/正能量 |
   | vi-IV-I-V | 流行/振奋 |
   | i-VI-III-VII | 暗黑/史诗 |
   | i-iv-VII-III | 悲伤/紧张 |

4. 分层BGM（高级）
   低层：基础节奏+低音（始终播放）
   中层：旋律线（战斗时加入）
   高层：打击乐/特效（高潮时加入）
   → 根据游戏状态动态混合各层
```

### AI协作方式
- **音乐生成**：用Suno/Udio生成BGM初稿
- **配器建议**：让AI根据场景情绪推荐乐器组合
- **乐理辅助**：让AI生成和弦进行、旋律变奏

---

## 二、音效制作（Sound Effects）

### 职责定义
制作游戏内所有短音效：攻击音、脚步声、UI音效、环境音、角色语音等。

### 关键产出物
- **音效表（SFX Sheet）**：所有音效的清单与规范
- **音效文件**：WAV格式音效
- **音效变体**：每个音效2-4个变体（防听觉疲劳）

### 详细操作步骤

#### Step 1: 制作音效需求表
```
SFX需求表模板：

| ID | 类别 | 名称 | 触发时机 | 时长 | 变体数 | 优先级 |
|----|------|------|---------|------|-------|-------|
| S01 | 战斗 | 剑挥 | 攻击动画第5帧 | 0.3s | 3 | P0 |
| S02 | 战斗 | 命中 | 伤害判定帧 | 0.2s | 4 | P0 |
| S03 | 战斗 | 格挡 | 格挡成功 | 0.3s | 2 | P1 |
| S04 | 角色 | 脚步-草地 | 行走每步 | 0.15s | 6 | P0 |
| S05 | 角色 | 脚步-石地 | 行走每步 | 0.15s | 6 | P0 |
| S06 | 角色 | 跳跃 | 起跳瞬间 | 0.3s | 1 | P0 |
| S07 | 角色 | 落地 | 着地瞬间 | 0.2s | 2 | P0 |
| S08 | 角色 | 受伤 | HP减少 | 0.2s | 3 | P0 |
| S09 | 角色 | 死亡 | HP=0 | 0.5s | 1 | P0 |
| S10 | UI | 按钮点击 | 按下按钮 | 0.1s | 1 | P0 |
| S11 | UI | 按钮悬停 | 鼠标经过 | 0.1s | 1 | P1 |
| S12 | UI | 获得物品 | 拾取道具 | 0.3s | 2 | P0 |
| S13 | UI | 升级 | 等级提升 | 0.5s | 1 | P0 |
| S14 | 环境 | 水流 | 河边场景 | 5s | 1 | P1 |
| S15 | 环境 | 风声 | 户外场景 | 5s | 1 | P1 |
| S16 | 环境 | 篝火 | 火堆旁 | 3s | 1 | P1 |
```

#### Step 2: AI辅助音效制作
```
音效制作方式对比：

| 方式 | 工具 | 质量 | 速度 | 适合 |
|------|------|------|------|------|
| AI生成 | ElevenLabs/Suno | 中高 | 快 | 快速原型 |
| 免费素材库 | freesound.org | 中 | 快 | 通用音效 |
| 拟音录制 | 手机+Audacity | 高 | 慢 | 定制音效 |
| 合成器制作 | sfxr/Bfxr | 中 | 快 | 像素/复古 |
| 购买素材包 | Asset Store | 高 | 快 | 预算充足 |

推荐流程：
1. 先从免费素材库找基础素材
2. 用AI生成难以录制的音效（魔法、科幻）
3. 用Audacity拼接/变调/混响加工
4. 为每个音效制作2-4个变体
```

#### Step 3: 音效变体制作
```
变体制作方法（防止听觉疲劳）：

1. 音高偏移（Pitch Shift）
   - 变体1: 原始音高
   - 变体2: +2 半音
   - 变体3: -2 半音
   - 变体4: +4 半音

2. 时间微调（Time Stretch）
   - 变体1: 原始时长
   - 变体2: 95% 速度
   - 变体3: 105% 速度

3. 滤波变化
   - 变体1: 原始
   - 变体2: 低通滤波（闷一点）
   - 变体3: 高通滤波（薄一点）

Audacity操作：
- 导入音频 → 选择区域
- 效果 → 变调（Pitch Shift）
- 效果 → 滤波器 → 低通/高通
- 导出为WAV
```

#### Step 4: 音效文件规范
```
音效文件规范：

格式：WAV（无损）
采样率：44100Hz 或 48000Hz
位深度：16bit
声道：单声道（3D音效）/ 立体声（2D音效/UI音效）

文件命名：snd_[类别]_[名称]_[变体]
  snd_combat_sword_hit_01.wav
  snd_combat_sword_hit_02.wav
  snd_step_grass_01.wav

文件大小限制：
  UI音效：≤50KB
  战斗音效：≤200KB
  环境音：≤500KB
```

---

## 三、语音制作（Voice & Dialogue）

### 职责定义
制作角色语音、旁白、战斗喊话等。

### 关键产出物
- **语音需求表**：所有语音台词清单
- **语音文件**：WAV格式录音

### 详细操作步骤

#### Step 1: 语音需求分类
```
语音类型表：

| 类型 | 示例 | 数量估计 | 时长 |
|------|------|---------|------|
| 战斗喊话 | "看招！"/"受死吧！" | 5-10条 | 0.5-1s |
| 受伤呻吟 | "啊！"/"唔..." | 3-5条 | 0.3-0.5s |
| 死亡台词 | "不...不可能..." | 1-3条 | 1-2s |
| 互动台词 | NPC对话语音 | 20-50条 | 2-5s |
| 技能名称 | "火球术！"/"治愈之光！" | 5-15条 | 0.5-1s |
| 旁白 | 开场/过场解说 | 5-10条 | 5-30s |
| 系统提示 | "任务完成"/"警告" | 10-20条 | 1-2s |
```

#### Step 2: AI语音制作
```
AI语音工具对比：

| 工具 | 质量 | 中文支持 | 免费 | 特点 |
|------|------|---------|------|------|
| ElevenLabs | ★★★★★ | 部分 | 有限 | 最逼真 |
| Edge TTS | ★★★★ | 是 | 免费 | 微软，质量好 |
| VITS | ★★★ | 是 | 免费 | 可训练 |
| 讯飞语音 | ★★★★ | 是 | 有限 | 中文最佳 |

推荐流程：
1. 编写台词文本
2. 用Edge TTS生成中文语音（免费且质量好）
3. 用Audacity进行后处理（EQ、压缩、混响）
4. 导出为规范格式

Edge TTS使用：
pip install edge-tts
edge-tts --text "看招！" --voice zh-CN-YunxiNeural --write-media output.wav
```

#### Step 3: 语音后处理
```
语音后处理链（Audacity）：

1. 降噪
   - 选择静音区域 → 获取噪声配置
   - 全选 → 降噪（降噪量12dB）

2. EQ均衡
   - 高通滤波：切除80Hz以下低频
   - 提升2-4kHz：增强清晰度

3. 压缩
   - 阈值：-18dB
   - 比率：3:1
   - 让音量更均匀

4. 归一化
   - 目标：-3dB
   - 确保所有文件音量一致

5. 混响（可选）
   - 室内场景：加轻微混响
   - 户外场景：不加或极少
```

---

## 四、音频引擎集成（Audio Integration）

### 职责定义
将所有音频资源集成到游戏引擎中，实现动态混音、3D音效、音频触发。

### 关键产出物
- **音频管理器代码**：统一的音频播放接口
- **音频配置表**：音量、衰减、混音参数
- **音频触发器**：场景中的音效触发点

### 详细操作步骤

#### Step 1: 搭建音频管理器
```csharp
public class AudioMgr {
    AudioSource _bgmSource;
    List<AudioSource> _sfxSources;
    float _bgmVol = 1f;
    float _sfxVol = 1f;

    public void Init(GameObject root) {
        _bgmSource = root.AddComponent<AudioSource>();
        _bgmSource.loop = true;
        _sfxSources = new List<AudioSource>();
        for (int i = 0; i < 10; i++) {
            var src = root.AddComponent<AudioSource>();
            _sfxSources.Add(src);
        }
    }

    public void PlayBGM(string name, float fadeTime = 1f) {
        var clip = LoadClip("Audio/BGM/" + name);
        if (clip == null) return;
        // 简单淡入
        _bgmSource.clip = clip;
        _bgmSource.volume = 0;
        _bgmSource.Play();
        // DOTween淡入
        DOTween.To(() => _bgmSource.volume, v => _bgmSource.volume = v, _bgmVol, fadeTime);
    }

    public void StopBGM(float fadeTime = 1f) {
        DOTween.To(() => _bgmSource.volume, v => _bgmSource.volume = v, 0f, fadeTime)
            .OnComplete(() => _bgmSource.Stop());
    }

    public void PlaySFX(string name, float vol = 1f) {
        var clip = LoadClip("Audio/SFX/" + name);
        if (clip == null) return;
        var src = GetAvailableSFXSource();
        src.volume = _sfxVol * vol;
        src.PlayOneShot(clip);
    }

    // 3D音效
    public void PlaySFX3D(string name, Vector3 pos, float maxDist = 20f) {
        var clip = LoadClip("Audio/SFX/" + name);
        if (clip == null) return;
        var src = GetAvailableSFXSource();
        src.spatialBlend = 1f;
        src.minDistance = 1f;
        src.maxDistance = maxDist;
        src.rolloffMode = AudioRolloffMode.Logarithmic;
        src.transform.position = pos;
        src.PlayOneShot(clip, _sfxVol);
    }

    AudioSource GetAvailableSFXSource() {
        return _sfxSources.FirstOrDefault(s => !s.isPlaying) ?? _sfxSources[0];
    }

    AudioClip LoadClip(string path) {
        return Resources.Load<AudioClip>(path);
    }

    public void SetBGMVolume(float vol) { _bgmVol = vol; }
    public void SetSFXVolume(float vol) { _sfxVol = vol; }
}
```

#### Step 2: 实现动态混音
```
动态混音规则：

| 游戏状态 | BGM音量 | SFX音量 | 环境音量 | 说明 |
|---------|---------|---------|---------|------|
| 主菜单 | 80% | 0% | 0% | 只放菜单音乐 |
| 探索 | 60% | 0% | 40% | 环境+轻BGM |
| 对话 | 30% | 0% | 10% | 压低BGM突出语音 |
| 战斗 | 80% | 100% | 20% | 战斗BGM+SFX为主 |
| 暂停 | 20% | 0% | 0% | 大幅压低BGM |

混音过渡时间：
- 探索→战斗：0.5s快速过渡
- 战斗→探索：2s缓慢恢复
- 进入对话：0.3s淡出
```

#### Step 3: 音频触发器配置
```csharp
// 区域音效触发器
public class AudioZone : MonoBehaviour {
    public string ambientClip;
    public float fadeTime = 1f;

    void OnTriggerEnter(Collider other) {
        if (other.CompareTag("Player")) {
            GameMgr.Inst.Audio.PlaySFX3D(ambientClip, transform.position);
            // 或切换环境音
        }
    }
}

// 动画音效触发
// 在Animation Event中调用
public class AnimAudio : MonoBehaviour {
    public void PlaySFX(string clipName) {
        GameMgr.Inst.Audio.PlaySFX(clipName);
    }
}

// 脚步声系统
public class FootstepPlayer : MonoBehaviour {
    public float stepInterval = 0.5f;
    public string[] surfaceTypes = { "grass", "stone", "wood", "water" };
    string _currentSurface;

    float _timer;

    void Update() {
        if (!IsMoving()) return;
        _timer += Time.deltaTime;
        if (_timer >= stepInterval) {
            _timer = 0;
            PlayFootstep();
        }
    }

    void PlayFootstep() {
        // 射线检测地面材质
        if (Physics.Raycast(transform.position + Vector3.up, Vector3.down, out var hit, 2f)) {
            _currentSurface = hit.collider.tag; // "grass"/"stone"等
        }
        string clipName = $"snd_step_{_currentSurface}_{Random.Range(1, 7):D2}";
        GameMgr.Inst.Audio.PlaySFX(clipName, 0.6f);
    }
}
```

#### Step 4: 音频资源配置
```
Unity音频导入设置：

BGM设置：
  - Load Type: Streaming（流式加载，节省内存）
  - Compression: Vorbis
  - Quality: 70-100%
  - Sample Rate Setting: Preserve Sample Rate

SFX设置（短音效）：
  - Load Type: Decompress on Load（解压后缓存）
  - Compression: PCM（无损）
  - 3D Sound: 勾选（需要3D定位的音效）
  - 3D Settings:
    - Volume Rolloff: Logarithmic
    - Min Distance: 1
    - Max Distance: 20-50

环境音设置：
  - Load Type: Compressed in Memory
  - Compression: Vorbis
  - Quality: 60-80%
  - Loop: 勾选
```

---

## 五、混音与优化（Mixing & Optimization）

### 职责定义
统一调整所有音频的音量平衡、频率分布、空间定位，确保最终音质。

### 关键产出物
- **混音规范文档**：音量标准、频率分配
- **音频性能报告**：内存占用、CPU占用

### 详细操作步骤

#### Step 1: 混音标准
```
音频层级音量标准：

| 层级 | 音量基准 | 说明 |
|------|---------|------|
| BGM | -12dB ~ -8dB | 始终作为背景 |
| 语音 | 0dB | 最重要，必须清晰 |
| 战斗SFX | -3dB ~ 0dB | 突出反馈感 |
| UI SFX | -6dB ~ -3dB | 清晰但不突兀 |
| 环境音 | -18dB ~ -12dB | 背景氛围 |

频率分配原则：
  BGM: 中低频为主（100Hz-2kHz）
  语音: 中频（500Hz-4kHz）
  SFX: 中高频（1kHz-8kHz）
  环境音: 低频+超高频（<500Hz + >4kHz）
```

#### Step 2: 音频性能优化
```
优化要点：

1. 内存优化
   - BGM使用Streaming加载
   - 短音效使用Compressed in Memory
   - 长环境音使用Streaming
   - 预估总音频内存：≤50MB（移动端）

2. CPU优化
   - 同时播放的AudioSource上限：15-20个
   - 使用对象池管理AudioSource
   - 距离远的3D音效自动静音

3. 文件大小优化
   - BGM: OGG 128kbps（1分钟≈1MB）
   - SFX: WAV 16bit（0.3秒≈30KB）
   - 环境音: OGG 96kbps（5秒≈60KB）
   - 总包体音频预算：≤30MB（移动端）/ ≤200MB（PC）

4. 加载优化
   - 常用SFX预加载到内存
   - BGM按场景异步加载
   - 场景切换时释放上一场景音频
```

#### Step 3: 音频测试检查
```
音频测试清单：

功能测试：
- [ ] BGM能否正常播放和循环？
- [ ] BGM切换是否有淡入淡出？
- [ ] 所有SFX是否正确触发？
- [ ] 3D音效空间感是否正确？
- [ ] 音量控制是否即时生效？

品质测试：
- [ ] 各层级音量是否平衡？
- [ ] 有无爆音/失真？
- [ ] 重复播放的SFX是否有变体？
- [ ] 语音是否清晰可辨？
- [ ] 环境音是否自然不突兀？

性能测试：
- [ ] 同时播放的音源数量是否合理？
- [ ] 音频总内存占用是否在预算内？
- [ ] 场景切换时音频是否正常释放？
- [ ] 低端设备是否卡顿？
```

---

## 音频阶段检查清单

- [ ] 音乐需求表是否完成？
- [ ] 所有BGM是否制作/选型完成？
- [ ] BGM是否能无缝循环？
- [ ] 音效需求表是否完成？
- [ ] 所有SFX是否制作完成？
- [ ] 每个高频SFX是否有2-4个变体？
- [ ] 语音是否制作完成？（如有）
- [ ] 音频管理器是否搭建？
- [ ] 动态混音是否实现？
- [ ] 3D音效是否正确配置？
- [ ] 音量标准是否统一？
- [ ] 音频总内存是否在预算内？
