# 02 程序开发（Programming）

## 一、引擎/框架选型（Engine & Framework Selection）

### 职责定义
选择最适合项目需求的游戏引擎、编程语言和工具链。这是技术决策的基石。

### 关键产出物
- **技术选型文档**：引擎对比分析、选择理由
- **开发环境配置文档**：引擎版本、插件列表、环境变量

### 主流引擎对比

| 引擎 | 语言 | 适合类型 | 优势 | 劣势 | AI辅助成熟度 |
|------|------|---------|------|------|-------------|
| Unity | C# | 全类型 | 生态丰富、2D/3D均强 | 抽水制度变化 | ★★★★★ |
| Unreal Engine | C++/蓝图 | 3A、写实3D | 渲染顶级、蓝图可视化 | 学习曲线陡 | ★★★★ |
| Godot | GDScript/C# | 2D/轻量3D | 开源免费、轻量 | 生态较小 | ★★★ |
| Cocos Creator | TypeScript | 2D/小游戏 | 中国生态、小游戏适配 | 3D能力弱 | ★★★ |

### 选型决策树
```
你的游戏是？
├── 2D为主
│   ├── 需要发布到微信小游戏？ → Cocos Creator
│   ├── 追求轻量和开源？ → Godot
│   └── 需要丰富生态？ → Unity
├── 3D写实风格
│   ├── 追求顶级画质？ → Unreal Engine
│   └── 平衡画质和效率？ → Unity
└── 特殊需求（大量定制渲染/物理）
    └── 考虑自研引擎（慎选）
```

### 详细操作步骤

#### Step 1: 确定技术需求清单
根据GDD列出技术需求：

| 需求类别 | 具体需求 | 必须满足 |
|---------|---------|---------|
| 渲染 | 2D/3D、粒子特效、后处理 |  |
| 物理 | 碰撞检测、刚体、射线 |  |
| 平台 | PC/移动端/Web/主机 |  |
| 网络 | 单机/联机/排行榜 |  |
| 音频 | 2D/3D音效、流式播放 |  |
| AI | 寻路、行为树、状态机 |  |
| UI | HUD、菜单、动画UI |  |
| 数据 | 存档、配置表、热更新 |  |

#### Step 2: 按需求筛选引擎
用上表逐一核对每个引擎是否满足需求。

#### Step 3: 搭建开发环境
```
Unity环境搭建清单：
- [ ] 安装Unity Hub
- [ ] 安装LTS版本（推荐最新LTS）
- [ ] 安装VS Code/Rider + 插件
- [ ] 创建项目（2D/3D/URP模板）
- [ ] 配置Git（.gitignore）
- [ ] 安装必要插件（UniTask、DoTween、etc）
- [ ] 搭建项目目录结构
```

### AI协作方式
- **技术选型分析**：描述项目需求，让AI对比引擎优劣
- **架构建议**：让AI根据引擎特性推荐架构模式

---

## 二、核心架构设计（Core Architecture）

### 职责定义
搭建游戏代码的整体架构，定义模块划分、数据流向、设计模式。

### 关键产出物
- **架构图**：模块关系图
- **编码规范文档**：命名、目录结构、代码风格
- **核心框架代码**：基础类和工具

### 详细操作步骤

#### Step 1: 选择架构模式

##### MVC（适合UI密集型）
```
Model（数据+逻辑）
  ↓ 数据变更通知
View（显示）
  ↑ 用户输入
Controller（协调）
```

##### ECS（适合大量同类对象）
```
Entity = 纯ID
Component = 纯数据（PositionComponent, HealthComponent）
System = 纯逻辑（MovementSystem, CombatSystem）

优势：数据与逻辑分离，天然支持缓存友好
适合：Roguelike、RTS、弹幕游戏
```

