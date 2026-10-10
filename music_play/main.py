# main.py

import keyboard

from config import (
    SONG_NAME,
    BEAT_DURATION,
    STOP_KEY,
)

from reader import (
    load_song,
    count_beats,
)

from player import (
    play_song,
    request_stop,
)


def main():
    print(f"Loading song: {SONG_NAME}")

    try:
        actions = load_song(SONG_NAME)

    except Exception as error:
        print()
        print("Failed to load song:")
        print(error)
        return

    total_beats = count_beats(actions)
    estimated_duration = total_beats * BEAT_DURATION

    tap_count = sum(
        1 for action in actions
        if action.action_type == "tap"
    )

    hold_count = sum(
        1 for action in actions
        if action.action_type == "hold"
    )

    rest_count = sum(
        1 for action in actions
        if action.action_type == "rest"
    )

    print()
    print(f"Song: {SONG_NAME}")
    print(f"Actions: {len(actions)}")
    print(f"Total beats: {total_beats}")
    print(
        f"Estimated duration: "
        f"{estimated_duration:.2f} seconds"
    )
    print()
    print(f"Tap actions:  {tap_count}")
    print(f"Hold actions: {hold_count}")
    print(f"Rests:        {rest_count}")
    print()
    print(f"Press {STOP_KEY.upper()} to stop.")
    print()

    keyboard.add_hotkey(
        STOP_KEY,
        request_stop,
    )

    try:
        play_song(actions)

    finally:
        keyboard.remove_hotkey(STOP_KEY)


if __name__ == "__main__":
    main()