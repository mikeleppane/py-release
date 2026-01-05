# Installation

## Install releasio

=== "pip"

    ```bash
    pip install releasio
    ```

=== "uv"

    ```bash
    uv add releasio --dev
    ```

=== "pipx (global)"

    ```bash
    pipx install releasio
    ```

## Install git-cliff

releasio uses [git-cliff](https://git-cliff.org/) for changelog generation. Install it using your preferred method:

=== "Homebrew (macOS/Linux)"

    ```bash
    brew install git-cliff
    ```

=== "Cargo (Rust)"

    ```bash
    cargo install git-cliff
    ```

=== "npm"

    ```bash
    npm install -g git-cliff
    ```

=== "Scoop (Windows)"

    ```bash
    scoop install git-cliff
    ```

!!! tip "Native Fallback"
    If git-cliff is not installed, releasio will use a basic native changelog
    generator. For best results, install git-cliff.

## Verify Installation

Check that everything is installed correctly:

```bash
# Check releasio
releasio --version

# Check git-cliff
git-cliff --version
```

## GitHub Actions

When using releasio in GitHub Actions, git-cliff is installed automatically
by the action. No additional setup required.

```yaml
- uses: mikeleppane/releasio@v2
  with:
    command: release-pr
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Next Steps

- [Quick Start](quickstart.md) - Get up and running in 5 minutes
- [First Release](first-release.md) - Complete walkthrough
