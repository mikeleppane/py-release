# releasio release

:material-tag: Create a git tag, GitHub release, and publish to PyPI.

---

## Usage

```bash
releasio release [PATH] [OPTIONS]
```

## Description

The `release` command finalizes a release:

1. **Creates** a git tag (e.g., `v1.2.0`)
2. **Pushes** the tag to remote
3. **Creates** a GitHub release with changelog
4. **Publishes** to PyPI (if configured)

Run this **after** merging a release PR.

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
| `--verbose` | Show detailed output |

---

## Examples

### Preview (Dry-Run)

```bash
releasio release
```

### Execute Release

```bash
releasio release --execute
```

??? example "Example Output"

    ```
    ╭─ Releasing my-project v1.3.0 ────────────────────────────╮
    │                                                          │
    │  ✅ Created tag v1.3.0                                   │
    │  ✅ Pushed tag to origin                                 │
    │  ✅ Created GitHub release                               │
    │  ✅ Built package                                        │
    │  ✅ Published to PyPI                                    │
    │                                                          │
    │  🔗 https://github.com/user/repo/releases/tag/v1.3.0     │
    │  📦 https://pypi.org/project/my-project/1.3.0/           │
    │                                                          │
    ╰──────────────────────────────────────────────────────────╯
    ```

### Skip PyPI Publishing

```bash
releasio release --execute --skip-publish
```

---

## What Gets Released

| Action | Condition |
|--------|-----------|
| Git tag | Always |
| GitHub release | Always |
| PyPI publish | If `publish.enabled = true` |

---

## GitHub Actions

Trigger release after merging a release PR:

```yaml title=".github/workflows/release.yml"
jobs:
  release:
    # Run when release PR is merged (detected by commit message)
    if: startsWith(github.event.head_commit.message, 'chore(release):')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Trusted Publishing

releasio supports PyPI trusted publishing (OIDC) - no API tokens needed!

See [Trusted Publishing](../../github/trusted-publishing.md) for setup.

---

## See Also

- [release-pr](release-pr.md) - Create release PR
- [do-release](do-release.md) - Complete workflow
- [PyPI Publishing](../../publishing/pypi.md) - Publishing options
