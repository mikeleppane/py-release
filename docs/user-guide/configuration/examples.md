# Configuration Examples

Common configuration patterns for different project types.

---

## Minimal Configuration

For most projects, this is all you need:

```toml title=".releasio.toml"
default_branch = "main"

[version]
tag_prefix = "v"

[changelog]
path = "CHANGELOG.md"
```

---

## Full-Featured Configuration

All commonly used options:

```toml title=".releasio.toml"
default_branch = "main"

[version]
tag_prefix = "v"
initial_version = "0.1.0"
auto_detect_version_files = true
update_lock_file = true

[changelog]
path = "CHANGELOG.md"
show_authors = true
show_commit_hash = true
show_first_time_contributors = true
first_contributor_badge = "🎉 First contribution!"
include_dependency_updates = true

[changelog.section_headers]
breaking = "⚠️ Breaking Changes"
feat = "✨ Features"
fix = "🐛 Bug Fixes"
perf = "⚡ Performance"
docs = "📚 Documentation"
refactor = "♻️ Refactoring"

[commits]
types_minor = ["feat"]
types_patch = ["fix", "perf", "docs", "refactor", "style", "test", "build", "ci"]

[github]
release_pr_branch = "releasio/release"
release_pr_labels = ["release", "automated"]
release_assets = ["dist/*.whl", "dist/*.tar.gz"]

[publish]
tool = "uv"
trusted_publishing = true
validate_before_publish = true

[hooks]
pre_bump = ["pytest"]
post_release = ["./scripts/notify.sh {version}"]
```

---

## Poetry Project

Configuration for Poetry-based projects:

```toml title=".releasio.toml"
default_branch = "main"

[version]
tag_prefix = "v"

[publish]
tool = "poetry"
```

---

## PDM Project

Configuration for PDM-based projects:

```toml title=".releasio.toml"
default_branch = "main"

[version]
tag_prefix = "v"

[publish]
tool = "pdm"
```

---

## TestPyPI Publishing

Publish to TestPyPI instead of PyPI:

```toml title=".releasio.toml"
[publish]
registry = "https://test.pypi.org/legacy/"
trusted_publishing = true
```

---

## Skip PyPI Publishing

Only create GitHub releases (no PyPI):

```toml title=".releasio.toml"
[publish]
enabled = false
```

---

## Gitmoji Support

Parse Gitmoji-style commits:

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^:sparkles:\\s*(?P<description>.+)$"
type = "feat"
group = "✨ Features"

[[commits.commit_parsers]]
pattern = "^:bug:\\s*(?P<description>.+)$"
type = "fix"
group = "🐛 Bug Fixes"

[[commits.commit_parsers]]
pattern = "^:zap:\\s*(?P<description>.+)$"
type = "perf"
group = "⚡ Performance"

[[commits.commit_parsers]]
pattern = "^:memo:\\s*(?P<description>.+)$"
type = "docs"
group = "📝 Documentation"

[[commits.commit_parsers]]
pattern = "^:boom:\\s*(?P<description>.+)$"
type = "breaking"
group = "💥 Breaking Changes"
breaking_indicator = ":boom:"

[commits]
use_conventional_fallback = true
```

---

## Multi-Branch Releases

Different release channels for different branches:

```toml title=".releasio.toml"
default_branch = "main"

[branches.main]
match = "main"
prerelease = false

[branches.beta]
match = "beta"
prerelease = true
prerelease_token = "beta"

[branches.alpha]
match = "develop"
prerelease = true
prerelease_token = "alpha"
```

This produces:

- `main` → `1.0.0`
- `beta` → `1.0.0-beta.1`
- `develop` → `1.0.0-alpha.1`

---

## GitHub Enterprise

For GitHub Enterprise installations:

```toml title=".releasio.toml"
[github]
api_url = "https://github.mycompany.com/api/v3"
owner = "myorg"
repo = "myproject"
```

---

## Release Hooks

Run scripts at release lifecycle points:

```toml title=".releasio.toml"
[hooks]
# Run before version bump
pre_bump = [
    "pytest",
    "ruff check .",
]

# Run after version bump
post_bump = [
    "npm run build",
]

# Run before release
pre_release = [
    "./scripts/validate-release.sh",
]

# Run after successful release
post_release = [
    "./scripts/notify-slack.sh {version}",
    "./scripts/update-docs.sh",
]

# Custom build command
build = "make build VERSION={version}"
```

---

## Security Advisories

Enable automatic security advisory creation:

```toml title=".releasio.toml"
[security]
enabled = true
auto_create_advisory = true
security_patterns = [
    "fix\\(security\\):",
    "security:",
    "CVE-\\d{4}-\\d+",
]
```

---

## Draft Releases

Create releases as drafts for review:

```toml title=".releasio.toml"
[github]
draft_releases = true
```

---

## Release Assets

Upload files as GitHub release assets:

```toml title=".releasio.toml"
[github]
release_assets = [
    "dist/*.whl",
    "dist/*.tar.gz",
    "docs/_build/html.zip",
]
```

---

## Custom Changelog Format

Customize changelog entries:

```toml title=".releasio.toml"
[changelog]
show_authors = true
show_commit_hash = true
commit_template = "- {description} ([{hash}](https://github.com/user/repo/commit/{hash})) by @{author}"

[changelog.section_headers]
feat = "🚀 New Features"
fix = "🔧 Bug Fixes"
perf = "⚡ Performance Improvements"
docs = "📖 Documentation"
breaking = "💥 Breaking Changes"
```
