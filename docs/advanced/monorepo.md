# Monorepo Support

:material-folder-multiple: Release multiple packages from one repository.

---

## Overview

releasio supports monorepo layouts where multiple Python packages live in a single repository:

```
my-monorepo/
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   └── src/
│   ├── cli/
│   │   ├── pyproject.toml
│   │   └── src/
│   └── web/
│       ├── pyproject.toml
│       └── src/
├── pyproject.toml  # Root config
└── .releasio.toml
```

---

## Configuration

### Root Configuration

```toml title=".releasio.toml"
[packages]
paths = [
    "packages/core",
    "packages/cli",
    "packages/web",
]

# Shared settings
default_branch = "main"

[version]
tag_prefix = "v"
```

### Package-specific Settings

Each package can have its own configuration:

```toml title="packages/core/.releasio.toml"
[version]
tag_prefix = "core-v"

[changelog]
path = "CHANGELOG.md"
```

```toml title="packages/cli/.releasio.toml"
[version]
tag_prefix = "cli-v"

[changelog]
path = "CHANGELOG.md"
```

---

## Versioning Strategies

### Independent Versioning

Each package has its own version:

```
packages/core    → core-v1.0.0, core-v1.1.0
packages/cli     → cli-v2.0.0, cli-v2.0.1
packages/web     → web-v0.5.0, web-v0.6.0
```

Configuration:

```toml title=".releasio.toml"
[packages]
versioning = "independent"
```

### Synchronized Versioning

All packages share the same version:

```
packages/core    → v1.0.0
packages/cli     → v1.0.0
packages/web     → v1.0.0
```

Configuration:

```toml title=".releasio.toml"
[packages]
versioning = "synchronized"
```

---

## Commands

### Check All Packages

```bash
releasio check
```

Output:
```
📦 core (packages/core)
   Current: core-v1.0.0
   Next:    core-v1.1.0 (minor)
   Changes: 3 commits

📦 cli (packages/cli)
   Current: cli-v2.0.0
   Next:    No changes

📦 web (packages/web)
   Current: web-v0.5.0
   Next:    web-v0.6.0 (minor)
   Changes: 2 commits
```

### Release Specific Package

```bash
releasio release --package core
```

### Release All Changed

```bash
releasio release --all
```

---

## Workflow Examples

### Independent Releases

```yaml title=".github/workflows/release.yml"
name: Release

on:
  push:
    branches: [main]
    paths:
      - 'packages/**'

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.changes.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect changed packages
        id: changes
        run: |
          # Find packages with changes since last tag
          packages=$(releasio check --json | jq -r '.packages | map(select(.has_changes)) | .[].name')
          echo "packages=$packages" >> $GITHUB_OUTPUT

  release:
    needs: detect-changes
    if: needs.detect-changes.outputs.packages != ''
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJson(needs.detect-changes.outputs.packages) }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          working-directory: packages/${{ matrix.package }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Synchronized Releases

```yaml title=".github/workflows/release.yml"
name: Release All

on:
  push:
    branches: [main]

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
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Tag Formats

### Independent Tags

```toml title=".releasio.toml"
[packages.core]
path = "packages/core"
tag_prefix = "core-v"

[packages.cli]
path = "packages/cli"
tag_prefix = "cli-v"
```

Results in:
```
core-v1.0.0
core-v1.1.0
cli-v2.0.0
cli-v2.0.1
```

### Unified Tags

```toml title=".releasio.toml"
[packages]
versioning = "synchronized"

[version]
tag_prefix = "v"
```

Results in:
```
v1.0.0  # All packages at 1.0.0
v1.1.0  # All packages at 1.1.0
```

---

## Changelog per Package

Each package maintains its own changelog:

```
packages/
├── core/
│   ├── CHANGELOG.md
│   └── pyproject.toml
├── cli/
│   ├── CHANGELOG.md
│   └── pyproject.toml
```

Configuration:

```toml title="packages/core/.releasio.toml"
[changelog]
path = "CHANGELOG.md"  # Relative to package root
```

---

## Dependencies Between Packages

### Internal Dependencies

When `cli` depends on `core`:

```toml title="packages/cli/pyproject.toml"
[project.dependencies]
my-core = ">=1.0.0"
```

### Synchronized Updates

```toml title=".releasio.toml"
[packages]
update_internal_dependencies = true

[packages.cli]
depends_on = ["core"]
```

When `core` releases, `cli` gets its dependency updated.

---

## Publishing

### Publish All

```bash
releasio release --all
```

### Publish Specific

```bash
releasio release --package core
releasio release --package cli
```

### Skip Publishing

```toml title="packages/internal/.releasio.toml"
[publish]
enabled = false  # Internal package, don't publish
```

---

## Best Practices

### Directory Structure

```
monorepo/
├── packages/           # All packages here
│   ├── core/
│   ├── cli/
│   └── web/
├── .releasio.toml      # Root config
├── .github/
│   └── workflows/
│       └── release.yml
└── README.md
```

### Naming Conventions

```
# Package names
my-project-core
my-project-cli
my-project-web

# Tag prefixes
core-v
cli-v
web-v
```

### Commit Scopes

Use scopes to identify package:

```bash
feat(core): add new feature
fix(cli): resolve issue
docs(web): update readme
```

---

## Troubleshooting

### Package Not Detected

```
Warning: No packages found
```

**Solution**: Verify paths in config:

```toml
[packages]
paths = ["packages/*"]  # Glob pattern
```

### Wrong Package Tagged

```
Error: Tag core-v1.0.0 created for wrong package
```

**Solution**: Ensure unique tag prefixes:

```toml
[packages.core]
tag_prefix = "core-v"

[packages.cli]
tag_prefix = "cli-v"  # Must be different
```

### Dependency Version Mismatch

When internal dependencies get out of sync:

```bash
# Update all internal deps
releasio update --all --sync-deps
```

---

## Limitations

Current monorepo support:

- [x] Multiple packages in one repo
- [x] Independent or synchronized versioning
- [x] Per-package configuration
- [x] Per-package changelogs
- [ ] Automatic dependency graph detection
- [ ] Transitive dependency updates

---

## See Also

- [Configuration Reference](../user-guide/configuration/reference.md) - All options
- [Multi-branch Releases](multi-branch.md) - Release channels
- [GitHub Actions](../github/actions/index.md) - CI/CD setup
