"""forge-skills: installable skill registry and tool library for Forge."""
from __future__ import annotations

import importlib.resources
import pathlib


def skills_path() -> str:
    """Return the absolute path to the bundled data directory.

    The data directory contains registry.json and skills/.
    Works for both editable installs (pip install -e) and wheel installs.
    """
    try:
        ref = importlib.resources.files("forge_skills") / "data"
        return str(ref)
    except Exception:
        return str(pathlib.Path(__file__).parent / "data")
