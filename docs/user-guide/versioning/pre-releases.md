# Pre-releases

:material-alpha: Create alpha, beta, and release candidate versions.

---

## Overview

Pre-releases let you publish unstable versions for testing before a stable release:

```
1.0.0-alpha.1  →  1.0.0-alpha.2  →  1.0.0-beta.1  →  1.0.0-rc.1  →  1.0.0
```

---

## Pre-release Types

| Type | Use Case | Example |
|------|----------|---------|
| `alpha` | Early development, unstable | `1.0.0-alpha.1` |
| `beta` | Feature complete, testing | `1.0.0-beta.1` |
| `rc` | Release candidate, final testing | `1.0.0-rc.1` |
| `dev` | Development builds | `1.0.0-dev.1` |

---

## Creating Pre-releases

### CLI

```bash
# Alpha release
releasio do-release --prerelease alpha --execute

# Beta release
releasio do-release --prerelease beta --execute

# Release candidate
releasio do-release --prerelease rc --execute
```

### GitHub Action

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: do-release
    execute: 'true'
    prerelease: beta
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Version Progression

### New Pre-release Series

Starting a new pre-release from stable:

```
Current: 1.0.0
Command: releasio do-release --prerelease alpha --execute

# With feat commit → 1.1.0-alpha.1
# With fix commit  → 1.0.1-alpha.1
```

### Incrementing Pre-releases

Subsequent pre-releases increment the pre-release number:

```
Current: 1.1.0-alpha.1
Command: releasio do-release --prerelease alpha --execute
Result:  1.1.0-alpha.2
```

### Transitioning Pre-release Types

Move from alpha to beta to rc:

```
1.0.0-alpha.3
  ↓ (--prerelease beta)
1.0.0-beta.1
  ↓ (--prerelease rc)
1.0.0-rc.1
  ↓ (no --prerelease flag)
1.0.0
```

---

## Multi-Branch Pre-releases

Configure different branches for different pre-release types:

```toml title=".releasio.toml"
default_branch = "main"

[branches.main]
match = "main"
prerelease = false

[branches.beta]
match = "beta"
prerelease = true
prerelease_token = "beta"

[branches.develop]
match = "develop"
prerelease = true
prerelease_token = "alpha"
```

This produces:

| Branch | Version Format |
|--------|----------------|
| `main` | `1.0.0` |
| `beta` | `1.0.0-beta.1` |
| `develop` | `1.0.0-alpha.1` |

---

## GitHub Releases

Pre-releases are marked as such on GitHub:

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release
    prerelease: beta
```

This creates a GitHub release marked as "Pre-release":

- Not shown as "Latest release"
- Displayed with a badge
- Users must opt-in to install

---

## PyPI Pre-releases

Pre-release versions on PyPI work automatically:

```
1.0.0-beta.1  →  PyPI shows as pre-release
```

Users must explicitly opt-in to install:

```bash
# Normal install (skips pre-releases)
pip install my-package

# Include pre-releases
pip install --pre my-package

# Specific pre-release
pip install my-package==1.0.0b1
```

!!! note "PyPI Version Format"
    PyPI uses PEP 440 format: `1.0.0b1` instead of `1.0.0-beta.1`.
    releasio automatically handles this conversion.

---

## Workflow Examples

### Dedicated Pre-release Workflow

```yaml title=".github/workflows/prerelease.yml"
name: Pre-release

on:
  push:
    branches: [develop]

permissions:
  contents: write
  pull-requests: write
  id-token: write

jobs:
  prerelease:
    if: "!startsWith(github.event.head_commit.message, 'chore(release):')"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: do-release
          execute: 'true'
          prerelease: alpha
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Manual Pre-release Trigger

```yaml title=".github/workflows/prerelease.yml"
name: Pre-release

on:
  workflow_dispatch:
    inputs:
      prerelease-type:
        description: 'Pre-release type'
        required: true
        type: choice
        options:
          - alpha
          - beta
          - rc

jobs:
  prerelease:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: do-release
          execute: 'true'
          prerelease: ${{ inputs.prerelease-type }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Changelog for Pre-releases

Pre-releases include changelog entries:

```markdown
## [1.0.0-beta.1] - 2024-01-15

### Features
- Add new dashboard (#42)

### Bug Fixes
- Resolve login timeout (#43)
```

Configure to group pre-release changes:

```toml title=".releasio.toml"
[changelog]
# Include pre-release entries
include_prereleases = true
```

---

## Best Practices

### Release Progression

```
Development → Alpha → Beta → RC → Stable
    ↓           ↓       ↓      ↓      ↓
  develop    alpha    beta    rc    main
```

### When to Use Each Type

| Type | Stage | Stability | Who Should Use |
|------|-------|-----------|----------------|
| Alpha | Early | Unstable | Developers |
| Beta | Testing | Mostly stable | Early adopters |
| RC | Final | Stable | All testers |
| Stable | Released | Production | Everyone |

### Naming Conventions

```
✓ 1.0.0-alpha.1    # Preferred
✓ 1.0.0-beta.1
✓ 1.0.0-rc.1

✗ 1.0.0-a1         # Less clear
✗ 1.0.0alpha1      # Non-standard
✗ 1.0.0-preview    # Not recognized
```

---

## Troubleshooting

### Pre-release Not Detected

```
Error: Could not determine pre-release type
```

**Solution**: Ensure correct tag format:

```
v1.0.0-beta.1  ✓
v1.0.0beta1    ✗
```

### Wrong Pre-release Number

If pre-release numbers aren't incrementing:

1. Check existing tags: `git tag -l "v1.0.0-*"`
2. Ensure tags are pushed: `git push --tags`
3. Verify tag format matches config

---

## See Also

- [Semantic Versioning](semver.md) - Version bump rules
- [Multi-branch Releases](../../advanced/multi-branch.md) - Branch strategies
- [Configuration Reference](../configuration/reference.md) - All options