##### 状态机FSM（适合角色AI和流程控制）
```
状态机模板：

States: [Idle, Walk, Run, Jump, Attack, Hurt, Dead]
Transitions:
  Idle → Walk:  输入移动
  Walk → Run:   按住Shift
  Any → Hurt:   受到伤害
  Hurt → Idle:  动画结束
  Any → Dead:   HP <= 0
```

#### Step 2: 搭建核心管理器系统
```csharp
// 游戏核心管理器架构
public class GameMgr : MonoBehaviour {
    public static GameMgr Inst { get; private set; }

    public EventMgr Event { get; private set; }
    public UIMgr UI { get; private set; }
    public AudioMgr Audio { get; private set; }
    public SaveMgr Save { get; private set; }
    public SceneMgr Scene { get; private set; }
    public PoolMgr Pool { get; private set; }

    void Awake() {
        Inst = this;
        DontDestroyOnLoad(gameObject);
        InitManagers();
    }

    void InitManagers() {
        Event = new EventMgr();
        UI = new UIMgr();
        Audio = new AudioMgr();
        Save = new SaveMgr();
        Scene = new SceneMgr();
        Pool = new PoolMgr();
    }
}
```

#### Step 3: 搭建事件系统
```csharp
// 全局事件总线
public class EventMgr {
    Dictionary<string, Action<object>> _handlers = new();

    public void On(string evt, Action<object> handler) {
        if (!_handlers.ContainsKey(evt)) _handlers[evt] = null;
        _handlers[evt] += handler;
    }

    public void Off(string evt, Action<object> handler) {
        if (_handlers.ContainsKey(evt)) _handlers[evt] -= handler;
    }

    public void Emit(string evt, object data = null) {
        if (_handlers.ContainsKey(evt)) _handlers[evt]?.Invoke(data);
    }
}

// 使用示例
GameMgr.Inst.Event.On("player_damaged", OnPlayerDamaged);
GameMgr.Inst.Event.Emit("player_damaged", new DmgInfo(10));
```

#### Step 4: 搭建对象池
```csharp
public class PoolMgr {
    Dictionary<string, Queue<GameObject>> _pools = new();

    public GameObject Spawn(GameObject prefab, Vector3 pos, Quaternion rot) {
        string key = prefab.name;
        if (_pools.TryGetValue(key, out var q) && q.Count > 0) {
            var go = q.Dequeue();
            go.transform.SetPositionAndRotation(pos, rot);
            go.SetActive(true);
            return go;
        }
        return Object.Instantiate(prefab, pos, rot);
    }

    public void Despawn(GameObject go) {
        string key = go.name.Replace("(Clone)", "");
        if (!_pools.ContainsKey(key)) _pools[key] = new Queue<GameObject>();
        go.SetActive(false);
        _pools[key].Enqueue(go);
    }
}
```

#### Step 5: 搭建存档系统
```csharp
public class SaveMgr {
    string _path = Path.Combine(Application.persistentDataPath, "save.json");

    public void Save(GameData data) {
        var json = JsonUtility.ToJson(data, true);
        File.WriteAllText(_path, json);
    }

    public GameData Load() {
        if (!File.Exists(_path)) return new GameData();
        var json = File.ReadAllText(_path);
        return JsonUtility.FromJson<GameData>(json);
    }
}

[Serializable]
public class GameData {
    public int level;
    public int hp;
    public float posX, posY;
    public List<string> items;
    public Dictionary<string, bool> flags;
}
```

### 推荐项目结构（Unity）
```
Assets/
├── Scripts/
│   ├── Core/           # 核心框架
│   │   ├── GameMgr.cs
│   │   ├── EventMgr.cs
│   │   ├── UIMgr.cs
│   │   ├── PoolMgr.cs
│   │   ├── SaveMgr.cs
│   │   └── Singleton.cs
│   ├── Gameplay/       # 游戏逻辑
│   │   ├── Player/
│   │   ├── Enemy/
│   │   ├── Item/
│   │   └── Weapon/
│   ├── AI/             # AI行为
│   │   ├── FSM.cs
│   │   ├── BehaviorTree.cs
│   │   └── AStar.cs
│   ├── UI/             # UI面板
│   ├── Data/           # 数据结构
│   └── Utils/          # 工具类
├── Prefabs/
├── Art/
├── Audio/
└── Scenes/
```

