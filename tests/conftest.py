import sys
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_ROOT.parent

sys.path = [
    path
    for path in sys.path
    if Path(path).resolve() != TESTS_ROOT
]
sys.path.insert(0, str(PROJECT_ROOT))
