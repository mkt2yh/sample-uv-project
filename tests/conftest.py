import sys
from pathlib import Path

# Ensure the project's 'src' dir is on sys.path so packages under src/ are importable
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
