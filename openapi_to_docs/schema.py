"""Turn JSON Schema objects into flat field tables with readable type labels."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Callable

from .examples import example_for, is_nullable, merge_all_of, primary_type
from .refs import Resolver

Linker = Callable[[str], str]  # schema name -> Markdown link text (or the plain name)

STRUCTURED = ("object", "array")
_PY_TYPE_NAMES = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}


@dataclass
class Field:
    """One row of a field table. `name` is the dotted path, e.g. `category.id` or `tags[].name`."""

    name: str
    type: str
    required: bool
    description: str
    example: str


def one_line(text: Any) -> str:
    """Collapse a description to one Markdown-table-safe line."""
    if text is None:
        return ""
    text = re.sub(r"\s*\n\s*", " ", str(text)).strip()
    return text.replace("|", "\\|")


def code(value: Any) -> str:
    """Render a value as inline code, JSON-style, for table cells."""
    text = json.dumps(value, ensure_ascii=False, default=str)
    if len(text) > 60:
        text = text[:57] + "..."
    return "`" + text.replace("|", "\\|").replace("`", "'") + "`"


def type_label(raw: Any, resolver: Resolver, link: Linker) -> str:
    """Human type for a schema: `string (date-time)`, `array of [Pet](...)`, `one of: A, B` ..."""
    node, name = resolver.resolve(raw)
    if not isinstance(node, dict) or node == {}:
        return "any"
    named = link(name) if name else None

    if "allOf" in node and primary_type(node) in (None, "object"):
        node = merge_all_of(node, resolver)

    for key, word in (("oneOf", "one of"), ("anyOf", "any of")):
        variants = node.get(key)
        if isinstance(variants, list) and variants:
            inner = ", ".join(type_label(v, resolver, link) for v in variants)
            label = f"{word}: {inner}"
            return f"{named} ({label})" if named else label

    t = primary_type(node)
    quals: list[str] = []
    if node.get("format"):
        quals.append(str(node["format"]))
    if is_nullable(node):
        quals.append("nullable")
    suffix = f" ({', '.join(quals)})" if quals else ""

    # Only objects carry a link to the Schemas page. A named string or array alias (`Date`,
    # `EventDates`) is clearer as its plain type, and the alias is still documented on that page.
    if t == "array":
        items = node.get("items")
        inner = type_label(items, resolver, link) if isinstance(items, dict) else "any"
        return f"array of {inner}{suffix}"
    if t == "object":
        extra = node.get("additionalProperties")
        if not node.get("properties") and extra not in (None, False):
            inner = type_label(extra, resolver, link) if isinstance(extra, dict) else "any"
            label = f"map of {inner}{suffix}"
        else:
            label = f"object{suffix}"
        if named:
            return named if label == "object" else f"{label} ({named})"
        return label
    if t is None:
        enum = node.get("enum")
        if isinstance(enum, list) and enum:
            t = _PY_TYPE_NAMES.get(type(enum[0]).__name__, "any")
        else:
            return "any"
    return f"{t}{suffix}"


def describe(node: Any, *, recursive: bool = False) -> str:
    """Description plus the constraints a reader cares about (allowed values, default, range)."""
    if not isinstance(node, dict):
        return ""
    parts: list[str] = []
    if node.get("description"):
        parts.append(one_line(node["description"]).rstrip("."))
    if node.get("deprecated"):
        parts.append("Deprecated")
    if recursive:
        parts.append("Recursive: same fields as the enclosing object")
    if isinstance(node.get("enum"), list):
        parts.append("Allowed: " + ", ".join(code(v) for v in node["enum"]))
    if "const" in node:
        parts.append("Always " + code(node["const"]))
    if "default" in node:
        parts.append("Default: " + code(node["default"]))
    lo, hi = node.get("minimum"), node.get("maximum")
    if lo is not None and hi is not None:
        parts.append(f"Range: {lo} to {hi}")
    elif lo is not None:
        parts.append(f"Minimum: {lo}")
    elif hi is not None:
        parts.append(f"Maximum: {hi}")
    lo, hi = node.get("minLength"), node.get("maxLength")
    if lo is not None and hi is not None:
        parts.append(f"Length: {lo} to {hi}")
    elif lo is not None:
        parts.append(f"Min length: {lo}")
    elif hi is not None:
        parts.append(f"Max length: {hi}")
    if node.get("pattern"):
        parts.append("Pattern: `" + str(node["pattern"]).replace("|", "\\|") + "`")
    if node.get("readOnly"):
        parts.append("Read-only")
    if node.get("writeOnly"):
        parts.append("Write-only")
    return ". ".join(parts) + ("." if parts else "")


def is_structured(raw: Any, resolver: Resolver) -> bool:
    """True when the schema is an object, array or composition (something a table can show)."""
    node = resolver.deref(raw)
    if not isinstance(node, dict):
        return False
    if any(k in node for k in ("allOf", "oneOf", "anyOf")):
        return True
    return primary_type(node) in STRUCTURED


def field_rows(raw: Any, resolver: Resolver, link: Linker, *, mode: str | None = None,
               max_depth: int = 4) -> list[Field]:
    """Flatten a schema into table rows, one per field, nested fields as dotted paths."""
    rows: list[Field] = []
    _Walker(resolver, link, mode, max_depth, rows).expand(raw, "", 0, ())
    return rows


class _Walker:
    def __init__(self, resolver: Resolver, link: Linker, mode: str | None, max_depth: int,
                 rows: list[Field]):
        self.resolver = resolver
        self.link = link
        self.mode = mode
        self.max_depth = max_depth
        self.rows = rows

    def hidden(self, node: Any) -> bool:
        if not isinstance(node, dict):
            return False
        if self.mode == "request":
            return bool(node.get("readOnly"))
        if self.mode == "response":
            return bool(node.get("writeOnly"))
        return False

    def example_cell(self, raw: Any, node: dict) -> str:
        if primary_type(node) == "object" or any(k in node for k in ("allOf", "oneOf", "anyOf")):
            return ""
        value = example_for(raw, self.resolver, self.mode)
        if value is None:
            return ""
        if isinstance(value, list) and any(isinstance(v, (dict, list)) for v in value):
            return ""
        return code(value)

    def refers_back(self, raw: Any, stack: tuple[str, ...]) -> bool:
        """True when `raw` is (or is an array of) a schema we are already inside of."""
        node, name = self.resolver.resolve(raw)
        if name and name in stack:
            return True
        if isinstance(node, dict) and primary_type(node) == "array" and isinstance(node.get("items"), dict):
            item_name = self.resolver.resolve(node["items"])[1]
            return bool(item_name and item_name in stack)
        return False

    def row(self, name: str, raw: Any, node: dict, required: bool, recursive: bool) -> None:
        self.rows.append(Field(
            name=name,
            type=type_label(raw, self.resolver, self.link),
            required=required,
            description=describe(node, recursive=recursive),
            example=self.example_cell(raw, node),
        ))

    def expand(self, raw: Any, path: str, depth: int, stack: tuple[str, ...]) -> None:
        node, name = self.resolver.resolve(raw)
        if not isinstance(node, dict):
            return
        if name and name in stack:
            return  # recursion: the row's description already says so
        if name:
            stack = stack + (name,)
        if depth > self.max_depth:
            return
        node = merge_all_of(node, self.resolver)

        for key in ("oneOf", "anyOf"):
            variants = node.get(key)
            if isinstance(variants, list) and variants:
                for i, variant in enumerate(variants, 1):
                    vname = self.resolver.resolve(variant)[1]
                    label = vname or f"option {i}"
                    self.expand(variant, f"{path} ({label})".strip(), depth, stack)
                return

        t = primary_type(node)
        if t == "array":
            items = node.get("items")
            if isinstance(items, dict):
                self.expand(items, f"{path}[]", depth, stack)
            return
        if t != "object":
            return

        required = set(node.get("required") or [])
        for pname, praw in (node.get("properties") or {}).items():
            pnode, pref = self.resolver.resolve(praw)
            if not isinstance(pnode, dict):
                pnode = {}
            if self.hidden(pnode):
                continue
            pnode = merge_all_of(pnode, self.resolver)
            fpath = f"{path}.{pname}" if path else pname
            self.row(fpath, praw, pnode, pname in required, self.refers_back(praw, stack))
            self.expand(praw, fpath, depth + 1, stack)

        extra = node.get("additionalProperties")
        if isinstance(extra, dict) and extra:
            fpath = f"{path}.<key>" if path else "<key>"
            enode = merge_all_of(self.resolver.deref(extra), self.resolver)
            if not isinstance(enode, dict):
                enode = {}
            self.row(fpath, extra, enode, False, False)
            self.expand(extra, fpath, depth + 1, stack)
