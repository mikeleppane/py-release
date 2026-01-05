# Action Reference

Complete reference for the releasio GitHub Action.

---

## Usage

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release-pr
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Inputs

### Required

| Input | Description |
|-------|-------------|
| `command` | Command to run (see below) |

### Authentication

| Input | Default | Description |
|-------|---------|-------------|
| `github-token` | `github.token` | GitHub token for API access |
| `pypi-token` | - | PyPI token (if not using trusted publishing) |

### Execution Control

| Input | Default | Description |
|-------|---------|-------------|
| `dry-run` | `false` | Run without making changes (release-pr, release) |
| `execute` | `false` | Apply changes (do-release, update) |
| `skip-publish` | `false` | Skip PyPI publishing |

### Version Options

| Input | Default | Description |
|-------|---------|-------------|
| `prerelease` | - | Pre-release type: `alpha`, `beta`, `rc` |
| `version-override` | - | Force specific version (e.g., `2.0.0`) |

### Environment

| Input | Default | Description |
|-------|---------|-------------|
| `python-version` | `3.11` | Python version: `3.11`, `3.12`, `3.13` |
| `working-directory` | `.` | Project directory |
| `releasio-version` | latest | Version to install (`source` for local) |

### PR Validation

| Input | Default | Description |
|-------|---------|-------------|
| `require-scope` | `false` | Require scope in PR title (check-pr only) |

---

## Commands

| Command | Description | Execution |
|---------|-------------|-----------|
| `check` | Preview release | Always dry-run |
| `release-pr` | Create/update release PR | Use `dry-run: 'false'` |
| `release` | Tag and publish | Use `dry-run: 'false'` |
| `do-release` | Complete workflow | Use `execute: 'true'` |
| `update` | Update version locally | Use `execute: 'true'` |
| `check-pr` | Validate PR title | N/A |
| `init` | Initialize config | N/A |

!!! note "Execution Modes"
    - `release-pr` and `release` use `dry-run` flag
    - `do-release` and `update` use `execute` flag

---

## Outputs

| Output | Description | Commands |
|--------|-------------|----------|
| `version` | Version released/to be released | All |
| `pr-number` | Created/updated PR number | `release-pr` |
| `pr-url` | Created/updated PR URL | `release-pr` |
| `release-url` | GitHub release URL | `release`, `do-release` |
| `tag` | Git tag created | `release`, `do-release` |
| `valid` | Whether PR title is valid | `check-pr` |

### Using Outputs

```yaml
- uses: mikeleppane/releasio@v2
  id: release
  with:
    command: release-pr
    github-token: ${{ secrets.GITHUB_TOKEN }}

- name: Comment on PR
  if: steps.release.outputs.pr-url
  run: echo "Created PR ${{ steps.release.outputs.pr-url }}"
```

---

## Examples

### Basic Release PR

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release-pr
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Full Release with Publishing

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release
    dry-run: 'false'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Do-Release (One Command)

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: do-release
    execute: 'true'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Pre-Release

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: do-release
    execute: 'true'
    prerelease: beta
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Force Version

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: do-release
    execute: 'true'
    version-override: '2.0.0'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Check PR Title

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: check-pr
    require-scope: 'true'
```

### Use Local Source

```yaml
- uses: ./  # Local action
  with:
    command: release-pr
    releasio-version: source  # Install from current repo
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Permissions

```yaml
permissions:
  contents: write       # Create tags, releases, push commits
  pull-requests: write  # Create and update PRs
  id-token: write       # PyPI trusted publishing (OIDC)
```

---

## Environment Variables

The action sets these for releasio:

| Variable | Value | Purpose |
|----------|-------|---------|
| `GITHUB_TOKEN` | Token input | API authentication |
| `PYPI_TOKEN` | Token input | PyPI publishing |
| `GITHUB_PR_TITLE` | PR title | check-pr validation |
| `NO_COLOR` | `1` | Disable color output |
