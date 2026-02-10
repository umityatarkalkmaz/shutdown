import sys
from PyQt6.QtWidgets import QApplication
from shutdown_package.gui import ShutdownTimer

def main():
    app = QApplication(sys.argv)
    window = ShutdownTimer()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
