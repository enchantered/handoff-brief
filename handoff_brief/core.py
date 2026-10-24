"""Compile explicitly selected local notes into a portable Markdown handoff."""
from __future__ import annotations

import os
from pathlib import Path
import re
import stat
import unicodedata

MAX_FILES = 16
MAX_FILE_BYTES = 64 * 1024
MAX_TOTAL_BYTES = 128 * 1024
MIN_OUTPUT_CHARS = 500
MAX_OUTPUT_CHARS = 50_000


class HandoffError(ValueError):
    """A safe, concise input error suitable for a command-line message."""


def _code_span(value: str) -> str:
    """Return a Markdown code span that safely contains untrusted path text."""
    longest = max((len(m.group()) for m in re.finditer(r"`+", value)), default=0)
    marker = "`" * (longest + 1)
    pad = " " if value.startswith("`") or value.endswith("`") or value.startswith(" ") or value.endswith(" ") else ""
    return f"{marker}{pad}{value}{pad}{marker}"


def _source_path(root: Path, raw: str) -> tuple[str, Path]:
    if not raw or any(ord(char) < 32 or ord(char) == 127 for char in raw):
        raise HandoffError("source path is empty or contains control characters")
    rel = Path(raw)
    if rel.is_absolute() or any(part == ".." for part in rel.parts):
        raise HandoffError("source paths must stay inside the root; absolute paths and '..' are not allowed")
    if not rel.parts or any(part.startswith(".") for part in rel.parts):
        raise HandoffError("hidden files and directories are not accepted as sources")
    if rel.suffix.lower() not in {".md", ".txt"}:
        raise HandoffError("sources must be Markdown (.md) or plain text (.txt)")

    current = root
    for part in rel.parts:
        current = current / part
        try:
            if current.is_symlink():
                raise HandoffError("symlink sources are not accepted")
        except OSError:
            raise HandoffError("cannot inspect source path") from None
    try:
        resolved = current.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError, RuntimeError):
        raise HandoffError("source file is missing or outside the selected root") from None
    return rel.as_posix(), resolved


def _read_source(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        raise HandoffError("cannot safely open a source file") from None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise HandoffError("every source must be a regular file")
        if info.st_size > MAX_FILE_BYTES:
            raise HandoffError("a source exceeds the 64 KiB per-file limit")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
    finally:
        os.close(fd)
    if len(data) > MAX_FILE_BYTES:
        raise HandoffError("a source exceeds the 64 KiB per-file limit")
    if b"\x00" in data:
        raise HandoffError("binary data is not accepted")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise HandoffError("every source must be UTF-8 text") from None
    if any(unicodedata.category(char) == "Cc" and char not in "\n\r\t" for char in text):
        raise HandoffError("terminal control characters are not accepted")
    return data


def bundle(root: str | Path, sources: list[str], max_chars: int = 12_000) -> str:
    """Render chosen Markdown/text sources as a bounded, source-labelled packet.

    The function never writes files, reads directories recursively, or contacts a
    model or service. The recipient still needs to review the content before sharing.
    """
    if not 1 <= len(sources) <= MAX_FILES:
        raise HandoffError(f"select between 1 and {MAX_FILES} source files")
    if not MIN_OUTPUT_CHARS <= max_chars <= MAX_OUTPUT_CHARS:
        raise HandoffError(f"output limit must be between {MIN_OUTPUT_CHARS} and {MAX_OUTPUT_CHARS} characters")
    base = Path(root)
    if base.is_symlink():
        raise HandoffError("root directory must not be a symlink")
    try:
        root_path = base.resolve(strict=True)
    except (OSError, RuntimeError):
        raise HandoffError("root directory is unavailable") from None
    if not root_path.is_dir():
        raise HandoffError("root path must be a directory")

    seen: set[str] = set()
    loaded: list[tuple[str, bytes]] = []
    total = 0
    for source in sources:
        display, path = _source_path(root_path, source)
        if display in seen:
            raise HandoffError("duplicate source path")
        seen.add(display)
        data = _read_source(path)
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise HandoffError("selected sources exceed the 128 KiB total-input limit")
        loaded.append((display, data))

    sections = [
        "# Portable project handoff",
        "",
        "> A source-labelled bundle of files selected by the user. It is not a transcript or verified project state.",
        "> Review every included line for private information, credentials, and instructions before sharing with another agent or service.",
        "",
    ]
    for display, data in loaded:
        text = data.decode("utf-8").rstrip("\n")
        runs = [len(match.group()) for match in re.finditer(r"`+", text)]
        fence = "`" * max(3, max(runs, default=0) + 1)
        sections.extend((f"## Source: {_code_span(display)}", "", fence + "text", text, fence, ""))
    rendered = "\n".join(sections).rstrip() + "\n"
    if len(rendered) > max_chars:
        raise HandoffError(f"rendered handoff exceeds the {max_chars}-character output limit; select fewer or shorter notes")
    return rendered
