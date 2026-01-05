# Custom Parsers

:material-code-braces: Parse non-conventional commit formats.

---

## Overview

If your project uses a non-standard commit format, releasio supports custom parsers:

- **Gitmoji** - Emoji-based commits
- **Angular** - Angular-style commits
- **Custom patterns** - Your own format

---

## Custom Commit Parsers

Define regex patterns to parse commits:

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+): (?P<description>.+)$"
type_group = "type"
description_group = "description"
```

### Parser Fields

| Field | Description | Required |
|-------|-------------|----------|
| `pattern` | Regex pattern with named groups | Yes |
| `type` | Static type if not in pattern | No |
| `group` | Changelog section | No |
| `type_group` | Named group for type | No |
| `scope_group` | Named group for scope | No |
| `description_group` | Named group for description | No |
| `breaking_indicator` | Pattern indicating breaking | No |

---

## Gitmoji

Parse [Gitmoji](https://gitmoji.dev/) commits:

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

[[commits.commit_parsers]]
pattern = "^:recycle:\\s*(?P<description>.+)$"
type = "refactor"
group = "♻️ Refactoring"

[[commits.commit_parsers]]
pattern = "^:white_check_mark:\\s*(?P<description>.+)$"
type = "test"
group = "✅ Testing"

[[commits.commit_parsers]]
pattern = "^:construction_worker:\\s*(?P<description>.+)$"
type = "ci"
group = "👷 CI/CD"

[commits]
use_conventional_fallback = true
```

### Gitmoji Reference

| Emoji | Code | Type |
|-------|------|------|
| ✨ | `:sparkles:` | feat |
| 🐛 | `:bug:` | fix |
| 📝 | `:memo:` | docs |
| ⚡ | `:zap:` | perf |
| ♻️ | `:recycle:` | refactor |
| ✅ | `:white_check_mark:` | test |
| 💥 | `:boom:` | breaking |
| 🔧 | `:wrench:` | chore |
| 👷 | `:construction_worker:` | ci |

---

## Angular Style

Parse Angular commit format:

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+)\\((?P<scope>[^)]+)\\):\\s*(?P<description>.+)$"
type_group = "type"
scope_group = "scope"
description_group = "description"

[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+):\\s*(?P<description>.+)$"
type_group = "type"
description_group = "description"
```

---

## Jira Integration

Parse commits with Jira ticket references:

```bash
PROJ-123: Add user authentication
```

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^(?P<ticket>[A-Z]+-\\d+):\\s*(?P<description>.+)$"
type = "feat"  # Default type
description_group = "description"

# With type prefix
[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+)\\s+(?P<ticket>[A-Z]+-\\d+):\\s*(?P<description>.+)$"
type_group = "type"
description_group = "description"
```

### Example Commits

```bash
PROJ-123: add user authentication
feat PROJ-456: implement OAuth2
fix PROJ-789: resolve login timeout
```

---

## GitHub Issue Style

Parse commits referencing GitHub issues:

