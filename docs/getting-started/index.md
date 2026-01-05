# Getting Started

Welcome to releasio! This guide will help you set up automated releases for your Python project.

## What is releasio?

releasio is a release automation tool for Python projects that:

- **Analyzes commits** to determine version bumps automatically
- **Generates changelogs** from your commit history
- **Creates release PRs** with version updates ready to merge
- **Publishes to PyPI** using trusted publishing (no tokens needed!)

## Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** installed
- **Git** repository for your project
- **pyproject.toml** with your project metadata
- **git-cliff** for changelog generation

## Quick Links

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install releasio and its dependencies

    [:octicons-arrow-right-24: Install now](installation.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running in 5 minutes

    [:octicons-arrow-right-24: Quick start](quickstart.md)

-   :material-tag:{ .lg .middle } **First Release**

    ---

    Complete walkthrough of your first release

    [:octicons-arrow-right-24: First release](first-release.md)

</div>

## Next Steps

After completing the getting started guide, explore:

- [CLI Commands](../user-guide/cli/index.md) - All available commands
- [Configuration](../user-guide/configuration/index.md) - Customize releasio
- [GitHub Actions](../github/actions/index.md) - Automate your releases
