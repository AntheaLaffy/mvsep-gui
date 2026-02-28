import os
import sys
import json
import time

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QSpinBox,
    QProgressBar,
    QGroupBox,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QProgressDialog,
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent

from mvsep_cli.api import MVSEP_API
from mvsep_cli.config import Config


BUTTON_STYLE = """
QPushButton {
    background-color: #0176b3;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: #1E9BDC;
}
QPushButton:pressed {
    background-color: #015a8a;
}
QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}
"""

INPUT_STYLE = """
QLineEdit, QComboBox, QSpinBox {
    padding: 8px;
    font-size: 13px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
"""

GROUP_STYLE = """
QGroupBox {
    font-weight: bold;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
"""


class SeparationThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

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
            self.progress.emit("Creating separation task...")
            result = self.api.create_task(
                audio_file=self.audio_file,
                sep_type=self.sep_type,
                add_opt1=self.add_opt1,
                add_opt2=self.add_opt2,
                add_opt3=self.add_opt3,
                output_format=self.output_format,
            )
            self.hash = result.get("hash")
            self.progress.emit(f"Task created! Hash: {self.hash}")
            self.progress.emit("Waiting for completion...")

            status_result = self.api.wait_for_completion(self.hash)

            if status_result.get("status") == "done":
                self.progress.emit("Downloading results...")
                files = self.api.download(self.hash, self.output_dir)
                file_names = ", ".join([os.path.basename(f) for f in files])
                self.progress.emit(f"Done! Files: {file_names}")
                self.finished.emit(
                    True, f"Success!\nFiles saved to:\n{self.output_dir}"
                )
            else:
                self.finished.emit(False, f"Failed: {status_result.get('status')}")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVSEP GUI - Music Separation Tool")
        self.setMinimumSize(600, 700)

        self.config = Config()
        self.api = None
        self.separation_thread = None
        self.algorithms = []

        self.init_ui()
        self.load_token()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("MVSEP Music Separation")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0176b3;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        token_group = QGroupBox("API Configuration")
        token_layout = QVBoxLayout()

        token_row = QHBoxLayout()
        token_row.addWidget(QLabel("API Token:"))
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter your MVSEP API token")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setStyleSheet(INPUT_STYLE)
        token_row.addWidget(self.token_input)

        self.save_token_btn = QPushButton("Save")
        self.save_token_btn.setStyleSheet(BUTTON_STYLE)
        self.save_token_btn.clicked.connect(self.save_token)
        token_row.addWidget(self.save_token_btn)
        token_layout.addLayout(token_row)

        token_hint = QLabel("<a href='https://mvsep.com/user-api'>Get API Token</a>")
        token_hint.setOpenExternalLinks(True)
        token_layout.addWidget(token_hint)

        token_group.setLayout(token_layout)
        layout.addWidget(token_group)

        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #666;")
        file_layout.addWidget(self.file_label)

        file_btn_layout = QHBoxLayout()
        self.select_file_btn = QPushButton("Select Audio File")
        self.select_file_btn.setStyleSheet(BUTTON_STYLE)
        self.select_file_btn.clicked.connect(self.select_file)
        file_btn_layout.addWidget(self.select_file_btn)

        self.select_output_btn = QPushButton("Select Output Dir")
        self.select_output_btn.setStyleSheet(BUTTON_STYLE)
        self.select_output_btn.clicked.connect(self.select_output_dir)
        file_btn_layout.addWidget(self.select_output_btn)
        file_layout.addLayout(file_btn_layout)

        self.output_label = QLabel(f"Output: {os.path.expanduser('~')}")
        file_layout.addWidget(self.output_label)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        algo_group = QGroupBox("Algorithm Selection")
        algo_layout = QVBoxLayout()

        algo_row = QHBoxLayout()
        algo_row.addWidget(QLabel("Separation Type:"))
        self.algo_combo = QComboBox()
        self.algo_combo.setStyleSheet(INPUT_STYLE)
        self.algo_combo.currentIndexChanged.connect(self.on_algo_changed)
        algo_row.addWidget(self.algo_combo)

        self.refresh_algo_btn = QPushButton("↻")
        self.refresh_algo_btn.setToolTip("Refresh algorithms")
        self.refresh_algo_btn.setFixedWidth(40)
        self.refresh_algo_btn.clicked.connect(self.load_algorithms)
        algo_row.addWidget(self.refresh_algo_btn)
        algo_layout.addLayout(algo_row)

        self.opt1_label = QLabel("Option 1:")
        self.opt1_combo = QComboBox()
        self.opt1_combo.setStyleSheet(INPUT_STYLE)
        algo_layout.addWidget(self.opt1_label)
        algo_layout.addWidget(self.opt1_combo)

        self.opt2_label = QLabel("Option 2:")
        self.opt2_combo = QComboBox()
        self.opt2_combo.setStyleSheet(INPUT_STYLE)
        algo_layout.addWidget(self.opt2_label)
        algo_layout.addWidget(self.opt2_combo)

        self.opt3_label = QLabel("Option 3:")
        self.opt3_combo = QComboBox()
        self.opt3_combo.setStyleSheet(INPUT_STYLE)
        algo_layout.addWidget(self.opt3_label)
        algo_layout.addWidget(self.opt3_combo)

        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)

        format_group = QGroupBox("Output Settings")
        format_layout = QHBoxLayout()

        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.setStyleSheet(INPUT_STYLE)
        self.format_combo.addItems(
            [
                "MP3 (320 kbps)",
                "WAV (16 bit)",
                "FLAC (16 bit)",
                "M4A (lossy)",
                "WAV (32 bit)",
                "FLAC (24 bit)",
            ]
        )
        self.format_combo.setCurrentIndex(1)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        self.separate_btn = QPushButton("Start Separation")
        self.separate_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.separate_btn.clicked.connect(self.start_separation)
        layout.addWidget(self.separate_btn)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet(
            "background-color: #f5f5f5; font-family: monospace;"
        )
        layout.addWidget(self.log_text)

        layout.addStretch()
        self.setLayout(layout)

    def log(self, message):
        self.log_text.append(message)

    def load_token(self):
        token = self.config.api_token
        if token:
            self.token_input.setText(token)
            self.init_api(token)

    def save_token(self):
        token = self.token_input.text().strip()
        if token:
            self.config.api_token = token
            self.init_api(token)
            QMessageBox.information(self, "Saved", "API token saved!")
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid token")

    def init_api(self, token):
        try:
            self.api = MVSEP_API(token, base_url=self.config.base_url)
            self.load_algorithms()
        except Exception as e:
            self.log(f"Error initializing API: {e}")

    def load_algorithms(self):
        if not self.api:
            QMessageBox.warning(self, "Error", "Please enter API token first")
            return

        try:
            self.log("Loading algorithms...")
            self.algorithms = self.api.get_algorithms()

            self.algo_combo.blockSignals(True)
            self.algo_combo.clear()

            for algo in sorted(self.algorithms, key=lambda x: x.get("render_id", 0)):
                render_id = algo.get("render_id", "")
                name = algo.get("name", "")
                self.algo_combo.addItem(f"{render_id}: {name}", render_id)

            self.algo_combo.blockSignals(False)

            if self.algo_combo.count() > 0:
                self.on_algo_changed(0)

            self.log(f"Loaded {len(self.algorithms)} algorithms")
        except Exception as e:
            self.log(f"Error loading algorithms: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load algorithms: {e}")

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

            if i == 0:
                self.opt1_label.setText(f"{field_text}:")
                self.opt1_label.setVisible(True)
                self.opt1_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt1_combo.addItem(val, key)
            elif i == 1:
                self.opt2_label.setText(f"{field_text}:")
                self.opt2_label.setVisible(True)
                self.opt2_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt2_combo.addItem(val, key)
            elif i == 2:
                self.opt3_label.setText(f"{field_text}:")
                self.opt3_label.setVisible(True)
                self.opt3_combo.setVisible(True)
                for key, val in sorted(options.items(), key=lambda x: str(x[0])):
                    self.opt3_combo.addItem(val, key)

        self.opt1_combo.blockSignals(False)
        self.opt2_combo.blockSignals(False)
        self.opt3_combo.blockSignals(False)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg);;All Files (*)",
        )
        if file_path:
            self.audio_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.file_label.setStyleSheet("color: #28a745; font-weight: bold;")

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.setText(f"Output: {dir_path}")

    def start_separation(self):
        if not self.api:
            QMessageBox.warning(self, "Error", "Please enter and save API token first")
            return

        if not hasattr(self, "audio_file") or not self.audio_file:
            QMessageBox.warning(self, "Error", "Please select an audio file")
            return

        if not hasattr(self, "output_dir"):
            self.output_dir = os.path.expanduser("~")

        sep_type = self.algo_combo.currentData()
        add_opt1 = (
            str(self.opt1_combo.currentData())
            if self.opt1_combo.currentIndex() >= 0
            else None
        )
        add_opt2 = (
            str(self.opt2_combo.currentData())
            if self.opt2_combo.currentIndex() >= 0
            else None
        )
        add_opt3 = (
            str(self.opt3_combo.currentData())
            if self.opt3_combo.currentIndex() >= 0
            else None
        )
        output_format = self.format_combo.currentIndex()

        self.separate_btn.setEnabled(False)
        self.log("=" * 50)
        self.log(f"Starting separation...")
        self.log(f"File: {os.path.basename(self.audio_file)}")
        self.log(f"Type: {sep_type}")

        self.separation_thread = SeparationThread(
            self.api,
            self.audio_file,
            sep_type,
            add_opt1,
            add_opt2,
            add_opt3,
            output_format,
            self.output_dir,
        )
        self.separation_thread.progress.connect(self.on_progress)
        self.separation_thread.finished.connect(self.on_finished)
        self.separation_thread.start()

    def on_progress(self, message):
        self.log(message)

    def on_finished(self, success, message):
        self.separate_btn.setEnabled(True)
        if success:
            self.log("=" * 50)
            self.log("Separation completed!")
            QMessageBox.information(self, "Success", message)
        else:
            self.log(f"ERROR: {message}")
            QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
