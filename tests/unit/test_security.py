"""Unit tests for security advisory detection and creation."""

from __future__ import annotations

from datetime import datetime

import pytest

from releasio.config.models import SecurityConfig
from releasio.core.commits import ParsedCommit
from releasio.core.security import (
    SecurityCommit,
    detect_security_commits,
    format_security_advisory_body,
    should_create_advisory,
)
from releasio.vcs.git import Commit


@pytest.fixture
def sample_commit() -> Commit:
    """Create a sample commit for testing."""
    return Commit(
        sha="abc123def456789012345678901234567890abcd",
        message="fix: some bug fix",
        author_name="Test Author",
        author_email="test@example.com",
        date=datetime.now(),
    )


@pytest.fixture
def security_commit() -> Commit:
    """Create a security-related commit."""
    return Commit(
        sha="sec123def456789012345678901234567890abcd",
        message="fix(security): patch SQL injection vulnerability CVE-2024-1234",
        author_name="Security Team",
        author_email="security@example.com",
        date=datetime.now(),
    )


@pytest.fixture
def cve_commit() -> Commit:
    """Create a commit with CVE ID."""
    return Commit(
        sha="cve123def456789012345678901234567890abcd",
        message="fix: address CVE-2024-5678 in authentication module",
        author_name="Developer",
        author_email="dev@example.com",
        date=datetime.now(),
    )


class TestDetectSecurityCommits:
    """Tests for detect_security_commits function."""

    def test_detect_disabled_returns_empty(self, sample_commit: Commit):
        """Return empty list when security detection is disabled."""
        parsed = ParsedCommit(
            commit=sample_commit,
            commit_type="fix",
            scope=None,
            description="some bug fix",
            is_breaking=False,
            is_conventional=True,
        )
        config = SecurityConfig(enabled=False)

        result = detect_security_commits([parsed], config)

        assert result == []

    def test_detect_security_scope_pattern(self, security_commit: Commit):
        """Detect commits with security scope."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="patch SQL injection vulnerability CVE-2024-1234",
            is_breaking=False,
            is_conventional=True,
        )
        config = SecurityConfig(enabled=True)

        result = detect_security_commits([parsed], config)

        assert len(result) == 1
        assert result[0].cve_id == "CVE-2024-1234"

    def test_detect_cve_pattern(self, cve_commit: Commit):
        """Detect commits with CVE ID in message."""
        parsed = ParsedCommit(
            commit=cve_commit,
            commit_type="fix",
            scope=None,
            description="address CVE-2024-5678 in authentication module",
            is_breaking=False,
            is_conventional=True,
        )
        config = SecurityConfig(enabled=True)

        result = detect_security_commits([parsed], config)

        assert len(result) == 1
        assert result[0].cve_id == "CVE-2024-5678"

    def test_detect_no_match(self, sample_commit: Commit):
        """Return empty list when no patterns match."""
        parsed = ParsedCommit(
            commit=sample_commit,
            commit_type="fix",
            scope=None,
            description="some bug fix",
            is_breaking=False,
            is_conventional=True,
        )
        config = SecurityConfig(enabled=True)

        result = detect_security_commits([parsed], config)

        assert result == []

    def test_detect_custom_patterns(self):
        """Detect security commits with custom patterns."""
        commit = Commit(
            sha="custom123",
            message="SECURITY-FIX: critical vulnerability patched",
            author_name="Dev",
            author_email="dev@example.com",
            date=datetime.now(),
        )
        parsed = ParsedCommit(
            commit=commit,
            commit_type=None,
            scope=None,
            description="critical vulnerability patched",
            is_breaking=False,
            is_conventional=False,
        )
        config = SecurityConfig(
            enabled=True,
            security_patterns=[r"SECURITY-FIX:"],
        )

        result = detect_security_commits([parsed], config)

        assert len(result) == 1


class TestFormatSecurityAdvisoryBody:
    """Tests for format_security_advisory_body function."""

    def test_format_basic_advisory(self, security_commit: Commit):
        """Format basic security advisory body."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="patch SQL injection vulnerability",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commit = SecurityCommit(
            commit=parsed,
            matched_pattern=r"fix\(security\):",
            cve_id="CVE-2024-1234",
        )

        result = format_security_advisory_body([sec_commit], "1.0.0", "myproject")

        assert "## Security fixes in myproject v1.0.0" in result
        assert "patch SQL injection vulnerability (CVE-2024-1234)" in result
        assert "Recommendation" in result
        assert "upgrade to version 1.0.0" in result

    def test_format_multiple_commits(self, security_commit: Commit, cve_commit: Commit):
        """Format advisory with multiple security commits."""
        parsed1 = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="first security fix",
            is_breaking=False,
            is_conventional=True,
        )
        parsed2 = ParsedCommit(
            commit=cve_commit,
            commit_type="fix",
            scope=None,
            description="second security fix",
            is_breaking=False,
            is_conventional=True,
        )

        sec_commits = [
            SecurityCommit(commit=parsed1, matched_pattern="", cve_id="CVE-2024-1111"),
            SecurityCommit(commit=parsed2, matched_pattern="", cve_id="CVE-2024-2222"),
        ]

        result = format_security_advisory_body(sec_commits, "2.0.0", "testpkg")

        assert "first security fix (CVE-2024-1111)" in result
        assert "second security fix (CVE-2024-2222)" in result


