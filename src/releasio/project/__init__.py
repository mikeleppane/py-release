"""Project detection and manipulation.

This module provides functionality for:
- Detecting Python project types (pyproject.toml, setup.py, etc.)
- Reading and updating version numbers
- Supporting monorepo/workspace configurations
"""

from __future__ import annotations

from releasio.project.detector import ProjectInfo, detect_project
from releasio.project.pyproject import update_pyproject_version

__all__ = [
    "ProjectInfo",
    "detect_project",
    "update_pyproject_version",
]
