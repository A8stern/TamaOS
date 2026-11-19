import json
import tempfile
import unittest
from pathlib import Path

from review_gate import LANES, REVIEW_SKILLS, validate_reviews


class ReviewGateTest(unittest.TestCase):
    commit = "a" * 40

    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def write_reports(self, root: Path, *, duplicate=False, blocking=False):
        review_dir = root / ".harness-state" / "reviews" / self.commit
        review_dir.mkdir(parents=True)
        for index, lane in enumerate(LANES):
            report = {
                "schema": 2,
                "commit": self.commit,
                "lane": lane,
                "skill": REVIEW_SKILLS[lane],
                "reviewer": "reviewer-0" if duplicate else f"reviewer-{index}",
                "verdict": "pass",
                "blocking_findings": ["bug"] if blocking and index == 0 else [],
                "notes": [],
            }
            (review_dir / f"{lane}.json").write_text(
                json.dumps(report), encoding="utf-8"
            )

    def test_accepts_three_independent_passing_reviews(self):
        root = self.make_root()
        self.write_reports(root)
        self.assertEqual([], validate_reviews(root, self.commit))

    def test_rejects_missing_review(self):
        root = self.make_root()
        self.write_reports(root)
        (root / ".harness-state" / "reviews" / self.commit / "architecture.json").unlink()
        self.assertTrue(any("missing review" in error for error in validate_reviews(root, self.commit)))

    def test_rejects_duplicate_reviewer(self):
        root = self.make_root()
        self.write_reports(root, duplicate=True)
        self.assertTrue(any("not independent" in error for error in validate_reviews(root, self.commit)))

    def test_rejects_whitespace_disguised_duplicate_reviewer(self):
        root = self.make_root()
        self.write_reports(root)
        review_dir = root / ".harness-state" / "reviews" / self.commit
        report = json.loads((review_dir / "architecture.json").read_text(encoding="utf-8"))
        report["reviewer"] = " reviewer-0 "
        (review_dir / "architecture.json").write_text(json.dumps(report), encoding="utf-8")
        self.assertTrue(any("not independent" in error for error in validate_reviews(root, self.commit)))

    def test_rejects_wrong_review_skill(self):
        root = self.make_root()
        self.write_reports(root)
        path = root / ".harness-state" / "reviews" / self.commit / "correctness.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        report["skill"] = "tamaos-review-architecture"
        path.write_text(json.dumps(report), encoding="utf-8")
        self.assertIn(
            "correctness: required skill is tamaos-review-correctness",
            validate_reviews(root, self.commit),
        )

    def test_rejects_blocking_finding(self):
        root = self.make_root()
        self.write_reports(root, blocking=True)
        self.assertIn(
            "correctness: unresolved blocking findings",
            validate_reviews(root, self.commit),
        )


if __name__ == "__main__":
    unittest.main()
