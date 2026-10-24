from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

from handoff_brief.core import HandoffError, bundle


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "notes").mkdir()
        (self.root / "notes" / "goal.md").write_text("Goal: fix the import path.\n", encoding="utf-8")
        (self.root / "notes" / "status.txt").write_text("Tests: 8 passed.\nNext: verify install.\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_source_labelled_bundle_is_deterministic_and_contains_only_selected_notes(self):
        first = bundle(self.root, ["notes/status.txt", "notes/goal.md"])
        second = bundle(self.root, ["notes/status.txt", "notes/goal.md"])
        self.assertEqual(first, second)
        self.assertIn("## Source: `notes/status.txt`", first)
        self.assertIn("## Source: `notes/goal.md`", first)
        self.assertLess(first.index("notes/status.txt"), first.index("notes/goal.md"))
        self.assertNotIn(str(self.root), first)
        self.assertNotIn("Goal: fix the import path", first.split("notes/status.txt", 1)[1].split("notes/goal.md", 1)[0])
        self.assertIn("not a transcript or verified project state", first)

    def test_bundle_reads_only_requested_sources(self):
        (self.root / "private.md").write_text("unselected secret", encoding="utf-8")
        result = bundle(self.root, ["notes/goal.md"])
        self.assertNotIn("unselected secret", result)

    def test_markdown_fence_grows_to_preserve_nested_backticks(self):
        (self.root / "notes" / "code.md").write_text("example: ````\n", encoding="utf-8")
        result = bundle(self.root, ["notes/code.md"])
        self.assertIn("`````text", result)
        self.assertIn("example: ````", result)

    def test_markdown_path_is_safely_quoted(self):
        path = self.root / "notes" / "a`b.md"
        path.write_text("note", encoding="utf-8")
        result = bundle(self.root, ["notes/a`b.md"])
        self.assertIn("## Source: ``notes/a`b.md``", result)

    def test_root_symlink_is_rejected(self):
        link = self.root.parent / (self.root.name + "-link")
        try:
            link.symlink_to(self.root, target_is_directory=True)
            with self.assertRaisesRegex(HandoffError, "root directory"):
                bundle(link, ["notes/goal.md"])
        finally:
            link.unlink(missing_ok=True)

    def test_absolute_and_parent_paths_are_rejected(self):
        for source in [str(self.root / "notes" / "goal.md"), "../outside.md", "notes/../../outside.md"]:
            with self.subTest(source=source), self.assertRaises(HandoffError):
                bundle(self.root, [source])

    def test_hidden_source_or_directory_is_rejected(self):
        (self.root / ".hidden").mkdir()
        (self.root / ".hidden" / "note.md").write_text("x", encoding="utf-8")
        (self.root / ".secret.md").write_text("x", encoding="utf-8")
        for source in [".secret.md", ".hidden/note.md"]:
            with self.subTest(source=source), self.assertRaisesRegex(HandoffError, "hidden"):
                bundle(self.root, [source])

    def test_symlink_source_is_rejected(self):
        link = self.root / "notes" / "link.md"
        link.symlink_to(self.root / "notes" / "goal.md")
        with self.assertRaisesRegex(HandoffError, "symlink"):
            bundle(self.root, ["notes/link.md"])

    def test_symlink_directory_is_rejected(self):
        (self.root / "elsewhere").symlink_to(self.root / "notes", target_is_directory=True)
        with self.assertRaises(HandoffError):
            bundle(self.root, ["elsewhere/goal.md"])

    def test_missing_and_outside_files_are_rejected(self):
        with self.assertRaisesRegex(HandoffError, "missing"):
            bundle(self.root, ["missing.md"])

    def test_non_text_extension_is_rejected(self):
        (self.root / "notes" / "source.py").write_text("print(1)", encoding="utf-8")
        with self.assertRaisesRegex(HandoffError, "Markdown"):
            bundle(self.root, ["notes/source.py"])

    def test_invalid_utf8_is_rejected_without_partial_output(self):
        (self.root / "notes" / "bad.md").write_bytes(b"\xff")
        with self.assertRaisesRegex(HandoffError, "UTF-8"):
            bundle(self.root, ["notes/goal.md", "notes/bad.md"])

    def test_nul_binary_file_is_rejected(self):
        (self.root / "notes" / "bad.md").write_bytes(b"text\x00data")
        with self.assertRaisesRegex(HandoffError, "Binary|binary"):
            bundle(self.root, ["notes/bad.md"])

    def test_terminal_escape_control_is_rejected(self):
        (self.root / "notes" / "terminal.md").write_text("\x1b[31mred\x1b[0m", encoding="utf-8")
        with self.assertRaisesRegex(HandoffError, "terminal control"):
            bundle(self.root, ["notes/terminal.md"])

    def test_fifo_is_rejected_without_blocking(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO not supported on this platform")
        os.mkfifo(self.root / "notes" / "pipe.md")
        with self.assertRaisesRegex(HandoffError, "regular file"):
            bundle(self.root, ["notes/pipe.md"])

    def test_per_file_limit_is_enforced(self):
        (self.root / "notes" / "large.md").write_bytes(b"x" * (64 * 1024 + 1))
        with self.assertRaisesRegex(HandoffError, "per-file"):
            bundle(self.root, ["notes/large.md"])

    def test_total_input_limit_is_enforced(self):
        (self.root / "a.md").write_bytes(b"x" * (64 * 1024))
        (self.root / "b.md").write_bytes(b"y" * (64 * 1024))
        (self.root / "c.md").write_bytes(b"z" * 1)
        with self.assertRaisesRegex(HandoffError, "total-input"):
            bundle(self.root, ["a.md", "b.md", "c.md"])

    def test_source_count_is_bounded(self):
        with self.assertRaisesRegex(HandoffError, "between 1 and 16"):
            bundle(self.root, ["notes/goal.md"] * 17)

    def test_duplicate_source_is_rejected(self):
        with self.assertRaisesRegex(HandoffError, "duplicate"):
            bundle(self.root, ["notes/goal.md", "notes/goal.md"])

    def test_output_character_budget_is_enforced(self):
        with self.assertRaisesRegex(HandoffError, "output limit"):
            bundle(self.root, ["notes/goal.md"], max_chars=100)
        with self.assertRaisesRegex(HandoffError, "output limit"):
            bundle(self.root, ["notes/goal.md"], max_chars=50_001)
        (self.root / "notes" / "long.md").write_text("x" * 600, encoding="utf-8")
        with self.assertRaisesRegex(HandoffError, "exceeds the 500-character"):
            bundle(self.root, ["notes/long.md"], max_chars=500)

    def test_non_directory_root_is_rejected(self):
        with self.assertRaisesRegex(HandoffError, "directory"):
            bundle(self.root / "notes" / "goal.md", ["goal.md"])


if __name__ == "__main__":
    unittest.main()
