"""Build example payloads from JSON Schema when the spec does not provide one."""

from __future__ import annotations

from typing import Any

from .refs import Resolver

# Plausible values for common `format`s. Anything else falls back to "string".
FORMAT_EXAMPLES: dict[str, str] = {
    "date": "2024-01-15",
    "date-time": "2024-01-15T09:30:00Z",
    "time": "09:30:00",
    "email": "user@example.com",
    "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "uri": "https://example.com/resource",
    "url": "https://example.com/resource",
    "hostname": "example.com",
    "ipv4": "192.168.0.1",
    "ipv6": "2001:db8::1",
    "byte": "U3dhZ2dlciByb2Nrcw==",
    "binary": "<binary data>",
    "password": "********",
}


def primary_type(node: dict) -> str | None:
    """The schema's main type. OpenAPI 3.1 allows a list such as ["string", "null"]."""
    t = node.get("type")
    if isinstance(t, list):
        non_null = [x for x in t if x != "null"]
        return non_null[0] if non_null else "null"
    if t is None:
        if "properties" in node or "additionalProperties" in node:
            return "object"
        if "items" in node:
            return "array"
    return t


def is_nullable(node: dict) -> bool:
    t = node.get("type")
    return bool(node.get("nullable")) or (isinstance(t, list) and "null" in t)


def merge_all_of(node: dict, resolver: Resolver) -> dict:
    """Flatten `allOf` into one object schema (properties and required are unioned)."""
    if not isinstance(node, dict) or not isinstance(node.get("allOf"), list):
        return node
    merged: dict = {k: v for k, v in node.items() if k != "allOf"}
    properties: dict = {}
    required: list[str] = []
    for part in node["allOf"]:
        part = merge_all_of(resolver.deref(part), resolver)
        if not isinstance(part, dict):
            continue
        for key, value in part.items():
            if key == "properties":
                properties.update(value)
            elif key == "required":
                required.extend(x for x in value if x not in required)
            elif key not in merged:
                merged[key] = value
    if properties:
        merged["properties"] = {**properties, **merged.get("properties", {})}
    if required:
        merged["required"] = required + [x for x in merged.get("required", []) if x not in required]
    merged.setdefault("type", "object")
    return merged


def example_for(schema: Any, resolver: Resolver, mode: str | None = None) -> Any:
    """Return an example value for `schema`.

    Explicit `example` / `examples` / `default` / `const` / `enum` values win; otherwise a value
    is generated from the type and format. `mode` is "request" (skips readOnly fields),
    "response" (skips writeOnly fields) or None.
    """
    return _Generator(resolver, mode).build(schema, ())


class _Generator:
    def __init__(self, resolver: Resolver, mode: str | None):
        self.resolver = resolver
        self.mode = mode

    def build(self, raw: Any, stack: tuple[str, ...]) -> Any:
        node, name = self.resolver.resolve(raw)
        if not isinstance(node, dict):
            return None
        if name and name in stack:
            # Recursive schema (e.g. a tree node whose children are nodes): stop here.
            t = primary_type(node)
            return [] if t == "array" else ({} if t == "object" else None)
        if name:
            stack = stack + (name,)

        for key in ("example", "const", "default"):
            if key in node:
                return node[key]
        if isinstance(node.get("examples"), list) and node["examples"]:
            return node["examples"][0]
        if isinstance(node.get("enum"), list) and node["enum"]:
            return node["enum"][0]

        if "allOf" in node:
            node = merge_all_of(node, self.resolver)
        for key in ("oneOf", "anyOf"):
            if isinstance(node.get(key), list) and node[key]:
                return self.build(node[key][0], stack)

        t = primary_type(node)
        if t == "object":
            return self._object(node, stack)
        if t == "array":
            items = node.get("items")
            if not isinstance(items, dict):
                return []
            item_name = self.resolver.resolve(items)[1]
            if item_name and item_name in stack:
                return []  # e.g. Folder.children: array of Folder
            value = self.build(items, stack)
            return [value] if value is not None else []
        if t == "string":
            return FORMAT_EXAMPLES.get(str(node.get("format", "")), "string")
        if t == "integer":
            return node.get("minimum", 0)
        if t == "number":
            return node.get("minimum", 0.0)
        if t == "boolean":
            return True
        return None

    def _object(self, node: dict, stack: tuple[str, ...]) -> dict:
        out: dict = {}
        for pname, praw in (node.get("properties") or {}).items():
            pnode = self.resolver.deref(praw)
            if isinstance(pnode, dict):
                if self.mode == "request" and pnode.get("readOnly"):
                    continue
                if self.mode == "response" and pnode.get("writeOnly"):
                    continue
            out[pname] = self.build(praw, stack)
        extra = node.get("additionalProperties")
        if not out and isinstance(extra, dict):
            out["key"] = self.build(extra, stack)
        elif not out and extra is True:
            out["key"] = "value"
        return out
