from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is importable when pytest is invoked as an entrypoint.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
