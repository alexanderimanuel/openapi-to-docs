from openapi_to_docs.generate import Generator, Options
from openapi_to_docs.refs import Resolver
from openapi_to_docs.schema import describe, field_rows, one_line


def _parameter_table(page: str) -> list[str]:
    lines = page.splitlines()
    start = lines.index("| Name | In | Type | Required | Description |")
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append(line)
    return rows


def test_parameters_merge_override_and_sort_by_location(spec):
    pages = Generator(spec("params.yaml"), Options()).build()
    rows = _parameter_table(pages["items.md"])
    assert rows == [
        "| `itemId` | path | integer (int64) | yes | Item identifier. |",
        "| `expand` | query | array of string | no | Related objects to include. |",
        "| `format` | query | string | no | Deprecated. Default: `\"json\"`. Example: `\"xml\"` |",
        "| `X-Trace` | header | string | no | Overridden at operation level. |",
        "| `session` | cookie | string | no | Length: 8 to 64. |",
    ]


def test_describe_lists_constraints():
    node = {"description": "Page size.", "default": 10, "minimum": 1, "maximum": 100,
            "enum": [10, 50, 100], "readOnly": True}
    assert describe(node) == "Page size. Allowed: `10`, `50`, `100`. Default: `10`. Range: 1 to 100. Read-only."
    assert describe({}) == ""
    assert one_line("a | b\n  c") == "a \\| b c"


def test_field_rows_dotted_paths_maps_and_one_of(spec):
    doc = spec("examples.yaml")
    resolver = Resolver(doc)
    rows = field_rows({"$ref": "#/components/schemas/Account"}, resolver, str)
    names = [r.name for r in rows]
    assert names == ["id", "email", "password", "plan", "createdAt", "tags", "website", "settings", "settings.<key>"]
    by_name = {r.name: r for r in rows}
    assert by_name["email"].required is True
    assert by_name["plan"].description == "Allowed: `\"free\"`, `\"pro\"`."
    assert by_name["website"].type == "string (uri, nullable)"
    assert by_name["settings"].type == "map of boolean"
    assert by_name["tags"].example == '`["string"]`'

    # request mode hides readOnly fields, response mode hides writeOnly fields
    assert "id" not in [r.name for r in field_rows({"$ref": "#/components/schemas/Account"}, resolver, str, mode="request")]
    assert "password" not in [r.name for r in field_rows({"$ref": "#/components/schemas/Account"}, resolver, str, mode="response")]

    variants = field_rows({"$ref": "#/components/schemas/PaymentMethod"}, resolver, str)
    assert [r.name for r in variants] == ["(Card).kind", "(Card).last4", "(BankAccount).kind", "(BankAccount).iban"]
    assert variants[0].description == "Always `\"card\"`."
    assert variants[1].description == "Pattern: `^[0-9]{4}$`."


def test_max_depth_limits_expansion():
    doc = {"openapi": "3.0.0", "components": {"schemas": {"Deep": {
        "type": "object", "properties": {"a": {"type": "object", "properties": {"b": {"type": "object", "properties": {
            "c": {"type": "string"}}}}}}}}}}
    resolver = Resolver(doc)
    all_rows = [r.name for r in field_rows({"$ref": "#/components/schemas/Deep"}, resolver, str)]
    assert all_rows == ["a", "a.b", "a.b.c"]
    shallow = [r.name for r in field_rows({"$ref": "#/components/schemas/Deep"}, resolver, str, max_depth=1)]
    assert shallow == ["a", "a.b"]


def test_response_headers_and_content_grouping(spec):
    pages = Generator(spec("examples.yaml"), Options()).build()
    page = pages["payment-methods.md"]  # no tags in this spec, so pages are per path segment
    assert "Content type: `application/json`" in page
    assert "Content type: `text/csv`" in page
    assert "| `[] (Card).kind` | string | yes | Always `\"card\"`. | `\"card\"` |" in page
    # the csv example is given in the spec and rendered verbatim
    assert "```\nid,kind\n1,card\n```" in page
