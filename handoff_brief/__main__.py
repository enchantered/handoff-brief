"""Command-line interface for user-selected project handoff notes."""
from __future__ import annotations

import argparse
import sys

from .core import HandoffError, MAX_OUTPUT_CHARS, MIN_OUTPUT_CHARS, bundle


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m handoff_brief",
        description="Bundle explicitly chosen local notes as a portable, source-labelled Markdown handoff.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    pack = sub.add_parser("bundle", help="compile selected Markdown/text files to standard output")
    pack.add_argument("root", help="trusted root directory containing the selected files")
    pack.add_argument("sources", nargs="+", help="1–16 relative .md/.txt source paths; no recursive scanning")
    pack.add_argument("--max-chars", type=int, default=12_000, help=f"maximum output characters ({MIN_OUTPUT_CHARS}–{MAX_OUTPUT_CHARS}; default 12000)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        output = bundle(args.root, args.sources, args.max_chars)
    except HandoffError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
