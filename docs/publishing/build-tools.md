# Build Tools

:material-hammer-wrench: Configure your preferred Python build tool.

---

## Overview

releasio supports three popular Python build and publish tools:

| Tool | Description | Default |
|------|-------------|---------|
| **uv** | Fast, modern package manager | Yes |
| **poetry** | Dependency management and packaging | No |
| **pdm** | Modern Python package manager | No |

---

## uv (Default)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver.

### Configuration

```toml title=".releasio.toml"
[publish]
tool = "uv"
```

### Commands Used

| Action | Command |
|--------|---------|
| Build | `uv build` |
| Publish | `uv publish` |
| Publish (OIDC) | `uv publish --trusted-publishing always` |

### Project Setup

```toml title="pyproject.toml"
[project]
name = "my-package"
version = "1.0.0"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Workflow Example

```yaml title=".github/workflows/release.yml"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Why uv?

- **Fast**: 10-100x faster than pip
- **Modern**: First-class `pyproject.toml` support
- **Reliable**: Deterministic resolution
- **Compatible**: Works with existing tools

---

## Poetry

[Poetry](https://python-poetry.org/) is a tool for dependency management and packaging.

### Configuration

```toml title=".releasio.toml"
[publish]
tool = "poetry"
```

### Commands Used

| Action | Command |
|--------|---------|
| Build | `poetry build` |
| Publish | `poetry publish` |
| Publish (token) | `poetry publish --username __token__ --password $TOKEN` |

### Project Setup

```toml title="pyproject.toml"
[tool.poetry]
name = "my-package"
version = "1.0.0"
description = "My awesome package"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Workflow Example

```yaml title=".github/workflows/release.yml"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: pipx install poetry

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pypi-token: ${{ secrets.PYPI_TOKEN }}
```

!!! note "Poetry and Trusted Publishing"
    Poetry doesn't natively support OIDC trusted publishing.
    Use an API token for authentication.

### Version Location

Poetry stores version in `[tool.poetry]`:

```toml
[tool.poetry]
version = "1.0.0"
```

releasio automatically detects and updates this.

---

## PDM

[PDM](https://pdm-project.org/) is a modern Python package and dependency manager.

### Configuration

```toml title=".releasio.toml"
[publish]
tool = "pdm"
```

### Commands Used

| Action | Command |
|--------|---------|
| Build | `pdm build` |
| Publish | `pdm publish` |
| Publish (token) | `pdm publish --username __token__ --password $TOKEN` |

### Project Setup

```toml title="pyproject.toml"
[project]
name = "my-package"
version = "1.0.0"
requires-python = ">=3.11"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

### Workflow Example

```yaml title=".github/workflows/release.yml"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install PDM
        run: pipx install pdm

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pypi-token: ${{ secrets.PYPI_TOKEN }}
```

### PDM Features

- PEP 582 support (local packages)
- Fast dependency resolution
- Lock file support
- Plugin system

---

## Comparison

| Feature | uv | Poetry | PDM |
|---------|----|---------|----|
| Speed | Fastest | Good | Good |
| Lock file | Yes | Yes | Yes |
| OIDC support | Yes | No | No |
| Dependency groups | Yes | Yes | Yes |
| PEP 621 | Yes | Partial | Yes |
| Scripts | Yes | Yes | Yes |

### Recommendation

| Use Case | Recommended Tool |
|----------|------------------|
| New projects | uv |
| Existing Poetry projects | Poetry |
| PEP 582 workflow | PDM |
| Maximum speed | uv |
| Rich plugin ecosystem | Poetry |

---

## Tool Detection

releasio can auto-detect your build tool:

| Indicator | Detected Tool |
|-----------|---------------|
| `poetry.lock` | Poetry |
| `pdm.lock` | PDM |
| `uv.lock` | uv |
| `[tool.poetry]` in pyproject.toml | Poetry |
| Default | uv |

To override, set explicitly:

```toml title=".releasio.toml"
[publish]
tool = "poetry"  # Force poetry even if uv.lock exists
```

---

## Custom Build Commands

For advanced use cases, configure custom build hooks:

```toml title=".releasio.toml"
[hooks]
# Custom build command
build = "make build VERSION={version}"

# Or multiple commands
pre_release = [
    "npm run build",      # Build frontend
    "uv build",           # Build Python package
]
```

---

## Lock File Updates

releasio can update lock files when bumping versions:

```toml title=".releasio.toml"
[version]
update_lock_file = true
```

This runs:

| Tool | Command |
|------|---------|
| uv | `uv lock` |
| Poetry | `poetry lock --no-update` |
| PDM | `pdm lock` |

---

## Troubleshooting

### "Tool not found"

```
Error: uv command not found
```

**Solution**: Install the tool in your workflow:

=== "uv"

    ```yaml
    - uses: astral-sh/setup-uv@v4
    ```

=== "Poetry"

    ```yaml
    - run: pipx install poetry
    ```

=== "PDM"

    ```yaml
    - run: pipx install pdm
    ```

### "Build failed"

```
Error: Build command failed
```

**Checklist**:

- [ ] Valid `pyproject.toml`
- [ ] All dependencies installed
- [ ] Correct Python version
- [ ] Build backend installed

### "Publish authentication failed"

**For Poetry/PDM**: Use API token:

```yaml
pypi-token: ${{ secrets.PYPI_TOKEN }}
```

**For uv**: Use trusted publishing:

```yaml
permissions:
  id-token: write
```

---

## See Also

- [PyPI Publishing](pypi.md) - Complete publishing guide
- [Trusted Publishing](../github/trusted-publishing.md) - OIDC authentication
- [Configuration Reference](../user-guide/configuration/reference.md) - All options
