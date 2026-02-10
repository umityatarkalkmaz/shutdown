# Tech Context

## Technologies Used

- **Python 3**: The core programming language.
- **PyQt6**: Modern GUI framework for cross-platform look and feel.
- **Subprocess**: Python module to invoke OS-native shutdown commands securely (list-based, no `shell=True`).
- **Logging**: Structured audit trail for all security-critical operations.

## Development Setup

- **Requirements**: Python 3.x installed. `pip install PyQt6`.
- **Execution**: Run `python main.py` in the terminal.

## Technical Constraints

- **Operating System**: Cross-platform — supports **Windows** (`shutdown /s /t`), **Linux** (`shutdown -h`), and **macOS** (`shutdown -h` + AppleScript fallback).
- **Permissions**: Unix systems may require `sudo` for the native shutdown command; app falls back to internal timer if OS scheduling fails.

## Dependencies

- **PyQt6** (`pip install PyQt6`)
- Standard Python Library (`subprocess`, `platform`, `logging`, `datetime`)
