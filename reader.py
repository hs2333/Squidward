# reader.py

from dataclasses import dataclass
from pathlib import Path

from config import NOTE_POSITIONS


@dataclass
class Action:
    action_type: str
    notes: list[str]


def expand_note_token(token: str) -> list[str]:
    """
    Expand shorthand hold notation.

    Examples:
        5h     -> [5h]
        5h-    -> [5h, 5h]
        5h--   -> [5h, 5h, 5h]
        5h---  -> [5h, 5h, 5h, 5h]
    """

    dash_count = len(token) - len(token.rstrip("-"))
    note = token.rstrip("-")

    if not note:
        raise ValueError(f"Invalid note token: {token}")

    return [note] * (dash_count + 1)


def validate_note(note: str, line_number: int):
    """
    Make sure the note exists in the configured note positions.
    """

    if note == "0":
        return

    if note not in NOTE_POSITIONS:
        raise ValueError(
            f"Unknown note '{note}' on line {line_number}."
        )


def parse_line(line: str, line_number: int) -> Action | None:
    """
    Convert one music-sheet line into an Action.
    """

    line = line.strip()

    if not line:
        return None

    tokens = line.split()
    expanded_notes = []

    for token in tokens:
        notes = expand_note_token(token)

        for note in notes:
            validate_note(note, line_number)
            expanded_notes.append(note)

    if expanded_notes == ["0"]:
        return Action(
            action_type="rest",
            notes=[],
        )

    if "0" in expanded_notes:
        raise ValueError(
            f"Invalid rest on line {line_number}. "
            f"'0' must appear by itself."
        )

    if len(expanded_notes) == 1:
        return Action(
            action_type="tap",
            notes=expanded_notes,
        )

    return Action(
        action_type="hold",
        notes=expanded_notes,
    )


def load_song(song_name: str) -> list[Action]:
    """
    Load and parse a song from the songs directory.
    """

    song_path = Path(__file__).parent / "songs" / f"{song_name}.txt"

    if not song_path.exists():
        raise FileNotFoundError(
            f"Song file not found: {song_path}"
        )

    actions = []

    with song_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            action = parse_line(line, line_number)

            if action is not None:
                actions.append(action)

    if not actions:
        raise ValueError(
            f"The song '{song_name}' contains no playable actions."
        )

    return actions


def count_beats(actions: list[Action]) -> int:
    """
    Count the total number of beats in the song.
    """

    total = 0

    for action in actions:
        if action.action_type in ("tap", "rest"):
            total += 1

        elif action.action_type == "hold":
            total += len(action.notes)

    return total