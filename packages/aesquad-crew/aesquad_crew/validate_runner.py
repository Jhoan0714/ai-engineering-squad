"""Optional post-run validation via packages/aesquad."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from aesquad_crew.kit import aesquad_bin


def maybe_validate(kit_root: Path, handoff_dir: Path) -> int:
    binary = aesquad_bin(kit_root)
    if not binary.is_file():
        print(f"Skip validate: missing {binary}", file=sys.stderr)
        return 0
    cmd = ["node", str(binary), "validate", "--dir", str(handoff_dir)]
    print("Running:", " ".join(cmd))
    completed = subprocess.run(cmd, check=False)
    return int(completed.returncode)
