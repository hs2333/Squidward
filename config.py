# config.py

SONG_NAME = "manbo"

NOTE_X = 855

# Duration of one musical beat in seconds.
BEAT_DURATION = 0.35

# Time for the game to register a new mouse position.
POSITION_SETTLE_TIME = 0.08

# Time to switch to the game window before any mouse movement starts.
PREPARATION_DELAY = 4.0

# Delay after moving to the first note before playback begins.
START_DELAY = 2.0

# Maximum continuous Space hold duration.
MAX_HOLD_DURATION = 4.8

# Short release duration when restarting a long hold.
HOLD_RESET_DURATION = 0.03

PLAY_KEY = "space"
STOP_KEY = "esc"


NOTE_POSITIONS = {
    # Highest group
    "1hh":  (NOTE_X, 230),

    # Middle note
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
