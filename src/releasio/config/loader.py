"""Configuration loading from pyproject.toml and custom config files."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from releasio.config.models import ReleasePyConfig
from releasio.exceptions import ConfigNotFoundError, ConfigValidationError


class ConfigSource(Enum):
    """Source of configuration data."""

    DOTFILE = ".releasio.toml"
    VISIBLE = "releasio.toml"
    PYPROJECT = "pyproject.toml"


@dataclass(frozen=True)
class ConfigPaths:
    """Paths to configuration files."""

    config_file: Path  # The releasio config file
    config_source: ConfigSource
    pyproject_file: Path  # Always needed for project metadata


def find_pyproject_toml(start_path: Path | None = None) -> Path:
    """Find pyproject.toml by walking up from start_path.

    Args:
        start_path: Directory to start searching from. Defaults to cwd.

    Returns:
        Path to pyproject.toml

    Raises:
        ConfigNotFoundError: If no pyproject.toml is found
    """
    current = (start_path or Path.cwd()).resolve()

    while current != current.parent:
        pyproject = current / "pyproject.toml"
        if pyproject.is_file():
            return pyproject
        current = current.parent

    # Check root as well
    pyproject = current / "pyproject.toml"
    if pyproject.is_file():
        return pyproject

    raise ConfigNotFoundError(
        f"No pyproject.toml found in {start_path or Path.cwd()} or any parent directory"
    )


def find_releasio_config(start_path: Path) -> ConfigPaths | None:
    """Find releasio configuration files.

    Searches in the following order:
    1. .releasio.toml (in start_path only)
    2. releasio.toml (in start_path only)
    3. pyproject.toml (walks up tree - existing behavior)

    Args:
        start_path: Directory to search for config

    Returns:
        ConfigPaths with config file and pyproject.toml paths,
        or None if no configuration found

    Raises:
        ConfigNotFoundError: If custom config found but no pyproject.toml
    """
    # Check for dotfile first (highest precedence)
    dotfile = start_path / ".releasio.toml"
    if dotfile.is_file():
        # Must also find pyproject.toml for project metadata
        try:
            pyproject_path = find_pyproject_toml(start_path)
            return ConfigPaths(
                config_file=dotfile,
                config_source=ConfigSource.DOTFILE,
                pyproject_file=pyproject_path,
            )
        except ConfigNotFoundError as e:
            raise ConfigNotFoundError(
                f"Found {dotfile.name} but no pyproject.toml for project metadata. "
                "releasio requires pyproject.toml for project name and version. "
                f"Original error: {e}"
            ) from e

    # Check for visible file (medium precedence)
    visible = start_path / "releasio.toml"
    if visible.is_file():
        try:
            pyproject_path = find_pyproject_toml(start_path)
            return ConfigPaths(
                config_file=visible,
                config_source=ConfigSource.VISIBLE,
                pyproject_file=pyproject_path,
            )
        except ConfigNotFoundError as e:
            raise ConfigNotFoundError(
                f"Found {visible.name} but no pyproject.toml for project metadata. "
                "releasio requires pyproject.toml for project name and version. "
                f"Original error: {e}"
            ) from e

    # Fall back to pyproject.toml (walks up tree)
    try:
        pyproject_path = find_pyproject_toml(start_path)
        return ConfigPaths(
            config_file=pyproject_path,
            config_source=ConfigSource.PYPROJECT,
            pyproject_file=pyproject_path,
        )
    except ConfigNotFoundError:
        return None


def load_toml_file(path: Path) -> dict[str, Any]:
    """Load and parse a TOML file.

    Args:
        path: Path to TOML file

    Returns:
        Parsed TOML as dictionary

    Raises:
        ConfigNotFoundError: If file doesn't exist
        ConfigValidationError: If TOML parsing fails
    """
    if not path.is_file():
        raise ConfigNotFoundError(f"File not found: {path}")

    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigValidationError(f"Invalid TOML in {path}: {e}") from e


def load_pyproject_toml(path: Path) -> dict[str, Any]:
    """Load and parse pyproject.toml.

    Deprecated: Use load_toml_file() for general TOML loading.
    Kept for backward compatibility.

    Args:
        path: Path to pyproject.toml

    Returns:
        Parsed TOML as dictionary

    Raises:
        ConfigNotFoundError: If file doesn't exist
        ConfigValidationError: If TOML parsing fails
    """
    return load_toml_file(path)


def extract_releasio_config(toml_data: dict[str, Any], source: ConfigSource) -> dict[str, Any]:
    """Extract releasio configuration from TOML data.

    For custom config files (.releasio.toml, releasio.toml):
        - Config is at top-level (no [tool.releasio] wrapper)

    For pyproject.toml:
        - Config is under [tool.releasio] section (existing behavior)

    Args:
        toml_data: Parsed TOML data
        source: Source type of the configuration

    Returns:
        The releasio configuration dict (empty if not present)
    """
    if source in (ConfigSource.DOTFILE, ConfigSource.VISIBLE):
        # Custom config files: top-level keys are releasio config
        return toml_data

    # pyproject.toml: extract from [tool.releasio]
    tool: dict[str, Any] = toml_data.get("tool", {})
    result: dict[str, Any] = tool.get("releasio", {})
    return result


def extract_release_py_config(pyproject: dict[str, Any]) -> dict[str, Any]:
    """Extract [tool.releasio] section from pyproject.toml data.

    Deprecated: Use extract_releasio_config() with ConfigSource.
    Kept for backward compatibility.

    Args:
        pyproject: Parsed pyproject.toml data

    Returns:
        The releasio configuration dict (empty if not present)
    """
    return extract_releasio_config(pyproject, ConfigSource.PYPROJECT)


def load_config(path: Path | None = None) -> ReleasePyConfig:
    """Load releasio configuration.

    Configuration is searched in this order:
    1. .releasio.toml (dotfile, in specified directory)
    2. releasio.toml (visible file, in specified directory)
    3. pyproject.toml under [tool.releasio] (walks up tree)

    Custom config files contain only releasio settings (no [tool] wrapper).
    pyproject.toml is always required for project name/version metadata.

    Args:
        path: Path to config file, or directory to search from.
              If None, searches from current directory.

    Returns:
        Validated configuration

    Raises:
        ConfigNotFoundError: If no configuration found
        ConfigValidationError: If configuration is invalid

    Examples:
        >>> # Auto-discover from current directory
        >>> config = load_config()

        >>> # Load from specific directory
        >>> config = load_config(Path("/path/to/project"))

        >>> # Load specific config file
        >>> config = load_config(Path("/path/to/.releasio.toml"))
    """
    start_path = (path or Path.cwd()).resolve()

    # Handle direct file path
    if start_path.is_file():
        # User specified exact config file
        if start_path.name in (".releasio.toml", "releasio.toml"):
            # Custom config file
            if start_path.name == ".releasio.toml":
                source = ConfigSource.DOTFILE
            else:
                source = ConfigSource.VISIBLE
            config_data = load_toml_file(start_path)

            # Still need pyproject.toml for project metadata
            try:
                # Just verify it exists
                find_pyproject_toml(start_path.parent)
            except ConfigNotFoundError as e:
                raise ConfigNotFoundError(
                    f"Found {start_path.name} but no pyproject.toml for project metadata. "
                    "releasio requires pyproject.toml for project name and version."
                ) from e

        elif start_path.name == "pyproject.toml":
            # pyproject.toml specified directly
            source = ConfigSource.PYPROJECT
            config_data = load_toml_file(start_path)
        else:
            raise ConfigValidationError(
                f"Unsupported config file: {start_path.name}. "
                "Expected .releasio.toml, releasio.toml, or pyproject.toml"
            )
    else:
        # Directory path: discover config
        config_paths = find_releasio_config(start_path)
        if not config_paths:
            raise ConfigNotFoundError(
                f"No releasio configuration found in {start_path} or parent directories. "
                "Expected .releasio.toml, releasio.toml, or [tool.releasio] in pyproject.toml"
            )

        config_data = load_toml_file(config_paths.config_file)
        source = config_paths.config_source

    # Extract releasio config based on source
    releasio_data = extract_releasio_config(config_data, source)

    # Validate and return
    try:
        return ReleasePyConfig.model_validate(releasio_data)
    except ValidationError as e:
        errors = []
        for error in e.errors():
            loc = ".".join(str(x) for x in error["loc"])
            msg = error["msg"]
            errors.append(f"  - {loc}: {msg}")

        config_file_name = start_path.name if start_path.is_file() else source.value
        raise ConfigValidationError(
            f"Invalid configuration in {config_file_name}:\n" + "\n".join(errors)
        ) from e


def get_project_name(path: Path | None = None) -> str:
    """Get the project name from pyproject.toml.

    Args:
        path: Path to pyproject.toml or directory to search from

    Returns:
        Project name

    Raises:
        ConfigNotFoundError: If pyproject.toml not found
        ConfigValidationError: If project name not found
    """
    if path is None:
        pyproject_path = find_pyproject_toml()
    elif path.is_dir():
        pyproject_path = find_pyproject_toml(path)
    else:
        pyproject_path = path

    pyproject_data = load_pyproject_toml(pyproject_path)

    try:
        name: str = pyproject_data["project"]["name"]
    except KeyError as e:
        raise ConfigValidationError(f"Missing [project].name in {pyproject_path}") from e
    else:
        return name


def get_project_version(path: Path | None = None) -> str:
    """Get the project version from pyproject.toml.

    Supports both PEP 621 format ([project].version) and
    Poetry format ([tool.poetry].version).

    Args:
        path: Path to pyproject.toml or directory to search from

    Returns:
        Project version string

    Raises:
        ConfigNotFoundError: If pyproject.toml not found
        ConfigValidationError: If project version not found
    """
    if path is None:
        pyproject_path = find_pyproject_toml()
    elif path.is_dir():
        pyproject_path = find_pyproject_toml(path)
    else:
        pyproject_path = path

    pyproject_data = load_pyproject_toml(pyproject_path)

    # Try PEP 621 format first
    if "project" in pyproject_data and "version" in pyproject_data["project"]:
        return str(pyproject_data["project"]["version"])

    # Try Poetry format
    if (
        "tool" in pyproject_data
        and "poetry" in pyproject_data["tool"]
        and "version" in pyproject_data["tool"]["poetry"]
    ):
        return str(pyproject_data["tool"]["poetry"]["version"])

    raise ConfigValidationError(
        f"Missing version in {pyproject_path}. "
        "Expected [project].version or [tool.poetry].version. "
        "Dynamic versioning is not yet supported."
    )
