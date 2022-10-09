"""Automate key press in window.

Small script used to automate set of keypresses in
a window. Takes a list of inputs and repeats until
program detects keypress combination to stop process.

For use on Linux. Requires xdotool to be installed.

Methods:
    auto_key_press:     Automate key press
"""
import keyboard
import time
import subprocess
import sys


def auto_key_press(
    process_name: str = None, commands: list = [], interval_period: int = 1
) -> None:
    """Automate list of key presses.

    Automates list of key presses by running through list of commands
    waiting for interval then repeating process. Process ends when
    cancellation key press combination is detected.

    Args:
        process_name (str):     Name of the process to send commands to.
        commands (list):        List of commands representing individual
                                key press sequences.
        interval_period (int):  Period to wait between each sequence. Uses
                                milliseconds and defaults to 1000ms when
                                not entered.
    """
    id = get_window_id(process_name)
    previous_run_start = time.time()
    current_time = time.time()
    while True:
        current_time = time.time()
        if keyboard.is_pressed("ctrl+q"):
            break
        else:
            if previous_run_start + interval_period < current_time:
                previous_run_start = time.time()
                run_commands(id, commands)


def get_window_id(process_name: str) -> str:
    """Gets window id of target process.

    Args:
        process_name (str):     Name of process.

    Returns:
        window_id (str):        Id of process window
    """
    return (
        subprocess.run(
            ["xdotool", "search", "--onlyvisible", "--name", process_name],
            timeout=5,
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )

def get_current_window_id() -> str:
    """Get the id of currently in use window."""
    pass

def get_focus(window_id: str) -> None:
    """Shifts window focus"""
    pass

def run_commands(window_id: str, commands: list) -> None:
    """Run list of commands as subprocesses.

    Args:
        window_id (str):    Id val of process window
        commands (list):    List of commands representing individual
                            key press sequences.
    """
    for command in commands:
        current_window_id = get_current_window_id()
        get_focus(window_id)
        entry_type = command[0]
        entry = command[1]
        run_sub_process(window_id, entry_type, entry)
        get_focus(current_window_id)

def run_sub_process(window_id: str, entry_type: str, entry: str) -> None:
    """Builds a subprocess list and runs it.

    Args:
        window_id (str):        Id val of process window
        entry_type (str):       Type of entry eg: key, type, keydown
        entry (str):            String of characters or keys to be
                                entered in single process.
    """
    print(f"Entering: {entry}")
    r = subprocess.run(
        ["xdotool", entry_type, "--window", window_id, entry], timeout=5
        )


def main():
    """Main method for module."""
    process_name = sys.argv[0]
    commands = sys.argv[1]
    auto_key_press(process_name, commands)


if __name__ == "__main__":
    main()
