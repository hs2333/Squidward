# config.py

MODE = "voice"  # "song" or "voice"

# Song mode
SONG_NAME = "test"
BEAT_DURATION = 0.30

# Voice mode
NOTE_FREQUENCY_FILE = "note_frequencies.json"
VOICE_PITCH_FILE = "voices/nizhou-audio.Pitch"

# Duration of each pitch-analysis window.
VOICE_STEP = 0.12

# Minimum Praat pitch confidence.
VOICE_MIN_STRENGTH = 0.30

# Minimum Praat frame intensity.
VOICE_MIN_INTENSITY = 0.03

# Minimum fraction of usable pitch frames inside one window.
VOICE_MIN_VOICED_FRACTION = 0.20

# Median smoothing window for pitch movement.
VOICE_SMOOTHING_WINDOW = 3

# Keep Space held across short unvoiced gaps.
VOICE_BRIDGE_GAP = 0.30

# Input timing
POSITION_SETTLE_TIME = 0.08
PREPARATION_DELAY = 4.0
START_DELAY = 2.0

# Maximum continuous Space hold duration.
MAX_HOLD_DURATION = 4.8

# Short release when the 4.8-second hold limit is reached.
HOLD_RESET_DURATION = 0.03

PLAY_KEY = "space"
STOP_KEY = "esc"

# Mouse coordinates
NOTE_X = 635

NOTE_POSITIONS = {
    # Highest group
    "1hh":  (NOTE_X, 230),
    "7h":   (NOTE_X, 255),
    "6.5h": (NOTE_X, 285),
    "6h":   (NOTE_X, 320),
    "5.5h": (NOTE_X, 345),
    "5h":   (NOTE_X, 370),
    "4.5h": (NOTE_X, 395),
    "4h":   (NOTE_X, 420),
    "3h":   (NOTE_X, 450),
    "2.5h": (NOTE_X, 485),
    "2h":   (NOTE_X, 510),
    "1.5h": (NOTE_X, 535),
    "1h":   (NOTE_X, 565),

    # Lowest group
    "7":    (NOTE_X, 595),
    "6.5":  (NOTE_X, 620),
    "6":    (NOTE_X, 650),
    "5.5":  (NOTE_X, 670),
    "5":    (NOTE_X, 700),
    "4.5":  (NOTE_X, 730),
    "4":    (NOTE_X, 760),
    "3":    (NOTE_X, 790),
    "2.5":  (NOTE_X, 810),
    "2":    (NOTE_X, 835),
    "1.5":  (NOTE_X, 865),
    "1":    (NOTE_X, 900),
}

# Small random mouse variation.
RANDOM_X_OFFSET = 7
RANDOM_Y_OFFSET = 3