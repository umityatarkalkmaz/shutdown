import sys
import logging
import platform
import subprocess
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Safety limit: maximum 24 hours (86400 seconds)
MAX_SHUTDOWN_SECONDS = 86400


class ShutdownManager:
    def __init__(self):
        self.os_type = platform.system()

    def _validate_seconds(self, seconds):
        """
        Validate and sanitize the seconds parameter.
        Returns a validated integer.
        Raises ValueError if input is invalid.
        """
        if not isinstance(seconds, (int, float)):
            raise ValueError(f"seconds must be a number, got {type(seconds).__name__}")
        seconds = int(seconds)
        if seconds < 0:
            raise ValueError("seconds must be non-negative")
        if seconds > MAX_SHUTDOWN_SECONDS:
            raise ValueError(
                f"seconds must not exceed {MAX_SHUTDOWN_SECONDS} ({MAX_SHUTDOWN_SECONDS // 3600}h)"
            )
        return seconds

    def schedule_shutdown(self, seconds):
        """
        Schedules a system shutdown in `seconds` seconds.
        Returns True if successful, False otherwise.
        """
        try:
            seconds = self._validate_seconds(seconds)
        except ValueError as e:
            logger.error("Input validation failed: %s", e)
            return False

        try:
            if self.os_type == "Windows":
                # Windows shutdown with timer
                # creationflags=subprocess.CREATE_NO_WINDOW hides the console window
                subprocess.run(
                    ["shutdown", "/s", "/t", str(seconds)],
                    check=True,
                    creationflags=(
                        subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                    ),
                )
                logger.info("Shutdown scheduled via Windows in %d seconds.", seconds)
                return True

            elif self.os_type == "Linux":
                # Linux shutdown expects "now" or +MINUTES rather than HH:MM.
                # Round up so short timers (<60s) still schedule in the future.
                if seconds == 0:
                    shutdown_arg = "now"
                else:
                    minutes = (seconds + 59) // 60
                    shutdown_arg = f"+{minutes}"

                subprocess.run(
                    ["shutdown", "-h", shutdown_arg],
                    check=True,
                    stderr=subprocess.PIPE,
                )
                logger.info(
                    "Shutdown scheduled via Linux with argument %s (%d seconds).",
                    shutdown_arg,
                    seconds,
                )
                return True

            elif self.os_type == "Darwin":
                dt_now = datetime.now()
                dt_target = dt_now + timedelta(seconds=seconds)
                time_str = dt_target.strftime("%H:%M")

                subprocess.run(
                    ["shutdown", "-h", time_str],
                    check=True,
                    stderr=subprocess.PIPE,
                )
                logger.info(
                    "Shutdown scheduled via macOS at %s (%d seconds).",
                    time_str,
                    seconds,
                )
                return True

            else:
                logger.warning("Unsupported OS: %s", self.os_type)
                return False

        except subprocess.CalledProcessError as e:
            logger.error("OS schedule command failed: %s", e)
            return False
        except FileNotFoundError:
            logger.error("Shutdown command not found on this system.")
            return False

    def trigger_immediate_shutdown(self):
        """
        Immediately shuts down the system.
        """
        try:
            if self.os_type == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
                logger.info("Immediate shutdown triggered (Windows).")

            elif self.os_type in ("Linux", "Darwin"):
                try:
                    subprocess.run(
                        ["shutdown", "-h", "now"],
                        check=True,
                        stderr=subprocess.PIPE,
                    )
                    logger.info("Immediate shutdown triggered (Unix).")
                except subprocess.CalledProcessError:
                    if self.os_type == "Darwin":
                        logger.info("Trying AppleScript fallback for macOS shutdown.")
                        subprocess.run(
                            [
                                "osascript",
                                "-e",
                                'tell application "System Events" to shut down',
                            ]
                        )
                    else:
                        raise RuntimeError(
                            "Could not execute shutdown. Please run app with sudo."
                        )

        except Exception as e:
            logger.error("Immediate shutdown failed: %s", e)
            raise

    def cancel_shutdown(self):
        """
        Cancels any scheduled system shutdown.
        """
        try:
            if self.os_type == "Windows":
                subprocess.run(["shutdown", "/a"], check=True)
                logger.info("Shutdown cancelled (Windows).")

            elif self.os_type == "Linux":
                subprocess.run(["shutdown", "-c"], check=True)
                logger.info("Shutdown cancelled (Linux).")

            elif self.os_type == "Darwin":
                try:
                    subprocess.run(
                        ["killall", "shutdown"],
                        check=True,
                        stderr=subprocess.DEVNULL,
                    )
                    logger.info("Shutdown cancelled (macOS).")
                except subprocess.CalledProcessError:
                    logger.warning(
                        "No active shutdown process found to cancel (macOS)."
                    )

        except subprocess.CalledProcessError as e:
            logger.warning("Cancel shutdown command failed: %s", e)
        except FileNotFoundError:
            logger.error("Shutdown/killall command not found on this system.")
