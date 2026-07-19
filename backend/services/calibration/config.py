import os

# Default calibration reference text containing alphabet pangrams, numbers, punctuation, and subject-specific vocabulary.
DEFAULT_REFERENCE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    "abcdefghijklmnopqrstuvwxyz "
    "0123456789 "
    "Current Voltage Resistance Electricity Circuit Battery Electron Potential Difference"
)

# Directory to persist student handwriting profiles
PROFILES_DIR = os.getenv("CALIBRATION_PROFILES_DIR", "backend/uploads/profiles")
