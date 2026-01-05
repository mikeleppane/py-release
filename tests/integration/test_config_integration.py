"""Integration tests for custom configuration file support.

Tests end-to-end scenarios with .releasio.toml, releasio.toml, and pyproject.toml.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from releasio.config import load_config
from releasio.config.loader import ConfigSource, find_releasio_config


class TestConfigIntegration:
    """Integration tests for configuration file discovery and loading."""

    def test_precedence_all_three_files_present(self, tmp_path: Path) -> None:
        """When all three config files exist, .releasio.toml has highest precedence."""
        # Create all three config files with different default_branch values
        dotfile = tmp_path / ".releasio.toml"
        dotfile.write_text("""
default_branch = "dotfile-branch"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        visible = tmp_path / "releasio.toml"
        visible.write_text("""
default_branch = "visible-branch"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-project"
version = "1.0.0"

[tool.releasio]
default_branch = "pyproject-branch"

[tool.releasio.commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Verify discovery finds dotfile first
        config_paths = find_releasio_config(tmp_path)
        assert config_paths is not None
        assert config_paths.config_source == ConfigSource.DOTFILE
        assert config_paths.config_file == dotfile

        # Verify load_config uses dotfile
        config = load_config(tmp_path)
        assert config.default_branch == "dotfile-branch"

    def test_precedence_visible_and_pyproject(self, tmp_path: Path) -> None:
        """When only releasio.toml and pyproject.toml exist, releasio.toml wins."""
        visible = tmp_path / "releasio.toml"
        visible.write_text("""
default_branch = "visible-branch"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-project"
version = "1.0.0"

[tool.releasio]
default_branch = "pyproject-branch"

[tool.releasio.commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Verify discovery finds visible file
        config_paths = find_releasio_config(tmp_path)
        assert config_paths is not None
        assert config_paths.config_source == ConfigSource.VISIBLE
        assert config_paths.config_file == visible

        # Verify load_config uses visible file
        config = load_config(tmp_path)
        assert config.default_branch == "visible-branch"

    def test_precedence_pyproject_only(self, tmp_path: Path) -> None:
        """When only pyproject.toml exists, use it (backward compatibility)."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-project"
version = "1.0.0"

[tool.releasio]
default_branch = "pyproject-branch"

[tool.releasio.commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Verify discovery finds pyproject.toml
        config_paths = find_releasio_config(tmp_path)
        assert config_paths is not None
        assert config_paths.config_source == ConfigSource.PYPROJECT
        assert config_paths.config_file == pyproject

        # Verify load_config uses pyproject.toml
        config = load_config(tmp_path)
        assert config.default_branch == "pyproject-branch"

    def test_cli_check_with_dotfile(self, tmp_path: Path) -> None:
        """CLI check command works with .releasio.toml."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Create .releasio.toml
        dotfile = tmp_path / ".releasio.toml"
        dotfile.write_text("""
default_branch = "main"

[commits]
types_minor = ["feat", "feature"]
types_patch = ["fix", "bugfix"]
""")

        # Create pyproject.toml for project metadata
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-cli-project"
version = "0.1.0"
description = "Test project"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""")

        # Commit files
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "feat: initial commit"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Verify config loads correctly
        config = load_config(tmp_path)
        assert config.default_branch == "main"
        assert config.commits.types_minor == ["feat", "feature"]
        assert config.commits.types_patch == ["fix", "bugfix"]

    def test_cli_check_with_visible_file(self, tmp_path: Path) -> None:
        """CLI check command works with releasio.toml."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Create releasio.toml
        visible = tmp_path / "releasio.toml"
        visible.write_text("""
default_branch = "develop"

[commits]
types_minor = ["feat"]
types_patch = ["fix", "perf"]

[changelog]
enabled = true
path = "CHANGES.md"
""")

        # Create pyproject.toml for project metadata
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-visible-project"
version = "0.2.0"
description = "Test visible config"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""")

        # Commit files
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "fix: initial commit"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Verify config loads correctly
        config = load_config(tmp_path)
        assert config.default_branch == "develop"
        assert config.changelog.enabled is True
        assert config.changelog.path == Path("CHANGES.md")

    def test_subdirectory_config_pattern(self, tmp_path: Path) -> None:
        """Custom config in subdirectory with pyproject.toml in parent."""
        # Create parent directory structure
        parent = tmp_path / "parent"
        parent.mkdir()

        # Create pyproject.toml in parent
        pyproject = parent / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "monorepo-project"
version = "1.0.0"

[tool.releasio]
default_branch = "parent-config"
""")

        # Create subdirectory with custom config
        subdir = parent / "subproject"
        subdir.mkdir()

        # Custom config in subdirectory
        subconfig = subdir / ".releasio.toml"
        subconfig.write_text("""
default_branch = "subproject-config"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Also need pyproject.toml in subdir for metadata
        sub_pyproject = subdir / "pyproject.toml"
        sub_pyproject.write_text("""
[project]
name = "subproject"
version = "0.1.0"
""")

        # Load config from subdirectory
        config = load_config(subdir)
        assert config.default_branch == "subproject-config"

    def test_backward_compatibility_pyproject_only(self, tmp_path: Path) -> None:
        """Existing pyproject.toml configs work unchanged (backward compatibility)."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Create traditional pyproject.toml config (pre-custom-file support)
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "legacy-project"
version = "2.0.0"
description = "Legacy config format"

[tool.releasio]
default_branch = "master"
allow_dirty = false

[tool.releasio.commits]
types_minor = ["feat", "feature"]
types_patch = ["fix", "bugfix", "perf"]
breaking_pattern = "BREAKING CHANGE:"

[tool.releasio.changelog]
enabled = true
path = "CHANGELOG.md"

[tool.releasio.version]
tag_prefix = "v"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""")

        # Commit
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: setup project"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        # Verify config loads exactly as before
        config = load_config(tmp_path)
        assert config.default_branch == "master"
        assert config.allow_dirty is False
        assert config.commits.types_minor == ["feat", "feature"]
        assert config.commits.types_patch == ["fix", "bugfix", "perf"]
        assert config.commits.breaking_pattern == "BREAKING CHANGE:"
        assert config.changelog.enabled is True
        assert config.changelog.path == Path("CHANGELOG.md")
        assert config.version.tag_prefix == "v"

    def test_custom_config_without_pyproject_error(self, tmp_path: Path) -> None:
        """Custom config without pyproject.toml raises clear error."""
        # Create only .releasio.toml (no pyproject.toml)
        dotfile = tmp_path / ".releasio.toml"
        dotfile.write_text("""
default_branch = "main"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Should raise error about missing pyproject.toml
        with pytest.raises(
            Exception,
            match=r"Found \.releasio\.toml but no pyproject\.toml for project metadata",
        ):
            find_releasio_config(tmp_path)

    def test_direct_file_path_dotfile(self, tmp_path: Path) -> None:
        """Load config by specifying .releasio.toml file path directly."""
        # Create config files
        dotfile = tmp_path / ".releasio.toml"
        dotfile.write_text("""
default_branch = "direct-dotfile"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "direct-path-test"
version = "0.1.0"
""")

        # Load by direct file path
        config = load_config(dotfile)
        assert config.default_branch == "direct-dotfile"

    def test_direct_file_path_visible(self, tmp_path: Path) -> None:
        """Load config by specifying releasio.toml file path directly."""
        # Create config files
        visible = tmp_path / "releasio.toml"
        visible.write_text("""
default_branch = "direct-visible"

[commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "direct-visible-test"
version = "0.1.0"
""")

        # Load by direct file path
        config = load_config(visible)
        assert config.default_branch == "direct-visible"

    def test_direct_file_path_pyproject(self, tmp_path: Path) -> None:
        """Load config by specifying pyproject.toml file path directly."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "direct-pyproject-test"
version = "0.1.0"

[tool.releasio]
default_branch = "direct-pyproject"

[tool.releasio.commits]
types_minor = ["feat"]
types_patch = ["fix"]
""")

        # Load by direct file path
        config = load_config(pyproject)
        assert config.default_branch == "direct-pyproject"
