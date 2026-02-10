# Product Context

## Why this project exists

Users often need to step away from their computer but want it to shut down after a certain task completes or at a specific time.

## Problems it solves

- **Complexity**: Removes need for CLI commands.
- **Safety**: Uses OS-native timers (Windows) to ensure a graceful shutdown warning rather than a forced kill.
- **Flexibility**: Supports both "Duration" (e.g., "in 1 hour") and "Target Time" (e.g., "at 03:00 AM").

## How it works

1.  **Mode Selection**: User chooses between "Duration" or "Specific Time".
2.  **Scheduling**:
    - **Windows**: The app sends the precise duration to the OS (`shutdown /s /t <sec>`). The OS handles the actual trigger. The app displays a synchronized visual countdown.
    - **Unix**: The app calculates the target time and uses `shutdown -h HH:MM` or `+m`.
3.  **Feedback**: The app shows exactly when the shutdown will occur and how much time is left.
4.  **Cancellation**: The app sends the OS-specific cancel command (`shutdown /a` or `shutdown -c`).
