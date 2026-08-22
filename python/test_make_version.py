import unittest
from unittest.mock import patch

from make_version import MYSTERY_VERSION, Version, current_version


class VersionTest(unittest.TestCase):
    def test_clean_tag(self) -> None:
        version = Version("0.4.0", draft=False)

        self.assertEqual(version.label, "0.4.0")
        self.assertEqual(version.filename_version, "0.4.0")

    def test_dirty_tag(self) -> None:
        version = Version("0.4.0", draft=True)

        self.assertEqual(version.label, "0.4.0 (draft)")
        self.assertEqual(version.filename_version, "0.4.0-draft")

    def test_dirty_commit(self) -> None:
        version = Version("a1b2c3d", draft=True)

        self.assertEqual(version.filename_version, "a1b2c3d-draft")

    def test_clean_commit(self) -> None:
        version = Version("a1b2c3d", draft=False)

        self.assertEqual(version.filename_version, "a1b2c3d")

    def test_filename_sanitizes_tag(self) -> None:
        version = Version("release/0.4.0+β", draft=False)

        self.assertEqual(version.filename_version, "release-0.4.0")

    def test_unknown_version(self) -> None:
        version = Version(None, draft=True)

        self.assertEqual(version.label, "unknown (draft)")
        self.assertEqual(version.filename_version, MYSTERY_VERSION)

    @patch("make_version.git_output")
    def test_current_version_prefers_tag_and_removes_v(self, git_output) -> None:
        git_output.side_effect = ["v0.4.0", ""]

        self.assertEqual(current_version(), Version("0.4.0", draft=False))

    @patch("make_version.git_output")
    def test_current_version_falls_back_to_commit(self, git_output) -> None:
        git_output.side_effect = ["", "a1b2c3d", "changed"]

        self.assertEqual(current_version(), Version("a1b2c3d", draft=True))

    @patch("make_version.git_output", return_value=None)
    def test_current_version_handles_git_failure(self, git_output) -> None:
        self.assertEqual(current_version(), Version(None, draft=True))


if __name__ == "__main__":
    unittest.main()
