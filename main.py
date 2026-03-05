"""
MVSEP GUI - Modern Music Separation Tool
With i18n and Theme Support (Dark/Light/Otaku/System)
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import List

# Debug mode flag - check environment variable
DEBUG = os.environ.get("MVSEP_DEBUG", "").lower() in ("1", "true", "yes")

# Log file path
LOG_DIR = os.path.expanduser("~/.mvsep-gui")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
HISTORY_FILE = os.path.join(LOG_DIR, "history.json")

def debug_log(*args, **kwargs):
    """Debug logging function"""
    message = ' '.join(str(a) for a in args)
    if DEBUG:
        print(f"[DEBUG] {message}", **kwargs)
    # Always write to log file
    log_to_file(f"DEBUG: {message}")


def log_to_file(message: str):
    """Write message to log file"""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Failed to write log: {e}")


def read_log_file() -> str:
    """Read log file content"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    except Exception as e:
        return f"Error reading log: {e}"


def save_local_history(hash: str, filename: str, status: str = "created"):
    """Save task to local history"""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        # Add new entry at the beginning
        entry = {
            "hash": hash,
            "original_filename": filename,
            "status": status,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        history.insert(0, entry)

        # Keep only last 100 entries
        history = history[:100]

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save history: {e}")


def load_local_history() -> list:
    """Load local history"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Failed to load history: {e}")
        return []


def update_local_history(hash: str, status: str):
    """Update status in local history"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

        for entry in history:
            if entry.get("hash") == hash:
                entry["status"] = status

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to update history: {e}")

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QFileDialog, QMessageBox,
    QGroupBox, QTextEdit, QFrame, QScrollArea, QSizePolicy,
    QProgressBar, QDialog, QButtonGroup, QRadioButton, QListWidget,
    QTabWidget
)
from PyQt6.QtCore import (
    QThread, pyqtSignal, Qt, QPropertyAnimation, QEasingCurve,
    QSize, QTimer, QMimeData, QSettings, QUrl
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import (
    QIcon, QColor, QPalette, QFont, QLinearGradient, QPainter,
    QBrush, QPen, QCursor, QFontDatabase
)

from mvsep_cli.api import MVSEP_API
from mvsep_cli.config import Config


# ============================================================
# INTERNATIONALIZATION (i18n)
# ============================================================

class I18n:
    """Internationalization support"""

    # Language code to name
    LANGUAGES = {
        "zh": "中文",
        "en": "English",
        "ja": "日本語"
    }

    # Default language
    DEFAULT = "zh"

    # Translations
    TRANSLATIONS = {
        "zh": {
            # App
            "app_title": "MVSEP 工作室",
            "app_subtitle": "音乐分离工具",

            # Header
            "settings": "设置",

            # API Config
            "api_config": "API 配置",
            "api_token": "API Token",
            "api_token_placeholder": "输入您的 MVSEP API Token",
            "save": "保存",
            "get_token": "获取 API Token",
            "token_help": "获取 Token 帮助",
            "token_help_title": "如何获取 API Token",
            "token_help_content": "1. 访问 mvsep.com 主站并登录账号<br>"
                                 "2. 首次点击获取 Token 链接会被重定向到主站<br>"
                                 "3. 请在主站页面右上角点击您的用户名<br>"
                                 "4. 在下拉菜单中点击第一个 \"API\" 选项<br>"
                                 "5. 复制显示的 API Key 并粘贴到此处<br><br>"
                                 "注意：如果浏览器已有登录记录，可直接点击获取 Token 链接",

            # Drop Zone
            "drop_zone": "拖放音频文件到此处",
            "or_click": "或点击选择文件",
            "supported_formats": "支持格式: MP3, WAV, FLAC, M4A, OGG",
            "file_ready": "文件已就绪",

            # Settings
            "separation_settings": "分离设置",
            "algorithm": "算法",
            "search_algorithm": "搜索算法...",
            "refresh": "刷新",
            "option1": "选项 1",
            "option2": "选项 2",
            "option3": "选项 3",
            "output_format": "输出格式",
            "download_option": "下载选项",
            "download_all": "全部下载",
            "output_dir": "输出目录",
            "browse": "浏览",

            # Formats
            "mp3_320": "MP3 (320 kbps)",
            "wav_16": "WAV (16 bit)",
            "flac_16": "FLAC (16 bit)",
            "m4a_lossy": "M4A (有损)",
            "wav_32": "WAV (32 bit)",
            "flac_24": "FLAC (24 bit)",

            # Actions
            "start_separation": "开始分离",
            "separating": "分离中...",
            "btn_uploading": "上传中...",
            "btn_downloading": "下载中...",

            # Status
            "status_log": "状态日志",
            "idle": "空闲",
            "processing": "处理中",
            "success": "成功",
            "error": "错误",

            # Messages
            "creating_task": "创建分离任务...",
            "task_created": "任务已创建! Hash:",
            "waiting": "等待完成...",
            "downloading": "下载结果...",
            "done": "完成! 文件:",
            "failed": "失败:",
            "completed": "分离完成!",
            "saved_to": "文件已保存到:",

            # Errors
            "error_api_token": "请先输入并保存 API Token",
            "error_file": "请选择音频文件",
            "error_algorithms": "加载算法失败:",
            "token_saved": "API Token 已保存!",
            "invalid_token": "请输入有效的 Token",
            "close": "关闭",

            # Settings Dialog
            "language": "语言",
            "mirror": "MVSEP 镜像源",
            "mirror_main": "MVSEP 主站",
            "mirror_mirror": "MVSEP 镜像（中国推荐）",

            # Network
            "network_settings": "网络设置",
            "timeout": "超时时间（秒）",
            "proxy": "代理",
            "proxy_auto": "自动（使用系统代理）",
            "proxy_manual": "手动设置",
            "proxy_host": "地址",
            "proxy_port": "端口",
            "test_connection": "测试连接",
            "connection_status": "连接状态",
            "connection_success": "连接成功！",
            "connection_failed": "连接失败",
            "connection_testing": "测试中...",

            "theme": "主题",
            "theme_dark": "纯黑",
            "theme_light": "亮白",
            "theme_otaku": "浅紫",
            "theme_system": "跟随系统",
            "close": "关闭",
            "apply": "应用",
            "restart_required": "部分设置需要重启后生效",

            # Misc
            "loading_algorithms": "加载算法中...",
            "loaded_algorithms": "已加载",
            "algorithms": "个算法",

            # History
            "history": "历史记录",
            "history_title": "历史记录",
            "no_history": "暂无历史记录",
            "load_more": "加载更多",

            # Log
            "log": "日志",
            "log_title": "运行日志",
            "no_log": "暂无日志",
            "copy_log": "复制日志",
            "open_log": "打开日志文件",
            "log_copied": "日志已复制到剪贴板",
        },
        "en": {
            # App
            "app_title": "MVSEP Studio",
            "app_subtitle": "Music Separation Tool",

            # Header
            "settings": "Settings",

            # API Config
            "api_config": "API Configuration",
            "api_token": "API Token",
            "api_token_placeholder": "Enter your MVSEP API token",
            "save": "Save",
            "get_token": "Get API Token",
            "token_help": "Get Token Help",
            "token_help_title": "How to Get API Token",
            "token_help_content": "1. Visit mvsep.com and log in<br>"
                                 "2. First click on 'Get Token' link may redirect to main site<br>"
                                 "3. Click your username in the top-right corner of main site<br>"
                                 "4. Click the first \"API\" option in the dropdown menu<br>"
                                 "5. Copy the displayed API Key and paste it here<br><br>"
                                 "Note: If browser has login history, you can directly click the link",

            # Drop Zone
            "drop_zone": "Drop Audio File Here",
            "or_click": "or click to browse",
            "supported_formats": "Supported: MP3, WAV, FLAC, M4A, OGG",
            "file_ready": "File ready",

            # Settings
            "separation_settings": "Separation Settings",
            "algorithm": "Algorithm",
            "search_algorithm": "Search algorithms...",
            "refresh": "Refresh",
            "option1": "Option 1",
            "option2": "Option 2",
            "option3": "Option 3",
            "output_format": "Output Format",
            "download_option": "Download Option",
            "download_all": "Download All",
            "output_dir": "Output Directory",
            "browse": "Browse",

            # Formats
            "mp3_320": "MP3 (320 kbps)",
            "wav_16": "WAV (16 bit)",
            "flac_16": "FLAC (16 bit)",
            "m4a_lossy": "M4A (lossy)",
            "wav_32": "WAV (32 bit)",
            "flac_24": "FLAC (24 bit)",

            # Actions
            "start_separation": "Start Separation",
            "separating": "Separating...",
            "btn_uploading": "Uploading...",
            "btn_downloading": "Downloading...",

            # Status
            "status_log": "Status Log",
            "idle": "Idle",
            "processing": "Processing",
            "success": "Success",
            "error": "Error",

            # Messages
            "creating_task": "Creating separation task...",
            "task_created": "Task created! Hash:",
            "waiting": "Waiting for completion...",
            "downloading": "Downloading results...",
            "done": "Done! Files:",
            "failed": "Failed:",
            "completed": "Separation completed!",
            "saved_to": "Files saved to:",

            # Errors
            "error_api_token": "Please enter and save API token first",
            "error_file": "Please select an audio file",
            "error_algorithms": "Error loading algorithms:",
            "token_saved": "API token saved!",
            "invalid_token": "Please enter a valid token",
            "close": "Close",

            # Settings Dialog
            "language": "Language",
            "mirror": "MVSEP Mirror",
            "mirror_main": "MVSEP Main",
            "mirror_mirror": "MVSEP Mirror (China Recommended)",

            # Network
            "network_settings": "Network Settings",
            "timeout": "Timeout (seconds)",
            "proxy": "Proxy",
            "proxy_auto": "Auto (Use system proxy)",
            "proxy_manual": "Manual",
            "proxy_host": "Host",
            "proxy_port": "Port",
            "test_connection": "Test Connection",
            "connection_status": "Connection Status",
            "connection_success": "Connection successful!",
            "connection_failed": "Connection failed",
            "connection_testing": "Testing...",

            "theme": "Theme",
            "theme_dark": "Pure Black",
            "theme_light": "Bright White",
            "theme_otaku": "Light Purple",
            "theme_system": "System Theme",
            "close": "Close",
            "apply": "Apply",
            "restart_required": "Some settings require restart",

            # Misc
            "loading_algorithms": "Loading algorithms...",
            "loaded_algorithms": "Loaded",
            "algorithms": "algorithms",

            # History
            "history": "History",
            "history_title": "History",
            "no_history": "No history yet",
            "load_more": "Load More",

            # Log
            "log": "Log",
            "log_title": "Application Log",
            "no_log": "No log yet",
            "copy_log": "Copy Log",
            "open_log": "Open Log File",
            "log_copied": "Log copied to clipboard",
        },
        "ja": {
            # App
            "app_title": "MVSEP スタジオ",
            "app_subtitle": "音楽分離ツール",

            # Header
            "settings": "設定",

            # API Config
            "api_config": "API設定",
            "api_token": "APIトークン",
            "api_token_placeholder": "MVSEP APIトークンを入力",
            "save": "保存",
            "get_token": "APIトークンを取得",
            "token_help": "トークン取得ヘルプ",
            "token_help_title": "APIトークンの取得方法",
            "token_help_content": "1. mvsep.comにアクセスしてログイン<br>"
                                 "2. 初めて「トークン取得」リンクをクリックするとメインサイトにリダイレクトされます<br>"
                                 "3. メインサイトの右上のユーザー名をクリック<br>"
                                 "4. ドロップダウンメニューの最初の「API」をクリック<br>"
                                 "5. 表示されたAPIキーをコピーしてここに貼り付け<br><br>"
                                 "注意：ブラウザにログイン履歴がある場合は、直接リンクをクリックできます",

            # Drop Zone
            "drop_zone": "音声ファイルをここにドロップ",
            "or_click": "またはクリックして選択",
            "supported_formats": "対応形式: MP3, WAV, FLAC, M4A, OGG",
            "file_ready": "ファイル準備完了",

            # Settings
            "separation_settings": "分離設定",
            "algorithm": "アルゴリズム",
            "search_algorithm": "アルゴリズムを検索...",
            "refresh": "更新",
            "option1": "オプション 1",
            "option2": "オプション 2",
            "option3": "オプション 3",
            "output_format": "出力形式",
            "download_option": "ダウンロードオプション",
            "download_all": "すべてダウンロード",
            "output_dir": "出力ディレクトリ",
            "browse": "参照",

            # Formats
            "mp3_320": "MP3 (320 kbps)",
            "wav_16": "WAV (16 bit)",
            "flac_16": "FLAC (16 bit)",
            "m4a_lossy": "M4A (可変)",
            "wav_32": "WAV (32 bit)",
            "flac_24": "FLAC (24 bit)",

            # Actions
            "start_separation": "分離開始",
            "separating": "分離中...",
            "btn_uploading": "アップロード中...",
            "btn_downloading": "ダウンロード中...",

            # Status
            "status_log": "ステータスログ",
            "idle": "待機中",
            "processing": "処理中",
            "success": "成功",
            "error": "エラー",

            # Messages
            "creating_task": "分離タスクを作成中...",
            "task_created": "タスク作成完了! ハッシュ:",
            "waiting": "完了を待機中...",
            "downloading": "結果をダウンロード中...",
            "done": "完了! ファイル:",
            "failed": "失敗:",
            "completed": "分離完了!",
            "saved_to": "ファイルを保存しました:",

            # Errors
            "error_api_token": "まずAPIトークンを入力して保存してください",
            "error_file": "音声ファイルを選択してください",
            "error_algorithms": "アルゴリズムの読み込みエラー:",
            "token_saved": "APIトークンを保存しました!",
            "invalid_token": "有効なトークンを入力してください",
            "close": "閉じる",

            # Settings Dialog
            "language": "言語",
            "mirror": "MVSEPミラー",
            "mirror_main": "MVSEP 本家",
            "mirror_mirror": "MVSEP ミラー（中国推奨）",

            # Network
            "network_settings": "ネットワーク設定",
            "timeout": "タイムアウト（秒）",
            "proxy": "プロキシ",
            "proxy_auto": "自動（システムプロキシを使用）",
            "proxy_manual": "手動設定",
            "proxy_host": "アドレス",
            "proxy_port": "ポート",
            "test_connection": "接続テスト",
            "connection_status": "接続状態",
            "connection_success": "接続成功!",
            "connection_failed": "接続失敗",
            "connection_testing": "テスト中...",

            "theme": "テーマ",
            "theme_dark": "純黒",
            "theme_light": "純白",
            "theme_otaku": "ライトパープル",
            "theme_system": "システムテーマ",
            "close": "閉じる",
            "apply": "適用",
            "restart_required": "一部の設定は再起動後に反映されます",

            # Misc
            "loading_algorithms": "アルゴリズムを読み込み中...",
            "loaded_algorithms": "読み込み完了",
            "algorithms": "個のアルゴリズム",

            # History
            "history": "履歴",
            "history_title": "履歴",
            "no_history": "履歴がありません",
            "load_more": "もっと読み込む",

            # Log
            "log": "ログ",
            "log_title": "アプリケーションログ",
            "no_log": "ログがありません",
            "copy_log": "ログをコピー",
            "open_log": "ログファイルを開く",
            "log_copied": "ログをクリップボードにコピーしました",
        }
    }

    def __init__(self, lang=None):
        self._lang = lang or self.DEFAULT

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        if value in self.TRANSLATIONS:
            self._lang = value

    def t(self, key):
        """Translate a key"""
        return self.TRANSLATIONS.get(self._lang, {}).get(key, key)

    @staticmethod
    def get_available_languages():
        return list(I18n.LANGUAGES.keys())


# ============================================================
# THEME MANAGER
# ============================================================

class ThemeManager:
    """Theme management with multiple theme support"""

    # Theme definitions
    THEMES = {
        "dark": {
            "name": "Pure Black",
            "name_zh": "纯黑",
            "bg_darkest": "#0d1117",
            "bg_dark": "#161b22",
            "bg_medium": "#21262d",
            "bg_light": "#30363d",
            "primary": "#58a6ff",       # 蓝色
            "primary_hover": "#79b8ff",
            "primary_dark": "#388bfd",
            "secondary": "#3fb950",     # 绿色
            "accent": "#58a6ff",
            "accent_hover": "#79b8ff",
            "text_primary": "#c9d1d9",
            "text_secondary": "#8b949e",
            "text_muted": "#6e7681",
            "error": "#f85149",
            "warning": "#d29922",
            "success": "#3fb950",
            "border": "#30363d",
            "border_focus": "#58a6ff",
        },
        "light": {
            "name": "Bright White",
            "name_zh": "亮白",
            "bg_darkest": "#ffffff",
            "bg_dark": "#fafbfc",
            "bg_medium": "#f3f4f6",
            "bg_light": "#e5e7eb",
            "primary": "#6366f1",       # Indigo 柔和蓝
            "primary_hover": "#818cf8",
            "primary_dark": "#4f46e5",
            "secondary": "#10b981",     # 柔和绿
            "accent": "#6366f1",
            "accent_hover": "#818cf8",
            "text_primary": "#374151",
            "text_secondary": "#6b7280",
            "text_muted": "#9ca3af",
            "error": "#ef4444",
            "warning": "#f59e0b",
            "success": "#10b981",
            "border": "#e5e7eb",
            "border_focus": "#6366f1",
        },
        "otaku": {
            "name": "Light Purple",
            "name_zh": "浅紫",
            "bg_darkest": "#1e1b2e",
            "bg_dark": "#252033",
            "bg_medium": "#2d2640",
            "bg_light": "#3a3250",
            "primary": "#ff69b4",      # 粉色
            "primary_hover": "#ff85c1",
            "primary_dark": "#ff4d9e",
            "secondary": "#a78bfa",     # 淡紫
            "accent": "#67e8f9",       # 青色
            "accent_hover": "#8bffff",
            "text_primary": "#fce7f3",  # 淡粉白
            "text_secondary": "#f9a8d4",
            "text_muted": "#c4b5fd",
            "error": "#fb7185",
            "warning": "#fcd34d",
            "success": "#a7f3d0",
            "border": "#4c3f6a",
            "border_focus": "#ff69b4",
        }
    }

    DEFAULT = "dark"

    def __init__(self, theme=None):
        self._theme = theme or self.DEFAULT

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if value in self.THEMES or value == "system":
            self._theme = value

    def get_theme_data(self):
        """Get current theme data"""
        if self._theme == "system":
            # Detect system theme (default to dark for now)
            return self.THEMES["dark"]
        return self.THEMES.get(self._theme, self.THEMES[self.DEFAULT])

    def get_color(self, key):
        """Get a specific color from current theme"""
        theme_data = self.get_theme_data()
        return theme_data.get(key, "#000000")

    @staticmethod
    def get_available_themes():
        return list(ThemeManager.THEMES.keys())


# ============================================================
# APP STATE (Singleton)
# ============================================================

class AppState:
    """Global application state"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Load settings
        self.settings = QSettings("MVSEP", "MVSEP-GUI")

        # Initialize i18n
        lang = self.settings.value("language", I18n.DEFAULT)
        self.i18n = I18n(lang)

        # Initialize theme
        theme = self.settings.value("theme", ThemeManager.DEFAULT)
        self.theme_manager = ThemeManager(theme)

        # Config
        self.config = Config()

    def set_language(self, lang):
        """Set language"""
        if lang in I18n.TRANSLATIONS:
            self.i18n.lang = lang
            self.settings.setValue("language", lang)

    def set_theme(self, theme):
        """Set theme"""
        self.theme_manager.theme = theme
        self.settings.setValue("theme", theme)

    def get_colors(self):
        """Get current theme colors"""
        return self.theme_manager.get_theme_data()


# Global state
app_state = AppState()


# ============================================================
# DESIGN SYSTEM
# ============================================================

def get_colors():
    """Get current theme colors"""
    return app_state.get_colors()


def t(key):
    """Translate a key"""
    return app_state.i18n.t(key)


class Colors:
    """Dynamic color palette based on current theme"""

    def __init__(self):
        self._update_colors()

    def _update_colors(self):
        colors = get_colors()
        for key, value in colors.items():
            setattr(self, key.upper(), value)

    def refresh(self):
        """Refresh colors from theme"""
        self._update_colors()


# Global colors instance
_colors = Colors()


def refresh_colors():
    """Refresh global colors"""
    _colors.refresh()


class Typography:
    """Typography system"""
    @staticmethod
    def title_font():
        font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        return font

    @staticmethod
    def heading_font():
        font = QFont("Segoe UI", 13, QFont.Weight.DemiBold)
        return font

    @staticmethod
    def body_font():
        font = QFont("Segoe UI", 12)
        return font

    @staticmethod
    def mono_font():
        font = QFont("Consolas", 11)
        return font


# ============================================================
# CUSTOM WIDGETS
# ============================================================

class ModernButton(QPushButton):
    """Modern gradient button with hover animation"""

    def __init__(self, text, primary=True, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._setup_style()
        self._setup_animation()

    def _setup_style(self):
        colors = get_colors()
        if self.primary:
            self.setStyleSheet(f"""
                ModernButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['primary']}, stop:1 {colors['primary_hover']});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                ModernButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['primary_hover']}, stop:1 {colors['primary']});
                }}
                ModernButton:pressed {{
                    background: {colors['primary_dark']};
                }}
                ModernButton:disabled {{
                    background: {colors['bg_light']};
                    color: {colors['text_muted']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                ModernButton {{
                    background: {colors['bg_medium']};
                    color: {colors['text_primary']};
                    border: 1px solid {colors['border']};
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 13px;
                }}
                ModernButton:hover {{
                    background: {colors['bg_light']};
                    border-color: {colors['primary']};
                }}
                ModernButton:pressed {{
                    background: {colors['bg_dark']};
                }}
            """)

    def _setup_animation(self):
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)

    def enterEvent(self, event):
        self.setGraphicsEffect(self._create_shadow())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def _create_shadow(self):
        colors = get_colors()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        c = QColor(colors['primary'])
        c.setAlpha(80)
        shadow.setColor(c)
        shadow.setOffset(0, 4)
        return shadow


class ModernCard(QFrame):
    """Card widget with subtle shadow and rounded corners"""

    def __init__(self, parent=None):
        super().__init__(parent)
        colors = get_colors()
        self.setStyleSheet(f"""
            ModernCard {{
                background: {colors['bg_dark']};
                border-radius: 12px;
                border: 1px solid {colors['border']};
            }}
        """)
        self.setGraphicsEffect(self._create_shadow(colors))

    def _create_shadow(self, colors):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        return shadow


class DropZone(QFrame):
    """Drag and drop zone for audio files"""

    fileDropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)

        # Icon
        self.icon_label = QLabel("🎵")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.icon_label)

        # Title
        self.title_label = QLabel(t("drop_zone"))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colors = get_colors()
        self.title_label.setStyleSheet(f"""
            color: {colors['text_primary']};
            font-size: 16px;
            font-weight: 600;
        """)
        layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel(t("or_click"))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet(f"""
            color: {colors['text_secondary']};
            font-size: 12px;
            margin-top: 8px;
        """)
        layout.addWidget(self.subtitle_label)

        # Format hint
        self.format_label = QLabel(t("supported_formats"))
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.format_label.setStyleSheet(f"""
            color: {colors['text_muted']};
            font-size: 11px;
            margin-top: 12px;
        """)
        layout.addWidget(self.format_label)

        layout.addStretch()

        self._update_style()

    def _update_style(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            DropZone {{
                background: {colors['bg_medium']};
                border: 2px dashed {colors['border']};
                border-radius: 12px;
            }}
            DropZone:hover {{
                border-color: {colors['primary']};
                background: {colors['bg_light']};
            }}
            DropZone[drag="true"] {{
                border-color: {colors['primary']};
                background: {colors['bg_light']};
            }}
        """)

    def setDragState(self, is_dragging):
        self.setProperty("drag", "true" if is_dragging else "false")
        self._update_style()
        self.style().unpolish(self)
        self.style().polish(self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setDragState(True)

    def dragLeaveEvent(self, event):
        self.setDragState(False)

    def dropEvent(self, event):
        self.setDragState(False)
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.fileDropped.emit(file_path)

    def mousePressEvent(self, event):
        self.select_file()
        super().mousePressEvent(event)

    def select_file(self):
        # Get last audio directory
        last_dir = app_state.settings.value("audio_dir", "")
        file_path, _ = QFileDialog.getOpenFileName(
            self.window(),
            t("or_click"),
            last_dir,
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg);;All Files (*)"
        )
        if file_path:
            # Save the directory
            audio_dir = os.path.dirname(file_path)
            app_state.settings.setValue("audio_dir", audio_dir)
            self.fileDropped.emit(file_path)

    def update_text(self):
        """Update text based on current language"""
        self.title_label.setText(t("drop_zone"))
        self.subtitle_label.setText(t("or_click"))
        self.format_label.setText(t("supported_formats"))


class ModernComboBox(QComboBox):
    """Modern styled combo box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._update_style()

    def _update_style(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QComboBox {{
                background: {colors['bg_medium']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 20px;
                font-size: 14px;
            }}
            QComboBox:hover {{
                border-color: {colors['primary']};
            }}
            QComboBox:focus {{
                border-color: {colors['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {colors['text_secondary']};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background: {colors['bg_dark']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                selection-background-color: {colors['primary']};
                selection-color: white;
                outline: none;
            }}
        """)


class ModernLineEdit(QLineEdit):
    """Modern styled line edit"""

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._update_style()

    def _update_style(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {colors['bg_medium']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 13px;
            }}
            QLineEdit:hover {{
                border-color: {colors['primary']};
            }}
            QLineEdit:focus {{
                border-color: {colors['primary']};
            }}
            QLineEdit::placeholder {{
                color: {colors['text_muted']};
            }}
        """)


class StatusIndicator(QFrame):
    """Audio-style level/status indicator"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status = "idle"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # LED dots
        self.leds = []
        for i in range(5):
            led = QFrame()
            led.setFixedSize(8, 8)
            led.setStyleSheet(f"""
                background: {get_colors()['bg_light']};
                border-radius: 4px;
            """)
            self.leds.append(led)
            layout.addWidget(led)

        self.setFixedHeight(16)

    def setStatus(self, status):
        self._status = status
        colors = get_colors()

        status_colors = {
            "idle": colors['text_muted'],
            "processing": colors['secondary'],
            "success": colors['success'],
            "error": colors['error']
        }

        active_color = status_colors.get(status, colors['text_muted'])

        for i, led in enumerate(self.leds):
            if status == "processing":
                led.setStyleSheet(f"""
                    background: {colors['secondary'] if i <= 2 else colors['bg_light']};
                    border-radius: 4px;
                """)
            else:
                led.setStyleSheet(f"""
                    background: {active_color if i == 0 else colors['bg_light']};
                    border-radius: 4px;
                """)


class ModernProgressBar(QProgressBar):
    """Modern styled progress bar with gradient"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._update_style()

    def _update_style(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QProgressBar {{
                background: {colors['bg_medium']};
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {colors['primary']}, stop:1 {colors['secondary']});
                border-radius: 4px;
            }}
        """)


