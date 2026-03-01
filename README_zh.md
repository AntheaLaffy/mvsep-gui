# MVSEP GUI

[English](./README.md) | [中文](./README_zh.md)

一款现代化美观的 MVSEP 音乐分离 API 图形界面工具。

## 功能特性

- **现代化 UI 设计** - 美观的多主题界面
- **主题支持** - 纯黑、亮白、浅紫三种主题
- **多语言支持** - 中文和英文
- **算法搜索** - 模糊搜索算法列表
- **拖放上传** - 拖放音频文件到应用
- **实时进度** - 实时状态日志和进度指示
- **多种输出格式** - MP3、WAV、FLAC、M4A
- **可配置输出目录** - 选择保存位置
- **自动保存令牌** - API 令牌自动保存

## 主题

| 主题 | 描述 |
|------|------|
| 纯黑 | 深色主题，蓝色强调色 |
| 亮白 | 浅色简洁主题 |
| 浅紫 | 二次元紫色主题 |

## 环境要求

- Python 3.8+
- PyQt6
- mvsep-cli

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install mvsep-gui
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/mvsep/mvsep-gui.git
cd mvsep-gui

# 安装依赖
pip install -r requirements.txt

# 安装
pip install -e .
```

## 使用方法

```bash
mvsep-gui
```

或直接运行：

```bash
python -m mvsep_gui
```

### 命令行选项

```bash
python -m mvsep_gui --debug    # 启用调试模式
```

### 环境变量

```bash
MVSEP_DEBUG=1 python -m mvsep_gui  # 启用调试模式
```

## 快速开始

1. 输入你的 MVSEP API 令牌，点击"保存"
2. 拖放音频文件或点击选择文件
3. 选择算法（使用搜索按钮筛选）
4. 配置选项和输出格式
5. 点击"开始分离"

## 切换语言

1. 点击标题栏的设置按钮 (⚙)
2. 选择语言
3. 点击"应用"

## 切换主题

1. 点击标题栏的设置按钮 (⚙)
2. 选择主题
3. 点击"应用"

## 获取 API 令牌

从 https://mvsep.com/user-api 获取免费 API 令牌

## 许可证

Apache License 2.0
