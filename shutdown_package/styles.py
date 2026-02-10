DARK_THEME = """
    /* ── Base ── */
    QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
        font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', sans-serif;
    }

    QLabel {
        font-size: 14px;
        color: #cdd6f4;
    }

    /* ── Primary Button ── */
    QPushButton {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #89b4fa, stop:1 #74c7ec
        );
        color: #1e1e2e;
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #74c7ec, stop:1 #89dceb
        );
    }
    QPushButton:pressed {
        background-color: #585b70;
        color: #cdd6f4;
    }
    QPushButton:disabled {
        background-color: #45475a;
        color: #6c7086;
    }

    /* ── Cancel Button ── */
    QPushButton#cancelBtn {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #f38ba8, stop:1 #eba0ac
        );
        color: #1e1e2e;
    }
    QPushButton#cancelBtn:hover {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #eba0ac, stop:1 #f5c2e7
        );
    }
    QPushButton#cancelBtn:pressed {
        background-color: #585b70;
        color: #cdd6f4;
    }
    QPushButton#cancelBtn:disabled {
        background-color: #45475a;
        color: #6c7086;
    }

    /* ── Inputs ── */
    QSpinBox, QTimeEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 2px solid #45475a;
        padding: 6px;
        border-radius: 6px;
        font-size: 16px;
        selection-background-color: #89b4fa;
        selection-color: #1e1e2e;
    }
    QSpinBox:focus, QTimeEdit:focus {
        border: 2px solid #89b4fa;
    }
    QSpinBox::up-button, QSpinBox::down-button,
    QTimeEdit::up-button, QTimeEdit::down-button {
        background-color: #45475a;
        border: none;
        width: 20px;
        border-radius: 3px;
    }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
        background-color: #585b70;
    }

    /* ── Tabs ── */
    QTabWidget::pane {
        border: 2px solid #313244;
        border-radius: 8px;
        background: #1e1e2e;
        top: -2px;
    }
    QTabBar::tab {
        background: #313244;
        color: #6c7086;
        padding: 10px 24px;
        margin-right: 2px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 13px;
        font-weight: bold;
    }
    QTabBar::tab:hover {
        background: #45475a;
        color: #a6adc8;
    }
    QTabBar::tab:selected {
        background: #1e1e2e;
        color: #89b4fa;
        border-bottom: 3px solid #89b4fa;
    }

    /* ── Message Box ── */
    QMessageBox {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    QMessageBox QLabel {
        color: #cdd6f4;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        min-width: 80px;
        padding: 8px 20px;
    }
"""
