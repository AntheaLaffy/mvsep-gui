# MVSEP GUI

[English](./README.md) | [中文](./README_zh.md)

A modern and beautiful GUI for MVSEP music separation API.

## Features

- **Modern UI Design** - Beautiful interface with multiple theme support
- **Theme Support** - Pure Black, Bright White, Light Purple themes
- **Multi-language** - English and Chinese (中文) support
- **Algorithm Search** - Fuzzy search through algorithms
- **Drag & Drop** - Drag audio files directly into the app
- **Real-time Progress** - Live status log and progress indicator
- **Multiple Output Formats** - MP3, WAV, FLAC, M4A
- **Configurable Output Directory** - Choose where to save results
- **Auto Token Saving** - API token saved automatically

## Themes

| Theme | Description |
|-------|-------------|
| Pure Black | Dark theme with blue accent |
| Bright White | Light clean theme |
| Light Purple | Otaku-style purple theme |

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
python -m mvsep-gui
```

### Command Line Options

```bash
python -m mvsep_gui --debug    # Enable debug mode
```

### Environment Variables

```bash
MVSEP_DEBUG=1 python -m mvsep_gui  # Enable debug mode
```

## Getting Started

1. Enter your MVSEP API token and click "Save"
2. Drag & drop an audio file or click to browse
3. Select an algorithm (use search button to filter)
4. Configure options and output format
5. Click "Start Separation"

## Changing Language

1. Click the settings button (⚙) in the header
2. Select your preferred language
3. Click "Apply"

## Changing Theme

1. Click the settings button (⚙) in the header
2. Select your preferred theme
3. Click "Apply"

## Getting API Token

Get your free API token from https://mvsep.com/user-api

## License

Apache License 2.0