### AI协作方式
- **架构设计**：描述游戏需求，让AI推荐架构方案
- **代码框架生成**：让AI生成基础框架代码
- **代码审查**：让AI审查代码质量和架构合理性

---

## 三、玩法实现（Gameplay Implementation）

### 职责定义
实现游戏的核心玩法逻辑，包括角色控制、物理系统、碰撞检测、战斗系统等。

### 关键产出物
- **核心玩法代码**：角色控制器、战斗系统、AI等
- **单元测试**：关键逻辑的测试用例

### 详细操作步骤

#### Step 1: 实现角色控制器
```csharp
public class PlayerCtrl : MonoBehaviour {
    [Header("移动参数")]
    public float walkSpeed = 5f;
    public float runSpeed = 8f;
    public float jumpForce = 10f;
    public float gravity = -20f;

    CharacterController _cc;
    Animator _anim;
    Vector3 _velocity;
    bool _isGrounded;

    void Awake() {
        _cc = GetComponent<CharacterController>();
        _anim = GetComponent<Animator>();
    }

    void Update() {
        _isGrounded = _cc.isGrounded;
        if (_isGrounded && _velocity.y < 0) _velocity.y = -2f;

        // 移动
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        Vector3 dir = transform.right * h + transform.forward * v;
        float speed = Input.GetKey(KeyCode.LeftShift) ? runSpeed : walkSpeed;
        _cc.Move(dir * speed * Time.deltaTime);

        // 跳跃
        if (Input.GetKeyDown(KeyCode.Space) && _isGrounded) {
            _velocity.y = Mathf.Sqrt(jumpForce * -2f * gravity);
        }

        // 重力
        _velocity.y += gravity * Time.deltaTime;
        _cc.Move(_velocity * Time.deltaTime);

        // 动画
        _anim.SetFloat("Speed", dir.magnitude * speed);
        _anim.SetBool("Grounded", _isGrounded);
    }
}
```

#### Step 2: 实现战斗系统
```csharp
public class CombatSystem : MonoBehaviour {
    public int baseAtk = 10;
    public float critRate = 0.1f;
    public float critDmg = 1.5f;

    // 计算伤害
    public int CalcDamage(int atk, int def, float skillMult) {
        float raw = atk * skillMult - def * 0.5f;
        bool isCrit = Random.value < critRate;
        if (isCrit) raw *= critDmg;
        return Mathf.Max(1, Mathf.RoundToInt(raw));
    }

    // 近战判定（扇形/盒体）
    public GameObject[] MeleeDetect(float range, float angle, LayerMask targetLayer) {
        var hits = Physics.OverlapSphere(transform.position, range, targetLayer);
        var result = new List<GameObject>();
        foreach (var hit in hits) {
            Vector3 dir = (hit.transform.position - transform.position).normalized;
            if (Vector3.Angle(transform.forward, dir) < angle * 0.5f) {
                result.Add(hit.gameObject);
            }
        }
        return result.ToArray();
    }
}

// 可复用的生命值组件
public class Health : MonoBehaviour {
    public int maxHp = 100;
    int _hp;

    public event Action<int, int> OnHpChanged;
    public event Action OnDeath;

    void Start() => _hp = maxHp;

    public void TakeDamage(int dmg) {
        _hp = Mathf.Max(0, _hp - dmg);
        OnHpChanged?.Invoke(_hp, maxHp);
        if (_hp <= 0) OnDeath?.Invoke();
    }

    public void Heal(int amt) {
        _hp = Mathf.Min(maxHp, _hp + amt);
        OnHpChanged?.Invoke(_hp, maxHp);
    }
}
```

