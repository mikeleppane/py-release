# releasio do-release

:material-rocket-launch: Complete release workflow in one command.

---

## Usage

```bash
releasio do-release [PATH] [OPTIONS]
```

## Description

The `do-release` command combines the entire release process:

1. **Updates** version and changelog
2. **Commits** the changes
3. **Creates** and pushes a git tag
4. **Publishes** to PyPI

Perfect for projects that don't need PR review.

---

## Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `PATH` | Path | `.` | Project directory path |

---

## Options

| Option | Description |
|--------|-------------|
| `--execute` | Actually release (default: dry-run) |
| `--skip-publish` | Skip PyPI publishing |
| `--version` | Override calculated version |
| `--prerelease` | Create pre-release (alpha, beta, rc) |
| `--verbose` | Show detailed output |

---

## Examples

### Preview (Dry-Run)

```bash
releasio do-release
```

### Execute Full Release

```bash
releasio do-release --execute
```

??? example "Example Output"

    ```
    ╭─ Full Release: my-project ───────────────────────────────╮
    │                                                          │
    │  📦 Version: 1.2.0 → 1.3.0                               │
    │                                                          │
    │  ✅ Updated pyproject.toml                               │
    │  ✅ Updated CHANGELOG.md                                 │
    │  ✅ Committed: chore(release): prepare v1.3.0            │
    │  ✅ Created tag v1.3.0                                   │
    │  ✅ Pushed to origin                                     │
    │  ✅ Created GitHub release                               │
    │  ✅ Published to PyPI                                    │
    │                                                          │
    │  🎉 Release complete!                                    │
    │                                                          │
    ╰──────────────────────────────────────────────────────────╯
    ```

### Force Specific Version

```bash
releasio do-release --execute --version 2.0.0
```

### Create Pre-Release

```bash
releasio do-release --execute --prerelease beta
```

Creates version like `1.3.0-beta.1`.

### Skip Publishing

```bash
releasio do-release --execute --skip-publish
```

---

## Workflow Comparison

| Approach | Commands | PR Review |
|----------|----------|-----------|
| **Release PR** | `release-pr` → merge → `release` | :material-check: Yes |
| **Do Release** | `do-release` | :material-close: No |

!!! tip "When to Use"
    Use `do-release` for:

    - Personal projects
    - CI/CD pipelines with existing review gates
    - Rapid iteration phases

    Use `release-pr` for:

    - Team projects
    - When changelog review is important
    - When PR checks need to run

---

## See Also

- [release-pr](release-pr.md) - PR-based workflow
- [release](release.md) - Just tag and publish