class TestShouldCreateAdvisory:
    """Tests for should_create_advisory function."""

    def test_should_create_when_enabled_and_commits(self, security_commit: Commit):
        """Return True when security enabled and commits found."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="security fix",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commits = [SecurityCommit(commit=parsed, matched_pattern="", cve_id=None)]
        config = SecurityConfig(enabled=True, auto_create_advisory=True)

        assert should_create_advisory(sec_commits, config) is True

    def test_should_not_create_when_disabled(self, security_commit: Commit):
        """Return False when security is disabled."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="security fix",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commits = [SecurityCommit(commit=parsed, matched_pattern="", cve_id=None)]
        config = SecurityConfig(enabled=False)

        assert should_create_advisory(sec_commits, config) is False

    def test_should_not_create_when_auto_advisory_disabled(self, security_commit: Commit):
        """Return False when auto_create_advisory is disabled."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="security fix",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commits = [SecurityCommit(commit=parsed, matched_pattern="", cve_id=None)]
        config = SecurityConfig(enabled=True, auto_create_advisory=False)

        assert should_create_advisory(sec_commits, config) is False

    def test_should_not_create_with_no_commits(self):
        """Return False when no security commits found."""
        config = SecurityConfig(enabled=True, auto_create_advisory=True)

        assert should_create_advisory([], config) is False


class TestSecurityCommitDataclass:
    """Tests for SecurityCommit dataclass."""

    def test_security_commit_immutable(self, security_commit: Commit):
        """SecurityCommit should be immutable (frozen)."""
        parsed = ParsedCommit(
            commit=security_commit,
            commit_type="fix",
            scope="security",
            description="security fix",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commit = SecurityCommit(
            commit=parsed,
            matched_pattern=r"fix\(security\):",
            cve_id="CVE-2024-1234",
        )

        with pytest.raises(AttributeError):
            sec_commit.cve_id = "CVE-2024-5678"  # type: ignore

    def test_security_commit_optional_cve(self, sample_commit: Commit):
        """SecurityCommit can have None CVE ID."""
        parsed = ParsedCommit(
            commit=sample_commit,
            commit_type="fix",
            scope=None,
            description="generic fix",
            is_breaking=False,
            is_conventional=True,
        )
        sec_commit = SecurityCommit(
            commit=parsed,
            matched_pattern="security:",
            cve_id=None,
        )

        assert sec_commit.cve_id is None
