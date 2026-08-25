# player.py

import time
import threading

import keyboard
import pydirectinput

from config import (
    NOTE_POSITIONS,
    BEAT_DURATION,
    POSITION_SETTLE_TIME,
    PREPARATION_DELAY,
    START_DELAY,
    MAX_HOLD_DURATION,
    HOLD_RESET_DURATION,
    PLAY_KEY,
)


stop_event = threading.Event()


def request_stop():
    """
    Request playback termination.
    """
    stop_event.set()


def interruptible_sleep(duration: float) -> bool:
    """
    Sleep while checking for a stop request.

    Returns False if playback was interrupted.
    """

    end_time = time.perf_counter() + duration

    while time.perf_counter() < end_time:
        if stop_event.is_set():
            return False

        remaining = end_time - time.perf_counter()
        time.sleep(min(0.01, max(0, remaining)))

    return True


def move_to_note(note: str) -> bool:
    """
    Move instantly to a note and wait for the game to register it.
    """

    x, y = NOTE_POSITIONS[note]

    pydirectinput.moveTo(
        x,
        y,
        duration=0,
    )

    return interruptible_sleep(POSITION_SETTLE_TIME)


def play_tap(note: str):
    """
    Play one tapped note.
    """

    if not move_to_note(note):
        return

    if stop_event.is_set():
        return

    pydirectinput.press(PLAY_KEY)

    interruptible_sleep(BEAT_DURATION)


def play_rest():
    """
    Wait for one beat without playing anything.
    """

    interruptible_sleep(BEAT_DURATION)


def play_hold(notes: list[str]):
    """
    Hold Space while moving through all notes in the row.

    Each note lasts one beat. The key is automatically released
    and pressed again before the continuous hold exceeds the
    configured maximum hold duration.
    """

    if not notes:
        return

    if not move_to_note(notes[0]):
        return

    if stop_event.is_set():
        return

    pydirectinput.keyDown(PLAY_KEY)

    hold_start = time.perf_counter()

    try:
        for index, note in enumerate(notes):

            if stop_event.is_set():
                return

            if index > 0:
                if not move_to_note(note):
                    return

            beat_start = time.perf_counter()

            while time.perf_counter() - beat_start < BEAT_DURATION:

                if stop_event.is_set():
                    return

                if time.perf_counter() - hold_start >= MAX_HOLD_DURATION:
                    pydirectinput.keyUp(PLAY_KEY)

                    if not interruptible_sleep(HOLD_RESET_DURATION):
                        return

                    pydirectinput.keyDown(PLAY_KEY)
                    hold_start = time.perf_counter()

                time.sleep(0.005)

    finally:
        pydirectinput.keyUp(PLAY_KEY)


def find_first_note(actions):
    """
    Find the first playable note in the song.
    """

    for action in actions:

        if action.action_type == "tap":
            return action.notes[0]

        if action.action_type == "hold":
            return action.notes[0]

    return None


def play_song(actions):
    """
    Play all parsed actions.
    """

    stop_event.clear()

    first_note = find_first_note(actions)

    if first_note is None:
        print("No playable notes found.")
        return

    print()
    print(
        f"You have {PREPARATION_DELAY:.1f} seconds "
        f"to switch to the game window."
    )

    if not interruptible_sleep(PREPARATION_DELAY):
        print("Playback cancelled.")
        return

    print(f"Moving to first note: {first_note}")

    if not move_to_note(first_note):
        print("Playback cancelled.")
        return

    print(
        f"Waiting {START_DELAY:.1f} seconds before playback."
    )

    if not interruptible_sleep(START_DELAY):
        print("Playback cancelled.")
        return

    print("Playing...")

    try:
        for action in actions:

            if stop_event.is_set():
                break

            if action.action_type == "rest":
                play_rest()

            elif action.action_type == "tap":
                play_tap(action.notes[0])

            elif action.action_type == "hold":
                play_hold(action.notes)

    finally:
        pydirectinput.keyUp(PLAY_KEY)

    if stop_event.is_set():
        print("Playback stopped.")

    else:
        print("Song finished.")