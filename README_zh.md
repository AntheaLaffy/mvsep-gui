# MVSEP GUI

[English](./README.md) | [中文](./README_zh.md)

一个简洁易用的 MVSEP 音乐分离 API 图形界面工具。

## 功能特性

- 简洁直观的界面
- 支持所有 MVSEP 算法和模型
- 实时显示分离进度
- 多种输出格式可选
- 可配置输出目录
- 自动保存 API 令牌

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

## 快速开始

1. 输入你的 MVSEP API 令牌，点击"保存"
2. 点击"选择音频文件"选择要处理的音频
3. 选择算法并配置选项
4. 点击"开始分离"

## 获取 API 令牌

从 https://mvsep.com/user-api 获取免费 API 令牌

## 许可证

Apache License 2.0