class LogPanel(QTextEdit):
    """Styled log output panel"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self._update_style()

    def _update_style(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QTextEdit {{
                background: {colors['bg_darkest']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 12px;
                font-family: Consolas, monospace;
                font-size: 11px;
                line-height: 1.6;
            }}
        """)

    def append_log(self, text, level="info"):
        colors = get_colors()
        level_colors = {
            "info": colors['text_secondary'],
            "success": colors['success'],
            "error": colors['error'],
            "warning": colors['warning']
        }
        color = level_colors.get(level, colors['text_secondary'])
        self.append(f'<span style="color: {color};">{text}</span>')


# ============================================================
# SETTINGS DIALOG
# ============================================================

class SettingsDialog(QDialog):
    """Settings dialog for language and theme"""

    themeChanged = pyqtSignal()
    languageChanged = pyqtSignal()
    mirrorChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("settings"))
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['bg_dark']};
                color: {colors['text_primary']};
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QRadioButton {{
                color: {colors['text_primary']};
            }}
            QRadioButton:hover {{
                color: {colors['primary']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title
        title = QLabel(t("settings"))
        title.setFont(Typography.title_font())
        layout.addWidget(title)

        # Language Selection
        lang_group = QGroupBox(t("language"))
        lang_layout = QVBoxLayout()

        self.lang_buttons = QButtonGroup(self)
        for lang_code, lang_name in I18n.LANGUAGES.items():
            radio = QRadioButton(lang_name)
            radio.setCheckable(True)
            if app_state.i18n.lang == lang_code:
                radio.setChecked(True)
            radio.lang_code = lang_code
            self.lang_buttons.addButton(radio)
            lang_layout.addWidget(radio)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Mirror Selection
        mirror_group = QGroupBox(t("mirror"))
        mirror_layout = QVBoxLayout()

        self.mirror_buttons = QButtonGroup(self)
        mirror_options = [
            ("main", t("mirror_main")),
            ("mirror", t("mirror_mirror")),
        ]

        current_mirror = app_state.config.mirror or "main"
        for mirror_code, mirror_name in mirror_options:
            radio = QRadioButton(mirror_name)
            radio.setCheckable(True)
            if current_mirror == mirror_code:
                radio.setChecked(True)
            radio.mirror_code = mirror_code
            self.mirror_buttons.addButton(radio)
            mirror_layout.addWidget(radio)

        mirror_group.setLayout(mirror_layout)
        layout.addWidget(mirror_group)

        # Theme Selection
        theme_group = QGroupBox(t("theme"))
        theme_layout = QVBoxLayout()

        theme_options = [
            ("dark", t("theme_dark")),
            ("light", t("theme_light")),
            ("otaku", t("theme_otaku")),
        ]

        self.theme_buttons = QButtonGroup(self)
        for theme_code, theme_name in theme_options:
            radio = QRadioButton(theme_name)
            radio.setCheckable(True)
            if app_state.theme_manager.theme == theme_code:
                radio.setChecked(True)
            radio.theme_code = theme_code
            self.theme_buttons.addButton(radio)
            theme_layout.addWidget(radio)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Network Settings
        network_group = QGroupBox(t("network_settings"))
        network_layout = QVBoxLayout()
        network_layout.setSpacing(10)

        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel(t("timeout"))
        timeout_label.setFixedWidth(120)
        self.timeout_input = ModernLineEdit()
        self.timeout_input.setText(str(app_state.settings.value("timeout", "60")))
        self.timeout_input.setFixedWidth(80)
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_input)
        network_layout.addLayout(timeout_layout)

        # Proxy mode
        proxy_mode_layout = QHBoxLayout()
        proxy_mode_label = QLabel(t("proxy"))
        proxy_mode_label.setFixedWidth(120)
        self.proxy_auto_radio = QRadioButton(t("proxy_auto"))
        self.proxy_manual_radio = QRadioButton(t("proxy_manual"))
        proxy_mode_layout.addWidget(proxy_mode_label)
        proxy_mode_layout.addWidget(self.proxy_auto_radio)
        proxy_mode_layout.addWidget(self.proxy_manual_radio)
        network_layout.addLayout(proxy_mode_layout)

        # Manual proxy input
        proxy_input_layout = QHBoxLayout()
        proxy_input_layout.setSpacing(5)
        proxy_input_layout.addSpacing(130)

        self.proxy_host_input = ModernLineEdit()
        self.proxy_host_input.setPlaceholderText(t("proxy_host"))
        self.proxy_host_input.setText(app_state.settings.value("proxy_host", ""))
        self.proxy_host_input.setFixedWidth(150)
        self.proxy_port_input = ModernLineEdit()
        self.proxy_port_input.setPlaceholderText(t("proxy_port"))
        self.proxy_port_input.setText(app_state.settings.value("proxy_port", ""))
        self.proxy_port_input.setFixedWidth(80)

        proxy_input_layout.addWidget(self.proxy_host_input)
        proxy_input_layout.addWidget(self.proxy_port_input)
        network_layout.addLayout(proxy_input_layout)

        # Set proxy mode radio
        proxy_mode = app_state.settings.value("proxy_mode", "auto")
        if proxy_mode == "manual":
            self.proxy_manual_radio.setChecked(True)
            self.proxy_host_input.setEnabled(True)
            self.proxy_port_input.setEnabled(True)
        else:
            self.proxy_auto_radio.setChecked(True)
            self.proxy_host_input.setEnabled(False)
            self.proxy_port_input.setEnabled(False)

        # Connect radio to toggle inputs
        self.proxy_auto_radio.toggled.connect(lambda x: self._on_proxy_mode_changed(x, True))
        self.proxy_manual_radio.toggled.connect(lambda x: self._on_proxy_mode_changed(x, False))

        # Test connection
        test_layout = QHBoxLayout()
        test_layout.setSpacing(10)
        test_btn = QPushButton(t("test_connection"))
        test_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background: {colors['accent_hover']};
            }}
        """)
        test_btn.clicked.connect(self._test_connection)
        test_layout.addWidget(test_btn)

        self.connection_status_label = QLabel("")
        self.connection_status_label.setStyleSheet(f"color: {colors['text_secondary']};")
        test_layout.addWidget(self.connection_status_label)
        test_layout.addStretch()
        network_layout.addLayout(test_layout)

        network_group.setLayout(network_layout)
        layout.addWidget(network_group)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = ModernButton(t("close"), primary=False)
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        apply_btn = ModernButton(t("apply"), primary=True)
        apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(apply_btn)

        layout.addLayout(btn_layout)

    def _on_proxy_mode_changed(self, auto_selected, is_auto):
        """Handle proxy mode radio change"""
        self.proxy_host_input.setEnabled(not is_auto)
        self.proxy_port_input.setEnabled(not is_auto)

    def _test_connection(self):
        """Test MVSEP API connection"""
        self.connection_status_label.setText(t("connection_testing"))
        self.connection_status_label.setStyleSheet(f"color: {get_colors()['warning']};")
        QApplication.processEvents()

        try:
            import requests
            # Get settings
            proxy_mode = "manual" if self.proxy_manual_radio.isChecked() else "auto"
            proxy = None
            if proxy_mode == "manual":
                host = self.proxy_host_input.text().strip()
                port = self.proxy_port_input.text().strip()
                if host and port:
                    proxy = {"http": f"http://{host}:{port}", "https": f"http://{host}:{port}"}

            timeout = int(self.timeout_input.text().strip() or "60")

            # Get base URL from config
            from mvsep_cli.config import Config
            config = Config()
            base_url = config.base_url
            test_url = f"{base_url}/api/app/algorithms"

            response = requests.get(test_url, proxies=proxy, timeout=timeout)
            if response.status_code == 200:
                self.connection_status_label.setText(t("connection_success"))
                self.connection_status_label.setStyleSheet(f"color: {get_colors()['success']};")
            else:
                self.connection_status_label.setText(f"{t('connection_failed')}: {response.status_code}")
                self.connection_status_label.setStyleSheet(f"color: {get_colors()['error']};")
        except Exception as e:
            self.connection_status_label.setText(f"{t('connection_failed')}: {str(e)}")
            self.connection_status_label.setStyleSheet(f"color: {get_colors()['error']};")

    def apply_settings(self):
        debug_log("apply_settings: starting...")

        # Get selected language
        for btn in self.lang_buttons.buttons():
            if btn.isChecked():
                new_lang = btn.lang_code
                debug_log(f"apply_settings: selected language: {new_lang}")
                if new_lang != app_state.i18n.lang:
                    app_state.set_language(new_lang)
                    debug_log("apply_settings: emitting languageChanged")
                    self.languageChanged.emit()
                break

        # Get selected theme
        for btn in self.theme_buttons.buttons():
            if btn.isChecked():
                new_theme = btn.theme_code
                debug_log(f"apply_settings: selected theme: {new_theme}")
                if new_theme != app_state.theme_manager.theme:
                    app_state.set_theme(new_theme)
                    debug_log("apply_settings: emitting themeChanged")
                    self.themeChanged.emit()
                break

        # Get selected mirror
        for btn in self.mirror_buttons.buttons():
            if btn.isChecked():
                new_mirror = btn.mirror_code
                debug_log(f"apply_settings: selected mirror: {new_mirror}")
                if new_mirror != app_state.config.mirror:
                    app_state.config.mirror = new_mirror
                    debug_log("apply_settings: mirror changed, need to recreate API")
                    self.mirrorChanged.emit()
                break

        # Save network settings
        timeout = self.timeout_input.text().strip() or "60"
        app_state.settings.setValue("timeout", timeout)

        proxy_mode = "manual" if self.proxy_manual_radio.isChecked() else "auto"
        app_state.settings.setValue("proxy_mode", proxy_mode)
        app_state.settings.setValue("proxy_host", self.proxy_host_input.text().strip())
        app_state.settings.setValue("proxy_port", self.proxy_port_input.text().strip())

        debug_log("apply_settings: closing dialog")
        self.close()


# ============================================================
# HISTORY DIALOG
# ============================================================

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle(t("history_title"))
        self.setMinimumSize(600, 500)
        self.history_data = []
        self.offset = 0
        self.limit = 20
        self.init_ui()
        # Delay loading to avoid blocking UI during separation
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self.load_history)

    def init_ui(self):
        colors = get_colors()
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(t("history_title"))
        title.setFont(Typography.title_font())
        title.setStyleSheet(f"color: {colors['text_primary']}; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                border-radius: 8px;
                background: {colors['bg_dark']};
            }}
            QTabBar::tab {{
                background: {colors['bg_medium']};
                color: {colors['text_primary']};
                padding: 8px 16px;
                border: 1px solid {colors['border']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background: {colors['bg_dark']};
            }}
        """)

        # History tab
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet(f"""
            QListWidget {{
                background: {colors['bg_dark']};
                color: {colors['text_primary']};
                border: none;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {colors['border']};
            }}
            QListWidget::item:selected {{
                background: {colors['bg_light']};
            }}
        """)
        history_layout.addWidget(self.history_list)

        # Load more button
        self.load_more_btn = QPushButton(t("load_more"))
        self.load_more_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {colors['accent_hover']};
            }}
        """)
        self.load_more_btn.clicked.connect(self.load_more)
        history_layout.addWidget(self.load_more_btn)

        self.tabs.addTab(history_widget, t("history"))

        # Log tab
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)

        # Log text
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background: {colors['bg_dark']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }}
        """)
        # Load log content
        log_content = read_log_file()
        if log_content:
            self.log_text.setPlainText(log_content)
        else:
            self.log_text.setPlainText(t("no_log"))
        log_layout.addWidget(self.log_text)

        # Buttons for log
        log_buttons = QHBoxLayout()

        # Copy button
        copy_btn = QPushButton(t("copy_log"))
        copy_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {colors['accent_hover']};
            }}
        """)
        copy_btn.clicked.connect(self.copy_log)
        log_buttons.addWidget(copy_btn)

        # Open file button
        open_btn = QPushButton(t("open_log"))
        open_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {colors['bg_light']};
            }}
        """)
        open_btn.clicked.connect(self.open_log_file)
        log_buttons.addWidget(open_btn)

        log_buttons.addStretch()
        log_layout.addLayout(log_buttons)

        self.tabs.addTab(log_widget, t("log"))

        layout.addWidget(self.tabs)

        # Close button
        close_btn = QPushButton(t("close"))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {colors['bg_light']};
            }}
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def copy_log(self):
        """Copy log content to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.log_text.toPlainText())
        QMessageBox.information(self, t("log"), t("log_copied"))

    def open_log_file(self):
        """Open log file with default application"""
        if os.path.exists(LOG_FILE):
            QDesktopServices.openUrl(QUrl.fromLocalFile(LOG_FILE))
        else:
            QMessageBox.warning(self, t("error"), t("no_log"))

    def load_history(self):
        """Load separation history - first try API, then fallback to local"""
        # First load local history
        local_history = load_local_history()
        for item in local_history:
            file_name = item.get("original_filename", "Unknown")
            status = item.get("status", "unknown")
            date = item.get("created_at", "")
            hash_id = item.get("hash", "")[:12] if item.get("hash") else "?"

            status_text = {
                "done": "✓",
                "failed": "✗",
                "waiting": "⏳",
                "processing": "⏳",
                "error": "✗"
            }.get(status, status)

            display_text = f"{status_text} {file_name} ({hash_id}) - {date}"
            self.history_list.addItem(display_text)

        # Try to load from API if available - use background thread
        if not hasattr(self.parent_window, 'api') or not self.parent_window.api:
            if not local_history:
                self.history_list.addItem(t("no_history"))
            self.load_more_btn.setEnabled(False)
            return

        # Load API history in background thread
        self.load_api_history_background(local_history)

    def load_api_history_background(self, local_history):
        """Load API history in background thread"""
        if hasattr(self, 'history_thread') and self.history_thread.isRunning():
            return

        self.history_thread = HistoryLoadThread(
            self.parent_window.api,
            self.offset,
            self.limit
        )
        self.history_thread.history_loaded.connect(
            lambda history: self._on_api_history_loaded(history, local_history)
        )
        self.history_thread.error_occurred.connect(
            lambda error: self._on_api_history_error(error, local_history)
        )
        self.history_thread.start()

    def _on_api_history_loaded(self, history, local_history):
        """Handle API history loaded"""
        if not history and not local_history:
            self.history_list.addItem(t("no_history"))
        self.load_more_btn.setEnabled(False)

    def _on_api_history_error(self, error, local_history):
        """Handle API history error"""
        if not local_history:
            self.history_list.addItem(f"Error: {str(error)}")
        self.load_more_btn.setEnabled(False)

    def load_more(self):
        self.load_history()


class HistoryLoadThread(QThread):
    """Background thread for loading history from API"""
    history_loaded = pyqtSignal(list)  # history list
    error_occurred = pyqtSignal(str)  # error message

    def __init__(self, api, offset, limit):
        super().__init__()
        self.api = api
        self.offset = offset
        self.limit = limit

    def run(self):
        try:
            result = self.api.get_separation_history(
                start=self.offset,
                limit=self.limit
            )
            history = result.get("history", [])
            self.history_loaded.emit(history)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ============================================================
# BACKGROUND THREAD
# ============================================================

class SeparationThread(QThread):
    progress = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    statusUpdate = pyqtSignal(str)
    statusMessage = pyqtSignal(str, str)  # message, level
    downloadProgress = pyqtSignal(int, int, float)  # downloaded, total, speed

    def __init__(
        self,
        api,
        audio_file,
        sep_type,
        add_opt1,
        add_opt2,
        add_opt3,
        output_format,
        output_dir,
        file_index=-1,
    ):
        super().__init__()
        self.api = api
        self.audio_file = audio_file
        self.sep_type = sep_type
        self.add_opt1 = add_opt1
        self.add_opt2 = add_opt2
        self.add_opt3 = add_opt3
        self.output_format = output_format
        self.output_dir = output_dir
        self.file_index = file_index
        self.hash = None

    def download_progress_callback(self, downloaded: int, total: int):
        """Callback for download progress"""
        self.downloadProgress.emit(downloaded, total)

    def download_with_progress(self, url: str, output_path: str) -> str:
        """Download file with progress reporting"""
        import time
        import requests
        # Get proxy settings from API if available
        proxies = getattr(self.api, 'proxies', None)
        timeout = getattr(self.api, 'timeout', 60)
        response = requests.get(url, stream=True, proxies=proxies, timeout=(timeout, timeout * 20))
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(output_path, "wb") as f:
            downloaded = 0
            start_time = time.time()
            last_time = start_time
            last_downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Calculate speed every 0.5 seconds
                    current_time = time.time()
                    if current_time - last_time >= 0.5:
                        elapsed = current_time - last_time
                        downloaded_since_last = downloaded - last_downloaded
                        speed = downloaded_since_last / elapsed if elapsed > 0 else 0
                        last_time = current_time
                        last_downloaded = downloaded
                    else:
                        # Calculate overall speed
                        total_elapsed = current_time - start_time
                        speed = downloaded / total_elapsed if total_elapsed > 0 else 0

                    self.downloadProgress.emit(downloaded, total_size, speed)

        return output_path

    def download_results_with_progress(self, hash: str, output_dir: str, file_index: int = -1) -> List[str]:
        """Download results with progress

        Args:
            hash: Task hash
            output_dir: Output directory
            file_index: Index of file to download (-1 for all files)
        """
        import requests

        debug_log(f"API get_status called for hash: {hash}")
        result = self.api.get_status(hash)
        debug_log(f"API get_status returned: {result.get('status')}")

        if result.get("status") != "done":
            raise Exception(f"Task not completed yet")

        files = result.get("data", {}).get("files", [])
        if not files:
            raise Exception("No files to download")

        debug_log(f"Files to download: {files}")

        # Filter files if file_index is specified
        if file_index >= 0:
            if file_index >= len(files):
                raise Exception(f"Invalid file index: {file_index}")
            files = [files[file_index]]

        # Get original filename
        original_name = hash
        if hasattr(self.api, '_get_task_meta'):
            original_name = self.api._get_task_meta(hash) or hash

        debug_log(f"Output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []
        file_urls = []
        for file_info in files:
            url = file_info.get("url")
            if not url:
                continue

            file_urls.append(url)

            url_basename = os.path.basename(url)
            url_name = os.path.splitext(url_basename)[0]
            suffix_parts = url_name.rsplit("_", 1)
            suffix = suffix_parts[-1] if len(suffix_parts) > 1 else url_name

            ext = os.path.splitext(url)[1] or ".mp3"
            final_name = f"{original_name}_{suffix}{ext}"
            output_path = os.path.join(output_dir, final_name)

            debug_log(f"Downloading file: {url}")
            debug_log(f"Saving to: {output_path}")
            self.download_with_progress(url, output_path)
            downloaded_files.append(output_path)

        # Emit URLs for display
        self.progress.emit(f"URLs: {', '.join(file_urls)}", "info")
        return downloaded_files

    def run(self):
        try:
            self.statusUpdate.emit("uploading")
            self.progress.emit(t("creating_task"), "info")

            # Log full API call details
            debug_log(f"API create_task called with:")
            debug_log(f"  audio_file: {self.audio_file}")
            debug_log(f"  sep_type: {self.sep_type}")
            debug_log(f"  add_opt1: {self.add_opt1}")
            debug_log(f"  add_opt2: {self.add_opt2}")
            debug_log(f"  add_opt3: {self.add_opt3}")
            debug_log(f"  output_format: {self.output_format}")
            debug_log(f"  output_dir: {self.output_dir}")

            result = self.api.create_task(
                audio_file=self.audio_file,
                sep_type=self.sep_type,
                add_opt1=self.add_opt1,
                add_opt2=self.add_opt2,
                add_opt3=self.add_opt3,
                output_format=self.output_format,
            )

            debug_log(f"API create_task returned: {result}")
            self.hash = result.get("hash")
            # Save to local history
            filename = os.path.basename(self.audio_file)
            save_local_history(self.hash, filename, "waiting")
            self.progress.emit(f"{t('task_created')} Hash: {self.hash}", "info")
            self.statusUpdate.emit("processing")
            self.progress.emit(t("waiting"), "info")

            # Status callback for wait_for_completion
            def on_status(status):
                self.statusMessage.emit(status, "info")
                QApplication.processEvents()

            debug_log(f"API wait_for_completion called with hash: {self.hash}")
            status_result = self.api.wait_for_completion(self.hash, status_callback=on_status)
            debug_log(f"API wait_for_completion returned status: {status_result.get('status')}")

            if status_result.get("status") == "done":
                update_local_history(self.hash, "done")
                self.statusUpdate.emit("downloading")
                self.progress.emit(t("downloading"), "info")
                files = self.download_results_with_progress(self.hash, self.output_dir, self.file_index)
                file_names = ", ".join([os.path.basename(f) for f in files])
                self.progress.emit(f"{t('done')} {file_names}", "success")
                self.statusUpdate.emit("success")
                self.finished.emit(
                    True,
                    f"{t('completed')}\n{t('saved_to')}:\n{self.output_dir}"
                )
            else:
                update_local_history(self.hash, "failed")
                self.statusUpdate.emit("error")
                self.progress.emit(f"{t('failed')} {status_result.get('status')}", "error")
                self.finished.emit(False, f"{t('failed')}: {status_result.get('status')}")

        except Exception as e:
            if self.hash:
                update_local_history(self.hash, "error")
            self.statusUpdate.emit("error")
            self.progress.emit(f"Error: {str(e)}", "error")
            self.finished.emit(False, f"Error: {str(e)}")


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(800, 700)

        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "MVSEP.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.api = None
        self.separation_thread = None
        self.algorithms = []
        self.current_file = None

        self._apply_theme()
        self.init_ui()
        self.load_token()
        self.load_settings()

    def _apply_theme(self):
        colors = get_colors()
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_darkest']};
                color: {colors['text_primary']};
            }}
            QGroupBox {{
                border: none;
                margin-top: 0;
            }}
            QGroupBox::title {{
                color: {colors['text_secondary']};
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 12px;
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
        """)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Content
        content = QScrollArea()
        content.setWidgetResizable(True)
        content.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 20, 30, 20)

        # Drop Zone
        self.drop_zone = DropZone()
        self.drop_zone.fileDropped.connect(self.on_file_selected)
        content_layout.addWidget(self.drop_zone)

        # Configuration Cards
        config_cards = self._create_config_cards()
        content_layout.addWidget(config_cards)

        # Action Button
        self.separate_btn = ModernButton(t("start_separation"), primary=True)
        self.separate_btn.clicked.connect(self.start_separation)
        self.separate_btn.setEnabled(False)
        content_layout.addWidget(self.separate_btn)

        # Status & Log
        status_log = self._create_status_log()
        content_layout.addWidget(status_log)

        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        content.setWidget(content_widget)

        main_layout.addWidget(content)
        self.setLayout(main_layout)

    def _create_header(self):
        colors = get_colors()
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet(f"""
            background: {colors['bg_dark']};
            border-bottom: 1px solid {colors['border']};
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Logo & Title
        title_layout = QVBoxLayout()

        title = QLabel(t("app_title"))
        title.setFont(Typography.title_font())
        title.setStyleSheet(f"color: {colors['text_primary']};")
        title_layout.addWidget(title)

        subtitle = QLabel(t("app_subtitle"))
        subtitle.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 12px;")
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout)

        layout.addStretch()

        # Status indicator
        self.status_indicator = StatusIndicator()
        layout.addWidget(self.status_indicator)

        # History button
        history_btn = QPushButton("📋")
        history_btn.setFixedSize(36, 36)
        history_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {colors['bg_light']};
                color: {colors['text_primary']};
            }}
        """)
        history_btn.clicked.connect(self.show_history)
        history_btn.setToolTip(t("history"))
        layout.addWidget(history_btn)

        # Settings button
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(36, 36)
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {colors['bg_light']};
                color: {colors['text_primary']};
            }}
        """)
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)

        # Save as instance attributes for later access
        self.header = header
        self.title_label = title
        self.subtitle_label = subtitle

        return header

    def _create_config_cards(self):
        cards = QVBoxLayout()
        cards.setSpacing(15)

        # API Configuration Card
        api_card = ModernCard()
        api_layout = QVBoxLayout(api_card)
        api_layout.setSpacing(12)

        self.api_title = QLabel(t("api_config"))
        self.api_title.setFont(Typography.heading_font())
        api_layout.addWidget(self.api_title)

        token_row = QHBoxLayout()
        self.token_input = ModernLineEdit(t("api_token_placeholder"))
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setMinimumWidth(400)
        token_row.addWidget(self.token_input)

        self.save_token_btn = ModernButton(t("save"), primary=False)
        self.save_token_btn.setFixedWidth(80)
        self.save_token_btn.clicked.connect(self.save_token)
        token_row.addWidget(self.save_token_btn)

        api_layout.addLayout(token_row)

        # Token link row with help button
        token_link_row = QHBoxLayout()
        token_link_row.setSpacing(8)
        self.token_hint = QLabel(f"<a href='https://mvsep.com/user-api'>{t('get_token')}</a>")
        self.token_hint.setOpenExternalLinks(True)
        colors = get_colors()
        self.token_hint.setStyleSheet(f"color: {colors['primary']}; font-size: 11px;")
        token_link_row.addWidget(self.token_hint)

        # Help button
        self.token_help_btn = QPushButton("?")
        self.token_help_btn.setFixedSize(20, 20)
        self.token_help_btn.setToolTip(t("token_help"))
        self.token_help_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {colors['primary']};
                color: white;
            }}
        """)
        self.token_help_btn.clicked.connect(self._show_token_help)
        token_link_row.addWidget(self.token_help_btn)

        token_link_row.addStretch()
        api_layout.addLayout(token_link_row)

        cards.addWidget(api_card)

        # Algorithm & Output Settings Card
        settings_card = ModernCard()
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setSpacing(12)

        self.settings_title = QLabel(t("separation_settings"))
        self.settings_title.setFont(Typography.heading_font())
        settings_layout.addWidget(self.settings_title)

        # Algorithm row
        algo_row = QHBoxLayout()
        self.algo_label = QLabel(t("algorithm") + ":")
        algo_row.addWidget(self.algo_label)

        # Searchable combo container
        algo_container = QHBoxLayout()
        algo_container.setSpacing(8)

        self.algo_combo = ModernComboBox()
        self.algo_combo.setMinimumWidth(300)
        self.algo_combo.currentIndexChanged.connect(self.on_algo_changed)
        self.algo_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        algo_container.addWidget(self.algo_combo)

        # Search button
        self.algo_search_btn = QPushButton("🔍")
        self.algo_search_btn.setFixedSize(36, 36)
        colors = get_colors()
        self.algo_search_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors['bg_medium']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {colors['bg_light']};
                border-color: {colors['primary']};
            }}
            QPushButton:checked {{
                background: {colors['primary']};
                color: white;
            }}
        """)
        self.algo_search_btn.setCheckable(True)
        self.algo_search_btn.toggled.connect(self.on_algo_search_toggled)
        algo_container.addWidget(self.algo_search_btn)

        # Search input (hidden by default)
        self.algo_search_input = ModernLineEdit(t("search_algorithm"))
        self.algo_search_input.setFixedWidth(200)
        self.algo_search_input.setVisible(False)
        self.algo_search_input.textChanged.connect(self.on_algo_search_changed)
        algo_container.addWidget(self.algo_search_input)

        algo_row.addLayout(algo_container)

        self.refresh_btn = ModernButton("↻", primary=False)
        self.refresh_btn.setFixedWidth(40)
        self.refresh_btn.setToolTip(t("refresh"))
        self.refresh_btn.clicked.connect(self.load_algorithms)
        algo_row.addWidget(self.refresh_btn)

        algo_row.addStretch()
        settings_layout.addLayout(algo_row)

        # Options row
        options_row = QHBoxLayout()
        options_row.setSpacing(25)

        # Option 1
        opt1_layout = QVBoxLayout()
        opt1_layout.setSpacing(8)
        self.opt1_label = QLabel(t("option1") + ":")
        colors = get_colors()
        self.opt1_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        self.opt1_combo = ModernComboBox()
        self.opt1_combo.setVisible(False)
        opt1_layout.addWidget(self.opt1_label)
        opt1_layout.addWidget(self.opt1_combo)
        options_row.addLayout(opt1_layout)

        # Option 2
        opt2_layout = QVBoxLayout()
        opt2_layout.setSpacing(10)
        self.opt2_label = QLabel(t("option2") + ":")
        self.opt2_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        self.opt2_combo = ModernComboBox()
        self.opt2_combo.setVisible(False)
        opt2_layout.addWidget(self.opt2_label)
        opt2_layout.addWidget(self.opt2_combo)
        options_row.addLayout(opt2_layout)

        # Option 3
        opt3_layout = QVBoxLayout()
        opt3_layout.setSpacing(10)
        self.opt3_label = QLabel(t("option3") + ":")
        self.opt3_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        self.opt3_combo = ModernComboBox()
        self.opt3_combo.setVisible(False)
        opt3_layout.addWidget(self.opt3_label)
        opt3_layout.addWidget(self.opt3_combo)
        options_row.addLayout(opt3_layout)

        # Output format
        format_layout = QVBoxLayout()
        format_layout.setSpacing(10)
        self.format_label = QLabel(t("output_format") + ":")
        self.format_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        self.format_combo = ModernComboBox()
        self.format_combo.addItems([
            t("mp3_320"), t("wav_16"), t("flac_16"),
            t("m4a_lossy"), t("wav_32"), t("flac_24")
        ])
        self.format_combo.setCurrentIndex(1)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)
        options_row.addLayout(format_layout)

        # Download option
        download_opt_layout = QVBoxLayout()
        download_opt_layout.setSpacing(10)
        self.download_opt_label = QLabel(t("download_option") + ":")
        self.download_opt_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        self.download_opt_combo = ModernComboBox()
        self.download_opt_combo.addItems([
            t("download_all"), "Vocals", "Instrumental", "Drums", "Bass", "Other"
        ])
        self.download_opt_combo.setCurrentIndex(0)
        download_opt_layout.addWidget(self.download_opt_label)
        download_opt_layout.addWidget(self.download_opt_combo)
        options_row.addLayout(download_opt_layout)

        # Output directory
        output_layout = QVBoxLayout()
        output_layout.setSpacing(10)
        self.output_label = QLabel(t("output_dir") + ":")
        self.output_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        output_dir_row = QHBoxLayout()
        self.output_dir_input = ModernLineEdit(os.path.expanduser("~"))
        output_dir_row.addWidget(self.output_dir_input)

        browse_btn = ModernButton(t("browse"), primary=False)
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.select_output_dir)
        output_dir_row.addWidget(browse_btn)
        output_layout.addWidget(self.output_label)
        output_layout.addLayout(output_dir_row)
        options_row.addLayout(output_layout)

        # Timeout setting
        timeout_layout = QVBoxLayout()
        timeout_layout.setSpacing(10)
        self.timeout_label = QLabel(t("timeout") + ":")
        self.timeout_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")
        timeout_row = QHBoxLayout()
        self.timeout_input = ModernLineEdit()
        self.timeout_input.setText(app_state.settings.value("timeout", "60"))
        self.timeout_input.setFixedWidth(80)
        timeout_row.addWidget(self.timeout_input)
        timeout_row.addStretch()
        timeout_layout.addWidget(self.timeout_label)
        timeout_layout.addLayout(timeout_row)
        options_row.addLayout(timeout_layout)

        options_row.addStretch()
        settings_layout.addLayout(options_row)

        cards.addWidget(settings_card)

        container = QWidget()
        container.setLayout(cards)
        return container

    def _create_status_log(self):
        container = ModernCard()

        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        # Title row
        title_row = QHBoxLayout()
        self.status_log_title = QLabel(t("status_log"))
        self.status_log_title.setFont(Typography.heading_font())
        title_row.addWidget(self.status_log_title)

        title_row.addStretch()

        # Progress bar
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setVisible(False)
        title_row.addWidget(self.progress_bar)

        layout.addLayout(title_row)

        # Log panel
        self.log_panel = LogPanel()
        self.log_panel.setMinimumHeight(120)
        layout.addWidget(self.log_panel)

        return container

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.themeChanged.connect(self.on_theme_changed)
        dialog.languageChanged.connect(self.on_language_changed)
        dialog.mirrorChanged.connect(self.on_mirror_changed)
        dialog.exec()

    def show_history(self):
        """Show history dialog"""
        dialog = HistoryDialog(self)
        dialog.exec()

    def on_theme_changed(self):
        """Handle theme change - refresh without closing"""
        debug_log("on_theme_changed: refreshing theme...")
        refresh_colors()
        self._refresh_theme()
        debug_log("on_theme_changed: done!")

    def _refresh_theme(self):
        """Refresh all widget styles"""
        colors = get_colors()

        # Update main window style
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors['bg_darkest']};
                color: {colors['text_primary']};
            }}
            QGroupBox {{
                border: none;
                margin-top: 0;
            }}
            QGroupBox::title {{
                color: {colors['text_secondary']};
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 12px;
            }}
            QLabel {{
                color: {colors['text_primary']};
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
        """)

        # Update header
        self.header.setStyleSheet(f"""
            background: {colors['bg_dark']};
            border-bottom: 1px solid {colors['border']};
        """)

        # Update drop zone
        self.drop_zone._update_style()
        self.drop_zone.title_label.setStyleSheet(f"color: {colors['text_primary']}; font-size: 16px; font-weight: 600;")
        self.drop_zone.subtitle_label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 12px; margin-top: 8px;")
        self.drop_zone.format_label.setStyleSheet(f"color: {colors['text_muted']}; font-size: 11px; margin-top: 12px;")

        # Update buttons
        self.separate_btn._setup_style()
        self.save_token_btn._setup_style()
        self.refresh_btn._setup_style()

        # Update input fields
        self.token_input._update_style()
        self.output_dir_input._update_style()

        # Update combos
        self.algo_combo._update_style()
        self.opt1_combo._update_style()
        self.opt2_combo._update_style()
        self.opt3_combo._update_style()
        self.format_combo._update_style()
        self.download_opt_combo._update_style()

        # Update progress bar
        self.progress_bar._update_style()

        # Update log panel
        self.log_panel._update_style()

        # Update labels
        for label in [self.opt1_label, self.opt2_label, self.opt3_label]:
            label.setStyleSheet(f"color: {colors['text_secondary']}; font-size: 11px;")

        debug_log("_refresh_theme: all styles updated")

    def _recreate_window(self):
        """Recreate window with new theme"""
        debug_log("_recreate_window: starting...")
        try:
            debug_log("_recreate_window: closing current window")
            self.close()
            debug_log("_recreate_window: getting QApplication instance")
            app = QApplication.instance()
            debug_log("_recreate_window: creating new MainWindow")
            window = MainWindow()
            debug_log("_recreate_window: showing new window")
            window.show()
            debug_log("_recreate_window: setting active window")
            app.setActiveWindow(window)
            debug_log("_recreate_window: done!")
        except Exception as e:
            debug_log(f"_recreate_window: ERROR: {e}")
            import traceback
            traceback.print_exc()

    def on_language_changed(self):
        """Handle language change - refresh without closing"""
        debug_log("on_language_changed: refreshing language...")
        self._refresh_language()
        debug_log("on_language_changed: done!")

    def on_mirror_changed(self):
        """Handle mirror change - recreate API"""
        debug_log("on_mirror_changed: recreating API...")
        token = app_state.config.api_token
        if token and self.api:
            self.init_api(token)
            self.log_panel.append_log(f"Switched to mirror: {app_state.config.mirror}", "info")
        debug_log("on_mirror_changed: done!")

    def _refresh_language(self):
        """Refresh all text elements"""
        # Update window title
        self.setWindowTitle(t("app_title"))

        # Update header
        self.title_label.setText(t("app_title"))
        self.subtitle_label.setText(t("app_subtitle"))

        # Update drop zone
        self.drop_zone.update_text()

        # Update buttons
        self.separate_btn.setText(t("start_separation"))
        self.save_token_btn.setText(t("save"))
        self.refresh_btn.setToolTip(t("refresh"))
        if hasattr(self, 'token_hint'):
            self.token_hint.setText(f"<a href='https://mvsep.com/user-api'>{t('get_token')}</a>")

        # Update config labels
        if hasattr(self, 'api_title'):
            self.api_title.setText(t("api_config"))
        if hasattr(self, 'settings_title'):
            self.settings_title.setText(t("separation_settings"))
        if hasattr(self, 'status_log_title'):
            self.status_log_title.setText(t("status_log"))
        if hasattr(self, 'algo_label'):
            self.algo_label.setText(t("algorithm") + ":")
        if hasattr(self, 'opt1_label'):
            self.opt1_label.setText(t("option1") + ":")
        if hasattr(self, 'opt2_label'):
            self.opt2_label.setText(t("option2") + ":")
        if hasattr(self, 'opt3_label'):
            self.opt3_label.setText(t("option3") + ":")
        if hasattr(self, 'format_label'):
            self.format_label.setText(t("output_format") + ":")
        if hasattr(self, 'download_opt_label'):
            self.download_opt_label.setText(t("download_option") + ":")
        if hasattr(self, 'download_opt_combo'):
            self._update_download_options()
        if hasattr(self, 'output_label'):
            self.output_label.setText(t("output_dir") + ":")
        if hasattr(self, 'timeout_label'):
            self.timeout_label.setText(t("timeout") + ":")

        debug_log("_refresh_language: done")

    def on_file_selected(self, file_path):
        """Handle file selection"""
        self.current_file = file_path
        file_name = os.path.basename(file_path)

        colors = get_colors()
        # Update drop zone appearance
        self.drop_zone.title_label.setText(file_name)
        self.drop_zone.title_label.setStyleSheet(f"""
            color: {colors['success']};
            font-size: 16px;
            font-weight: 600;
        """)
        self.drop_zone.subtitle_label.setText(t("file_ready"))
        self.drop_zone.icon_label.setText("✓")

        self.separate_btn.setEnabled(bool(self.api and self.current_file))
        self.log_panel.append_log(f"Selected: {file_name}", "info")

    def load_token(self):
        token = app_state.config.api_token
        if token:
            self.token_input.setText(token)
            self.init_api(token)

    def save_token(self):
        token = self.token_input.text().strip()
        if token:
            app_state.config.api_token = token
            self.init_api(token)
            QMessageBox.information(self, t("save"), t("token_saved"))
        else:
            QMessageBox.warning(self, t("error"), t("invalid_token"))

    def _show_token_help(self):
        """Show token help dialog"""
        msg = QDialog(self)
        msg.setWindowTitle(t("token_help_title"))
        msg.setMinimumWidth(400)

        layout = QVBoxLayout(msg)

        # Content
        content = QLabel(t("token_help_content"))
        content.setWordWrap(True)
        content.setTextFormat(Qt.TextFormat.RichText)
        content.setStyleSheet("font-size: 12px; padding: 10px;")
        layout.addWidget(content)

        # Close button
        close_btn = ModernButton(t("close"), primary=True)
        close_btn.clicked.connect(msg.accept)
        layout.addWidget(close_btn)

        msg.exec()

    def load_settings(self):
        """Load separation settings from QSettings"""
        settings = app_state.settings

        # Load output directory
        output_dir = settings.value("output_dir", os.path.expanduser("~"))
        self.output_dir_input.setText(output_dir)

        # Load output format
        output_format = int(settings.value("output_format", 1))
        self.format_combo.setCurrentIndex(output_format)

        # Load download option
        download_opt = int(settings.value("download_opt", 0))
        self.download_opt_combo.setCurrentIndex(download_opt)

        # Load timeout
        timeout = settings.value("timeout", "60")
        self.timeout_input.setText(timeout)

        # Load algorithm (will be applied after algorithms are loaded)
        self._saved_algo_index = int(settings.value("algorithm_index", 0))

        # Load algorithm options (will be applied after algorithms are loaded)
        self._saved_opt1_index = int(settings.value("opt1_index", 0))
        self._saved_opt2_index = int(settings.value("opt2_index", 0))
        self._saved_opt3_index = int(settings.value("opt3_index", 0))

        # Connect signals for saving settings
        self.output_dir_input.textChanged.connect(self._save_output_dir)
        self.timeout_input.textChanged.connect(self._save_timeout)
        self.format_combo.currentIndexChanged.connect(self._save_output_format)
        self.download_opt_combo.currentIndexChanged.connect(self._save_download_opt)

    def _save_output_dir(self):
        app_state.settings.setValue("output_dir", self.output_dir_input.text())

    def _save_timeout(self):
        app_state.settings.setValue("timeout", self.timeout_input.text())

    def _save_output_format(self, index):
        app_state.settings.setValue("output_format", index)

    def _save_download_opt(self, index):
        app_state.settings.setValue("download_opt", index)

    def _save_algorithm_index(self, index):
        app_state.settings.setValue("algorithm_index", index)

    def _save_opt1_index(self, index):
        app_state.settings.setValue("opt1_index", index)

    def _save_opt2_index(self, index):
        app_state.settings.setValue("opt2_index", index)

    def _save_opt3_index(self, index):
        app_state.settings.setValue("opt3_index", index)

    def _on_opt_changed(self, index):
        """Handle option change - save and update download options"""
        # Determine which combo sent the signal
        sender = self.sender()
        if sender == self.opt1_combo:
            app_state.settings.setValue("opt1_index", index)
        elif sender == self.opt2_combo:
            app_state.settings.setValue("opt2_index", index)
        elif sender == self.opt3_combo:
            app_state.settings.setValue("opt3_index", index)

        # Update download options based on new model selection
        self._update_download_options()

    def init_api(self, token):
        try:
            # Get network settings
            timeout = int(app_state.settings.value("timeout", "60"))
            proxy_mode = app_state.settings.value("proxy_mode", "auto")
            proxies = None
            if proxy_mode == "manual":
                host = app_state.settings.value("proxy_host", "")
                port = app_state.settings.value("proxy_port", "")
                if host and port:
                    proxies = {"http": f"http://{host}:{port}", "https": f"http://{host}:{port}"}

            self.api = MVSEP_API(
                token,
                base_url=app_state.config.base_url,
                timeout=timeout,
                proxies=proxies
            )
            self.load_algorithms()
            self.separate_btn.setEnabled(bool(self.current_file))
        except Exception as e:
            self.log_panel.append_log(f"API init error: {e}", "error")

    def load_algorithms(self):
        if not self.api:
            QMessageBox.warning(self, t("error"), t("error_api_token"))
            return

        try:
            self.log_panel.append_log(t("loading_algorithms"), "info")
            self.algorithms = self.api.get_algorithms()

            # Clear search input
            self.algo_search_input.clear()
            self.algo_search_btn.setChecked(False)
            self.algo_search_input.setVisible(False)

            self.algo_combo.blockSignals(True)
            self.algo_combo.clear()

            for algo in sorted(self.algorithms, key=lambda x: x.get("render_id", 0)):
                render_id = algo.get("render_id", "")
                name = algo.get("name", "")
                self.algo_combo.addItem(f"{render_id}: {name}", render_id)

            self.algo_combo.blockSignals(False)

            # Apply saved algorithm index and options
            self._applying_saved_opts = True
            if hasattr(self, '_saved_algo_index') and self._saved_algo_index < self.algo_combo.count():
                self.algo_combo.setCurrentIndex(self._saved_algo_index)
            elif self.algo_combo.count() > 0:
                self.on_algo_changed(0)
            self._applying_saved_opts = False

            # Connect signal to save algorithm selection
            self.algo_combo.currentIndexChanged.connect(self._save_algorithm_index)
            # Connect signals to save opt selections and update download options
            self.opt1_combo.currentIndexChanged.connect(self._on_opt_changed)
            self.opt2_combo.currentIndexChanged.connect(self._on_opt_changed)
            self.opt3_combo.currentIndexChanged.connect(self._on_opt_changed)

            self.log_panel.append_log(f"{t('loaded_algorithms')} {len(self.algorithms)} {t('algorithms')}", "success")
        except Exception as e:
            self.log_panel.append_log(f"{t('error_algorithms')} {e}", "error")
            QMessageBox.warning(self, t("error"), f"{t('error_algorithms')} {e}")

    def on_algo_changed(self, index):
        if index < 0 or not self.algorithms:
            return

        render_id = self.algo_combo.currentData()

        algo = None
        for a in self.algorithms:
            if a.get("render_id") == render_id:
                algo = a
                break

        if not algo:
            return

        fields = algo.get("algorithm_fields", [])

        self.opt1_combo.blockSignals(True)
        self.opt2_combo.blockSignals(True)
        self.opt3_combo.blockSignals(True)

        self.opt1_combo.clear()
        self.opt2_combo.clear()
        self.opt3_combo.clear()

        self.opt1_label.setVisible(False)
        self.opt1_combo.setVisible(False)
        self.opt2_label.setVisible(False)
        self.opt2_combo.setVisible(False)
        self.opt3_label.setVisible(False)
        self.opt3_combo.setVisible(False)

        for i, field in enumerate(fields):
            field_name = field.get("name", f"Option {i + 1}")
            field_text = field.get("text", field_name)
            options_str = field.get("options", "{}")

            try:
                options = json.loads(options_str)
            except:
                options = {}

            if i == 0 and options:
                self.opt1_label.setText(f"{field_text}:")
                self.opt1_label.setVisible(True)
                self.opt1_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt1_combo.addItem(val, key)
            elif i == 1 and options:
                self.opt2_label.setText(f"{field_text}:")
                self.opt2_label.setVisible(True)
                self.opt2_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt2_combo.addItem(val, key)
            elif i == 2 and options:
                self.opt3_label.setText(f"{field_text}:")
                self.opt3_label.setVisible(True)
                self.opt3_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt3_combo.addItem(val, key)

        self.opt1_combo.blockSignals(False)
        self.opt2_combo.blockSignals(False)
        self.opt3_combo.blockSignals(False)

        # Update download options based on algorithm
        self._update_download_options(algo)

        # Apply saved opt indices (only if we just loaded algorithms)
        if hasattr(self, '_applying_saved_opts') and self._applying_saved_opts:
            if self.opt1_combo.count() > 0 and hasattr(self, '_saved_opt1_index'):
                self.opt1_combo.setCurrentIndex(min(self._saved_opt1_index, self.opt1_combo.count() - 1))
            if self.opt2_combo.count() > 0 and hasattr(self, '_saved_opt2_index'):
                self.opt2_combo.setCurrentIndex(min(self._saved_opt2_index, self.opt2_combo.count() - 1))
            if self.opt3_combo.count() > 0 and hasattr(self, '_saved_opt3_index'):
                self.opt3_combo.setCurrentIndex(min(self._saved_opt3_index, self.opt3_combo.count() - 1))
            self._applying_saved_opts = False

    def _parse_track_types_from_model(self, algo):
        """Parse track types from current model selection"""
        import re
        track_types = []

        # Get current model selection from opt combos
        model_text = ""
        if self.opt1_combo.count() > 0 and self.opt1_combo.isVisible():
            model_text = self.opt1_combo.currentText()
        elif self.opt2_combo.count() > 0 and self.opt2_combo.isVisible():
            model_text = self.opt2_combo.currentText()
        elif self.opt3_combo.count() > 0 and self.opt3_combo.isVisible():
            model_text = self.opt3_combo.currentText()

        # Check if model text contains stems info like "(vocals, drums, bass, other)"
        stems_match = re.search(r'\(([^)]+)\)', model_text)
        if stems_match:
            stems = stems_match.group(1).lower()
            # Parse stems
            if "vocals" in stems:
                track_types.append("Vocals")
            if "music" in stems or "instrum" in stems:
                track_types.append("Instrumental")
            if "drums" in stems:
                track_types.append("Drums")
            if "bass" in stems:
                track_types.append("Bass")
            if "piano" in stems:
                track_types.append("Piano")
            if "guitar" in stems:
                track_types.append("Guitar")
            if "other" in stems:
                track_types.append("Other")
            # Check for back vocals / lead vocals
            if "lead" in stems or "back" in stems:
                track_types.append("Back Vocals")

        return track_types

    def _update_download_options(self, algo=None):
        """Update download options based on algorithm name and model selection"""
        # Default track types
        default_tracks = ["Vocals", "Instrumental", "Drums", "Bass", "Other"]

        # Track types to collect
        track_types = []

        # If no algo provided, get current algorithm
        if not algo and self.algorithms:
            render_id = self.algo_combo.currentData()
            for a in self.algorithms:
                if a.get("render_id") == render_id:
                    algo = a
                    break

        if algo:
            # Step 1: Try to parse from MODEL first (higher priority)
            model_tracks = self._parse_track_types_from_model(algo)
            if model_tracks:
                track_types = model_tracks
            else:
                # Step 2: If model has no stems info, try algorithm name
                algo_name = algo.get("name", "").lower()

                # Parse track types from algorithm name
                if "vocals" in algo_name:
                    track_types.append("Vocals")
                if "instrum" in algo_name:
                    track_types.append("Instrumental")
                if "drums" in algo_name:
                    track_types.append("Drums")
                if "bass" in algo_name:
                    track_types.append("Bass")
                if "other" in algo_name:
                    track_types.append("Other")
                # Check for guitar and piano in algorithm name (e.g., "All-In" models)
                if "guitar" in algo_name:
                    track_types.append("Guitar")
                if "piano" in algo_name:
                    track_types.append("Piano")
                if "lead" in algo_name or "back" in algo_name:
                    track_types.append("Back Vocals")

            # Also check model options for stems info (e.g., "2 stems (vocals, music)")
            if not track_types:
                model_tracks = self._parse_track_types_from_model(algo)
                if model_tracks:
                    track_types = model_tracks

        # If no tracks parsed, use default
        if not track_types:
            track_types = default_tracks

        # Save current selection
        current_index = self.download_opt_combo.currentIndex()
        current_data = self.download_opt_combo.currentData()

        # Update combo
        self.download_opt_combo.blockSignals(True)
        self.download_opt_combo.clear()
        self.download_opt_combo.addItem(t("download_all"), -1)
        for i, track in enumerate(track_types):
            self.download_opt_combo.addItem(track, i)

        # Try to restore selection
        if current_data == -1:
            self.download_opt_combo.setCurrentIndex(0)
        elif current_data is not None and current_data >= 0:
            # Find matching track index
            idx = current_data + 1  # +1 because first item is "all"
            if idx < self.download_opt_combo.count():
                self.download_opt_combo.setCurrentIndex(idx)

        self.download_opt_combo.blockSignals(False)

    def on_algo_search_toggled(self, checked):
        """Toggle search input visibility"""
        self.algo_search_input.setVisible(checked)
        if checked:
            self.algo_search_input.setFocus()
            # Show dropdown
            self.algo_combo.showPopup()
        else:
            self.algo_search_input.clear()

    def on_algo_search_changed(self, text):
        """Filter algorithms based on search text"""
        if not self.algorithms:
            return

        search_text = text.lower().strip()

        self.algo_combo.blockSignals(True)
        self.algo_combo.clear()

        for algo in sorted(self.algorithms, key=lambda x: x.get("render_id", 0)):
            render_id = algo.get("render_id", "")
            name = algo.get("name", "")

            # Fuzzy search - check if search text is in render_id or name
            if not search_text or (search_text in str(render_id).lower()) or (search_text in name.lower()):
                self.algo_combo.addItem(f"{render_id}: {name}", render_id)

        self.algo_combo.blockSignals(False)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            t("output_dir"),
            self.output_dir_input.text() or os.path.expanduser("~")
        )
        if dir_path:
            self.output_dir_input.setText(dir_path)

    def start_separation(self):
        if not self.api:
            QMessageBox.warning(self, t("error"), t("error_api_token"))
            return

        if not self.current_file:
            QMessageBox.warning(self, t("error"), t("error_file"))
            return

        output_dir = self.output_dir_input.text() or os.path.expanduser("~")

        sep_type = self.algo_combo.currentData()
        add_opt1 = (
            str(self.opt1_combo.currentData())
            if self.opt1_combo.currentIndex() >= 0 and self.opt1_combo.isVisible()
            else None
        )
        add_opt2 = (
            str(self.opt2_combo.currentData())
            if self.opt2_combo.currentIndex() >= 0 and self.opt2_combo.isVisible()
            else None
        )
        add_opt3 = (
            str(self.opt3_combo.currentData())
            if self.opt3_combo.currentIndex() >= 0 and self.opt3_combo.isVisible()
            else None
        )
        output_format = self.format_combo.currentIndex()

        # Get download option: -1 for all, 0-4 for specific track
        download_opt = self.download_opt_combo.currentIndex()
        file_index = -1 if download_opt == 0 else download_opt - 1

        self.separate_btn.setEnabled(False)
        self.separate_btn.setText(t("separating"))
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.log_panel.append_log("=" * 40, "info")
        self.log_panel.append_log(t("separating"), "info")
        self.log_panel.append_log(f"File: {os.path.basename(self.current_file)}", "info")
        self.log_panel.append_log(f"Algorithm: {sep_type}", "info")

        self.separation_thread = SeparationThread(
            self.api,
            self.current_file,
            sep_type,
            add_opt1,
            add_opt2,
            add_opt3,
            output_format,
            output_dir,
            file_index,
        )
        self.separation_thread.progress.connect(self.on_progress)
        self.separation_thread.finished.connect(self.on_finished)
        self.separation_thread.statusUpdate.connect(self.on_status_update)
        self.separation_thread.statusMessage.connect(self.on_status_message)
        self.separation_thread.downloadProgress.connect(self.on_download_progress)
        self.separation_thread.start()

    def on_progress(self, message, level):
        self.log_panel.append_log(message, level)

    def on_status_message(self, message, level):
        """Handle status messages from wait loop"""
        self.log_panel.append_log(f"Status: {message}", level)
        QApplication.processEvents()

    def on_status_update(self, status):
        self.status_indicator.setStatus(status)
        # Update button text based on status
        if status == "uploading":
            self.separate_btn.setText(t("btn_uploading"))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
        elif status == "processing":
            self.separate_btn.setText(t("separating"))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
        elif status == "downloading":
            self.separate_btn.setText(t("btn_downloading"))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)  # Determinate

    def on_download_progress(self, downloaded: int, total: int, speed: float = 0):
        """Handle download progress"""
        if total > 0:
            percent = int((downloaded / total) * 100)
            self.progress_bar.setValue(percent)

            # Format size
            def format_size(size):
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                elif size < 1024 * 1024 * 1024:
                    return f"{size / (1024 * 1024):.1f} MB"
                else:
                    return f"{size / (1024 * 1024 * 1024):.2f} GB"

            # Format speed
            def format_speed(speed):
                if speed < 1024:
                    return f"{speed:.0f} B/s"
                elif speed < 1024 * 1024:
                    return f"{speed / 1024:.1f} KB/s"
                else:
                    return f"{speed / (1024 * 1024):.2f} MB/s"

            # Update progress bar text
            size_text = f"{format_size(downloaded)} / {format_size(total)}"
            speed_text = format_speed(speed) if speed > 0 else ""
            if speed_text:
                self.progress_bar.setFormat(f"{percent}% ({size_text}) {speed_text}")
            else:
                self.progress_bar.setFormat(f"{percent}% ({size_text})")

            # Force UI update
            QApplication.processEvents()

    def on_finished(self, success, message):
        self.separate_btn.setEnabled(True)
        self.separate_btn.setText(t("start_separation"))
        self.progress_bar.setVisible(False)

        self.log_panel.append_log("=" * 40, "info")

        if success:
            self.log_panel.append_log(t("completed"), "success")
            QMessageBox.information(self, t("success"), message)
        else:
            self.log_panel.append_log(f"ERROR: {message}", "error")
            QMessageBox.critical(self, t("error"), message)


