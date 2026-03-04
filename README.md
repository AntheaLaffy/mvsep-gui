# MVSEP GUI

[English](./README.md) | [中文](./README_zh.md) | [日本語](./README_ja.md)

A modern and beautiful GUI for MVSEP music separation API.

## Features

- **Modern UI Design** - Beautiful interface with multiple theme support
- **Theme Support** - Pure Black, Bright White, Light Purple themes
- **Multi-language** - English, Chinese (中文), and Japanese (日本語) support
- **Algorithm Search** - Fuzzy search through algorithms
- **Drag & Drop** - Drag audio files directly into the app
- **Real-time Progress** - Live status log, progress bar with speed display
- **Multiple Output Formats** - MP3, WAV, FLAC, M4A
- **Configurable Output Directory** - Choose where to save results
- **Auto Token Saving** - API token saved automatically
- **Settings Cache** - Output directory, format, timeout, algorithm, and options are cached
- **Local History** - Track separation tasks locally even without API
- **Network Settings** - Configurable timeout and proxy support
- **Connection Test** - Test API connectivity in settings

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

```bash
pip install PyQt6 mvsep-cli
```

## Usage

```bash
python main.py
```

### Command Line Options

```bash
python main.py --debug    # Enable debug mode
```

### Environment Variables

```bash
MVSEP_DEBUG=1 python main.py  # Enable debug mode
```

## Getting Started

1. Enter your MVSEP API token and click "Save"
2. Drag & drop an audio file or click to browse
3. Select an algorithm (use search button to filter)
4. Configure options and output format
5. Click "Start Separation"

## Features Detail

### Status Display
- Upload progress with percentage
- Queue position during waiting
- Processing status (processing, distributing, merging)
- Download progress with speed and size

### Download URLs
- After download completes, file URLs are displayed in log
- Copy URLs to download in browser if needed

### History
- Local history is saved automatically
- View past tasks in History dialog
- Log tab shows application runtime logs

### Settings
- **Language**: Switch between English and Chinese
- **Theme**: Choose Pure Black, Bright White, or Light Purple
- **Mirror**: Select MVSEP main server or mirror
- **Timeout**: Set API request timeout (seconds)
- **Proxy**: Auto-detect system proxy or manual configuration
- **Test Connection**: Verify API connectivity

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

**Note**: The first click may redirect to the main site. Follow these steps to get your Token correctly:

1. Visit mvsep.com and log in
2. Click your username in the top-right corner of the main site
3. Click the first "API" option in the dropdown menu
4. Copy the displayed API Key and paste it into the GUI

> Tip: If your browser already has login history, you can directly click the "Get Token" link in the GUI

## License

Apache License 2.0
