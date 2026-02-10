# System Patterns

## System Architecture

The application is a standalone desktop application built with **PyQt6**. It follows a modular architecture separating logic, UI, and styles.

## Key Technical Decisions

- **PyQt6**: Modern GUI framework for cross-platform consistency.
- **Subprocess (list-based)**: Invokes native OS shutdown commands without `shell=True` to prevent injection.
- **Modular Design**: Split into `core` (logic), `gui` (interface), and `styles` (QSS).
- **Defense-in-Depth**: Input validation at backend + confirmation dialog at frontend + structured logging.

## Design Patterns

- **Event-Driven**: Standard GUI pattern connecting signals (clicks, timer) to slots (functions).
- **Manager Pattern**: `ShutdownManager` class handles all OS-specific logic, isolating it from the UI.
- **Validation Pattern**: `_validate_seconds()` enforces type, range, and safety limits before subprocess calls.

## Component Relationships

- **`main.py`**: Entry point, initializes the `QApplication`.
- **`shutdown_package.gui.ShutdownTimer`**: The main window class.
- **`shutdown_package.core.ShutdownManager`**: Handles `shutdown` and `cancel` commands for different OSs.
- **`shutdown_package.styles.DARK_THEME`**: Catppuccin Mocha-based QSS styling.