# ============================================================
# MAIN ENTRY
# ============================================================

def main():
    global DEBUG

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MVSEP GUI")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args, _ = parser.parse_known_args()

    # Check env var or command line arg
    DEBUG = args.debug or os.environ.get("MVSEP_DEBUG", "").lower() in ("1", "true", "yes")

    if DEBUG:
        print("[MVSEP GUI] Debug mode enabled")

    # Log startup
    log_to_file(f"=== MVSEP GUI Started (debug={DEBUG}) ===")

    debug_log("Starting MVSEP GUI...")

    # Create Qt Application
    debug_log("Creating QApplication...")
    app = QApplication(sys.argv)
    debug_log("QApplication created")

    # Set application palette based on current theme
    colors = get_colors()
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(colors['bg_darkest']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['text_primary']))
    palette.setColor(QPalette.ColorRole.Base, QColor(colors['bg_medium']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['bg_dark']))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors['bg_dark']))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors['text_primary']))
    palette.setColor(QPalette.ColorRole.Text, QColor(colors['text_primary']))
    palette.setColor(QPalette.ColorRole.Button, QColor(colors['bg_medium']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['text_primary']))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(colors['text_primary']))
    palette.setColor(QPalette.ColorRole.Link, QColor(colors['primary']))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['primary']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['text_primary']))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
