# Configuration

Customize releasio to fit your project's workflow.

---

## Zero Configuration

releasio works out of the box with sensible defaults:

```bash
# Just works!
releasio check
```

Only create configuration when you need to customize behavior.

---

## Configuration Files

releasio looks for configuration in this order:

| File | Priority | Format |
|------|----------|--------|
| `.releasio.toml` | Highest | Top-level keys |
| `releasio.toml` | Medium | Top-level keys |
| `pyproject.toml` | Lowest | Under `[tool.releasio]` |

=== ".releasio.toml"

    ```toml
    default_branch = "main"

    [version]
    tag_prefix = "v"

    [changelog]
    path = "CHANGELOG.md"
    ```

=== "pyproject.toml"

    ```toml
    [tool.releasio]
    default_branch = "main"

    [tool.releasio.version]
    tag_prefix = "v"

    [tool.releasio.changelog]
    path = "CHANGELOG.md"
    ```

!!! note "Format Difference"
    Standalone files use **top-level keys**.
    `pyproject.toml` uses the `[tool.releasio]` prefix.

---

## Quick Reference

<div class="grid cards" markdown>

-   :material-file-document:{ .lg .middle } **Configuration Files**

    ---

    File formats and precedence

    [:octicons-arrow-right-24: Files](files.md)

-   :material-book-open-variant:{ .lg .middle } **Full Reference**

    ---

    Complete configuration options

    [:octicons-arrow-right-24: Reference](reference.md)

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    Common configuration patterns

    [:octicons-arrow-right-24: Examples](examples.md)

</div>

---

## Configuration Sections

| Section | Purpose |
|---------|---------|
| [`[version]`](reference.md#version) | Version management |
| [`[changelog]`](reference.md#changelog) | Changelog generation |
| [`[commits]`](reference.md#commits) | Commit parsing rules |
| [`[github]`](reference.md#github) | GitHub integration |
| [`[publish]`](reference.md#publish) | PyPI publishing |
| [`[hooks]`](reference.md#hooks) | Release lifecycle hooks |
| [`[security]`](reference.md#security) | Security advisories |
| [`[branches]`](reference.md#branches) | Multi-channel releases |

---

## Initialize Configuration

Generate a configuration file with defaults:

```bash
releasio init
```

This creates `.releasio.toml` with common options you can customize.
