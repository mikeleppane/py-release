# Commit Format

:material-format-text: Complete conventional commit specification.

---

## Structure

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

---

## Type (Required)

The type describes the category of change:

```bash
feat: add user authentication
fix: resolve login issue
docs: update API documentation
```

### Available Types

| Type | Description | Changelog Section |
|------|-------------|-------------------|
| `feat` | New feature | Features |
| `fix` | Bug fix | Bug Fixes |
| `docs` | Documentation | Documentation |
| `style` | Formatting, whitespace | (hidden) |
| `refactor` | Code restructuring | Refactoring |
| `perf` | Performance improvement | Performance |
| `test` | Adding/updating tests | (hidden) |
| `build` | Build system, dependencies | Build |
| `ci` | CI/CD configuration | (hidden) |
| `chore` | Maintenance, tooling | (hidden) |
| `revert` | Reverting changes | Reverts |

---

## Scope (Optional)

The scope provides context about what part of the codebase is affected:

```bash
feat(auth): add OAuth2 support
fix(api): handle timeout errors
docs(readme): add installation section
```

### Naming Conventions

```bash
# Module/package name
feat(parser): add JSON support
fix(validator): handle edge cases

# Feature area
feat(auth): implement 2FA
fix(payments): correct tax calculation

# Component
feat(button): add loading state
fix(modal): prevent scroll lock
```

### Multiple Scopes

For changes affecting multiple areas:

```bash
# Option 1: Primary scope
feat(api): add user endpoint and update docs

# Option 2: Comma-separated
feat(api,docs): add user endpoint with documentation
```

---

## Breaking Change Indicator (!)

Add `!` after the type/scope for breaking changes:

```bash
# Without scope
feat!: remove deprecated API

# With scope
feat(api)!: change response format

# Fix with breaking change
fix!: correct calculation (changes results)
```

---

## Description (Required)

A short summary of the change:

```bash
feat: add user authentication        # Good
feat: Add User Authentication        # Bad - capitalized
feat: added user authentication      # Bad - past tense
feat: adding user authentication     # Bad - gerund
feat: add user authentication.       # Bad - period
```

### Guidelines

| Do | Don't |
|----|-------|
| Use imperative mood | Use past tense |
| Start lowercase | Start uppercase |
| Be concise (<50 chars) | Write paragraphs |
| Omit period at end | End with punctuation |

### Good Examples

```bash
feat: add password reset functionality
fix: prevent race condition in cache
docs: clarify installation requirements
perf: optimize database query performance
refactor: simplify error handling logic
```

---

## Body (Optional)

Provide additional context when the description isn't sufficient:

```bash
git commit -m "fix: prevent data loss on connection timeout

The previous implementation would silently drop data when the
connection timed out. This change ensures all data is persisted
to local storage before the connection closes.

Affected endpoints:
- POST /api/data
- PUT /api/data/:id"
```

### When to Use

- Explain the **why**, not the what
- Provide context for complex changes
- List affected areas
- Reference related issues

### Formatting

```bash
# Wrap at 72 characters
# Use bullet points for lists
# Separate paragraphs with blank lines
```

---

## Footer (Optional)

Footers contain metadata about the commit:

```bash
git commit -m "feat: add user dashboard

Implements the new user dashboard with activity feed,
notifications, and quick actions.

BREAKING CHANGE: Dashboard API endpoints have changed.
Closes #123
Reviewed-by: @teammate
Co-authored-by: Partner <partner@example.com>"
```

### Common Footers

| Footer | Purpose |
|--------|---------|
| `BREAKING CHANGE:` | Describe breaking change |
| `Closes #123` | Close GitHub issue |
| `Fixes #123` | Fix GitHub issue |
| `Refs #123` | Reference issue |
| `Reviewed-by:` | Credit reviewer |
| `Co-authored-by:` | Credit co-author |

### Breaking Change Footer

```bash
BREAKING CHANGE: <description>

# Can span multiple lines
BREAKING CHANGE: The authentication API has changed.
Old: POST /auth/login { username, password }
New: POST /auth/login { email, password }

Migration: Update all login calls to use email instead of username.
```

---

## Complete Examples

### Simple Feature

```bash
feat: add dark mode toggle
```

### Feature with Scope

```bash
feat(ui): add dark mode toggle

Adds a toggle button in the settings panel that switches
between light and dark themes. Theme preference is persisted
in local storage.

Closes #456
```

### Bug Fix

```bash
fix(api): handle null response from external service

The payment gateway occasionally returns null instead of
an error object. This change adds explicit null checking
and returns a user-friendly error message.

Fixes #789
```

### Breaking Change

```bash
feat(api)!: migrate to v2 authentication

BREAKING CHANGE: The authentication API has been completely
redesigned. All existing API tokens are invalidated.

Migration steps:
1. Generate new API tokens in the dashboard
2. Update client applications with new tokens
3. Use the new /auth/v2/* endpoints

Old endpoints will return 410 Gone after 2024-06-01.

Closes #321
Reviewed-by: @security-team
```

### Documentation

```bash
docs(api): add authentication examples

Adds code examples for all authentication methods:
- API key authentication
- OAuth2 authorization code flow
- JWT token refresh

Examples are provided in Python, JavaScript, and cURL.
```

### Performance

```bash
perf(db): optimize user query with index

Adds a composite index on (user_id, created_at) to speed up
the activity feed query. Reduces query time from ~500ms to ~10ms.

Before: EXPLAIN shows sequential scan
After: EXPLAIN shows index scan

Refs #555
```

---

## Validation

### Using Commitlint

Install and configure:

```bash
npm install --save-dev @commitlint/{cli,config-conventional}
```

```javascript title="commitlint.config.js"
module.exports = {
  extends: ['@commitlint/config-conventional'],
};
```

### Using Pre-commit Hook

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

### In CI

```yaml title=".github/workflows/lint.yml"
- name: Validate PR title
  uses: mikeleppane/releasio@v2
  with:
    command: check-pr
    require-scope: 'true'
```

---

## See Also

- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [Custom Parsers](custom-parsers.md) - Non-standard formats
- [Semantic Versioning](../versioning/semver.md) - Version bumps