#### Step 3: 实现简单AI（状态机）
```csharp
public enum EnemyState { Idle, Patrol, Chase, Attack, Dead }

public class EnemyAI : MonoBehaviour {
    public float detectRange = 8f;
    public float atkRange = 2f;
    public float patrolRadius = 5f;

    EnemyState _state = EnemyState.Idle;
    Transform _target;
    NavMeshAgent _agent;
    float _idleTimer;

    void Awake() {
        _agent = GetComponent<NavMeshAgent>();
        _target = GameObject.FindGameObjectWithTag("Player").transform;
    }

    void Update() {
        float dist = Vector3.Distance(transform.position, _target.position);

        switch (_state) {
            case EnemyState.Idle:
                _idleTimer -= Time.deltaTime;
                if (_idleTimer <= 0) { _state = EnemyState.Patrol; Patrol(); }
                if (dist < detectRange) _state = EnemyState.Chase;
                break;

            case EnemyState.Patrol:
                if (dist < detectRange) _state = EnemyState.Chase;
                if (!_agent.hasPath) { _state = EnemyState.Idle; _idleTimer = 2f; }
                break;

            case EnemyState.Chase:
                _agent.SetDestination(_target.position);
                if (dist < atkRange) _state = EnemyState.Attack;
                if (dist > detectRange * 1.5f) _state = EnemyState.Idle;
                break;

            case EnemyState.Attack:
                // 攻击逻辑
                if (dist > atkRange) _state = EnemyState.Chase;
                break;
        }
    }

    void Patrol() {
        Vector3 rnd = transform.position + Random.insideUnitSphere * patrolRadius;
        NavMeshHit hit;
        if (NavMesh.SamplePosition(rnd, out hit, patrolRadius, 1)) {
            _agent.SetDestination(hit.position);
        }
    }
}
```

#### Step 4: 实现摄像机系统
```csharp
public class CameraFollow : MonoBehaviour {
    public Transform target;
    public float smoothSpeed = 5f;
    public Vector3 offset = new(0, 5, -10);

    // 摄像机震动
    float _shakeDuration, _shakeIntensity;
    Vector3 _shakeOffset;

    void LateUpdate() {
        if (!target) return;

        Vector3 desired = target.position + offset;
        transform.position = Vector3.Lerp(transform.position, desired, smoothSpeed * Time.deltaTime);

        // 应用震动
        if (_shakeDuration > 0) {
            _shakeOffset = Random.insideUnitSphere * _shakeIntensity;
            _shakeDuration -= Time.deltaTime;
        } else {
            _shakeOffset = Vector3.zero;
        }
        transform.position += _shakeOffset;
    }

    public void Shake(float duration, float intensity) {
        _shakeDuration = duration;
        _shakeIntensity = intensity;
    }
}
```

### 性能优化要点
| 优化项 | 方法 | 影响程度 |
|--------|------|---------|
| GC优化 | 使用对象池，避免每帧new | 高 |
| 缓存引用 | Awake中缓存组件引用 | 高 |
| 合批渲染 | SpriteAtlas / Static Batch | 高 |
| LOD | 远处使用低精度模型 | 中 |
| 遮挡剔除 | Occlusion Culling | 中 |
| 异步加载 | Addressables / Scene异步加载 | 中 |
| 减少Find | 避免GameObject.Find | 中 |

### AI协作方式
- **算法实现**：描述需求，让AI生成具体代码
- **Bug修复**：提供错误信息，让AI定位修复
- **性能优化**：让AI分析代码瓶颈并优化

---

## 四、UI/UX开发（UI/UX Development）

### 职责定义
实现游戏的用户界面系统，包括菜单、HUD、弹窗、设置等。

### 关键产出物
- **UI系统架构**：面板管理器、动画系统
- **UI预制体**：各界面组件
- **UX交互规范**：交互反馈标准

