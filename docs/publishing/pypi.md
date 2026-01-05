# PyPI Publishing

:material-package-up: Publish your Python packages to the Python Package Index.

---

## Overview

releasio handles the complete PyPI publishing workflow:

1. Build source distribution and wheel
2. Validate package metadata
3. Authenticate with PyPI
4. Upload to registry
5. Verify successful publication

---

## Prerequisites

### Package Structure

Your project needs a valid `pyproject.toml`:

```toml title="pyproject.toml"
[project]
name = "my-package"
version = "1.0.0"
description = "My awesome package"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### PyPI Account

1. Create account at [pypi.org](https://pypi.org/account/register/)
2. Verify your email
3. Set up [trusted publishing](../github/trusted-publishing.md) or create API token

---

## Authentication

### Trusted Publishing (Recommended)

Configure on PyPI:

1. Go to **Manage** → **Publishing**
2. Add trusted publisher:
   - Owner: `your-username`
   - Repository: `your-repo`
   - Workflow: `release.yml`

Configure releasio:

```toml title=".releasio.toml"
[publish]
trusted_publishing = true
```

Set workflow permissions:

```yaml
permissions:
  id-token: write
```

### API Token

Create token on PyPI:

1. Go to **Account settings** → **API tokens**
2. Create token with **project scope**
3. Add as GitHub secret `PYPI_TOKEN`

Use in workflow:

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release
    dry-run: 'false'
    pypi-token: ${{ secrets.PYPI_TOKEN }}
```

---

## Configuration

### Basic Setup

```toml title=".releasio.toml"
[publish]
tool = "uv"
trusted_publishing = true
```

### All Options

```toml title=".releasio.toml"
[publish]
# Build and publish tool
tool = "uv"  # or "poetry", "pdm"

# Enable PyPI publishing
enabled = true

# Use OIDC trusted publishing
trusted_publishing = true

# Validate package before upload
validate_before_publish = true

# Target registry
registry = "https://upload.pypi.org/legacy/"
```

---

## Workflow Examples

### Standard Release

```yaml title=".github/workflows/release.yml"
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write
  id-token: write

jobs:
  release:
    if: startsWith(github.event.head_commit.message, 'chore(release):')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### With Build Verification

```yaml
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

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build and verify
        run: |
          uv build
          uv run twine check dist/*

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## TestPyPI

Test your publishing workflow before going live.

### Setup TestPyPI

1. Create account at [test.pypi.org](https://test.pypi.org)
2. Configure trusted publishing (same as PyPI)

### Configuration

```toml title=".releasio.toml"
[publish]
registry = "https://test.pypi.org/legacy/"
trusted_publishing = true
```

### Workflow

```yaml title=".github/workflows/test-publish.yml"
name: Test Publish

on:
  push:
    branches: [develop]

permissions:
  id-token: write

jobs:
  test-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: do-release
          execute: 'true'
          prerelease: dev
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Installing from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ my-package
```

---

## Package Validation

releasio validates packages before upload:

### Checks Performed

| Check | Description |
|-------|-------------|
| Metadata | Required fields present |
| README | Renders correctly |
| License | Valid license specified |
| Version | Follows PEP 440 |
| Wheel | Platform tags correct |

### Enable Validation

```toml title=".releasio.toml"
[publish]
validate_before_publish = true
```

### Manual Validation

```bash
# Build package
uv build

# Check with twine
uv run twine check dist/*
```

---

## Troubleshooting

### "Package already exists"

```
HTTPError: 400 Bad Request: File already exists
```

**Cause**: Version already published to PyPI.

**Solution**: PyPI doesn't allow re-uploading. Bump version and release again.

### "Invalid distribution"

```
InvalidDistribution: Invalid distribution
```

**Causes**:

1. Malformed `pyproject.toml`
2. Missing required metadata
3. Invalid version format

**Solution**: Validate locally:

```bash
uv build
uv run twine check dist/*
```

### "Authentication failed"

```
HTTPError: 403 Forbidden: Invalid credentials
```

**For trusted publishing**:

- Verify `id-token: write` permission
- Check publisher config on PyPI matches exactly

**For API token**:

- Verify token is valid and not expired
- Check token scope includes your project

### "Rate limited"

```
HTTPError: 429 Too Many Requests
```

**Solution**: Wait and retry. Consider:

- Using TestPyPI for testing
- Batching releases less frequently

---

## Best Practices

### Security

- [x] Use trusted publishing over API tokens
- [x] Use GitHub environments for production
- [x] Enable two-factor authentication on PyPI
- [x] Review package contents before release

### Quality

- [x] Test on TestPyPI first
- [x] Validate package before upload
- [x] Include comprehensive README
- [x] Add proper classifiers

### Process

- [x] Use release PRs for review
- [x] Tag releases in Git
- [x] Keep CHANGELOG updated
- [x] Announce major releases

---

## See Also

- [Trusted Publishing](../github/trusted-publishing.md) - OIDC authentication
- [Build Tools](build-tools.md) - Configure uv, poetry, pdm
- [Full Workflow](../github/actions/full-workflow.md) - Complete CI/CD
