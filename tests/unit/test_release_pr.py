"""Unit tests for release-pr command functions."""

from __future__ import annotations

from dataclasses import dataclass

from releasio.cli.commands.release_pr import (
    _extract_pr_number,
    _format_commit_entry,
    _generate_pr_body,
)
from releasio.core.version import Version


@dataclass
class MockCommit:
    """Mock commit for testing."""

    sha: str = "abc123def456"
    short_sha: str = "abc123d"
    author_name: str = "John Doe"
    author_email: str = "john@example.com"


@dataclass
class MockParsedCommit:
    """Mock parsed commit for testing."""

    commit: MockCommit
    commit_type: str | None = "feat"
    scope: str | None = None
    description: str = "add new feature"
    is_conventional: bool = True
    is_breaking: bool = False


class TestExtractPrNumber:
    """Tests for _extract_pr_number function."""

    def test_extract_pr_number_squash_format(self):
        """Extract PR number from squash merge format."""
        description, pr_number = _extract_pr_number("add new feature (#123)")
        assert description == "add new feature"
        assert pr_number == 123

    def test_extract_pr_number_no_pr(self):
        """Return None when no PR number in description."""
        description, pr_number = _extract_pr_number("add new feature")
        assert description == "add new feature"
        assert pr_number is None

    def test_extract_pr_number_pr_in_middle(self):
        """Only extract PR number at end of description."""
        description, pr_number = _extract_pr_number("fix (#123) issue")
        assert description == "fix (#123) issue"
        assert pr_number is None


class TestFormatCommitEntry:
    """Tests for _format_commit_entry function."""

    def test_format_with_github_username(self):
        """Format entry with GitHub username."""
        pc = MockParsedCommit(
            commit=MockCommit(author_name="John Doe"),
            description="add new feature (#123)",
        )

        result = _format_commit_entry(
            pc,
            github_url="https://github.com/owner/repo",
            github_username="johndoe",
        )

        assert "John Doe (@johndoe)" in result
        assert "PR [#123]" in result

    def test_format_without_github_username(self):
        """Format entry without GitHub username."""
        pc = MockParsedCommit(
            commit=MockCommit(author_name="John Doe"),
            description="add new feature (#123)",
        )

        result = _format_commit_entry(
            pc,
            github_url="https://github.com/owner/repo",
            github_username=None,
        )

        assert "by John Doe." in result
        assert "@" not in result.split("by ")[1]  # No @ after "by"

    def test_format_with_scope(self):
        """Format entry with scope."""
        pc = MockParsedCommit(
            commit=MockCommit(),
            scope="api",
            description="handle null response (#456)",
        )

        result = _format_commit_entry(
            pc,
            github_url="https://github.com/owner/repo",
        )

        assert "**api:**" in result

    def test_format_without_pr_number(self):
        """Format entry without PR number shows commit link."""
        pc = MockParsedCommit(
            commit=MockCommit(sha="abc123def", short_sha="abc123d"),
            description="direct commit",
        )

        result = _format_commit_entry(
            pc,
            github_url="https://github.com/owner/repo",
            github_username="johndoe",
        )

        assert "Commit [abc123d]" in result
        assert "/commit/abc123def" in result
        assert "John Doe (@johndoe)" in result

    def test_format_without_github_url(self):
        """Format entry without GitHub URL shows plain references."""
        pc = MockParsedCommit(
            commit=MockCommit(short_sha="abc123d"),
            description="some change (#789)",
        )

        result = _format_commit_entry(pc, github_url=None)

        assert "PR #789" in result
        assert "http" not in result

    def test_format_with_type_emoji(self):
        """Format entry with type emoji."""
        pc = MockParsedCommit(
            commit=MockCommit(),
            commit_type="feat",
            description="add feature (#1)",
        )

        result = _format_commit_entry(
            pc,
            github_url="https://github.com/owner/repo",
            include_type_emoji=True,
        )

        assert "✨" in result


class TestGeneratePrBody:
    """Tests for _generate_pr_body function."""

    def test_generate_body_with_github_usernames(self):
        """Generate PR body with GitHub usernames for authors."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(sha="abc123", author_name="John Doe"),
                commit_type="feat",
                description="add feature (#1)",
            ),
            MockParsedCommit(
                commit=MockCommit(sha="def456", author_name="Jane Smith"),
                commit_type="fix",
                description="fix bug (#2)",
            ),
        ]

        sha_to_username: dict[str, str | None] = {
            "abc123": "johndoe",
            "def456": "janesmith",
        }

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(1, 0, 0),
            next_version=Version(1, 1, 0),
            parsed_commits=commits,
            github_url="https://github.com/owner/repo",
            sha_to_username=sha_to_username,
        )

        assert "John Doe (@johndoe)" in body
        assert "Jane Smith (@janesmith)" in body

    def test_generate_body_mixed_usernames(self):
        """Generate PR body with some authors having usernames, some not."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(sha="abc123", author_name="John Doe"),
                commit_type="feat",
                description="add feature (#1)",
            ),
            MockParsedCommit(
                commit=MockCommit(sha="def456", author_name="External Dev"),
                commit_type="feat",
                description="add another feature (#2)",
            ),
        ]

        # Only one author has a GitHub username
        sha_to_username = {
            "abc123": "johndoe",
            "def456": None,
        }

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(1, 0, 0),
            next_version=Version(1, 1, 0),
            parsed_commits=commits,
            github_url="https://github.com/owner/repo",
            sha_to_username=sha_to_username,
        )

        assert "John Doe (@johndoe)" in body
        assert "External Dev" in body
        # External Dev should not have @ mention
        assert "External Dev (@" not in body

    def test_generate_body_no_username_mapping(self):
        """Generate PR body without username mapping."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(sha="abc123", author_name="John Doe"),
                commit_type="feat",
                description="add feature (#1)",
            ),
        ]

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(1, 0, 0),
            next_version=Version(1, 1, 0),
            parsed_commits=commits,
            github_url="https://github.com/owner/repo",
            sha_to_username=None,
        )

        assert "John Doe" in body
        # Should not have @ mention
        assert "(@" not in body

    def test_generate_body_first_release(self):
        """Generate PR body for first release."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(sha="abc123"),
                commit_type="feat",
                description="initial feature (#1)",
            ),
        ]

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(0, 1, 0),
            next_version=Version(0, 1, 0),
            parsed_commits=commits,
            is_first_release=True,
            github_url="https://github.com/owner/repo",
        )

        assert "First release" in body or "🎉" in body
        assert "Initial version" in body

    def test_generate_body_breaking_changes(self):
        """Generate PR body with breaking changes highlighted."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(sha="abc123", author_name="John Doe"),
                commit_type="feat",
                description="breaking change (#1)",
                is_breaking=True,
            ),
        ]

        sha_to_username: dict[str, str | None] = {"abc123": "johndoe"}

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(1, 0, 0),
            next_version=Version(2, 0, 0),
            parsed_commits=commits,
            github_url="https://github.com/owner/repo",
            sha_to_username=sha_to_username,
        )

        assert "Breaking Changes" in body
        assert "John Doe (@johndoe)" in body

    def test_generate_body_contains_releasio_footer(self):
        """PR body contains releasio footer link."""
        commits = [
            MockParsedCommit(
                commit=MockCommit(),
                description="change (#1)",
            ),
        ]

        body = _generate_pr_body(
            project_name="myproject",
            current_version=Version(1, 0, 0),
            next_version=Version(1, 0, 1),
            parsed_commits=commits,
        )

        assert "releasio" in body.lower()
