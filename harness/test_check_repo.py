import os
import tempfile
import unittest
from pathlib import Path

from check_repo import check_repository


class RepositoryChecksTest(unittest.TestCase):
    def make_repo(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "harness").mkdir()
        (root / "harness" / "projects").write_text("", encoding="utf-8")
        return root

    def test_valid_relative_markdown_link(self):
        root = self.make_repo()
        (root / "target.md").write_text("# Target\n", encoding="utf-8")
        (root / "README.md").write_text("[target](target.md)\n", encoding="utf-8")
        self.assertEqual([], check_repository(root))

    def test_broken_relative_markdown_link(self):
        root = self.make_repo()
        (root / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")
        self.assertIn("README.md: broken relative link 'missing.md'", check_repository(root))

    def test_registered_project_requires_executable_adapter(self):
        root = self.make_repo()
        project = root / "app"
        project.mkdir()
        adapter = project / ".harness"
        adapter.write_text("#!/bin/sh\n", encoding="utf-8")
        os.chmod(adapter, 0o644)
        (root / "harness" / "projects").write_text("app\tapp\n", encoding="utf-8")
        self.assertIn("app/.harness: missing or not executable", check_repository(root))


if __name__ == "__main__":
    unittest.main()
