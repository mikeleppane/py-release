# GitHub Actions

Automate your release workflow with the releasio GitHub Action.

---

## Overview

The releasio action provides:

- :material-package: Automatic Python & tool installation
- :material-git: Git configuration for commits
- :material-shield-lock: Trusted publishing support (OIDC)
- :material-cog: Full CLI access

---

## Quick Links

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Minimal Setup**

    ---

    Get started with a simple two-job workflow

    [:octicons-arrow-right-24: Minimal](minimal.md)

-   :material-tune:{ .lg .middle } **Full Workflow**

    ---

    Extended workflow with manual triggers

    [:octicons-arrow-right-24: Full Workflow](full-workflow.md)

-   :material-book-open:{ .lg .middle } **Action Reference**

    ---

    All inputs, outputs, and options

    [:octicons-arrow-right-24: Reference](reference.md)

</div>

---

## Basic Usage

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release-pr
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Commands

| Command | Description |
|---------|-------------|
| `check` | Preview release (dry-run) |
| `release-pr` | Create/update release PR |
| `release` | Tag and publish |
| `do-release` | Complete workflow |
| `check-pr` | Validate PR title |

---

## Permissions Required

```yaml
permissions:
  contents: write       # Create tags and releases
  pull-requests: write  # Create and update PRs
  id-token: write       # PyPI trusted publishing (OIDC)
```

---

## Repository Settings

Enable these settings for full functionality:

1. **Settings** → **Actions** → **General**
2. ✅ "Allow GitHub Actions to create and approve pull requests"
