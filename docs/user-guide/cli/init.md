# releasio init

:material-cog: Initialize releasio configuration for your project.

---

## Usage

```bash
releasio init [PATH] [OPTIONS]
```

## Description

The `init` command creates a `.releasio.toml` configuration file with
sensible defaults that you can customize.

---

## Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `PATH` | Path | `.` | Project directory |

---

## Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |

---

## Example

```bash
releasio init
```

Creates `.releasio.toml`:

```toml title=".releasio.toml"
# releasio configuration
# See: https://mikeleppane.github.io/releasio/user-guide/configuration/

default_branch = "main"

[version]
tag_prefix = "v"

[changelog]
path = "CHANGELOG.md"

[commits]
types_minor = ["feat"]
types_patch = ["fix", "perf", "docs", "refactor", "style", "test", "build", "ci"]

[github]
release_pr_branch = "releasio/release"
release_pr_labels = ["release"]

[publish]
tool = "uv"
```

---

## When to Use

Use `init` when you want to:

- **Customize** version bumping rules
- **Change** changelog settings
- **Configure** GitHub release options
- **Set up** PyPI publishing preferences

!!! note "Zero Config"
    releasio works without any configuration. Only run `init` if you need
    to customize the defaults.

---

## Configuration Files

releasio supports three configuration locations:

| File | Priority | Notes |
|------|----------|-------|
| `.releasio.toml` | Highest | Created by `init` |
| `releasio.toml` | Medium | Visible config file |
| `pyproject.toml` | Lowest | Under `[tool.releasio]` |

---

## See Also

- [Configuration Overview](../configuration/index.md)
- [Full Reference](../configuration/reference.md)
- [Examples](../configuration/examples.md)
