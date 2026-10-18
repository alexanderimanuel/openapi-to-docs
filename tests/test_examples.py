from openapi_to_docs.examples import example_for
from openapi_to_docs.generate import Generator, Options
from openapi_to_docs.refs import Resolver


def test_examples_are_generated_from_types_formats_enums_and_defaults(spec):
    resolver = Resolver(spec("examples.yaml"))
    assert example_for({"$ref": "#/components/schemas/Account"}, resolver) == {
        "id": 0,
        "email": "user@example.com",
        "password": "********",
        "plan": "free",
        "createdAt": "2024-01-15T09:30:00Z",
        "tags": ["string"],
        "website": "https://example.com/resource",
        "settings": {"key": True},
    }
    assert example_for({"type": "integer", "minimum": 5}, resolver) == 5
    assert example_for({"type": "string", "default": "eu"}, resolver) == "eu"
    assert example_for({"type": "number"}, resolver) == 0.0
    assert example_for({"type": "boolean"}, resolver) is True
    assert example_for({"type": "string", "examples": ["first", "second"]}, resolver) == "first"


def test_request_and_response_modes_skip_read_only_and_write_only(spec):
    resolver = Resolver(spec("examples.yaml"))
    request = example_for({"$ref": "#/components/schemas/Account"}, resolver, mode="request")
    response = example_for({"$ref": "#/components/schemas/Account"}, resolver, mode="response")
    assert "id" not in request and "createdAt" not in request and "password" in request
    assert "password" not in response and "id" in response


def test_one_of_uses_first_variant_and_const_wins(spec):
    resolver = Resolver(spec("examples.yaml"))
    assert example_for({"$ref": "#/components/schemas/PaymentMethod"}, resolver) == {"kind": "card", "last4": "4242"}


def test_explicit_examples_take_precedence_in_pages(spec):
    pages = Generator(spec("examples.yaml"), Options()).build()
    page = pages["accounts.md"]
    # components/examples via $ref on the 201 response
    assert '"email": "ada@example.com"' in page
    assert '"plan": "pro"' in page
    # media-type `example` on the 400 response
    assert '"message": "email is required"' in page
    # generated request example skips readOnly fields
    request_part = page.split("### Responses")[0]
    assert '"password": "********"' in request_part
    assert '"createdAt"' not in request_part


def test_schemas_page_has_examples_and_descriptions(spec):
    pages = Generator(spec("examples.yaml"), Options()).build()
    page = pages["schemas.md"]
    assert "## PaymentMethod" in page
    assert "## Card" in page
    assert '"last4": "4242"' in page
