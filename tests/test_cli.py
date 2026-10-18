import re
from pathlib import Path

import pytest

from openapi_to_docs.cli import main

ROOT = Path(__file__).resolve().parent.parent


def test_multi_page_output_links_between_pages(fixture_path, tmp_path, capsys):
    assert main([str(fixture_path("tiny.yaml")), "-o", str(tmp_path)]) == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == ["README.md", "other.md", "owners.md", "pets.md", "schemas.md"]
    index = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert index.startswith("# Tiny API\n")
    assert "| `GET` | [`/pets`](pets.md#get-pets) | List pets |" in index
    assert "| `GET` | [`/health`](other.md#get-health) | Health check |" in index
    assert "**`bearer`**: HTTP bearer (JWT)." in index
    assert "Unless an endpoint says otherwise, requests need: `bearer` (HTTP bearer (JWT))." in index
    assert "[Pet](schemas.md#pet)" in index

    pets = (tmp_path / "pets.md").read_text(encoding="utf-8")
    assert "## GET /pets" in pets and "## POST /pets" in pets
    assert "- **Auth:** none required" in pets  # `security: []` on POST
    assert "| `[].name` | string | yes |  | `\"Rex\"` |" in pets
    assert "array of [Pet](schemas.md#pet)" not in pets  # arrays link via their rows, not the label

    out = capsys.readouterr().out
    assert "5 files written" in out and "(4 endpoints, 3 groups, 1 schemas)" in out


def test_single_file_mode_writes_one_document(fixture_path, tmp_path):
    target = tmp_path / "API.md"
    assert main([str(fixture_path("tiny.yaml")), "--single-file", "-o", str(target)]) == 0
    text = target.read_text(encoding="utf-8")
    assert list(tmp_path.iterdir()) == [target]
    # headings nest under one document and the overview links to in-page anchors
    assert "\n## pets\n" in text and "\n### GET /pets\n" in text and "\n#### Responses\n" in text
    assert "[`/pets`](#get-pets)" in text
    assert "\n## Schemas\n" in text and "\n### Pet\n" in text
    # a directory path puts the file at README.md inside it
    assert main([str(fixture_path("tiny.yaml")), "--single-file", "-o", str(tmp_path / "docs")]) == 0
    assert (tmp_path / "docs" / "README.md").exists()
    # schema links inside a single file point at in-page anchors
    assert main([str(fixture_path("refs.yaml")), "--single-file", "-o", str(tmp_path / "refs.md")]) == 0
    refs = (tmp_path / "refs.md").read_text(encoding="utf-8")
    assert "| `owner` | [User](#user) | no |" in refs


def test_group_by_path_and_no_schemas(fixture_path, tmp_path):
    assert main([str(fixture_path("tiny.yaml")), "--group-by", "path", "--no-schemas", "-o", str(tmp_path)]) == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == ["README.md", "health.md", "owners.md", "pets.md"]
    assert "## Schemas" not in (tmp_path / "README.md").read_text(encoding="utf-8")

    assert main([str(fixture_path("refs.yaml")), "--no-schemas", "-o", str(tmp_path / "refs")]) == 0
    folders = (tmp_path / "refs" / "folders.md").read_text(encoding="utf-8")
    assert "| `owner` | User | no |" in folders  # names stay as plain text
    assert "schemas.md" not in folders


def test_untagged_spec_falls_back_to_path_grouping(fixture_path, tmp_path):
    assert main([str(fixture_path("params.yaml")), "-o", str(tmp_path), "--title", "Items"]) == 0
    assert (tmp_path / "items.md").exists()
    assert (tmp_path / "README.md").read_text(encoding="utf-8").startswith("# Items\n")


def test_errors_are_reported_with_exit_code_1(tmp_path, capsys):
    swagger2 = tmp_path / "old.json"
    swagger2.write_text('{"swagger": "2.0", "info": {"title": "x"}}', encoding="utf-8")
    assert main([str(swagger2), "-o", str(tmp_path / "out")]) == 1
    assert "Swagger 2.0" in capsys.readouterr().err

    assert main([str(tmp_path / "missing.yaml"), "-o", str(tmp_path / "out")]) == 1
    assert "file not found" in capsys.readouterr().err

    broken = tmp_path / "broken.yaml"
    broken.write_text("openapi: 3.0.0\npaths:\n  /x:\n    get:\n      responses:\n        '200':\n          $ref: '#/nope'\n",
                      encoding="utf-8")
    assert main([str(broken), "-o", str(tmp_path / "out")]) == 1
    assert "unresolvable reference" in capsys.readouterr().err


@pytest.mark.parametrize("name", ["petstore", "museum"])
def test_showcase_docs_are_up_to_date(name, tmp_path):
    """examples/<name>/docs must match what the current code generates from examples/<name>/openapi.*"""
    example_dir = ROOT / "examples" / name
    spec = next(p for p in example_dir.iterdir() if p.suffix in (".json", ".yaml", ".yml"))
    assert main([str(spec), "-o", str(tmp_path)]) == 0
    committed = {p.name: p.read_text(encoding="utf-8") for p in (example_dir / "docs").glob("*.md")}
    fresh = {p.name: p.read_text(encoding="utf-8") for p in tmp_path.glob("*.md")}
    assert fresh == committed, "regenerate with: python -m openapi_to_docs examples/%s/%s -o examples/%s/docs" % (
        name, spec.name, name)


def test_generated_markdown_has_no_placeholder_leaks(fixture_path, tmp_path):
    main([str(fixture_path("examples.yaml")), "-o", str(tmp_path)])
    for page in tmp_path.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        assert not re.search(r"[\x00-\x02]", text), page.name
