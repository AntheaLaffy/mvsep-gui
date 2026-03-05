# MVSEP GUI Rust 重写实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 使用 Tauri v2 + React + TypeScript 将 MVSEP 音乐分离 GUI 从 Python PyQt6 重写为 Rust

**架构:** Tauri 桌面应用，Rust 后端处理 API 调用和配置，前端使用 React + Tailwind CSS 实现现代化 UI

**技术栈:** Tauri v2, React 18, TypeScript, Tailwind CSS, Zustand, reqwest, serde

---

## 阶段 1: 项目初始化

### Task 1: 创建 Tauri + React 项目

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/package.json`
- Create: `/home/kisaragi/code/mvsep-gui-rust/vite.config.ts`
- Create: `/home/kisaragi/code/mvsep-gui-rust/tsconfig.json`
- Create: `/home/kisaragi/code/mvsep-gui-rust/index.html`
- Create: `/home/kisaragi/code/mvsep-gui-rust/tailwind.config.js`
- Create: `/home/kisaragi/code/mvsep-gui-rust/postcss.config.js`

**Step 1: 创建 package.json**

```json
{
  "name": "mvsep-gui",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "tauri": "tauri"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tauri-apps/api": "^2.0.0",
    "zustand": "^4.5.0",
    "i18next": "^23.7.0",
    "react-i18next": "^14.0.0"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^2.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

**Step 2: 初始化 Tauri 项目**

```bash
cd /home/kisaragi/code/mvsep-gui-rust
npm install
npx tauri init --app-name "MVSEP Studio" --window-title "MVSEP Studio" --dev-url "http://localhost:5173" --before-dev-command "npm run dev" --before-build-command "npm run build" --ci
```

**Step 3: 验证项目可以运行**

```bash
npm run tauri dev
```

**预期:** 应用窗口打开，显示默认 Tauri 页面

---

## 阶段 2: Rust 后端开发

### Task 2: 配置 Cargo.toml 依赖

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/Cargo.toml`

**Step 1: 创建 Cargo.toml**

```toml
[package]
name = "mvsep-gui"
version = "1.0.0"
edition = "2021"

[lib]
name = "mvsep_gui_lib"
crate-type = ["staticlib", "cdylib", "rlib"]

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
tauri = { version = "2", features = ["devtools"] }
tauri-plugin-shell = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
reqwest = { version = "0.12", features = ["json", "multipart", "stream"] }
tokio = { version = "1", features = ["full"] }
dirs = "5"
chrono = "0.4"
log = "0.4"
env_logger = "0.11"

[profile.release]
strip = true
lto = true
codegen-units = 1
```

**Step 2: 更新 tauri.conf.json**

```json
{
  "productName": "MVSEP Studio",
  "version": "1.0.0",
  "identifier": "com.mvsep.studio",
  "build": {
    "beforeDevCommand": "npm run dev",
    "devUrl": "http://localhost:5173",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [
      {
        "title": "MVSEP Studio",
        "width": 900,
        "height": 700,
        "resizable": true,
        "fullscreen": false,
        "minWidth": 800,
        "minHeight": 600
      }
    ],
    "security": {
      "csp": null
    }
  }
}
```

---

### Task 3: 实现 Rust 类型定义

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/types.rs`

**Step 1: 创建 types.rs**

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub api_token: Option<String>,
    pub language: String,
    pub theme: String,
    pub mirror: String,
    pub timeout: u64,
    pub proxy: Option<ProxyConfig>,
    pub output_dir: String,
    pub output_format: i32,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            api_token: None,
            language: "zh".to_string(),
            theme: "dark".to_string(),
            mirror: "main".to_string(),
            timeout: 60,
            proxy: None,
            output_dir: dirs::download_dir()
                .unwrap_or_else(|| dirs::home_dir().unwrap_or_default())
                .to_string_lossy()
                .to_string(),
            output_format: 1,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProxyConfig {
    pub enabled: bool,
    pub host: String,
    pub port: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskResult {
    pub hash: String,
    pub success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StatusResult {
    pub status: String,
    pub queue_count: Option<i32>,
    pub files: Vec<FileInfo>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileInfo {
    pub url: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Algorithm {
    pub render_id: i32,
    pub name: String,
    pub algorithm_fields: Vec<AlgorithmField>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AlgorithmField {
    pub name: String,
    pub options: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryEntry {
    pub hash: String,
    pub original_filename: String,
    pub status: String,
    pub created_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProgressEvent {
    pub event_type: String,
    pub message: String,
    pub progress: Option<f64>,
}
```

---

### Task 4: 实现配置管理模块

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/config.rs`

**Step 1: 创建 config.rs**

```rust
use std::fs;
use std::path::PathBuf;
use crate::types::AppConfig;

const CONFIG_DIR: &str = ".mvsep-gui";
const CONFIG_FILE: &str = "config.json";

fn get_config_path() -> PathBuf {
    dirs::home_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join(CONFIG_DIR)
        .join(CONFIG_FILE)
}

pub fn load_config() -> AppConfig {
    let path = get_config_path();
    if path.exists() {
        match fs::read_to_string(&path) {
            Ok(content) => {
                serde_json::from_str(&content).unwrap_or_default()
            }
            Err(_) => AppConfig::default(),
        }
    } else {
        AppConfig::default()
    }
}

pub fn save_config(config: &AppConfig) -> Result<(), String> {
    let path = get_config_path();
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }
    let content = serde_json::to_string_pretty(config).map_err(|e| e.to_string())?;
    fs::write(path, content).map_err(|e| e.to_string())?;
    Ok(())
}
```

**Step 2: 测试配置保存和加载**

```bash
cd /home/kisaragi/code/mvsep-gui-rust/src-tauri
cargo build
```

---

### Task 5: 实现 API 调用模块

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/api.rs`

**Step 1: 创建 api.rs (核心 API 调用)**

```rust
use reqwest::{Client, multipart};
use std::path::Path;
use std::fs::File;
use std::io::Read;
use crate::types::*;

const BASE_URL_MAIN: &str = "https://mvsep.com";
const BASE_URL_MIRROR: &str = "https://mirror.mvsep.com";

pub struct MvsepApi {
    client: Client,
    api_token: String,
    base_url: String,
}

impl MvsepApi {
    pub fn new(api_token: String, mirror: &str, timeout: u64) -> Self {
        let base_url = match mirror {
            "mirror" => BASE_URL_MIRROR.to_string(),
            _ => BASE_URL_MAIN.to_string(),
        };

        let client = Client::builder()
            .timeout(std::time::Duration::from_secs(timeout))
            .build()
            .unwrap_or_default();

        Self { client, api_token, base_url }
    }

    pub async fn create_task(
        &self,
        audio_file: &str,
        sep_type: i32,
        output_format: i32,
        add_opt1: Option<&str>,
        add_opt2: Option<&str>,
        add_opt3: Option<&str>,
    ) -> Result<TaskResult, String> {
        let url = format!("{}/api/separation/create", self.base_url);

        let mut form = reqwest::multipart::Form::new()
            .text("api_token", self.api_token.clone())
            .text("sep_type", sep_type.to_string())
            .text("output_format", output_format.to_string())
            .text("is_demo", "0");

        if let Some(opt) = add_opt1 {
            form = form.text("add_opt1", opt.to_string());
        }
        if let Some(opt) = add_opt2 {
            form = form.text("add_opt2", opt.to_string());
        }
        if let Some(opt) = add_opt3 {
            form = form.text("add_opt3", opt.to_string());
        }

        // 添加文件
        let path = Path::new(audio_file);
        let filename = path.file_name()
            .unwrap_or_default()
            .to_string_lossy();
        let mut file = File::open(path).map_err(|e| e.to_string())?;
        let mut buffer = Vec::new();
        file.read_to_end(&mut buffer).map_err(|e| e.to_string())?;

        let part = multipart::Part::bytes(buffer)
            .file_name(filename.to_string())
            .mime_str("audio/wav")
            .map_err(|e| e.to_string())?;
        form = form.file("audiofile", part);

        let response = self.client.post(&url)
            .multipart(form)
            .send()
            .await
            .map_err(|e| e.to_string())?;

        let result: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;

        if result.get("success").and_then(|v| v.as_bool()).unwrap_or(false) {
            let hash = result["data"]["hash"]
                .as_str()
                .unwrap_or("")
                .to_string();
            Ok(TaskResult { hash, success: true })
        } else {
            Err(result["data"]["message"]
                .as_str()
                .unwrap_or("Unknown error")
                .to_string())
        }
    }

    pub async fn get_status(&self, hash: &str) -> Result<StatusResult, String> {
        let url = format!("{}/api/separation/get", self.base_url);

        let response = self.client.get(&url)
            .query(&[("hash", hash)])
            .send()
            .await
            .map_err(|e| e.to_string())?;

        let result: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;

        let status = result["status"].as_str().unwrap_or("").to_string();
        let queue_count = result["data"]["queue_count"].as_i64().map(|v| v as i32);
        let files: Vec<FileInfo> = result["data"]["files"]
            .as_array()
            .map(|arr| {
                arr.iter()
                    .map(|f| FileInfo {
                        url: f["url"].as_str().unwrap_or("").to_string(),
                    })
                    .collect()
            })
            .unwrap_or_default();

        Ok(StatusResult { status, queue_count, files })
    }

    pub async fn get_algorithms(&self) -> Result<Vec<Algorithm>, String> {
        let url = format!("{}/api/app/algorithms", self.base_url);

        let response = self.client.get(&url)
            .query(&[("scopes", "single_upload")])
            .send()
            .await
            .map_err(|e| e.to_string())?;

        let algorithms: Vec<Algorithm> = response.json().await.map_err(|e| e.to_string())?;
        Ok(algorithms)
    }

    pub async fn test_connection(&self) -> Result<bool, String> {
        let url = format!("{}/api/app/algorithms", self.base_url);

        match self.client.get(&url).send().await {
            Ok(response) => Ok(response.status().is_success()),
            Err(_) => Ok(false),
        }
    }
}
```

---

### Task 6: 实现历史记录和日志模块

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/history.rs`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/logging.rs`

**Step 1: 创建 history.rs**

```rust
use std::fs;
use std::path::PathBuf;
use crate::types::HistoryEntry;

const HISTORY_FILE: &str = "history.json";

fn get_history_path() -> PathBuf {
    dirs::home_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join(".mvsep-gui")
        .join(HISTORY_FILE)
}

pub fn load_history() -> Vec<HistoryEntry> {
    let path = get_history_path();
    if path.exists() {
        match fs::read_to_string(&path) {
            Ok(content) => serde_json::from_str(&content).unwrap_or_default(),
            Err(_) => vec![],
        }
    } else {
        vec![]
    }
}

pub fn save_history_entry(entry: HistoryEntry) -> Result<(), String> {
    let mut history = load_history();
    history.insert(0, entry);
    // 只保留最近 100 条
    history.truncate(100);

    let path = get_history_path();
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }

    let content = serde_json::to_string_pretty(&history).map_err(|e| e.to_string())?;
    fs::write(path, content).map_err(|e| e.to_string())?;
    Ok(())
}

pub fn update_history_status(hash: &str, status: &str) -> Result<(), String> {
    let mut history = load_history();
    for entry in &mut history {
        if entry.hash == hash {
            entry.status = status.to_string();
            break;
        }
    }

    let path = get_history_path();
    let content = serde_json::to_string_pretty(&history).map_err(|e| e.to_string())?;
    fs::write(path, content).map_err(|e| e.to_string())?;
    Ok(())
}
```

**Step 2: 创建 logging.rs**

```rust
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::PathBuf;
use chrono::Local;

const LOG_FILE: &str = "app.log";

fn get_log_path() -> PathBuf {
    dirs::home_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join(".mvsep-gui")
        .join(LOG_FILE)
}

pub fn log_to_file(level: &str, message: &str) {
    let path = get_log_path();
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }

    let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S");
    let log_line = format!("[{}] {}: {}\n", timestamp, level, message);

    if let Ok(mut file) = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&path)
    {
        let _ = file.write_all(log_line.as_bytes());
    }
}

pub fn debug_log(message: &str) {
    log_to_file("DEBUG", message);
}

pub fn info_log(message: &str) {
    log_to_file("INFO", message);
}

pub fn error_log(message: &str) {
    log_to_file("ERROR", message);
}

pub fn read_log() -> String {
    let path = get_log_path();
    if path.exists() {
        fs::read_to_string(path).unwrap_or_default()
    } else {
        String::new()
    }
}
```

---

### Task 7: 实现 Tauri Commands

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/commands.rs`

**Step 1: 创建 commands.rs**

```rust
use tauri::{command, AppHandle, Window, Emitter};
use crate::api::MvsepApi;
use crate::config;
use crate::history;
use crate::logging;
use crate::types::*;

#[command]
pub fn save_config(config: AppConfig) -> Result<(), String> {
    config::save_config(&config)
}

#[command]
pub fn load_config() -> AppConfig {
    config::load_config()
}

#[command]
pub async fn get_algorithms(config: AppConfig) -> Result<Vec<Algorithm>, String> {
    let api = MvsepApi::new(
        config.api_token.unwrap_or_default(),
        &config.mirror,
        config.timeout,
    );
    api.get_algorithms().await
}

#[command]
pub async fn test_connection(config: AppConfig) -> Result<bool, String> {
    let api = MvsepApi::new(
        config.api_token.unwrap_or_default(),
        &config.mirror,
        config.timeout,
    );
    api.test_connection().await
}

#[command]
pub async fn create_task(
    file_path: String,
    sep_type: i32,
    output_format: i32,
    add_opt1: Option<String>,
    add_opt2: Option<String>,
    add_opt3: Option<String>,
    app: AppHandle,
) -> Result<String, String> {
    let config = config::load_config();
    let api_token = config.api_token.clone().unwrap_or_default();

    logging::info_log(&format!("Creating task for file: {}", file_path));

    let api = MvsepApi::new(api_token, &config.mirror, config.timeout);

    let result = api.create_task(
        &file_path,
        sep_type,
        output_format,
        add_opt1.as_deref(),
        add_opt2.as_deref(),
        add_opt3.as_deref(),
    ).await?;

    // 保存到历史记录
    let filename = std::path::Path::new(&file_path)
        .file_name()
        .map(|s| s.to_string_lossy().to_string())
        .unwrap_or_default();

    history::save_history_entry(HistoryEntry {
        hash: result.hash.clone(),
        original_filename: filename,
        status: "waiting".to_string(),
        created_at: chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
    }).ok();

    Ok(result.hash)
}

#[command]
pub async fn wait_for_completion(
    hash: String,
    window: Window,
) -> Result<String, String> {
    let config = config::load_config();
    let api = MvsepApi::new(
        config.api_token.unwrap_or_default(),
        &config.mirror,
        config.timeout,
    );

    loop {
        let status_result = api.get_status(&hash).await?;
        let status = &status_result.status;

        // 发送状态更新到前端
        let _ = window.emit("status-update", status);

        if status == "done" {
            history::update_history_status(&hash, "done").ok();
            return Ok("done".to_string());
        } else if status == "failed" || status == "not_found" {
            history::update_history_status(&hash, "failed").ok();
            return Ok(status.clone());
        }

        // 等待 5 秒
        tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
    }
}

#[command]
pub async fn download_results(
    hash: String,
    output_dir: String,
    window: Window,
) -> Result<Vec<String>, String> {
    let config = config::load_config();
    let api = MvsepApi::new(
        config.api_token.unwrap_or_default(),
        &config.mirror,
        config.timeout,
    );

    let status_result = api.get_status(&hash).await?;

    if status_result.status != "done" {
        return Err("Task not completed".to_string());
    }

    let mut downloaded = vec![];

    for (i, file) in status_result.files.iter().enumerate() {
        let _ = window.emit("download-progress", (i, status_result.files.len()));

        let url = &file.url;
        let filename = url.split('/').last().unwrap_or("output.mp3");

        let response = reqwest::get(url).await.map_err(|e| e.to_string())?;
        let bytes = response.bytes().await.map_err(|e| e.to_string())?;

        let output_path = std::path::Path::new(&output_dir).join(filename);
        std::fs::write(&output_path, bytes).map_err(|e| e.to_string())?;

        downloaded.push(output_path.to_string_lossy().to_string());
    }

    Ok(downloaded)
}

#[command]
pub fn get_history() -> Vec<HistoryEntry> {
    history::load_history()
}

#[command]
pub fn get_log() -> String {
    logging::read_log()
}
```

---

### Task 8: 更新 main.rs 和 lib.rs

**Files:**
- Modify: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/main.rs`
- Modify: `/home/kisaragi/code/mvsep-gui-rust/src-tauri/src/lib.rs`

**Step 1: 更新 lib.rs**

```rust
pub mod api;
pub mod commands;
pub mod config;
pub mod history;
pub mod logging;
pub mod types;

use commands::*;
use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    env_logger::init();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            save_config,
            load_config,
            get_algorithms,
            test_connection,
            create_task,
            wait_for_completion,
            download_results,
            get_history,
            get_log,
        ])
        .setup(|app| {
            // 确保配置目录存在
            if let Some(home) = dirs::home_dir() {
                let config_dir = home.join(".mvsep-gui");
                std::fs::create_dir_all(config_dir).ok();
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Step 2: 更新 main.rs**

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    mvsep_gui_lib::run()
}
```

---

## 阶段 3: 前端 UI 开发

### Task 9: 创建前端基础结构

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/main.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/App.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/index.css`

**Step 1: 创建 index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #eaeaea;
  --text-secondary: #a0a0a0;
  --accent: #0f3460;
  --accent-hover: #e94560;
  --border: #2a2a4a;
}

[data-theme="light"] {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #333333;
  --text-secondary: #666666;
  --accent: #4a90e2;
  --accent-hover: #357abd;
  --border: #e0e0e0;
}

[data-theme="otaku"] {
  --bg-primary: #1a1a2e;
  --bg-secondary: #2d1b4e;
  --text-primary: #eaeaea;
  --text-secondary: #b0b0b0;
  --accent: #7c3aed;
  --accent-hover: #c084fc;
  --border: #4a2c7a;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

---

### Task 10: 创建 Zustand Store

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/stores/appStore.ts`

**Step 1: 创建 appStore.ts**

```typescript
import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';

interface AppConfig {
  api_token: string | null;
  language: string;
  theme: string;
  mirror: string;
  timeout: number;
  proxy: { enabled: boolean; host: string; port: number } | null;
  output_dir: string;
  output_format: number;
}

interface Algorithm {
  render_id: number;
  name: string;
  algorithm_fields: { name: string; options: string }[];
}

interface HistoryEntry {
  hash: string;
  original_filename: string;
  status: string;
  created_at: string;
}

interface AppState {
  config: AppConfig;
  algorithms: Algorithm[];
  selectedAlgorithm: number;
  selectedFormat: number;
  selectedFile: string | null;
  history: HistoryEntry[];
  logs: string;
  isProcessing: boolean;
  progress: string;
  status: 'idle' | 'processing' | 'success' | 'error';

  // Actions
  loadConfig: () => Promise<void>;
  saveConfig: (config: AppConfig) => Promise<void>;
  loadAlgorithms: () => Promise<void>;
  loadHistory: () => Promise<void>;
  setSelectedFile: (file: string | null) => void;
  startSeparation: () => Promise<void>;
  testConnection: () => Promise<boolean>;
}
```

---

### Task 11: 创建 UI 组件

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/DropZone.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/AlgorithmSelect.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/FormatSelect.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/ProgressPanel.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/SettingsDialog.tsx`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/components/HistoryDialog.tsx`

**每个组件按照以下结构实现:**
1. 组件文件创建
2. 基本样式和功能实现
3. 与 Store 集成

---

### Task 12: 实现 i18n 国际化

**Files:**
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/i18n/index.ts`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/i18n/locales/zh.json`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/i18n/locales/en.json`
- Create: `/home/kisaragi/code/mvsep-gui-rust/src/i18n/locales/ja.json`

**Step 1: 创建 i18n 配置**

```typescript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import zh from './locales/zh.json';
import en from './locales/en.json';
import ja from './locales/ja.json';

i18n.use(initReactI18next).init({
  resources: {
    zh: { translation: zh },
    en: { translation: en },
    ja: { translation: ja },
  },
  lng: 'zh',
  fallbackLng: 'zh',
});

export default i18n;
```

---

### Task 13: 实现主界面布局

**Files:**
- Modify: `/home/kisaragi/code/mvsep-gui-rust/src/App.tsx`

**Step 1: 组装所有组件到主界面**

```tsx
import { useState, useEffect } from 'react';
import { useAppStore } from './stores/appStore';
import DropZone from './components/DropZone';
import AlgorithmSelect from './components/AlgorithmSelect';
import FormatSelect from './components/FormatSelect';
import ProgressPanel from './components/ProgressPanel';
import SettingsDialog from './components/SettingsDialog';
import HistoryDialog from './components/HistoryDialog';

function App() {
  const {
    config, loadConfig, loadAlgorithms, isProcessing, status
  } = useAppStore();
  const [showSettings, setShowSettings] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    loadConfig();
    loadAlgorithms();
  }, []);

  return (
    <div data-theme={config.theme} className="min-h-screen p-6">
      {/* Header */}
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">MVSEP Studio</h1>
        <div className="flex gap-2">
          <button onClick={() => setShowHistory(true)}>History</button>
          <button onClick={() => setShowSettings(true)}>Settings</button>
        </div>
      </header>

      {/* Main Content */}
      <main className="space-y-4">
        <DropZone />
        <AlgorithmSelect />
        <FormatSelect />
        <ProgressPanel />
      </main>

      {/* Dialogs */}
      {showSettings && <SettingsDialog onClose={() => setShowSettings(false)} />}
      {showHistory && <HistoryDialog onClose={() => setShowHistory(false)} />}
    </div>
  );
}

export default App;
```

---

## 阶段 4: 测试与构建

### Task 14: 本地开发测试

**Step 1: 启动开发服务器**

```bash
cd /home/kisaragi/code/mvsep-gui-rust
npm run tauri dev
```

**验证项:**
- [ ] 应用窗口打开
- [ ] 可以输入和保存 API Token
- [ ] 可以拖放音频文件
- [ ] 可以搜索和选择算法
- [ ] 可以开始分离任务
- [ ] 进度显示正常

---

### Task 15: 构建发布版本

**Step 1: 构建 Windows/Mac/Linux 应用**

```bash
cd /home/kisaragi/code/mvsep-gui-rust
npm run tauri build
```

**Step 2: 验证可执行文件**

```bash
ls -la src-tauri/target/release/bundle/
```

---

## 任务依赖关系

```
Phase 1: 项目初始化
├── Task 1: 创建 Tauri + React 项目
│
Phase 2: Rust 后端
├── Task 2: 配置 Cargo.toml
├── Task 3: 实现类型定义
├── Task 4: 实现配置管理
├── Task 5: 实现 API 调用
├── Task 6: 实现历史记录和日志
├── Task 7: 实现 Tauri Commands
└── Task 8: 更新 main.rs 和 lib.rs
    │
    └─► Phase 3: 前端 UI (可并行)
        ├── Task 9: 创建前端基础结构
        ├── Task 10: 创建 Zustand Store
        ├── Task 11: 创建 UI 组件
        ├── Task 12: 实现 i18n
        └── Task 13: 实现主界面
            │
            └─► Phase 4: 测试与构建
                ├── Task 14: 本地开发测试
                └── Task 15: 构建发布版本
```

---

## 验收标准

1. ✅ Rust 后端可以编译
2. ✅ 前端可以正常启动
3. ✅ API Token 可以保存和加载
4. ✅ 可以获取算法列表
5. ✅ 可以创建分离任务
6. ✅ 可以轮询任务状态
7. ✅ 可以下载结果文件
8. ✅ 可以切换主题
9. ✅ 可以切换语言
10. ✅ 可以查看历史记录
11. ✅ 可以查看日志
12. ✅ 可以测试连接
13. ✅ 可以构建发布版本
