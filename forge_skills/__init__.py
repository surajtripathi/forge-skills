"""forge-skills: skill registry and tool library for the Forge Answer Engine."""
from __future__ import annotations

import pathlib


def skills_path() -> str:
    """Return the path to the repo root (contains skills/ and registry.json)."""
    return str(pathlib.Path(__file__).parent.parent)
