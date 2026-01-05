"""Security advisory detection and creation.

This module provides functionality for detecting security-related commits
and optionally creating GitHub Security Advisories for them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from releasio.config.models import SecurityConfig
    from releasio.core.commits import ParsedCommit
    from releasio.forge.github import GitHubClient


@dataclass(frozen=True, slots=True)
class SecurityCommit:
    """Represents a security-related commit.

    Attributes:
        commit: The parsed commit
        matched_pattern: The pattern that matched
        cve_id: CVE identifier if found, None otherwise
    """

    commit: ParsedCommit
    matched_pattern: str
    cve_id: str | None = None


def detect_security_commits(
    commits: list[ParsedCommit],
    config: SecurityConfig,
) -> list[SecurityCommit]:
    """Detect security-related commits from a list of parsed commits.

    Uses regex patterns from config to identify commits that may be
    security fixes.

    Args:
        commits: List of parsed commits to analyze
        config: Security configuration with patterns

    Returns:
        List of SecurityCommit objects for commits matching security patterns
    """
    if not config.enabled:
        return []

    security_commits: list[SecurityCommit] = []
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in config.security_patterns]
    cve_pattern = re.compile(r"CVE-\d{4}-\d+", re.IGNORECASE)

    for parsed_commit in commits:
        # Check against all patterns
        for pattern in compiled_patterns:
            # Check commit subject/description
            subject = parsed_commit.commit.subject
            if pattern.search(subject):
                # Check if there's a CVE ID
                cve_match = cve_pattern.search(subject)
                cve_id = cve_match.group(0) if cve_match else None

                security_commits.append(
                    SecurityCommit(
                        commit=parsed_commit,
                        matched_pattern=pattern.pattern,
                        cve_id=cve_id,
                    )
                )
                break  # Don't match same commit multiple times

            # Also check commit body
            body = parsed_commit.commit.body
            if body and pattern.search(body):
                cve_match = cve_pattern.search(body) or cve_pattern.search(subject)
                cve_id = cve_match.group(0) if cve_match else None

                security_commits.append(
                    SecurityCommit(
                        commit=parsed_commit,
                        matched_pattern=pattern.pattern,
                        cve_id=cve_id,
                    )
                )
                break

    return security_commits


def format_security_advisory_body(
    security_commits: list[SecurityCommit],
    version: str,
    project_name: str,
) -> str:
    """Format the body of a security advisory.

    Args:
        security_commits: List of security commits
        version: Version being released
        project_name: Name of the project

    Returns:
        Formatted advisory body in markdown
    """
    lines = [
        f"## Security fixes in {project_name} v{version}",
        "",
        "The following security issues have been addressed in this release:",
        "",
    ]

    for sec_commit in security_commits:
        commit = sec_commit.commit
        cve_str = f" ({sec_commit.cve_id})" if sec_commit.cve_id else ""
        lines.append(f"- {commit.description}{cve_str}")
        if commit.commit.body:
            # Add first paragraph of body as description
            body_lines = commit.commit.body.strip().split("\n\n")[0]
            if body_lines:
                lines.append(f"  {body_lines[:200]}...")
        lines.append("")

    lines.extend(
        [
            "## Recommendation",
            "",
            f"Users are encouraged to upgrade to version {version} or later.",
        ]
    )

    return "\n".join(lines)


async def create_security_advisory(
    github_client: GitHubClient,
    security_commits: list[SecurityCommit],
    version: str,
    project_name: str,
    owner: str,
    repo: str,
) -> str | None:
    """Create a GitHub Security Advisory for security commits.

    Args:
        github_client: GitHub client instance
        security_commits: List of security commits
        version: Version being released
        project_name: Name of the project
        owner: Repository owner
        repo: Repository name

    Returns:
        URL of the created advisory, or None if creation failed
    """
    if not security_commits:
        return None

    # Extract CVE IDs if any
    cve_ids = [sc.cve_id for sc in security_commits if sc.cve_id]

    # Generate advisory body
    body = format_security_advisory_body(security_commits, version, project_name)

    # Generate title
    if cve_ids:
        title = f"Security Advisory for {project_name} v{version}: {', '.join(cve_ids[:3])}"
    else:
        title = f"Security Advisory for {project_name} v{version}"

    # Call GitHub API to create advisory
    try:
        result = await github_client.create_security_advisory(
            owner=owner,
            repo=repo,
            title=title,
            description=body,
            severity="medium",  # Default to medium, could be configurable
            vulnerabilities=[{"package": project_name, "patched_versions": f">= {version}"}],
            cve_ids=cve_ids if cve_ids else None,
        )
        return result.url if result else None
    except Exception:
        # Security advisory creation is best-effort
        # Don't fail the release if it doesn't work
        return None


def should_create_advisory(
    security_commits: list[SecurityCommit],
    config: SecurityConfig,
) -> bool:
    """Determine if a security advisory should be created.

    Args:
        security_commits: List of detected security commits
        config: Security configuration

    Returns:
        True if an advisory should be created
    """
    return config.enabled and config.auto_create_advisory and len(security_commits) > 0
