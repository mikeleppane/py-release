# Semantic Versioning

:material-semantic-web: Understanding how releasio determines version bumps.

---

## What is Semantic Versioning?

[Semantic Versioning](https://semver.org/) (SemVer) uses a three-part version number:

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, no API changes
  │     └──────── New features, backwards compatible
  └────────────── Breaking changes
```

---

## Version Bump Rules

### Major Version (Breaking Changes)

Bump when you make incompatible API changes:

```bash
# Exclamation mark indicator
git commit -m "feat!: remove deprecated API"

# BREAKING CHANGE in body
git commit -m "refactor: update auth flow

BREAKING CHANGE: JWT tokens now required for all endpoints"
```

**Result**: `1.2.3` → `2.0.0`

### Minor Version (New Features)

Bump when you add functionality in a backwards-compatible manner:

```bash
git commit -m "feat: add user dashboard"
git commit -m "feat(api): add pagination support"
```

**Result**: `1.2.3` → `1.3.0`

### Patch Version (Bug Fixes)

Bump when you make backwards-compatible bug fixes:

```bash
git commit -m "fix: resolve login timeout"
git commit -m "docs: update installation guide"
git commit -m "perf: optimize database queries"
```

**Result**: `1.2.3` → `1.2.4`

---

## Commit Type Mapping

### Default Configuration

```toml title=".releasio.toml"
[commits]
# Minor version bump
types_minor = ["feat"]

# Patch version bump
types_patch = [
    "fix",
    "perf",
    "docs",
    "refactor",
    "style",
    "test",
    "build",
    "ci",
]
```

### Type Reference

| Type | Description | Default Bump |
|------|-------------|--------------|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation | Patch |
| `style` | Code style | Patch |
| `refactor` | Code refactoring | Patch |
| `perf` | Performance | Patch |
| `test` | Testing | Patch |
| `build` | Build system | Patch |
| `ci` | CI/CD | Patch |
| `chore` | Maintenance | No bump |

### Custom Mapping

Customize which types trigger which bumps:

```toml title=".releasio.toml"
[commits]
# Make performance improvements minor bumps
types_minor = ["feat", "perf"]

# Reduce patch bump triggers
types_patch = ["fix", "docs"]
```

---

## Breaking Change Detection

### Exclamation Mark

Add `!` after the type:

```bash
feat!: redesign user API
fix!: change error response format
refactor!: rename core modules
```

### BREAKING CHANGE Footer

Include in commit body:

```bash
git commit -m "feat: update authentication

BREAKING CHANGE: OAuth2 is now required. Legacy API key
authentication has been removed."
```

### Custom Pattern

Configure breaking change detection:

```toml title=".releasio.toml"
[commits]
breaking_patterns = [
    "BREAKING CHANGE:",
    "BREAKING:",
    "!:",
]
```

---

## Bump Priority

When multiple commit types exist, the **highest** bump wins:

```
Commits:
  fix: resolve bug          → patch
  feat: add new feature     → minor (highest)
  docs: update readme       → patch

Result: Minor bump (1.2.3 → 1.3.0)
```

If any commit is breaking:

```
Commits:
  fix: resolve bug          → patch
  feat!: breaking change    → major (highest)
  feat: new feature         → minor

Result: Major bump (1.2.3 → 2.0.0)
```

---

## Version Examples

### Scenario 1: Bug Fixes Only

```
Current: v1.2.3

Commits:
  fix: resolve login issue
  fix: handle null response

Next: v1.2.4 (patch)
```

### Scenario 2: New Features

```
Current: v1.2.3

Commits:
  feat: add dashboard
  fix: resolve bug
  docs: update guide

Next: v1.3.0 (minor - feat is highest)
```

### Scenario 3: Breaking Change

```
Current: v1.2.3

Commits:
  feat!: redesign API
  feat: add new endpoint
  fix: resolve bug

Next: v2.0.0 (major - breaking change)
```

### Scenario 4: Pre-1.0 Semantics

For versions before 1.0.0, breaking changes bump minor:

```
Current: v0.2.3

Commits:
  feat!: breaking change

Next: v0.3.0 (minor, not major)
```

!!! info "Pre-1.0 Versions"
    SemVer treats 0.x.x versions as development. Breaking changes
    are expected and don't require major bumps.

---

## Zero Version Handling

### Initial Release

If no tags exist:

```toml title=".releasio.toml"
[version]
initial_version = "0.1.0"
```

### First Stable Release

Force 1.0.0 when ready:

```bash
releasio update --version 1.0.0 --execute
```

---

## Version Overrides

### Force Specific Version

```bash
# CLI
releasio update --version 2.0.0 --execute

# GitHub Action
- uses: mikeleppane/releasio@v2
  with:
    command: do-release
    version-override: '2.0.0'
    execute: 'true'
```

### Skip Version Bump

If no releasable commits exist:

```
Current: v1.2.3

Commits:
  chore: update dependencies
  ci: fix workflow

Next: No release (no feat/fix commits)
```

---

## Best Practices

### Do

- [x] Use `feat` for all new functionality
- [x] Use `fix` for bug fixes
- [x] Mark breaking changes with `!` or `BREAKING CHANGE`
- [x] Start at 0.1.0 for new projects
- [x] Release 1.0.0 when API is stable

### Don't

- [ ] Manually edit version numbers
- [ ] Skip breaking change markers
- [ ] Mix multiple changes in one commit
- [ ] Use vague commit types

---

## See Also

- [Conventional Commits](../commits/format.md) - Commit format specification
- [Pre-releases](pre-releases.md) - Alpha, beta, RC versions
- [Version Files](version-files.md) - Managing version files
