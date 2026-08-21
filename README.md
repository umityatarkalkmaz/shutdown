# Shutdown Timer

A simple, modern, cross-platform shutdown timer built with Python and PyQt6.

## Features

- **Modern UI**: Dark theme, clean interface.
- **Two Modes**:
  - **Duration**: Set a timer for *X* hours, minutes, seconds.
  - **Specific Time**: Schedule a shutdown at a specific clock time (e.g., 03:30).
- **Cross-Platform**: Windows and Linux. See *Known issues* below before relying on macOS.
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

## Known issues

These are real defects, found while porting this project to Rust. They are
listed here so anyone reading or contributing knows what they are looking at.
Every one of them is fixed in [shutdown-rust](https://github.com/umityatarkalkmaz/shutdown-rust);
`docs/SPEC.md` there explains each fix.

**Cancelling is never verified.** `ShutdownManager.cancel_shutdown()` returns
`None` in every case — success, failure, or nothing to cancel — and the GUI
resets its labels to "Ready to schedule" regardless. If the cancel command
fails, the user is told they are safe while the machine is still scheduled to
power off. This is the most serious one.

**The countdown and the operating system disagree.** Linux's `shutdown -h +N`
takes whole minutes, so a 30-second timer is scheduled for 60 seconds while the
window counts down from 30. The countdown reaches zero and nothing happens.

**macOS can be scheduled roughly 24 hours late.** `datetime.strftime("%H:%M")`
truncates the target to the current minute. When that minute has already begun,
macOS reads it as tomorrow. A 30-second timer becomes a next-day shutdown, and
the same applies to a zero-second request, which has no special case at all.

**macOS scheduling is believed to block the GUI.** BSD `shutdown` does not
detach; it stays alive until the deadline, and `subprocess.run` waits for it.
If so, the window freezes from the moment Schedule is pressed. This has not
been confirmed on real hardware — it is inferred from BSD `shutdown`'s
behaviour and from the fact that cancelling here needs `killall`, which only
makes sense if the process is still running.

**Cancelling on macOS uses `killall shutdown`**, which signals any process on
the machine with that name, including ones this application did not start.

**The hours spinner allows 99, the validator allows 24.** Any request above
24 hours is refused by `_validate_seconds` and then reported to the user as
"likely missing sudo/admin rights", which is not what happened. The GUI can
express a request that is guaranteed to fail.

**The in-app fallback cannot do what it promises.** When the OS refuses to
schedule, the app starts its own countdown and, when it reaches zero, runs the
same command that just failed. The user waits for a shutdown that was never
going to happen and only finds out at the end.

**Specific-time mode does arithmetic on seconds since midnight**, so it is
wrong on any day that is not 24 hours long — that is, on daylight-saving
transitions.

**The countdown drifts.** It subtracts one from a counter on each timer tick
rather than measuring against a deadline, so it loses time whenever a tick is
late and loses it entirely across suspend and resume.

**Unsupported platforms fail silently, and inconsistently.**
`trigger_immediate_shutdown()` and `cancel_shutdown()` have no branch for an
unrecognised platform: they run nothing, log nothing, and return `None`, which
is indistinguishable from success. `schedule_shutdown()` at least logs a
warning.

**`_validate_seconds` does not validate types.** It rejects non-numbers, then
calls `int()`, so `3.7` silently becomes 3 seconds. And because `bool` is a
subclass of `int` in Python, `True` passes the check and schedules 1 second.

**There are no tests.**
