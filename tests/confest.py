import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = None
for p in [HERE] + list(HERE.parents):
    if (p / "app").is_dir():
        REPO_ROOT = p
        break

if REPO_ROOT is None:
    REPO_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(REPO_ROOT))
