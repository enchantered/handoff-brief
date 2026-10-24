from __future__ import annotations

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from handoff_brief.__main__ import main


class CLITests(unittest.TestCase):
    def test_bundle_prints_only_the_markdown_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "note.md").write_text("One human-curated note.\n", encoding="utf-8")
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(["bundle", tmp, "note.md"])
            self.assertEqual(code, 0)
            self.assertIn("One human-curated note.", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")

    def test_invalid_path_returns_concise_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(["bundle", tmp, "../outside.md"])
            self.assertEqual(code, 2)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("error:", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
