# Changelog Templates

:material-palette: Customize your changelog format.

---

## Overview

releasio provides flexible template options for changelog entries:

- **Section headers** - Group commits by type
- **Commit templates** - Format individual entries
- **Custom sections** - Add your own groupings

---

## Commit Templates

### Basic Template

```toml title=".releasio.toml"
[changelog]
commit_template = "- {description}"
```

Output:
```markdown
- Add user dashboard
```

### With Issue Links

```toml title=".releasio.toml"
[changelog]
commit_template = "- {description} (#{pr_number})"
```

Output:
```markdown
- Add user dashboard (#42)
```

### With Author

```toml title=".releasio.toml"
[changelog]
commit_template = "- {description} by @{author}"
show_authors = true
```

Output:
```markdown
- Add user dashboard by @username
```

### With Commit Hash

```toml title=".releasio.toml"
[changelog]
commit_template = "- {description} ([{short_hash}]({commit_url}))"
show_commit_hash = true
```

Output:
```markdown
- Add user dashboard ([abc123](https://github.com/user/repo/commit/abc123def))
```

### Full Template

```toml title=".releasio.toml"
[changelog]
commit_template = "- {description} ([{short_hash}]({commit_url})) by @{author}"
show_authors = true
show_commit_hash = true
```

Output:
```markdown
- Add user dashboard ([abc123](https://github.com/user/repo/commit/abc123def)) by @username
```

---

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{description}` | Commit description | `Add user dashboard` |
| `{type}` | Commit type | `feat` |
| `{scope}` | Commit scope | `api` |
| `{hash}` | Full commit hash | `abc123def456...` |
| `{short_hash}` | Short hash (7 chars) | `abc123d` |
| `{author}` | Author username | `username` |
| `{author_email}` | Author email | `user@example.com` |
| `{pr_number}` | PR number (if available) | `42` |
| `{commit_url}` | Full commit URL | `https://github.com/...` |
| `{date}` | Commit date | `2024-01-15` |

---

## Section Headers

### Default Headers

```toml title=".releasio.toml"
[changelog.section_headers]
breaking = "Breaking Changes"
feat = "Features"
fix = "Bug Fixes"
docs = "Documentation"
perf = "Performance"
refactor = "Refactoring"
test = "Testing"
build = "Build"
ci = "CI/CD"
chore = "Chores"
```

### With Emojis

```toml title=".releasio.toml"
[changelog.section_headers]
breaking = "💥 Breaking Changes"
feat = "✨ Features"
fix = "🐛 Bug Fixes"
docs = "📚 Documentation"
perf = "⚡ Performance"
refactor = "♻️ Refactoring"
test = "🧪 Testing"
build = "📦 Build"
ci = "🔧 CI/CD"
```

### Minimal

```toml title=".releasio.toml"
[changelog.section_headers]
feat = "Added"
fix = "Fixed"
breaking = "Changed"
```

---

## Section Order

Control the order of sections:

```toml title=".releasio.toml"
[changelog]
section_order = [
    "breaking",
    "feat",
    "fix",
    "perf",
    "docs",
    "refactor",
]
```

Sections appear in this order. Unlisted types are appended at the end.

---

## Header Format

### Version Header

```toml title=".releasio.toml"
[changelog]
version_header_template = "## [{version}] - {date}"
```

Output:
```markdown
## [1.2.0] - 2024-01-15
```

### Without Date

```toml title=".releasio.toml"
[changelog]
version_header_template = "## [{version}]"
```

Output:
```markdown
## [1.2.0]
```

### With Link

```toml title=".releasio.toml"
[changelog]
version_header_template = "## [{version}]({compare_url}) - {date}"
```

Output:
```markdown
## [1.2.0](https://github.com/user/repo/compare/v1.1.0...v1.2.0) - 2024-01-15
```

---

## Scope Handling

### Include Scope in Entry

```toml title=".releasio.toml"
[changelog]
commit_template = "- **{scope}**: {description}"
include_scope = true
```

Output:
```markdown
- **api**: Add user endpoint
- **ui**: Update dashboard
```

### Group by Scope

```toml title=".releasio.toml"
[changelog]
group_by_scope = true
```

Output:
```markdown
### Features

#### API
- Add user endpoint
- Add auth endpoint

#### UI
- Update dashboard
```

---

## Example Configurations

### Keep a Changelog Format

Following [keepachangelog.com](https://keepachangelog.com/) style:

```toml title=".releasio.toml"
[changelog]
path = "CHANGELOG.md"

[changelog.section_headers]
feat = "Added"
fix = "Fixed"
breaking = "Changed"
deprecated = "Deprecated"
removed = "Removed"
security = "Security"

[changelog]
version_header_template = "## [{version}] - {date}"
commit_template = "- {description}"
```

### GitHub Style

Optimized for GitHub rendering:

```toml title=".releasio.toml"
[changelog]
path = "CHANGELOG.md"
show_authors = true
show_commit_hash = true
commit_template = "- {description} ([{short_hash}]({commit_url})) @{author}"

[changelog.section_headers]
breaking = "⚠️ Breaking Changes"
feat = "🚀 Features"
fix = "🐛 Bug Fixes"
docs = "📖 Documentation"
perf = "⚡ Performance"
```

### Minimal Style

Simple, no frills:

```toml title=".releasio.toml"
[changelog]
path = "CHANGELOG.md"
commit_template = "- {description}"

[changelog.section_headers]
feat = "New"
fix = "Fixed"
```

---

## Filtering Commits

### Exclude Types

```toml title=".releasio.toml"
[changelog]
exclude_types = ["chore", "ci", "test"]
```

### Include Only

```toml title=".releasio.toml"
[changelog]
include_types = ["feat", "fix", "breaking"]
```

### Exclude Scopes

```toml title=".releasio.toml"
[changelog]
exclude_scopes = ["deps", "internal"]
```

---

## First-Time Contributors

Highlight new contributors:

```toml title=".releasio.toml"
[changelog]
show_first_time_contributors = true
first_contributor_badge = "🎉 First contribution!"
```

Output:
```markdown
### Features
- Add user dashboard (#42) by @newuser 🎉 First contribution!
```

---

## Dependency Updates

Include or exclude dependency bumps:

```toml title=".releasio.toml"
[changelog]
include_dependency_updates = true
dependency_section_header = "📦 Dependencies"
```

Output:
```markdown
### 📦 Dependencies
- Bump requests from 2.28.0 to 2.31.0
- Bump pytest from 7.0.0 to 8.0.0
```

---

## See Also

- [git-cliff Integration](git-cliff.md) - Advanced templating
- [Conventional Commits](../commits/index.md) - Commit format
- [Configuration Reference](../configuration/reference.md) - All options
