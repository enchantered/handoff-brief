# Handoff Brief

A tiny, local-only Python utility for making a portable Markdown packet from project notes you **explicitly select**. Use it when one coding assistant needs a concise set of notes prepared for another.

The packet labels each source by its relative filename and includes its text in a Markdown code fence; trailing line-feed characters are trimmed for display, so it is not a lossless file archive. It does not capture private agent transcripts, inspect Git history, scan folders, run tests, contact a model or claim the handoff reflects current project state. It uses standard Markdown rather than defining a new memory protocol.

## Quick start

Python 3.11 or later; no installation and no third-party packages:

```sh
python3 -m handoff_brief bundle examples \
  handoff.md project-status.md
```

Why this project exists: see the [October 24 decision and evidence](docs/2026-10-24-decision.md), [dated behavior log](docs/consumer-behavior-log.md), and [portfolio arc](docs/portfolio-arc.md).

The command prints a Markdown packet to standard output. To save it, redirect output to a file you choose:

```sh
python3 -m handoff_brief bundle examples \
  handoff.md project-status.md > /tmp/handoff.md
```

Review `/tmp/handoff.md` before pasting it into another tool. Include only notes you are willing to share. Paths in the output are relative; the local root path is not included. The included example handoff is synthetic.

## Why these fields

A useful handoff states the goal, verified completed work, unresolved work, decisions, relevant tests and next step. Keep stable project instructions in your existing `AGENTS.md` or equivalent. Put only the current session's notes in `handoff.md`; do not copy the entire chat history. Mark tests as reported by a person unless separately verified. A new agent should verify the current checkout before acting.

This is intentionally a transport helper, not an autonomous memory agent. The source files remain the single human-reviewed input. The tool cannot tell whether a statement is true, current, complete or safe to share.

## Limits and safety

The CLI accepts 1–16 explicit relative `.md`/`.txt` paths under one trusted root. It rejects absolute paths, parent traversal, hidden paths, symlinks, non-regular files, invalid UTF-8, binary NUL bytes and terminal control characters. Limits are 64 KiB per file, 128 KiB combined input and 12,000 output characters by default; `--max-chars` can be set from 500 to 50,000. It never recursively searches or writes files.

Markdown can carry misleading instructions as well as useful context. The output wrapper and code fences preserve display boundaries; **they do not neutralize prompt injection** in source text. Review the packet and only share trusted notes. Use a trusted directory and avoid pasting into tools that should not receive the data. There is no secret detector, encryption, access control, provider adapter, test-result verification, automatic redaction or remote storage. Concurrent hostile filesystem mutation is outside this prototype's threat model.

The code and synthetic examples are original; no third-party source, dataset or media is bundled. This repository intentionally has no `LICENSE` file, so public visibility does not grant reuse rights. Research summaries link to their sources; each source remains under its own terms. No patent freedom-to-operate review has been performed.

## Tests

```sh
python3 -m unittest discover -s tests -v
python3 -m handoff_brief bundle examples handoff.md project-status.md
```

`handoff_brief/core.py` validates selected paths, enforces input bounds, reads only those files and renders fenced Markdown to a string. `handoff_brief/__main__.py` is a thin standard-library CLI. Regression tests cover path boundaries, special files, control characters, UTF-8, limits and deterministic output.
