"""Resolve `$ref` pointers inside one OpenAPI document."""

from __future__ import annotations

from typing import Any
from urllib.parse import unquote


class RefError(ValueError):
    """A `$ref` could not be followed."""


def _unescape(part: str) -> str:
    # JSON Pointer escaping (RFC 6901): ~1 is '/', ~0 is '~'. URL escaping comes first.
    return unquote(part).replace("~1", "/").replace("~0", "~")


class Resolver:
    """Follows `#/...` references within a single document.

    External references (other files or URLs) are not supported and raise RefError.
    """

    def __init__(self, doc: dict):
        self.doc = doc

    def pointer(self, ref: str) -> Any:
        """Return the node a `#/a/b/c` reference points at."""
        if not ref.startswith("#"):
            raise RefError(f"external reference not supported: {ref}")
        node: Any = self.doc
        parts = ref[1:].split("/")
        if parts and parts[0] == "":
            parts = parts[1:]
        for raw_part in parts:
            part = _unescape(raw_part)
            if isinstance(node, list) and part.isdigit() and int(part) < len(node):
                node = node[int(part)]
            elif isinstance(node, dict) and part in node:
                node = node[part]
            else:
                raise RefError(f"unresolvable reference: {ref}")
        return node

    @staticmethod
    def name_of(ref: str) -> str:
        """`#/components/schemas/Pet` -> `Pet`."""
        return _unescape(ref.rsplit("/", 1)[-1])

    def resolve(self, node: Any) -> tuple[Any, str | None]:
        """Follow a chain of `$ref`s and return `(target, name)`.

        `name` is the last path segment of the outermost reference (`Pet` for
        `#/components/schemas/Pet`) or None when `node` was not a reference.
        Keys written next to `$ref` (allowed in OpenAPI 3.1, e.g. a `description`)
        are kept and override the target's own keys.
        """
        name: str | None = None
        seen: set[str] = set()
        overrides: dict = {}
        while isinstance(node, dict) and "$ref" in node:
            ref = node["$ref"]
            if not isinstance(ref, str):
                raise RefError(f"$ref must be a string, got {type(ref).__name__}")
            if ref in seen:
                raise RefError(f"circular reference: {ref}")
            seen.add(ref)
            siblings = {k: v for k, v in node.items() if k != "$ref"}
            overrides = {**siblings, **overrides}  # the outermost reference wins
            if name is None:
                name = self.name_of(ref)
            node = self.pointer(ref)
        if overrides and isinstance(node, dict):
            node = {**node, **overrides}
        return node, name

    def deref(self, node: Any) -> Any:
        """Like `resolve` but returns only the target."""
        return self.resolve(node)[0]