### 详细操作步骤

#### Step 1: 搭建UI管理器
```csharp
public class UIMgr {
    Canvas _canvas;
    Dictionary<string, UIPanel> _panels = new();
    Stack<UIPanel> _history = new();

    public void Init(Canvas canvas) {
        _canvas = canvas;
        // 预加载所有UI面板
        foreach (var panel in _canvas.GetComponentsInChildren<UIPanel>(true)) {
            _panels[panel.panelName] = panel;
            panel.gameObject.SetActive(false);
        }
    }

    public T Open<T>(object data = null) where T : UIPanel {
        string name = typeof(T).Name;
        if (_panels.TryGetValue(name, out var panel)) {
            panel.gameObject.SetActive(true);
            panel.OnOpen(data);
            _history.Push(panel);
            return panel as T;
        }
        return null;
    }

    public void CloseTop() {
        if (_history.Count > 0) {
            var panel = _history.Pop();
            panel.OnClose();
            panel.gameObject.SetActive(false);
        }
    }

    public void CloseAll() {
        while (_history.Count > 0) CloseTop();
    }
}

// UI面板基类
public abstract class UIPanel : MonoBehaviour {
    public string panelName;

    public virtual void OnOpen(object data = null) { }
    public virtual void OnClose() { }
}
```

#### Step 2: 实现HUD
```csharp
public class HUD : UIPanel {
    [SerializeField] Slider hpBar;
    [SerializeField] Text hpText;
    [SerializeField] Image[] skillIcons;
    [SerializeField] GameObject dmgPopupPrefab;

    Health _playerHP;

    public override void OnOpen(object data = null) {
        _playerHP = GameObject.FindGameObjectWithTag("Player").GetComponent<Health>();
        _playerHP.OnHpChanged += UpdateHP;
    }

    void UpdateHP(int cur, int max) {
        hpBar.value = (float)cur / max;
        hpText.text = $"{cur}/{max}";
    }

    // 伤害数字弹出
    public void ShowDamage(Vector3 worldPos, int dmg, bool isCrit) {
        var go = Instantiate(dmgPopupPrefab, transform);
        // worldPos → screenPos
        Vector2 screenPos = Camera.main.WorldToScreenPoint(worldPos);
        go.GetComponent<RectTransform>().position = screenPos;
        go.GetComponent<DmgPopup>().Show(dmg, isCrit);
    }
}
```

#### Step 3: 实现设置面板
```csharp
public class SettingsPanel : UIPanel {
    [SerializeField] Slider bgmSlider;
    [SerializeField] Slider sfxSlider;
    [SerializeField] Dropdown qualityDropdown;
    [SerializeField] Toggle fullscreenToggle;

    public override void OnOpen(object data = null) {
        // 读取当前设置
        bgmSlider.value = PlayerPrefs.GetFloat("bgm_vol", 1f);
        sfxSlider.value = PlayerPrefs.GetFloat("sfx_vol", 1f);
        qualityDropdown.value = QualitySettings.GetQualityLevel();
        fullscreenToggle.isOn = Screen.fullScreen;
    }

    public void OnBGMChanged(float val) {
        PlayerPrefs.SetFloat("bgm_vol", val);
        GameMgr.Inst.Audio.SetBGMVolume(val);
    }

    public void OnSFXChanged(float val) {
        PlayerPrefs.SetFloat("sfx_vol", val);
    }

    public void OnQualityChanged(int idx) {
        QualitySettings.SetQualityLevel(idx);
    }

    public void OnFullscreenChanged(bool val) {
        Screen.fullScreen = val;
    }
}
```

