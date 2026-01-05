# Your First Release

A complete walkthrough of releasing your first version with releasio.

## Overview

In this guide, you'll:

1. :material-cog: Set up your project
2. :material-git: Make conventional commits
3. :material-eye: Preview the release
4. :material-pull-request: Create a release PR
5. :material-tag: Publish to PyPI

---

## Step 1: Project Setup

### Ensure Your `pyproject.toml` is Ready

releasio reads project metadata from `pyproject.toml`:

```toml
[project]
name = "my-awesome-project"
version = "0.1.0"
description = "An awesome Python project"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

!!! info "Version Location"
    releasio automatically updates the `version` field in `pyproject.toml`.
    No additional configuration needed.

### Initialize Configuration (Optional)

Create a configuration file for customization:

```bash
releasio init
```

This creates `.releasio.toml` with default settings you can customize.

---

## Step 2: Make Commits

Use [conventional commits](../user-guide/commits/format.md) for automatic version detection:

```bash
# Add a new feature (bumps minor version)
git commit -m "feat: add user registration endpoint"

# Fix a bug (bumps patch version)
git commit -m "fix: validate email format correctly"

# Add documentation (bumps patch version)
git commit -m "docs: add API usage examples"

# Breaking change (bumps major version)
git commit -m "feat!: change authentication flow

BREAKING CHANGE: JWT tokens now required for all endpoints"
```

### Commit Type Reference

| Type | Version Bump | Use When |
|------|--------------|----------|
| `feat` | Minor | Adding new functionality |
| `fix` | Patch | Fixing bugs |
| `docs` | Patch | Documentation changes |
| `perf` | Patch | Performance improvements |
| `refactor` | Patch | Code refactoring |
| `test` | Patch | Adding tests |
| `chore` | Patch | Maintenance tasks |
| `feat!` | **Major** | Breaking changes |

---

## Step 3: Preview Your Release

Before making any changes, preview what will happen:

```bash
releasio check
```

??? example "Example Output"

    ```
    ╭─ Release Preview ────────────────────────────────────────╮
    │                                                          │
    │  📦 Project: my-awesome-project                          │
    │  📌 Current: v0.1.0                                      │
    │  🚀 Next:    v0.2.0 (minor bump)                         │
    │                                                          │
    │  📝 Commits since v0.1.0:                                │
    │                                                          │
    │  ✨ Features:                                            │
    │    • feat: add user registration endpoint                │
    │                                                          │
    │  🐛 Bug Fixes:                                           │
    │    • fix: validate email format correctly                │
    │                                                          │
    │  📚 Documentation:                                       │
    │    • docs: add API usage examples                        │
    │                                                          │
    ╰──────────────────────────────────────────────────────────╯
    ```

This command is always safe - it never modifies any files.

---

## Step 4: Create the Release PR

### Option A: Local Release PR

Create a release PR from your local machine:

```bash
releasio release-pr --execute
```

This will:

- [x] Create branch `releasio/release`
- [x] Update version in `pyproject.toml`
- [x] Generate/update `CHANGELOG.md`
- [x] Commit changes
- [x] Push branch
- [x] Create pull request

### Option B: GitHub Actions (Recommended)

Set up automatic release PR creation:

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
  release-pr:
    if: "!startsWith(github.event.head_commit.message, 'chore(release):')"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: mikeleppane/releasio@v2
        with:
          command: release-pr
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

Now every push to `main` automatically creates/updates a release PR!

---

## Step 5: Review and Merge

### Review the PR

The release PR includes:

- **Version bump** - Updated `pyproject.toml`
- **Changelog** - New entries in `CHANGELOG.md`
- **Summary** - List of changes in PR description

??? example "Example PR Description"

    ```markdown
    ## 🚀 Release v0.2.0

    ### ✨ Features
    - Add user registration endpoint (#42)

    ### 🐛 Bug Fixes
    - Validate email format correctly (#43)

    ### 📚 Documentation
    - Add API usage examples (#44)

    ---
    *This PR was automatically created by releasio*
    ```

### Merge the PR

Once you're happy with the changes, merge the PR. This triggers the release!

---

## Step 6: Automatic Release

When the release PR is merged, the release workflow runs:

```yaml title=".github/workflows/release.yml" hl_lines="3-5"
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

This automatically:

- [x] Creates git tag `v0.2.0`
- [x] Creates GitHub release with changelog
- [x] Publishes to PyPI (using trusted publishing)

---

## :tada: Congratulations!

You've completed your first release with releasio!

### What's Next?

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Customize version bumping, changelog format, and more

    [:octicons-arrow-right-24: Configuration guide](../user-guide/configuration/index.md)

-   :material-github:{ .lg .middle } **GitHub Actions**

    ---

    Learn about advanced workflow configurations

    [:octicons-arrow-right-24: Actions guide](../github/actions/index.md)

-   :material-shield-lock:{ .lg .middle } **Trusted Publishing**

    ---

    Set up PyPI publishing without API tokens

    [:octicons-arrow-right-24: Trusted publishing](../github/trusted-publishing.md)

</div>
