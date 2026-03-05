# MVSEP GUI Rust 重写设计方案

## 1. 项目概述

- **项目名称**: MVSEP GUI (Rust)
- **项目类型**: 桌面应用程序 (Tauri)
- **核心功能**: MVSEP 音乐分离 API 的图形界面工具，支持音频文件上传、分离任务管理、进度跟踪、结果下载
- **目标用户**: 音乐制作人、音频工程师、普通用户

## 2. 技术栈

| 层次 | 技术选择 | 理由 |
|------|----------|------|
| GUI 框架 | Tauri v2 | 体积小 (~10MB)，性能好，支持现代 Web 技术 |
| 前端框架 | React 18 + TypeScript | 组件化，适合复杂 UI，类型安全 |
| 样式 | Tailwind CSS | 灵活，易于实现多主题 |
| 状态管理 | Zustand | 轻量级，简单易用 |
| 后端语言 | Rust | 高性能，减少外部依赖 |
| HTTP 客户端 | reqwest | 成熟的 Rust HTTP 库 |
| 国际化 | i18next | React 生态主流选择 |

## 3. 功能范围

完整移植原 Python PyQt6 版本的所有功能：

### 3.1 核心功能
- [ ] API Token 管理与自动保存
- [ ] 音频文件拖放上传 (MP3, WAV, FLAC, M4A, OGG)
- [ ] 分离算法搜索和选择
- [ ] 多种输出格式支持
- [ ] 实时进度显示 (上传/处理/下载)
- [ ] 结果自动下载到本地

### 3.2 设置功能
- [ ] 多语言支持 (中文、英文、日文)
- [ ] 多主题支持 (纯黑、亮白、浅紫)
- [ ] 输出目录配置
- [ ] 超时时间设置
- [ ] 代理配置
- [ ] 镜像源选择

### 3.3 辅助功能
- [ ] 本地历史记录
- [ ] 日志面板
- [ ] 连接测试
- [ ] 获取 Token 帮助

## 4. 架构设计

### 4.1 项目结构

```
mvsep-gui-rust/
├── src-tauri/              # Rust 后端
│   ├── src/
│   │   ├── main.rs         # 入口点
│   │   ├── api.rs          # MVSEP API 调用
│   │   ├── commands.rs     # Tauri 命令
│   │   ├── config.rs       # 配置管理
│   │   ├── history.rs      # 历史记录
│   │   ├── logging.rs      # 日志系统
│   │   └── types.rs        # 类型定义
│   ├── Cargo.toml
│   └── tauri.conf.json
├── src/                    # React 前端
│   ├── components/         # UI 组件
│   │   ├── DropZone.tsx
│   │   ├── AlgorithmSelect.tsx
│   │   ├── ProgressPanel.tsx
│   │   ├── SettingsDialog.tsx
│   │   ├── HistoryDialog.tsx
│   │   └── ...
│   ├── hooks/              # React Hooks
│   ├── i18n/               # 国际化
│   │   ├── index.ts
│   │   └── locales/
│   │       ├── zh.json
│   │       ├── en.json
│   │       └── ja.json
│   ├── themes/             # 主题样式
│   ├── stores/             # Zustand stores
│   ├── types/              # TypeScript 类型
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

### 4.2 Rust 后端模块

#### api.rs - MVSEP API 调用
```rust
// 主要功能：
// - create_task: 创建分离任务
// - get_status: 获取任务状态
// - wait_for_completion: 等待任务完成（带回调）
// - download_results: 下载结果文件
// - get_algorithms: 获取算法列表
// - get_separation_history: 获取历史记录
// - test_connection: 测试连接
```

#### config.rs - 配置管理
```rust
// 配置项：
// - api_token: API 令牌
// - language: 语言 (zh/en/ja)
// - theme: 主题 (dark/light/otaku/system)
// - mirror: 镜像源 (main/mirror)
// - timeout: 超时时间（秒）
// - proxy: 代理设置
// - output_dir: 输出目录
// - output_format: 输出格式
```

#### history.rs - 历史记录
```rust
// 功能：
// - save_history: 保存任务到历史
// - load_history: 加载历史记录
// - update_history: 更新任务状态
```

#### logging.rs - 日志系统
```rust
// 功能：
// - debug_log: 调试日志
// - info_log: 信息日志
// - error_log: 错误日志
// - read_log: 读取日志文件
```

### 4.3 前端组件

| 组件 | 功能 |
|------|------|
| DropZone | 拖放上传区域，支持点击选择文件 |
| AlgorithmSelect | 算法搜索下拉选择框 |
| FormatSelect | 输出格式选择 |
| ProgressPanel | 进度显示面板（状态、百分比、速度） |
| StatusIndicator | 状态指示器（空闲/处理中/成功/错误） |
| SettingsDialog | 设置对话框 |
| HistoryDialog | 历史记录对话框 |
| LogPanel | 日志面板 |

### 4.4 主题系统

使用 CSS 变量实现主题切换：

```css
/* dark theme (default) */
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #eaeaea;
  --accent: #0f3460;
  --accent-hover: #e94560;
}

