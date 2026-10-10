# pitch_reader.py

from dataclasses import dataclass
from pathlib import Path
import json
import math
import re
import statistics

from config import (
    VOICE_STEP,
    VOICE_MIN_STRENGTH,
    VOICE_MIN_INTENSITY,
    VOICE_MIN_VOICED_FRACTION,
    VOICE_SMOOTHING_WINDOW,
    VOICE_BRIDGE_GAP,
)


NOTE_NAMES_LOW_TO_HIGH = [
    "1",
    "1.5",
    "2",
    "2.5",
    "3",
    "4",
    "4.5",
    "5",
    "5.5",
    "6",
    "6.5",
    "7",
    "1h",
    "1.5h",
    "2h",
    "2.5h",
    "3h",
    "4h",
    "4.5h",
    "5h",
    "5.5h",
    "6h",
    "6.5h",
    "7h",
    "1hh",
]


@dataclass
class PitchFrame:
    time: float
    intensity: float
    frequency: float
    strength: float


@dataclass
class VoiceEvent:
    note: str | None
    duration: float


@dataclass
class PitchData:
    dx: float
    x1: float
    frames: list[PitchFrame]


_FRAME_RE = re.compile(
    r"\n    frames \[\d+\]:\r?\n"
)


def load_note_frequencies(
    path: str | Path,
) -> dict[str, float]:
    """
    Load the saved 25-note frequency calibration.
    """

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    missing = [
        note
        for note in NOTE_NAMES_LOW_TO_HIGH
        if note not in data
    ]

    if missing:
        raise ValueError(
            f"Missing calibrated notes in {path}: "
            f"{missing}"
        )

    return {
        note: float(data[note])
        for note in NOTE_NAMES_LOW_TO_HIGH
    }


def load_praat_pitch(
    path: str | Path,
) -> PitchData:
    """
    Load the selected pitch track from a Praat
    long-text Pitch file.
    """

    path = Path(path)

    text = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    dx_match = re.search(
        r"\ndx = ([0-9.eE+-]+)",
        text,
    )

    x1_match = re.search(
        r"\nx1 = ([0-9.eE+-]+)",
        text,
    )

    if not dx_match or not x1_match:
        raise ValueError(
            f"Could not read Praat Pitch header from: "
            f"{path}"
        )

    dx = float(dx_match.group(1))
    x1 = float(x1_match.group(1))

    blocks = _FRAME_RE.split(text)[1:]

    frames: list[PitchFrame] = []

    for index, block in enumerate(blocks):

        intensity_match = re.search(
            r"intensity = ([0-9.eE+-]+)",
            block,
        )

        candidate_match = re.search(
            r"candidates \[1\]:\s*\r?\n"
            r"\s*frequency = ([0-9.eE+-]+)\s*\r?\n"
            r"\s*strength = ([0-9.eE+-]+)",
            block,
        )

        if (
            not intensity_match
            or not candidate_match
        ):
            raise ValueError(
                f"Could not parse Pitch frame "
                f"{index + 1} in: {path}"
            )

        frames.append(
            PitchFrame(
                time=x1 + index * dx,
                intensity=float(
                    intensity_match.group(1)
                ),
                frequency=float(
                    candidate_match.group(1)
                ),
                strength=float(
                    candidate_match.group(2)
                ),
            )
        )

    return PitchData(
        dx=dx,
        x1=x1,
        frames=frames,
    )


def nearest_note(
    frequency: float,
    calibration: dict[str, float],
) -> str:
    """
    Map a frequency to the closest calibrated
    in-game note.
    """

    return min(
        calibration,
        key=lambda note: abs(
            math.log2(
                frequency
                / calibration[note]
            )
        ),
    )


def _smooth_note_run(
    notes: list[str],
    window: int,
) -> list[str]:
    """
    Apply a small median filter to one continuous
    voiced section.
    """

    if window <= 1 or len(notes) < 3:
        return notes

    if window % 2 == 0:
        window += 1

    note_to_index = {
        note: index
        for index, note
        in enumerate(
            NOTE_NAMES_LOW_TO_HIGH
        )
    }

    index_to_note = {
        index: note
        for index, note
        in enumerate(
            NOTE_NAMES_LOW_TO_HIGH
        )
    }

    radius = window // 2

    indices = [
        note_to_index[note]
        for note in notes
    ]

    result = []

    for i in range(len(indices)):

        left = max(
            0,
            i - radius,
        )

        right = min(
            len(indices),
            i + radius + 1,
        )

        median_index = round(
            statistics.median(
                indices[left:right]
            )
        )

        result.append(
            index_to_note[median_index]
        )

    return result


