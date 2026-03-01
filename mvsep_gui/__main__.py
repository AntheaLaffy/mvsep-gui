"""
MVSEP GUI - Modern Music Separation Tool
With i18n and Theme Support (Dark/Light/Otaku/System)
"""

import os
import sys
import json
import argparse

# Debug mode flag - check environment variable
DEBUG = os.environ.get("MVSEP_DEBUG", "").lower() in ("1", "true", "yes")

def debug_log(*args, **kwargs):
    """Debug logging function"""
    if DEBUG:
        print(f"[DEBUG] {' '.join(str(a) for a in args)}", **kwargs)

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QFileDialog, QMessageBox,
    QGroupBox, QTextEdit, QFrame, QScrollArea, QSizePolicy,
    QProgressBar, QDialog, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import (
    QThread, pyqtSignal, Qt, QPropertyAnimation, QEasingCurve,
    QSize, QTimer, QMimeData, QSettings
)
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
        "en": "English"
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

            # Settings Dialog
            "language": "语言",
            "mirror": "MVSEP 镜像源",
            "mirror_main": "MVSEP 主站",
            "mirror_mirror": "MVSEP 镜像（中国推荐）",
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

            # Settings Dialog
            "language": "Language",
            "mirror": "MVSEP Mirror",
            "mirror_main": "MVSEP Main",
            "mirror_mirror": "MVSEP Mirror (China Recommended)",
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
        file_path, _ = QFileDialog.getOpenFileName(
            self.window(),
            t("or_click"),
            "",
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg);;All Files (*)"
        )
        if file_path:
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

        debug_log("apply_settings: closing dialog")
        self.close()


# ============================================================
# BACKGROUND THREAD
# ============================================================

class SeparationThread(QThread):
    progress = pyqtSignal(str, str)
    finished = pyqtSignal(bool, str)
    statusUpdate = pyqtSignal(str)

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
        self.hash = None

    def run(self):
        try:
            self.statusUpdate.emit("processing")
            self.progress.emit(t("creating_task"), "info")

            result = self.api.create_task(
                audio_file=self.audio_file,
                sep_type=self.sep_type,
                add_opt1=self.add_opt1,
                add_opt2=self.add_opt2,
                add_opt3=self.add_opt3,
                output_format=self.output_format,
            )

            self.hash = result.get("hash")
            self.progress.emit(f"{t('task_created')} {self.hash[:12]}...", "info")
            self.progress.emit(t("waiting"), "info")

            status_result = self.api.wait_for_completion(self.hash)

            if status_result.get("status") == "done":
                self.progress.emit(t("downloading"), "info")
                files = self.api.download(self.hash, self.output_dir)
                file_names = ", ".join([os.path.basename(f) for f in files])
                self.progress.emit(f"{t('done')} {file_names}", "success")
                self.statusUpdate.emit("success")
                self.finished.emit(
                    True,
                    f"{t('completed')}\n{t('saved_to')}:\n{self.output_dir}"
                )
            else:
                self.statusUpdate.emit("error")
                self.progress.emit(f"{t('failed')} {status_result.get('status')}", "error")
                self.finished.emit(False, f"{t('failed')}: {status_result.get('status')}")

        except Exception as e:
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

        api_title = QLabel(t("api_config"))
        api_title.setFont(Typography.heading_font())
        api_layout.addWidget(api_title)

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

        token_hint = QLabel(f"<a href='https://mvsep.com/user-api'>{t('get_token')}</a>")
        token_hint.setOpenExternalLinks(True)
        colors = get_colors()
        token_hint.setStyleSheet(f"color: {colors['primary']}; font-size: 11px;")
        api_layout.addWidget(token_hint)

        cards.addWidget(api_card)

        # Algorithm & Output Settings Card
        settings_card = ModernCard()
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setSpacing(12)

        settings_title = QLabel(t("separation_settings"))
        settings_title.setFont(Typography.heading_font())
        settings_layout.addWidget(settings_title)

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
        title = QLabel(t("status_log"))
        title.setFont(Typography.heading_font())
        title_row.addWidget(title)

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

        # Update config labels
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
        if hasattr(self, 'output_label'):
            self.output_label.setText(t("output_dir") + ":")

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

    def init_api(self, token):
        try:
            self.api = MVSEP_API(token, base_url=app_state.config.base_url)
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

            if self.algo_combo.count() > 0:
                self.on_algo_changed(0)

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
        )
        self.separation_thread.progress.connect(self.on_progress)
        self.separation_thread.finished.connect(self.on_finished)
        self.separation_thread.statusUpdate.connect(self.on_status_update)
        self.separation_thread.start()

    def on_progress(self, message, level):
        self.log_panel.append_log(message, level)

    def on_status_update(self, status):
        self.status_indicator.setStatus(status)

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
