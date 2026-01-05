# releasio check-pr

:material-check-circle: Validate that a PR title follows conventional commit format.

---

## Usage

```bash
releasio check-pr [OPTIONS]
```

## Description

The `check-pr` command validates PR titles against the conventional commit format.
Use it in CI to enforce commit conventions.

---

## Options

| Option | Description |
|--------|-------------|
| `--require-scope` | Require scope (e.g., `feat(api):` not just `feat:`) |
| `--help` | Show help message |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_PR_TITLE` | The PR title to validate |

In GitHub Actions, this is automatically set by the action.

---

## Examples

### Basic Validation

```bash
GITHUB_PR_TITLE="feat: add user authentication" releasio check-pr
```

### Require Scope

```bash
GITHUB_PR_TITLE="feat(auth): add user authentication" releasio check-pr --require-scope
```

---

## Valid PR Titles

| Title | Valid | Notes |
|-------|-------|-------|
| `feat: add feature` | :material-check: | Standard feature |
| `fix: resolve bug` | :material-check: | Bug fix |
| `feat(api): add endpoint` | :material-check: | With scope |
| `feat!: breaking change` | :material-check: | Breaking change |
| `add feature` | :material-close: | Missing type |
| `Feature: add feature` | :material-close: | Capitalized type |

---

## GitHub Actions

Validate PR titles in CI:

```yaml title=".github/workflows/pr.yml"
name: PR Validation

on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  check-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: mikeleppane/releasio@v2
        with:
          command: check-pr
          # require-scope: 'true'  # Optional
```

!!! tip "Squash Merging"
    If you squash merge PRs, the PR title becomes the commit message.
    Validating PR titles ensures proper version bumps.

---

## See Also

- [Conventional Commits](../commits/format.md) - Commit format reference