def _bridge_short_unvoiced_gaps(
    notes: list[str | None],
) -> list[str | None]:
    """
    Keep short unvoiced gaps connected.

    Short consonants and brief Praat pitch-detection
    failures are filled with the previous note so
    Space remains held.

    Longer pauses remain real rests.
    """

    result = list(notes)

    max_gap_bins = max(
        0,
        math.floor(
            VOICE_BRIDGE_GAP
            / VOICE_STEP
            + 1e-9
        ),
    )

    i = 0

    while i < len(result):

        if result[i] is not None:
            i += 1
            continue

        start = i

        while (
            i < len(result)
            and result[i] is None
        ):
            i += 1

        end = i

        gap_bins = end - start

        has_previous_note = (
            start > 0
            and result[start - 1]
            is not None
        )

        has_next_note = (
            end < len(result)
            and result[end]
            is not None
        )

        if (
            gap_bins <= max_gap_bins
            and has_previous_note
            and has_next_note
        ):
            previous_note = (
                result[start - 1]
            )

            for j in range(
                start,
                end,
            ):
                result[j] = (
                    previous_note
                )

    return result


def _smooth_notes_without_crossing_rests(
    notes: list[str | None],
) -> list[str | None]:
    """
    Smooth pitch changes while preserving
    remaining real pauses.
    """

    result = list(notes)

    i = 0

    while i < len(result):

        if result[i] is None:
            i += 1
            continue

        j = i

        while (
            j < len(result)
            and result[j] is not None
        ):
            j += 1

        result[i:j] = _smooth_note_run(
            [
                note
                for note in result[i:j]
                if note is not None
            ],
            VOICE_SMOOTHING_WINDOW,
        )

        i = j

    return result


def build_voice_events(
    voice_pitch_path: str | Path,
    calibration: dict[str, float],
) -> list[VoiceEvent]:
    """
    Convert a Praat Pitch track into timed
    in-game note/rest events.
    """

    pitch = load_praat_pitch(
        voice_pitch_path
    )

    if not pitch.frames:
        return []

    start_time = pitch.frames[0].time

    end_time = (
        pitch.frames[-1].time
        + pitch.dx
    )

    notes: list[str | None] = []

    bin_start = start_time
    frame_index = 0

    while bin_start < end_time:

        bin_end = min(
            bin_start + VOICE_STEP,
            end_time,
        )

        current_frames = []

        while (
            frame_index
            < len(pitch.frames)
            and pitch.frames[
                frame_index
            ].time
            < bin_end
        ):

            if (
                pitch.frames[
                    frame_index
                ].time
                >= bin_start
            ):
                current_frames.append(
                    pitch.frames[
                        frame_index
                    ]
                )

            frame_index += 1

        usable = [
            frame
            for frame
            in current_frames
            if frame.frequency > 0
            and frame.strength
            >= VOICE_MIN_STRENGTH
            and frame.intensity
            >= VOICE_MIN_INTENSITY
        ]

        minimum_usable = max(
            1,
            math.ceil(
                len(current_frames)
                * VOICE_MIN_VOICED_FRACTION
            ),
        )

        if (
            len(usable)
            < minimum_usable
        ):
            notes.append(None)

        else:
            median_frequency = (
                statistics.median(
                    frame.frequency
                    for frame
                    in usable
                )
            )

            notes.append(
                nearest_note(
                    median_frequency,
                    calibration,
                )
            )

        bin_start += VOICE_STEP

    # Reconnect short gaps before smoothing.
    notes = (
        _bridge_short_unvoiced_gaps(
            notes
        )
    )

    notes = (
        _smooth_notes_without_crossing_rests(
            notes
        )
    )

    events: list[VoiceEvent] = []

    for index, note in enumerate(notes):

        event_start = (
            start_time
            + index * VOICE_STEP
        )

        event_end = min(
            event_start + VOICE_STEP,
            end_time,
        )

        duration = max(
            0.0,
            event_end - event_start,
        )

        if duration <= 0:
            continue

        if (
            events
            and events[-1].note
            == note
        ):
            events[-1].duration += (
                duration
            )

        else:
            events.append(
                VoiceEvent(
                    note=note,
                    duration=duration,
                )
            )

    return events


def total_voice_duration(
    events: list[VoiceEvent],
) -> float:
    """
    Return total voice playback duration.
    """

    return sum(
        event.duration
        for event in events
    )