# User Guide

Everything you need to know about using releasio effectively.

---

## Core Concepts

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **CLI Commands**

    ---

    Master all releasio commands from `check` to `do-release`

    [:octicons-arrow-right-24: CLI Reference](cli/index.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Customize every aspect of the release process

    [:octicons-arrow-right-24: Configuration](configuration/index.md)

-   :material-tag:{ .lg .middle } **Version Management**

    ---

    Semantic versioning, pre-releases, and version files

    [:octicons-arrow-right-24: Versioning](versioning/index.md)

-   :material-file-document:{ .lg .middle } **Changelog**

    ---

    Beautiful changelog generation with templates

    [:octicons-arrow-right-24: Changelog](changelog/index.md)

-   :material-format-list-checks:{ .lg .middle } **Commits**

    ---

    Conventional commits and custom parsers

    [:octicons-arrow-right-24: Commits](commits/index.md)

</div>

---

## Quick Reference

### Common Commands

```bash
# Preview release (safe, no changes)
releasio check

# Create/update release PR
releasio release-pr --execute

# Publish release
releasio release --execute

# Full release workflow
releasio do-release --execute
```

### Configuration Files

releasio looks for configuration in this order:

1. `.releasio.toml` (highest priority)
2. `releasio.toml`
3. `pyproject.toml` under `[tool.releasio]`

### Version Bumping

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor | `0.1.0 → 0.2.0` |
| `fix:` | Patch | `0.1.0 → 0.1.1` |
| `feat!:` | Major | `0.1.0 → 1.0.0` |
