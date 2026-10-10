# main.py

from pathlib import Path
import keyboard

from config import (
    MODE,
    SONG_NAME,
    BEAT_DURATION,
    STOP_KEY,
    NOTE_FREQUENCY_FILE,
    VOICE_PITCH_FILE,
)

from reader import (
    load_song,
    count_beats,
)

from pitch_reader import (
    load_note_frequencies,
    build_voice_events,
    total_voice_duration,
)

from player import (
    play_song,
    play_voice,
    request_stop,
)


def project_path(
    relative_path: str,
) -> Path:
    """
    Resolve a path relative to this project.
    """

    return (
        Path(__file__).parent
        / relative_path
    )


def run_song_mode():
    """
    Load and play a beat-based song.
    """

    print(
        f"Loading song: "
        f"{SONG_NAME}"
    )

    actions = load_song(
        SONG_NAME
    )

    total_beats = count_beats(
        actions
    )

    estimated_duration = (
        total_beats
        * BEAT_DURATION
    )

    tap_count = sum(
        1
        for action in actions
        if action.action_type
        == "tap"
    )

    hold_count = sum(
        1
        for action in actions
        if action.action_type
        == "hold"
    )

    rest_count = sum(
        1
        for action in actions
        if action.action_type
        == "rest"
    )

    print()
    print(
        f"Song: {SONG_NAME}"
    )
    print(
        f"Actions: "
        f"{len(actions)}"
    )
    print(
        f"Total beats: "
        f"{total_beats}"
    )
    print(
        f"Estimated duration: "
        f"{estimated_duration:.2f} "
        f"seconds"
    )
    print(
        f"Tap actions:  "
        f"{tap_count}"
    )
    print(
        f"Hold actions: "
        f"{hold_count}"
    )
    print(
        f"Rests:        "
        f"{rest_count}"
    )

    play_song(actions)


def run_voice_mode():
    """
    Load saved note frequencies and play
    a Praat Pitch contour.
    """

    frequency_path = project_path(
        NOTE_FREQUENCY_FILE
    )

    voice_path = project_path(
        VOICE_PITCH_FILE
    )

    print(
        f"Loading note frequencies: "
        f"{frequency_path.name}"
    )

    calibration = (
        load_note_frequencies(
            frequency_path
        )
    )

    print(
        f"Loading voice pitch: "
        f"{voice_path.name}"
    )

    events = build_voice_events(
        voice_path,
        calibration,
    )

    voiced_events = sum(
        1
        for event in events
        if event.note is not None
    )

    rest_events = sum(
        1
        for event in events
        if event.note is None
    )

    print()
    print(
        f"Voice events: "
        f"{len(events)}"
    )

    print(
        f"Voiced events: "
        f"{voiced_events}"
    )

    print(
        f"Rest events: "
        f"{rest_events}"
    )

    print(
        f"Duration: "
        f"{total_voice_duration(events):.2f} "
        f"seconds"
    )

    print()
    print(
        "Saved note frequencies:"
    )

    for note, frequency in reversed(
        list(calibration.items())
    ):
        print(
            f"  {note:>4}: "
            f"{frequency:7.2f} Hz"
        )

    play_voice(events)


def main():
    print(
        f"Mode: {MODE}"
    )

    print(
        f"Press "
        f"{STOP_KEY.upper()} "
        f"to stop."
    )

    print()

    keyboard.add_hotkey(
        STOP_KEY,
        request_stop,
    )

    try:

        if MODE == "song":
            run_song_mode()

        elif MODE == "voice":
            run_voice_mode()

        else:
            raise ValueError(
                "MODE must be either "
                "'song' or 'voice'."
            )

    except Exception as error:
        print()
        print(
            "Playback failed:"
        )
        print(error)

    finally:
        keyboard.remove_hotkey(
            STOP_KEY
        )


if __name__ == "__main__":
    main()