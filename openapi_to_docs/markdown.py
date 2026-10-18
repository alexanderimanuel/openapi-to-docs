"""A tiny Markdown builder with GitHub-style heading anchors and cross-page links."""

from __future__ import annotations

import re
from typing import Iterable, Sequence

# Links are written as placeholders while pages are being built, because the anchor of a
# heading is only known once every heading before it has been emitted. `finalize()` turns
# them into real links (or plain text when the target does not exist).
_LINK, _SEP, _END = "\x00", "\x01", "\x02"
_PLACEHOLDER = re.compile(f"{_LINK}(.*?){_SEP}(.*?){_END}")


def link(key: str, text: str) -> str:
    """Placeholder for a link to the heading registered under `key` (see Document.heading)."""
    return f"{_LINK}{key}{_SEP}{text}{_END}"


class Slugger:
    """GitHub's heading-anchor rules: lowercase, drop punctuation, spaces to '-', dedupe with -1, -2."""

    def __init__(self, reserved: Iterable[str] = ()):
        self.seen: dict[str, int] = {r: 1 for r in reserved}

    def slug(self, text: str) -> str:
        base = re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")
        n = self.seen.get(base, 0)
        self.seen[base] = n + 1
        return base if n == 0 else f"{base}-{n}"


def filename_slug(text: str) -> str:
    """`Special Events` -> `special-events`, for page file names."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "page"


class Document:
    """One output Markdown file."""

    def __init__(self, filename: str):
        self.filename = filename
        self.lines: list[str] = []
        self.slugger = Slugger()
        self.anchors: dict[str, str] = {}  # link key -> anchor in this file

    def heading(self, level: int, text: str, key: str | None = None) -> None:
        anchor = self.slugger.slug(text)
        if key is not None:
            self.anchors[key] = anchor
        self.lines += [f"{'#' * level} {text}", ""]

    def para(self, text: str) -> None:
        text = text.strip()
        if text:
            self.lines += [text, ""]

    def bullets(self, items: Sequence[str]) -> None:
        self.block([f"- {item}" for item in items])

    def block(self, lines: Sequence[str]) -> None:
        """Verbatim lines followed by a blank line (for nested lists and the like)."""
        if lines:
            self.lines += list(lines) + [""]

    def table(self, headers: Sequence[str], rows: Iterable[Sequence[str]]) -> None:
        def cell(value: object) -> str:
            return str(value).replace("\r", "").replace("\n", " ")

        self.lines.append("| " + " | ".join(headers) + " |")
        self.lines.append("|" + "|".join("---" for _ in headers) + "|")
        for row in rows:
            self.lines.append("| " + " | ".join(cell(c) for c in row) + " |")
        self.lines.append("")

    def code_block(self, text: str, lang: str = "") -> None:
        self.lines += [f"```{lang}", text.rstrip("\n"), "```", ""]

    def rule(self) -> None:
        self.lines += ["---", ""]

    def render(self) -> str:
        text = "\n".join(self.lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip("\n") + "\n"


def finalize(docs: Sequence[Document]) -> dict[str, str]:
    """Render every document and replace link placeholders with relative Markdown links."""
    targets: dict[str, tuple[str, str]] = {}
    for doc in docs:
        for key, anchor in doc.anchors.items():
            targets.setdefault(key, (doc.filename, anchor))

    out: dict[str, str] = {}
    for doc in docs:
        def replace(match: re.Match, current: str = doc.filename) -> str:
            key, text = match.group(1), match.group(2)
            if key not in targets:
                return text
            filename, anchor = targets[key]
            href = f"#{anchor}" if filename == current else f"{filename}#{anchor}"
            return f"[{text}]({href})"

        out[doc.filename] = _PLACEHOLDER.sub(replace, doc.render())
    return out
