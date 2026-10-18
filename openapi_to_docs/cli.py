from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from . import __version__
from .generate import INDEX, Generator, Options
from .loader import SpecError, load_spec
from .refs import RefError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="openapi_to_docs",
        description="Generate readable Markdown API documentation from an OpenAPI 3.x spec (JSON or YAML).",
    )
    p.add_argument("spec", help="path to the OpenAPI 3.x document (.json, .yaml or .yml)")
    p.add_argument("-o", "--out", default="docs", metavar="PATH",
                   help="output directory (default: docs). With --single-file, a .md file path is also accepted")
    p.add_argument("--single-file", action="store_true",
                   help="write one README-style document instead of one page per group")
    p.add_argument("--group-by", choices=["tag", "path"], default="tag",
                   help="one page per tag (default) or per first path segment; "
                        "falls back to path when the spec has no tags")
    p.add_argument("--no-schemas", action="store_true", help="skip the Schemas page / section")
    p.add_argument("--max-depth", type=int, default=4, metavar="N",
                   help="how many levels of nested objects to expand in field tables (default: 4)")
    p.add_argument("--title", default=None, help="override the API title from the spec")
    p.add_argument("--version", action="version", version=f"openapi-to-docs {__version__}")
    return p


@dataclass
class Result:
    files: list[Path]
    endpoints: int
    groups: int
    schemas: int


def generate(spec_path: str | Path, out: str | Path, *, single_file: bool = False, group_by: str = "tag",
             schemas: bool = True, max_depth: int = 4, title: str | None = None) -> Result:
    """Load a spec and write the documentation. Returns the files written plus some counts."""
    spec_path = Path(spec_path)
    doc = load_spec(spec_path)
    options = Options(single_file=single_file, group_by=group_by, schemas=schemas, max_depth=max_depth,
                      title=title, source_name=spec_path.name)
    generator = Generator(doc, options)
    pages = generator.build()

    out = Path(out)
    if single_file:
        target = out if out.suffix.lower() == ".md" else out / INDEX
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(pages[INDEX], encoding="utf-8", newline="\n")
        files = [target]
    else:
        out.mkdir(parents=True, exist_ok=True)
        files = []
        for filename, text in pages.items():
            path = out / filename
            path.write_text(text, encoding="utf-8", newline="\n")
            files.append(path)
    return Result(files, len(generator.endpoints), len(generator.groups), len(generator.schemas))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = generate(args.spec, args.out, single_file=args.single_file, group_by=args.group_by,
                          schemas=not args.no_schemas, max_depth=args.max_depth, title=args.title)
    except (SpecError, RefError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    where = result.files[0] if args.single_file else Path(args.out)
    n = len(result.files)
    print(f"{n} file{'s' if n != 1 else ''} written to {where} "
          f"({result.endpoints} endpoints, {result.groups} groups, {result.schemas} schemas)")
    return 0
