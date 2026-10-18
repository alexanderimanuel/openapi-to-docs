"""Read an OpenAPI 3.x document from JSON or YAML."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


class SpecError(ValueError):
    """The input is not an OpenAPI 3.x document this tool can work with."""


class _Yaml12Loader(yaml.SafeLoader):
    """SafeLoader with YAML 1.2 scalar rules.

    PyYAML follows YAML 1.1, where `18:00` is the integer 1080, `2023-02-23` becomes a date
    object and `yes`/`no` are booleans. OpenAPI documents are written with YAML 1.2 tools, where
    all of those are plain strings, so the 1.1 resolvers are replaced here.
    """


_DROPPED_TAGS = {
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:timestamp",
    "tag:yaml.org,2002:value",
}
_Yaml12Loader.yaml_implicit_resolvers = {
    first: [(tag, regexp) for tag, regexp in resolvers if tag not in _DROPPED_TAGS]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
_Yaml12Loader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF"))
_Yaml12Loader.add_implicit_resolver(
    "tag:yaml.org,2002:int", re.compile(r"^(?:[-+]?[0-9]+|0x[0-9a-fA-F]+)$"), list("-+0123456789"))
_Yaml12Loader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"),
    list("-+.0123456789"))


def _construct_int(loader: yaml.SafeLoader, node: yaml.Node) -> int:
    value = loader.construct_scalar(node)
    return int(value, 16) if value.startswith("0x") else int(value, 10)


_Yaml12Loader.add_constructor("tag:yaml.org,2002:int", _construct_int)


def load_spec(path: str | Path) -> dict:
    """Load `path` (JSON or YAML, detected from the content) and check it is OpenAPI 3.x."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SpecError(f"{p}: file not found") from None
    return parse_spec(text, name=str(p))


def parse_spec(text: str, name: str = "<spec>") -> dict:
    """Parse spec text. JSON is tried when the text starts with '{', YAML otherwise."""
    if text.lstrip().startswith("{"):
        try:
            doc = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SpecError(f"{name}: invalid JSON ({exc})") from None
    else:
        try:
            doc = yaml.load(text, Loader=_Yaml12Loader)
        except yaml.YAMLError as exc:
            raise SpecError(f"{name}: invalid YAML ({exc})") from None

    if not isinstance(doc, dict):
        raise SpecError(f"{name}: expected a mapping at the top level")
    if "swagger" in doc and "openapi" not in doc:
        raise SpecError(f"{name}: this is a Swagger 2.0 document; only OpenAPI 3.x is supported")
    version = str(doc.get("openapi", ""))
    if not version.startswith("3."):
        raise SpecError(f"{name}: missing or unsupported 'openapi' version {version!r} (need 3.x)")
    return doc
