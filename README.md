# Shutdown Timer

A simple, modern, cross-platform shutdown timer built with Python and PyQt6.

## Features

- **Modern UI**: Dark theme, clean interface.
- **Two Modes**:
  - **Duration**: Set a timer for *X* hours, minutes, seconds.
  - **Specific Time**: Schedule a shutdown at a specific clock time (e.g., 03:30).
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Safe**: Uses native OS commands (`shutdown`) for reliable execution.

## Requirements

- Python 3.x
- PyQt6

## How to Run

1.  **Install Dependencies**:
    ```bash
    pip install PyQt6
    ```

2.  **Run the Application**:
    ```bash
    python main.py
    ```

## Build (Optional)

To create a standalone executable:
```bash
pyinstaller main.py -F -w -n ShutdownTimer --add-data "shutdown_package:shutdown_package"
```