### UI系统模块
| 模块 | 功能 | 设计要点 |
|------|------|---------|
| 主菜单 | 开始/继续/设置/退出 | 简洁、快速进入游戏 |
| HUD | 血条/弹药/小地图/提示 | 信息层级清晰、不遮挡视野 |
| 背包/装备 | 物品管理、装备穿戴 | 拖拽操作、信息密度 |
| 对话系统 | NPC对话、选择分支 | 打字机效果、选项高亮 |
| 设置面板 | 音量/画质/按键绑定 | 即时生效、可重置 |
| 成就面板 | 成就列表、进度 | 解锁动画、分类展示 |

### UX设计原则
1. **响应性**：所有交互在100ms内给出视觉反馈
2. **一致性**：同类操作使用相同的交互方式
3. **容错性**：重要操作需要确认，支持撤销
4. **可达性**：支持键鼠/手柄/触屏多种输入

---

## 五、工具链/管线（Toolchain & Pipeline）

### 职责定义
构建开发自动化工具、资源管线、编辑器扩展。

### 关键产出物
- **编辑器扩展**：自定义Inspector、工具窗口
- **构建脚本**：一键打包多平台
- **数据管线**：Excel/JSON → 游戏配置

### 详细操作步骤

#### Step 1: 编辑器扩展示例
```csharp
// 自定义关卡编辑器窗口
public class LevelEditor : EditorWindow {
    [MenuItem("Tools/关卡编辑器")]
    static void Open() => GetWindow<LevelEditor>("关卡编辑器");

    void OnGUI() {
        GUILayout.Label("关卡工具", EditorStyles.boldLabel);

        if (GUILayout.Button("生成敌人波次")) {
            // 批量生成敌人配置
        }
        if (GUILayout.Button("检查关卡完整性")) {
            // 检查所有必要元素是否就位
        }
        if (GUILayout.Button("导出关卡数据")) {
            // 导出为JSON
        }
    }
}
```

#### Step 2: 自动构建脚本
```csharp
public class BuildScript {
    static void BuildAll() {
        string[] scenes = GetScenePaths();
        string buildPath = "Builds/";

        // PC构建
        BuildPipeline.BuildPlayer(new BuildPlayerOptions {
            scenes = scenes,
            locationPathName = buildPath + "PC/game.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        });

        Debug.Log("构建完成: " + buildPath);
    }

    static string[] GetScenePaths() {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }
}
```

#### Step 3: 数据导表工具
```csharp
// 从JSON配置生成C#数据类
public class ConfigGenerator {
    [MenuItem("Tools/生成配置代码")]
    static void Generate() {
        string jsonDir = "Assets/Data/Raw/";
        string outDir = "Assets/Scripts/Data/AutoGen/";

        foreach (var file in Directory.GetFiles(jsonDir, "*.json")) {
            string name = Path.GetFileNameWithoutExtension(file);
            string json = File.ReadAllText(file);
            // 解析JSON结构，生成C#类
            string code = GenerateClass(name, json);
            File.WriteAllText(outDir + name + ".cs", code);
        }
        AssetDatabase.Refresh();
    }
}
```

### 关键工具
| 工具 | 用途 | 优先级 |
|------|------|-------|
| 编辑器扩展 | 自定义Inspector、工具窗口 | 高 |
| 自动构建 | 一键打包多平台 | 高 |
| 数据导表 | Excel/JSON → 游戏配置 | 高 |
| 资源检查 | 检查资源规范（大小、格式） | 中 |
| CI/CD | 自动化测试和构建 | 中 |

---

## 编程阶段检查清单

- [ ] 引擎选型是否确定？
- [ ] 项目目录结构是否规范？
- [ ] 核心架构是否搭建完成？（GameMgr/EventMgr/UIMgr/PoolMgr）
- [ ] 编码规范是否文档化？
- [ ] 角色控制器是否实现？
- [ ] 战斗系统是否实现？
- [ ] AI系统是否实现？
- [ ] UI框架是否搭建完成？
- [ ] 是否有自动构建流程？
- [ ] 关键代码是否有单元测试？
- [ ] 性能基线是否建立？
