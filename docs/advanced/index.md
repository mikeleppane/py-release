# Advanced Features

:material-rocket-launch: Power-user features for complex release workflows.

---

## Overview

releasio includes advanced features for sophisticated release needs:

<div class="grid cards" markdown>

-   :material-source-branch:{ .lg .middle } **Multi-branch Releases**

    ---

    Different release channels from different branches

    [:octicons-arrow-right-24: Multi-branch](multi-branch.md)

-   :material-hook:{ .lg .middle } **Release Hooks**

    ---

    Run custom scripts at release lifecycle points

    [:octicons-arrow-right-24: Hooks](hooks.md)

-   :material-folder-multiple:{ .lg .middle } **Monorepo Support**

    ---

    Release multiple packages from one repository

    [:octicons-arrow-right-24: Monorepo](monorepo.md)

</div>

---

## Feature Summary

### Multi-branch Releases

Release different version types from different branches:

```
main     → 1.0.0          (stable)
beta     → 1.1.0-beta.1   (pre-release)
develop  → 1.1.0-alpha.1  (development)
```

### Release Hooks

Execute scripts at key lifecycle points:

```toml
[hooks]
pre_bump = ["pytest"]
post_release = ["./scripts/notify.sh {version}"]
```

### Monorepo Support

Manage multiple packages in a single repository:

```
my-monorepo/
├── packages/
│   ├── core/
│   ├── cli/
│   └── web/
└── .releasio.toml
```

---

## When to Use

| Feature | Use When |
|---------|----------|
| Multi-branch | Multiple release channels needed |
| Hooks | Custom CI/CD integration required |
| Monorepo | Multiple packages in one repo |

---

## See Also

- [Configuration Reference](../user-guide/configuration/reference.md) - All options
- [GitHub Actions](../github/actions/index.md) - CI/CD integration
- [Architecture](../architecture/index.md) - System design
