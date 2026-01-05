"""Generate API reference pages for mkdocstrings."""

from pathlib import Path

import mkdocs_gen_files

# Source directory
SRC_DIR = Path("src/releasio")

# Navigation structure
nav = mkdocs_gen_files.Nav()

for path in sorted(SRC_DIR.rglob("*.py")):
    # Skip __pycache__ and private modules
    if "__pycache__" in str(path):
        continue
    if path.name.startswith("_") and path.name != "__init__.py":
        continue

    # Get module path
    module_path = path.relative_to("src")
    doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    # Create module identifier
    parts = list(module_path.with_suffix("").parts)

    # Skip __init__ files from nav but still generate docs
    if parts[-1] == "__init__":
        parts = parts[:-1]
        if not parts:
            continue
        doc_path = Path(*parts) / "index.md"
        full_doc_path = Path("reference", doc_path)

    identifier = ".".join(parts)

    # Add to navigation
    nav[parts] = doc_path.as_posix()

    # Generate markdown file
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        fd.write(f"# {parts[-1]}\n\n")
        fd.write(f"::: {identifier}\n")

    # Set edit path
    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Write navigation file
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
