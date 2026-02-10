from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSpinBox, QTimeEdit, QTabWidget, QMessageBox)
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QFont
from .core import ShutdownManager
from .styles import DARK_THEME

class ShutdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = ShutdownManager()
        self.initUI()
        self.remaining_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.shutdown_scheduled_by_os = False

    def initUI(self):
        self.setWindowTitle("Shutdown Timer")
        self.setFixedSize(400, 400)
        self.setStyleSheet(DARK_THEME)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Duration
        self.tab_duration = QWidget()
        self.setup_duration_tab()
        self.tabs.addTab(self.tab_duration, "Timer Duration")
        
        # Tab 2: Specific Time
        self.tab_time = QWidget()
        self.setup_time_tab()
        self.tabs.addTab(self.tab_time, "Specific Time")

        main_layout.addWidget(self.tabs)

        # Status & Countdown Area (Common)
        self.status_label = QLabel("Ready to schedule")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 12))
        main_layout.addWidget(self.status_label)

        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont('Arial', 36, QFont.Weight.Bold))
        self.countdown_label.setStyleSheet("color: #89b4fa;")
        main_layout.addWidget(self.countdown_label)

        # Controls (Common)
        controls_layout = QHBoxLayout()
        self.start_btn = QPushButton("Schedule Shutdown")
        self.start_btn.clicked.connect(self.schedule_shutdown)
        controls_layout.addWidget(self.start_btn)

        self.cancel_btn = QPushButton("Cancel Shutdown")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.cancel_shutdown)
        self.cancel_btn.setEnabled(False)
        controls_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

    def setup_duration_tab(self):
        layout = QVBoxLayout()
        
        # Inputs Container
        input_container = QHBoxLayout()
        
        # Hours
        h_layout = QVBoxLayout()
        self.hours = QSpinBox()
        self.hours.setRange(0, 99)
        h_layout.addWidget(QLabel("Hours"))
        h_layout.addWidget(self.hours)
        input_container.addLayout(h_layout)

        # Minutes
        m_layout = QVBoxLayout()
        self.minutes = QSpinBox()
        self.minutes.setRange(0, 59)
        m_layout.addWidget(QLabel("Minutes"))
        m_layout.addWidget(self.minutes)
        input_container.addLayout(m_layout)
        
        # Seconds
        s_layout = QVBoxLayout()
        self.seconds = QSpinBox()
        self.seconds.setRange(0, 59)
        s_layout.addWidget(QLabel("Seconds"))
        s_layout.addWidget(self.seconds)
        input_container.addLayout(s_layout)

        layout.addLayout(input_container)

        # Presets
        presets_layout = QHBoxLayout()
        btn_15m = QPushButton("15m")
        btn_15m.clicked.connect(lambda: self.set_preset(15))
        presets_layout.addWidget(btn_15m)

        btn_30m = QPushButton("30m")
        btn_30m.clicked.connect(lambda: self.set_preset(30))
        presets_layout.addWidget(btn_30m)

        btn_1h = QPushButton("1h")
        btn_1h.clicked.connect(lambda: self.set_preset(60))
        presets_layout.addWidget(btn_1h)
        layout.addLayout(presets_layout)
        
        layout.addStretch()
        self.tab_duration.setLayout(layout)

    def setup_time_tab(self):
        layout = QVBoxLayout()
        
        lbl = QLabel("Select Shutdown Time:")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_edit.setFont(QFont('Arial', 20))
        layout.addWidget(self.time_edit)

        layout.addStretch()
        self.tab_time.setLayout(layout)

    def set_preset(self, minutes):
        self.hours.setValue(0)
        self.minutes.setValue(minutes)
        self.seconds.setValue(0)

    def schedule_shutdown(self):
        total_seconds = 0
        
        if self.tabs.currentIndex() == 0:  # Duration Mode
            h = self.hours.value()
            m = self.minutes.value()
            s = self.seconds.value()
            total_seconds = h * 3600 + m * 60 + s
        else:  # Specific Time Mode
            target_time = self.time_edit.time()
            now = QTime.currentTime()
            
            # Calculate difference
            secs_now = now.msecsSinceStartOfDay() // 1000
            secs_target = target_time.msecsSinceStartOfDay() // 1000
            
            if secs_target > secs_now:
                total_seconds = secs_target - secs_now
            else:
                # If target is earlier than now, assume tomorrow
                total_seconds = (24 * 3600 - secs_now) + secs_target

        if total_seconds <= 0:
            QMessageBox.warning(self, "Invalid Time", "Please set a time in the future.")
            return

        # Confirmation dialog — prevent accidental shutdown scheduling
        h_display = total_seconds // 3600
        m_display = (total_seconds % 3600) // 60
        s_display = total_seconds % 60
        confirm = QMessageBox.question(
            self,
            "Confirm Shutdown",
            f"Are you sure you want to schedule a shutdown in "
            f"{h_display:02}:{m_display:02}:{s_display:02}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.remaining_seconds = total_seconds
        
        # Try to Schedule with OS
        success = self.manager.schedule_shutdown(total_seconds)
        
        if success:
            self.shutdown_scheduled_by_os = True
            self.status_label.setText("System Shutdown Scheduled")
            self.countdown_label.setStyleSheet("color: #f38ba8;") 
        else:
            self.shutdown_scheduled_by_os = False
            self.status_label.setText("Internal Timer Active")
            self.countdown_label.setStyleSheet("color: #f9e2af;")
            QMessageBox.information(self, "Fallback Mode", 
                                  "Could not schedule via OS (likely missing sudo/admin rights).\n"
                                  "Switched to Internal Timer. App must remain open.")

        self.lock_interface(True)
        self.timer.start(1000)
        self.update_display()

    def cancel_shutdown(self):
        # Cancel OS Command if it was scheduled
        if self.shutdown_scheduled_by_os:
            self.manager.cancel_shutdown()
        
        self.timer.stop()
        self.shutdown_scheduled_by_os = False
        self.remaining_seconds = 0
        self.update_display()
        
        self.status_label.setText("Ready to schedule")
        self.lock_interface(False)
        self.countdown_label.setStyleSheet("color: #89b4fa;")
        self.countdown_label.setText("--:--:--")

    def update_timer(self):
        self.remaining_seconds -= 1
        self.update_display()

        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.status_label.setText("Shutting Down Now...")
            
            # If not scheduled by OS, we must trigger it now
            if not self.shutdown_scheduled_by_os:
                try:
                    self.manager.trigger_immediate_shutdown()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def update_display(self):
        if self.remaining_seconds < 0:
            self.remaining_seconds = 0
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60
        self.countdown_label.setText(f"{h:02}:{m:02}:{s:02}")

    def lock_interface(self, locked):
        self.tabs.setEnabled(not locked)
        self.start_btn.setEnabled(not locked)
        self.cancel_btn.setEnabled(locked)
