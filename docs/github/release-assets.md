# Release Assets

:material-file-upload: Upload files to GitHub releases automatically.

---

## Overview

releasio can automatically upload build artifacts to your GitHub releases, making it easy to distribute:

- Python wheel files (`.whl`)
- Source distributions (`.tar.gz`)
- Documentation archives
- Platform-specific binaries
- Any other build artifacts

---

## Configuration

### Basic Setup

Configure assets in your config file:

=== ".releasio.toml"

    ```toml
    [github]
    release_assets = [
        "dist/*.whl",
        "dist/*.tar.gz",
    ]
    ```

=== "pyproject.toml"

    ```toml
    [tool.releasio.github]
    release_assets = [
        "dist/*.whl",
        "dist/*.tar.gz",
    ]
    ```

### Glob Patterns

Use glob patterns to match files:

| Pattern | Matches |
|---------|---------|
| `dist/*.whl` | All wheel files in dist/ |
| `dist/*.tar.gz` | All source distributions |
| `docs/_build/*.zip` | All zips in docs/_build/ |
| `build/**/*.exe` | All .exe files recursively |

### Multiple Asset Types

```toml title=".releasio.toml"
[github]
release_assets = [
    # Python packages
    "dist/*.whl",
    "dist/*.tar.gz",

    # Documentation
    "docs/_build/html.zip",

    # Binaries (if using PyInstaller, etc.)
    "build/myapp-linux",
    "build/myapp-macos",
    "build/myapp-windows.exe",
]
```

---

## Workflow Examples

### Standard Python Package

```yaml title=".github/workflows/release.yml"
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write
  id-token: write

jobs:
  release:
    if: startsWith(github.event.head_commit.message, 'chore(release):')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

With config:

```toml title=".releasio.toml"
[github]
release_assets = ["dist/*.whl", "dist/*.tar.gz"]
```

### Multi-Platform Binaries

For projects that build platform-specific binaries:

```yaml title=".github/workflows/release.yml"
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  build:
    if: startsWith(github.event.head_commit.message, 'chore(release):')
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            artifact: myapp-linux
          - os: macos-latest
            artifact: myapp-macos
          - os: windows-latest
            artifact: myapp-windows.exe
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Build binary
        run: |
          pip install pyinstaller
          pyinstaller --onefile src/myapp/__main__.py -n ${{ matrix.artifact }}

      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact }}
          path: dist/${{ matrix.artifact }}

  release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/download-artifact@v4
        with:
          path: build/

      - name: Flatten artifacts
        run: |
          mkdir -p dist
          find build -type f -exec mv {} dist/ \;

      - uses: mikeleppane/releasio@v2
        with:
          command: release
          dry-run: 'false'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

With config:

```toml title=".releasio.toml"
[github]
release_assets = [
    "dist/myapp-linux",
    "dist/myapp-macos",
    "dist/myapp-windows.exe",
]
```

### Documentation Bundle

Include documentation with your release:

```yaml
- name: Build docs
  run: |
    uv sync --extra docs
    uv run mkdocs build
    cd site && zip -r ../docs.zip . && cd ..

- uses: mikeleppane/releasio@v2
  with:
    command: release
    dry-run: 'false'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

```toml title=".releasio.toml"
[github]
release_assets = [
    "dist/*.whl",
    "dist/*.tar.gz",
    "docs.zip",
]
```

---

## Asset Naming

### Automatic Names

Assets are uploaded with their original filenames:

```
dist/mypackage-1.0.0-py3-none-any.whl
  → mypackage-1.0.0-py3-none-any.whl

dist/mypackage-1.0.0.tar.gz
  → mypackage-1.0.0.tar.gz
```

### Version in Filenames

Include version in your build artifacts:

```yaml
- name: Build with version
  run: |
    VERSION=$(grep 'version' pyproject.toml | head -1 | cut -d'"' -f2)
    uv build
    # Wheels already include version
```

---

## Verifying Uploads

### Check Release Page

After release, verify on GitHub:

1. Go to **Releases**
2. Click on the latest release
3. Scroll to **Assets** section
4. Verify all expected files are present

### Download Counts

GitHub tracks download counts for each asset, visible on the release page.

### API Verification

```bash
# List assets for a release
gh release view v1.0.0 --json assets

# Download a specific asset
gh release download v1.0.0 --pattern "*.whl"
```

---

## Troubleshooting

### "No matching files found"

```
Warning: No files matching pattern 'dist/*.whl'
```

**Causes**:

1. Build step didn't run or failed
2. Wrong pattern or path
3. Files in different directory

**Solution**: Verify build output:

```yaml
- name: Build package
  run: uv build

- name: List build artifacts
  run: ls -la dist/

- uses: mikeleppane/releasio@v2
  # ...
```

### "Upload failed"

```
Error: Failed to upload asset: mypackage.whl
```

**Causes**:

1. File too large (GitHub limit: 2GB)
2. Network issues
3. Insufficient permissions

**Solution**: Check permissions and file size:

```yaml
permissions:
  contents: write  # Required for asset uploads
```

### Duplicate Assets

If re-running a release, existing assets may conflict.

releasio handles this by:

1. Checking for existing assets
2. Skipping duplicates (same name and size)
3. Warning about conflicts

---

## Best Practices

### Do

- [x] Build artifacts in CI before release step
- [x] Use specific glob patterns
- [x] Include checksums for binaries
- [x] Test patterns locally with `ls dist/*.whl`

### Don't

- [ ] Upload sensitive files (configs, secrets)
- [ ] Include debug builds in releases
- [ ] Upload very large files (>100MB without good reason)
- [ ] Rely on artifacts from previous jobs without explicit download

---

## Checksums

For security-conscious users, generate checksums:

```yaml
- name: Build and checksum
  run: |
    uv build
    cd dist && sha256sum * > SHA256SUMS && cd ..
```

```toml title=".releasio.toml"
[github]
release_assets = [
    "dist/*.whl",
    "dist/*.tar.gz",
    "dist/SHA256SUMS",
]
```

Users can then verify:

```bash
cd dist
sha256sum -c SHA256SUMS
```

---

## See Also

- [Full Workflow](actions/full-workflow.md)
- [Action Reference](actions/reference.md)
- [PyPI Publishing](../publishing/pypi.md)
