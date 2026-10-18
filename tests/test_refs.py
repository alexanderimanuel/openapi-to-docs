import pytest

from openapi_to_docs.examples import example_for
from openapi_to_docs.generate import Generator, Options
from openapi_to_docs.refs import RefError, Resolver
from openapi_to_docs.schema import field_rows, type_label

plain = str  # a Linker that renders schema names without links


def test_pointer_follows_json_pointer_escapes():
    doc = {"paths": {"/a/b": {"get": {"x": 1}}}, "components": {"schemas": {"A~B": {"type": "string"}}}}
    resolver = Resolver(doc)
    assert resolver.pointer("#/paths/~1a~1b/get/x") == 1
    assert resolver.pointer("#/components/schemas/A~0B") == {"type": "string"}
    assert resolver.pointer("#/paths/%7E1a%7E1b/get") == {"x": 1}  # URL-encoded form
    assert Resolver.name_of("#/components/schemas/A~0B") == "A~B"


def test_resolve_follows_chains_and_keeps_sibling_overrides():
    doc = {"components": {"schemas": {
        "Alias": {"$ref": "#/components/schemas/Target"},
        "Target": {"type": "string", "description": "target"},
    }}}
    resolver = Resolver(doc)
    node, name = resolver.resolve({"$ref": "#/components/schemas/Alias", "description": "closer"})
    assert node == {"type": "string", "description": "closer"}
    assert name == "Alias"
    assert resolver.resolve({"type": "integer"}) == ({"type": "integer"}, None)


def test_bad_references_raise_clear_errors():
    resolver = Resolver({"components": {"schemas": {"Loop": {"$ref": "#/components/schemas/Loop"}}}})
    with pytest.raises(RefError, match="unresolvable"):
        resolver.pointer("#/components/schemas/Missing")
    with pytest.raises(RefError, match="external"):
        resolver.resolve({"$ref": "other.yaml#/Pet"})
    with pytest.raises(RefError, match="circular"):
        resolver.resolve({"$ref": "#/components/schemas/Loop"})


def test_field_table_resolves_nested_refs_and_all_of(spec):
    doc = spec("refs.yaml")
    resolver = Resolver(doc)
    rows = field_rows({"$ref": "#/components/schemas/Folder"}, resolver, plain)
    by_name = {r.name: r for r in rows}

    # allOf merged FolderInput + Timestamps + inline children
    assert list(by_name) == ["name", "owner", "owner.id", "owner.email", "createdAt", "children"]
    assert by_name["name"].required is True
    assert by_name["createdAt"].required is True
    assert by_name["owner"].type == "User"
    assert by_name["owner.email"].type == "string (email)"
    # recursive Folder.children is labelled, not expanded forever
    assert by_name["children"].type == "array of Folder"
    assert "Recursive" in by_name["children"].description


def test_recursive_example_terminates(spec):
    resolver = Resolver(spec("refs.yaml"))
    value = example_for({"$ref": "#/components/schemas/Folder"}, resolver)
    assert value["name"] == "Invoices"
    assert value["owner"] == {"id": 7, "email": "user@example.com"}
    assert value["children"] == []  # nested Folder stops at the recursion


def test_type_label_links_objects_only(spec):
    resolver = Resolver(spec("refs.yaml"))
    link = lambda name: f"<{name}>"  # noqa: E731
    assert type_label({"$ref": "#/components/schemas/User"}, resolver, link) == "<User>"
    assert type_label({"type": "array", "items": {"$ref": "#/components/schemas/User"}}, resolver, link) == "array of <User>"
    assert type_label({"type": "string", "format": "uuid", "nullable": True}, resolver, link) == "string (uuid, nullable)"
    assert type_label({"type": "object", "additionalProperties": {"type": "integer"}}, resolver, link) == "map of integer"


def test_referenced_parameters_bodies_and_responses_are_rendered(spec):
    pages = Generator(spec("refs.yaml"), Options()).build()
    page = pages["folders.md"]
    assert "| `folderId` | path | string (uuid) | yes | Folder identifier. |" in page
    assert "**Required.** Folder to store" in page
    assert "**404**: No such folder" in page
    assert "| `code` | integer | no |  | `0` |" in page  # Error schema via components/responses
