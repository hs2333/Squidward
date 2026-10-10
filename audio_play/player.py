# player.py

import random
import threading
import time

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
    RANDOM_X_OFFSET,
    RANDOM_Y_OFFSET,
)


stop_event = threading.Event()


def request_stop():
    """Request playback termination."""
    stop_event.set()


def interruptible_sleep(duration: float) -> bool:
    """Sleep while checking for a stop request."""
    end_time = time.perf_counter() + duration

    while time.perf_counter() < end_time:
        if stop_event.is_set():
            return False

        remaining = end_time - time.perf_counter()
        time.sleep(min(0.01, max(0.0, remaining)))

    return True


def interruptible_sleep_until(deadline: float) -> bool:
    """Sleep until an absolute deadline while checking for a stop request."""
    while True:
        if stop_event.is_set():
            return False

        remaining = deadline - time.perf_counter()
        if remaining <= 0:
            return True

        time.sleep(min(0.01, remaining))


def move_to_note(note: str, settle: bool = True) -> bool:
    """Move to a note with a small random offset."""
    x, y = NOTE_POSITIONS[note]

    target_x = x + random.randint(-RANDOM_X_OFFSET, RANDOM_X_OFFSET)
    target_y = y + random.randint(-RANDOM_Y_OFFSET, RANDOM_Y_OFFSET)

    pydirectinput.moveTo(target_x, target_y, duration=0)

    if settle:
        return interruptible_sleep(POSITION_SETTLE_TIME)

    return not stop_event.is_set()


def play_tap(note: str):
    """Play one tapped note in song mode."""
    if not move_to_note(note, settle=True):
        return

    if stop_event.is_set():
        return

    pydirectinput.press(PLAY_KEY)
    interruptible_sleep(BEAT_DURATION)


def play_rest():
    """Wait for one beat in song mode."""
    interruptible_sleep(BEAT_DURATION)


def play_hold(notes: list[str]):
    """Hold Space while moving through a row of song notes."""
    if not notes:
        return

    if not move_to_note(notes[0], settle=True):
        return

    if stop_event.is_set():
        return

    pydirectinput.keyDown(PLAY_KEY)
    hold_start = time.perf_counter()

    try:
        for index, note in enumerate(notes):
            if stop_event.is_set():
                return

            if index > 0 and not move_to_note(note, settle=True):
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
    """Find the first playable note in song mode."""
    for action in actions:
        if action.action_type in ("tap", "hold"):
            return action.notes[0]

    return None


def play_song(actions):
    """Play parsed beat-based song actions."""
    stop_event.clear()
    first_note = find_first_note(actions)

    if first_note is None:
        print("No playable notes found.")
        return

    print()
    print(f"You have {PREPARATION_DELAY:.1f} seconds to switch to the game window.")

    if not interruptible_sleep(PREPARATION_DELAY):
        print("Playback cancelled.")
        return

    print(f"Moving to first note: {first_note}")
    if not move_to_note(first_note, settle=True):
        print("Playback cancelled.")
        return

    print(f"Waiting {START_DELAY:.1f} seconds before playback.")
    if not interruptible_sleep(START_DELAY):
        print("Playback cancelled.")
        return

    print("Playing song...")

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

    print("Playback stopped." if stop_event.is_set() else "Song finished.")


def _first_voice_note(events):
    """Find the first voiced event."""
    for event in events:
        if event.note is not None:
            return event.note
    return None


def play_voice(events):
    """
    Play a real-time voice pitch contour.

    Space stays held through voiced sections. Mouse movement changes pitch.
    Space is released during unvoiced sections.
    """
    stop_event.clear()
    first_note = _first_voice_note(events)

    if first_note is None:
        print("No voiced pitch was found.")
        return

    print()
    print(f"You have {PREPARATION_DELAY:.1f} seconds to switch to the game window.")

    if not interruptible_sleep(PREPARATION_DELAY):
        print("Playback cancelled.")
        return

    print(f"Moving to first voice note: {first_note}")
    if not move_to_note(first_note, settle=True):
        print("Playback cancelled.")
        return

    print(f"Waiting {START_DELAY:.1f} seconds before playback.")
    if not interruptible_sleep(START_DELAY):
        print("Playback cancelled.")
        return

    print("Playing voice contour...")

    key_is_down = False
    current_note = None
    hold_start = None
    deadline = time.perf_counter()

    try:
        for event in events:
            if stop_event.is_set():
                break

            deadline += event.duration

            if event.note is None:
                if key_is_down:
                    pydirectinput.keyUp(PLAY_KEY)
                    key_is_down = False
                    hold_start = None

                current_note = None

                if not interruptible_sleep_until(deadline):
                    break
                continue

            if event.note != current_note:
                if not move_to_note(event.note, settle=False):
                    break
                current_note = event.note

            if not key_is_down:
                pydirectinput.keyDown(PLAY_KEY)
                key_is_down = True
                hold_start = time.perf_counter()

            while time.perf_counter() < deadline:
                if stop_event.is_set():
                    break

                if hold_start is not None and time.perf_counter() - hold_start >= MAX_HOLD_DURATION:
                    pydirectinput.keyUp(PLAY_KEY)
                    key_is_down = False

                    if not interruptible_sleep(HOLD_RESET_DURATION):
                        break

                    pydirectinput.keyDown(PLAY_KEY)
                    key_is_down = True
                    hold_start = time.perf_counter()

                remaining = deadline - time.perf_counter()
                if remaining > 0:
                    time.sleep(min(0.005, remaining))

            if stop_event.is_set():
                break

    finally:
        if key_is_down:
            pydirectinput.keyUp(PLAY_KEY)
        else:
            pydirectinput.keyUp(PLAY_KEY)

    print("Playback stopped." if stop_event.is_set() else "Voice contour finished.")
