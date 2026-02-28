# MVSEP GUI

[English](./README.md) | [中文](./README_zh.md)

A simple and easy-to-use GUI for MVSEP music separation API.

## Features

- Clean and intuitive interface
- Support for all MVSEP algorithms and models
- Real-time separation progress display
- Multiple output format options
- Configurable output directory
- Automatic API token saving

## Requirements

- Python 3.8+
- PyQt6
- mvsep-cli

## Installation

### From PyPI (Recommended)

```bash
pip install mvsep-gui
```

### From Source

```bash
# Clone repository
git clone https://github.com/mvsep/mvsep-gui.git
cd mvsep-gui

# Install dependencies
pip install -r requirements.txt

# Install
pip install -e .
```

## Usage

```bash
mvsep-gui
```

Or run directly:

```bash
python -m mvsep_gui
```

## Getting Started

1. Enter your MVSEP API token and click "Save"
2. Click "Select Audio File" to choose an audio file
3. Select an algorithm and configure options
4. Click "Start Separation"

## Getting API Token

Get your free API token from https://mvsep.com/user-api

## License

Apache License 2.0