/* light theme */
[data-theme="light"] {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #333333;
  --accent: #4a90e2;
}

/* otaku theme */
[data-theme="otaku"] {
  --bg-primary: #1a1a2e;
  --bg-secondary: #2d1b4e;
  --text-primary: #eaeaea;
  --accent: #7c3aed;
  --accent-hover: #c084fc;
}
```

## 5. API 接口映射

根据 mvsep-cli 的实现，Rust 后端需要实现以下接口：

### 5.1 创建任务
```
POST /api/separation/create
参数:
  - api_token: str
  - audiofile: File
  - sep_type: int (算法ID)
  - output_format: int (0-5)
  - add_opt1/2/3: Optional[str]
返回:
  - hash: str
  - success: bool
```

### 5.2 获取状态
```
GET /api/separation/get?hash=xxx
返回:
  - status: "waiting"|"processing"|"done"|"failed"
  - data.files: [{"url": "...", ...}]
  - data.queue_count: int
```

### 5.3 获取算法列表
```
GET /api/app/algorithms?scopes=single_upload
返回:
  - [{"render_id": 20, "name": "...", "algorithm_fields": [...]}]
```

### 5.4 输出格式

| ID | 格式 |
|----|------|
| 0 | MP3 (320 kbps) |
| 1 | WAV (16 bit) |
| 2 | FLAC (16 bit) |
| 3 | M4A (lossy) |
| 4 | WAV (32 bit) |
| 5 | FLAC (24 bit) |

### 5.5 镜像源

| 名称 | URL |
|------|-----|
| main | https://mvsep.com |
| mirror | https://mirror.mvsep.com |

## 6. 数据流

```
用户选择文件
    ↓
前端调用 Tauri 命令 (create_task)
    ↓
Rust 后端上传文件到 MVSEP API
    ↓
获取 hash，返回给前端
    ↓
前端显示进度，后端轮询状态
    ↓
状态变为 done
    ↓
后端下载结果文件
    ↓
返回文件路径给前端，显示完成
```

## 7. Tauri 命令设计

```rust
#[tauri::command]
async fn create_separation_task(
    file_path: String,
    sep_type: i32,
    output_format: i32,
    add_opt1: Option<String>,
    add_opt2: Option<String>,
    add_opt3: Option<String>,
) -> Result<TaskResult, String>

#[tauri::command]
async fn get_task_status(hash: String) -> Result<StatusResult, String>

#[tauri::command]
async fn wait_for_completion(hash: String, window: Window) -> Result<StatusResult, String>

#[tauri::command]
async fn download_results(
    hash: String,
    output_dir: String,
    window: Window,
) -> Result<Vec<String>, String>

#[tauri::command]
fn get_algorithms() -> Result<Vec<Algorithm>, String>

#[tauri::command]
fn save_config(config: AppConfig) -> Result<(), String>

#[tauri::command]
fn load_config() -> Result<AppConfig, String>

#[tauri::command]
fn test_connection() -> Result<bool, String>
```

## 8. 国际化文本

需要翻译的文本（约 80+ 条）：

### 中文 (zh)
- "MVSEP 工作室" / "音乐分离工具"
- "拖放音频文件到此处" / "或点击选择文件"
- "开始分离" / "分离中..."
- "设置" / "语言" / "主题"
- ...

### 英文 (en)
- "MVSEP Studio" / "Music Separation Tool"
- ...

### 日文 (ja)
- "MVSEP スタジオ" / "音楽分離ツール"
- ...

## 9. 验收标准

1. ✅ 应用可以启动并显示主界面
2. ✅ 可以输入和保存 API Token
3. ✅ 可以拖放或选择音频文件
4. ✅ 可以搜索和选择分离算法
5. ✅ 可以选择输出格式和目录
6. ✅ 可以开始分离任务并显示进度
7. ✅ 任务完成后自动下载结果
8. ✅ 可以切换语言（中文/英文/日文）
9. ✅ 可以切换主题（纯黑/亮白/浅紫）
10. ✅ 可以查看历史记录
11. ✅ 可以查看日志
12. ✅ 可以配置代理和超时
13. ✅ 可以测试连接
14. ✅ 配置文件正确保存和加载

## 10. 已知限制

- 暂不支持远程 URL 上传（仅本地文件）
- 暂不支持取消任务功能
- 暂不支持 quality_checker 相关功能
