"""forge-skills: skill registry and tool library for the Forge Answer Engine."""
from __future__ import annotations

import importlib.resources
import pathlib


def skills_path() -> str:
    """Return the path to the data directory (contains skills/ and registry.json)."""
    try:
        ref = importlib.resources.files("forge_skills") / "data"
        return str(ref)
    except Exception:
        return str(pathlib.Path(__file__).parent / "data")
