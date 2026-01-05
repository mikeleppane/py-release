# API Reference

:material-api: Auto-generated API documentation from source code.

---

## Overview

This section contains automatically generated documentation from the releasio source code.

---

## Modules

### Core

Core business logic modules:

- **version** - Version parsing and bumping
- **commits** - Commit message parsing
- **changelog** - Changelog generation
- **version_files** - Version file management

### Configuration

Configuration handling:

- **config.loader** - Configuration file loading
- **config.models** - Pydantic configuration models

### Version Control

Git operations:

- **vcs.git** - Git repository abstraction

### Integrations

External service integrations:

- **forge.github** - GitHub API client
- **publish.pypi** - PyPI publishing

### CLI

Command-line interface:

- **cli.app** - Typer application setup
- **cli.check** - check command
- **cli.update** - update command
- **cli.release** - release command
- **cli.release_pr** - release-pr command

---

## Quick Links

| Module | Description |
|--------|-------------|
| `releasio.core.version` | Version class and bump calculation |
| `releasio.core.commits` | Commit parsing and analysis |
| `releasio.config.models` | Configuration models |
| `releasio.vcs.git` | Git operations |

---

!!! note "Auto-generated Documentation"
    The API documentation below this page is automatically generated from
    docstrings in the source code using mkdocstrings.