```bash
Add user authentication (#123)
Fix login bug (fixes #456)
```

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^(?P<description>.+)\\s+\\(#(?P<issue>\\d+)\\)$"
type = "feat"
description_group = "description"

[[commits.commit_parsers]]
pattern = "^(?P<description>.+)\\s+\\(fixes #(?P<issue>\\d+)\\)$"
type = "fix"
description_group = "description"
```

---

## Simple Prefix Style

For simple `[TYPE] message` format:

```bash
[FEATURE] Add user authentication
[BUG] Fix login issue
[DOCS] Update README
```

```toml title=".releasio.toml"
[[commits.commit_parsers]]
pattern = "^\\[FEATURE\\]\\s*(?P<description>.+)$"
type = "feat"
group = "Features"

[[commits.commit_parsers]]
pattern = "^\\[BUG\\]\\s*(?P<description>.+)$"
type = "fix"
group = "Bug Fixes"

[[commits.commit_parsers]]
pattern = "^\\[DOCS\\]\\s*(?P<description>.+)$"
type = "docs"
group = "Documentation"

[[commits.commit_parsers]]
pattern = "^\\[BREAKING\\]\\s*(?P<description>.+)$"
type = "breaking"
group = "Breaking Changes"
breaking_indicator = "[BREAKING]"
```

---

## Mixed Formats

Support multiple formats with fallback:

```toml title=".releasio.toml"
# Try Gitmoji first
[[commits.commit_parsers]]
pattern = "^:sparkles:\\s*(?P<description>.+)$"
type = "feat"
group = "✨ Features"

[[commits.commit_parsers]]
pattern = "^:bug:\\s*(?P<description>.+)$"
type = "fix"
group = "🐛 Bug Fixes"

# Then try Jira
[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+)\\s+[A-Z]+-\\d+:\\s*(?P<description>.+)$"
type_group = "type"
description_group = "description"

# Fall back to conventional commits
[commits]
use_conventional_fallback = true
```

---

## Pattern Testing

### Regex Tips

```python
# Test your patterns
import re

pattern = r"^:sparkles:\s*(?P<description>.+)$"
message = ":sparkles: add new feature"

match = re.match(pattern, message)
if match:
    print(match.group("description"))  # "add new feature"
```

### Common Patterns

| Element | Pattern |
|---------|---------|
| Word | `\\w+` |
| Any text | `.+` |
| Optional scope | `(?:\\((?P<scope>[^)]+)\\))?` |
| Issue number | `#(?P<issue>\\d+)` |
| Jira ticket | `[A-Z]+-\\d+` |
| Emoji shortcode | `:[a-z_]+:` |

---

## Breaking Change Detection

### In Pattern

```toml
[[commits.commit_parsers]]
pattern = "^:boom:\\s*(?P<description>.+)$"
type = "breaking"
breaking_indicator = ":boom:"
```

### Separate Pattern

```toml
[commits]
breaking_patterns = [
    "BREAKING CHANGE:",
    "BREAKING:",
    ":boom:",
    "[BREAKING]",
]
```

---

## Fallback Behavior

When no custom parser matches:

```toml
[commits]
# Try conventional commits as fallback
use_conventional_fallback = true

# Or mark as unknown
unknown_type = "other"
unknown_group = "Other Changes"
```

---

## Debugging Parsers

Enable verbose output:

```bash
releasio check --verbose
```

Output:
```
Parsing commit: ":sparkles: add user dashboard"
  Trying parser 1: ^:sparkles:\s*(?P<description>.+)$
  ✓ Match! type=feat, description="add user dashboard"

Parsing commit: "fix: resolve bug"
  Trying parser 1: ^:sparkles:\s*(?P<description>.+)$
  ✗ No match
  Trying conventional fallback...
  ✓ Match! type=fix, description="resolve bug"
```

---

## Examples by Project Type

### Open Source with Gitmoji

```toml
[[commits.commit_parsers]]
pattern = "^:sparkles:\\s*(?P<description>.+)$"
type = "feat"

[[commits.commit_parsers]]
pattern = "^:bug:\\s*(?P<description>.+)$"
type = "fix"

[commits]
use_conventional_fallback = true
```

### Enterprise with Jira

```toml
[[commits.commit_parsers]]
pattern = "^(?P<type>\\w+)\\((?P<ticket>[A-Z]+-\\d+)\\):\\s*(?P<description>.+)$"
type_group = "type"
description_group = "description"
```

### Legacy Project Migration

```toml
# Support old format
[[commits.commit_parsers]]
pattern = "^\\[(?P<type>\\w+)\\]\\s*(?P<description>.+)$"
type_group = "type"
description_group = "description"

# And new format
[commits]
use_conventional_fallback = true
```

---

## See Also

- [Commit Format](format.md) - Conventional commit spec
- [Changelog Templates](../changelog/templates.md) - Customize output
- [Configuration Reference](../configuration/reference.md) - All options
