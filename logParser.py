#!/usr/bin/env python3

"""File-system helpers used by the management console endpoints.

The functions in this module intentionally do not import Flask or inspect
``request``.  That keeps the file operations reusable from the REST handlers
and makes them straightforward to test.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from typing import Any


_WORD_PATTERN = re.compile(r"[\w]+(?:[-'][\w]+)*", re.UNICODE)


def list_files(directory: str | Path, recursive: bool = False) -> list[str]:
    """Return the files in ``directory`` in deterministic path order.

    Returned paths are strings so they can be passed directly to a JSON
    response.  Only regular files are included; directories and symlinks are
    excluded.  ``FileNotFoundError`` and ``NotADirectoryError`` are allowed to
    reach the caller so an endpoint can return an appropriate client error.
    """

    root = Path(directory)
    if not root.exists():
        raise FileNotFoundError(f"Directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    paths = root.rglob("*") if recursive else root.iterdir()
    return sorted(
        str(path)
        for path in paths
        if path.is_file() and not path.is_symlink()
    )


def count_words(file_path: str | Path) -> int:
    """Count word-like tokens in a UTF-8 text file.

    Words may contain internal hyphens or apostrophes, while punctuation and
    whitespace are separators.  ``Unicode`` word characters are supported.
    """

    path = _require_file(file_path)
    text = path.read_text(encoding="utf-8")
    return len(_WORD_PATTERN.findall(text))


def search_word(
    directory: str | Path,
    word: str,
    recursive: bool = False,
    case_sensitive: bool = False,
) -> list[dict[str, Any]]:
    """Find a whole-word match in UTF-8 files under ``directory``.

    Each result contains the file path, the number of matches, and the
    one-based line numbers containing at least one match.  Files that cannot
    be decoded as UTF-8 are skipped because they are not searchable text
    files; file-system and permission errors still propagate to the caller.
    """

    if not word or not word.strip():
        raise ValueError("word must not be empty")

    pattern = re.compile(
        rf"(?<![\w'-]){re.escape(word.strip())}(?![\w'-])",
        0 if case_sensitive else re.IGNORECASE,
    )
    results: list[dict[str, Any]] = []

    target = Path(directory)
    files = [str(target)] if target.is_file() else list_files(target, recursive=recursive)

    for file_path in files:
        path = Path(file_path)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        matching_lines = [
            line_number
            for line_number, line in enumerate(lines, start=1)
            if pattern.search(line)
        ]
        match_count = sum(
            len(pattern.findall(line))
            for line in lines
        )
        if match_count:
            results.append(
                {
                    "file": file_path,
                    "matches": match_count,
                    "lines": matching_lines,
                }
            )

    return results


def get_modified_date(file_path: str | Path) -> datetime:
    """Return a file's last-modified time as a timezone-aware datetime."""

    path = _require_file(file_path)
    return datetime.fromtimestamp(path.stat().st_mtime).astimezone()


def _require_file(file_path: str | Path) -> Path:
    """Validate and return a regular file path."""

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Not a file: {path}")
    return path
