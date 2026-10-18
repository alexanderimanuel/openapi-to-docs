# openapi-to-docs

Turn an **OpenAPI 3.x** spec (JSON or YAML) into clean **Markdown** API documentation: an index page plus one page per tag, or a single README-style file, with a field table and an example payload for every request and response.

Most small SaaS teams already have an OpenAPI file because their framework generates one, but the human-readable docs are missing or six months stale. This tool makes the spec the single source of truth: run it on every change and the Markdown is always current, readable on GitHub without a docs site, and reviewable in pull requests like any other code.

[![tests](https://github.com/alexanderimanuel/openapi-to-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/alexanderimanuel/openapi-to-docs/actions/workflows/ci.yml)

## Run it in three commands

```bash
git clone https://github.com/alexanderimanuel/openapi-to-docs.git && cd openapi-to-docs
pip install -e .
python -m openapi_to_docs examples/petstore/openapi.json -o docs
```

```
5 files written to docs (19 endpoints, 3 groups, 6 schemas)
```

That gives you `docs/README.md` (index), `docs/pet.md`, `docs/store.md`, `docs/user.md` and `docs/schemas.md`. Point it at your own spec instead of the Petstore one and you are done.

Two complete, committed results to browse:

| Spec | Format | Generated docs |
|---|---|---|
| [Swagger Petstore](examples/petstore/openapi.json) (OpenAPI 3.0.4) | JSON | [`examples/petstore/docs`](examples/petstore/docs/README.md) |
| [Redocly Museum API](examples/museum/openapi.yaml) (OpenAPI 3.1.0) | YAML | [`examples/museum/docs`](examples/museum/docs/README.md) |

## What the output looks like

This is `GET /pet/{petId}` from [`examples/petstore/docs/pet.md`](examples/petstore/docs/pet.md), exactly as generated:

> ## GET /pet/{petId}
>
> **Find pet by ID.**
>
> Returns a single pet.
>
> - **Auth:** `api_key` (API key in header `api_key`) or `petstore_auth` (OAuth 2.0, implicit flow; scopes `write:pets`, `read:pets`)
> - **Operation ID:** `getPetById`
>
> ### Parameters
>
> | Name | In | Type | Required | Description |
> |---|---|---|---|---|
> | `petId` | path | integer (int64) | yes | ID of pet to return. |
>
> ### Responses
>
> **200**: successful operation
>
> Content types: `application/json`, `application/xml`
>
> | Field | Type | Required | Description | Example |
> |---|---|---|---|---|
> | `id` | integer (int64) | no |  | `10` |
> | `name` | string | yes |  | `"doggie"` |
> | `category` | [Category](examples/petstore/docs/schemas.md#category) | no |  |  |
> | `category.id` | integer (int64) | no |  | `1` |
> | `category.name` | string | no |  | `"Dogs"` |
> | `photoUrls` | array of string | yes |  | `["string"]` |
> | `tags` | array of [Tag](examples/petstore/docs/schemas.md#tag) | no |  |  |
> | `tags[].id` | integer (int64) | no |  | `0` |
> | `tags[].name` | string | no |  | `"string"` |
> | `status` | string | no | pet status in the store. Allowed: `"available"`, `"pending"`, `"sold"`. | `"available"` |
>
> Example:
>
> ```json
> {
>   "id": 10,
>   "name": "doggie",
>   "category": { "id": 1, "name": "Dogs" },
>   "photoUrls": ["string"],
>   "tags": [{ "id": 0, "name": "string" }],
>   "status": "available"
> }
> ```
>
> **400**: Invalid ID supplied
>
> **404**: Pet not found

The Petstore spec has no example for `Pet`, so the payload above was generated from the schema. The `10`, `"doggie"` and `"Dogs"` values come from `example` fields on individual properties; the rest come from the types.

## What you get

**`README.md`, the index.** Title, version, contact and license from `info`; the description as written; a servers table; an **Authentication** section that explains every security scheme in plain words (where the API key goes, which OAuth flow and scopes, bearer format) and what the global default is; an endpoint table per group linking to each endpoint; links to every schema.

**One page per tag** (or per first path segment with `--group-by path`, which is also the automatic fallback for specs without tags). For every endpoint:

- method and path as the heading, so anchors are predictable (`pet.md#get-petpetid`)
- summary, description, deprecation notice, auth requirement, operation ID
- **parameters table**: name, location, type, required, description with allowed values, default, example and constraints
- **request body**: content types sharing a schema are listed once; a field table with nested fields as dotted paths (`category.id`, `tags[].name`), types, required, description and example per field; then a JSON example
- **responses**: every status code with its description, response headers, field table and example

**`schemas.md`.** Every schema under `components/schemas` with its description, field table and example, linked from the type columns.

**Examples that match the spec.** The spec's own examples are used first, wherever they live: media-type `example`, `examples` (including `$ref` to `components/examples`), schema `example`, `default`, `const`, `enum`. Only when none exists is a value generated from the type and `format` (`date-time`, `email`, `uuid`, `uri`, ...). `readOnly` fields are left out of request examples, `writeOnly` fields out of response examples.

**`$ref` resolved everywhere.** Schemas, parameters, request bodies, responses, headers, examples and path items. `allOf` is merged into one table; `oneOf` / `anyOf` variants are listed as `(Card).last4`; recursive schemas (a folder with child folders) are stopped and labelled instead of looping.

## Options

```
python -m openapi_to_docs --help

  spec                 path to the OpenAPI 3.x document (.json, .yaml or .yml)
  -o, --out PATH       output directory (default: docs). With --single-file, a .md path works too
  --single-file        one README-style document instead of one page per group
  --group-by tag|path  one page per tag (default) or per first path segment
  --no-schemas         skip the Schemas page; type names are shown without links
  --max-depth N        levels of nested objects to expand in field tables (default: 4)
  --title TEXT         override the API title from the spec
  --version            print the version and exit
```

Examples:

```bash
# One file you can paste into a wiki or ship as API.md
python -m openapi_to_docs openapi.yaml --single-file -o API.md

# No tags in your spec? Group by resource instead
python -m openapi_to_docs openapi.json --group-by path -o docs
```

Keep the docs current with two lines in CI; the job fails when someone changes the spec without regenerating:

```yaml
- run: python -m openapi_to_docs openapi.yaml -o docs
- run: git diff --exit-code docs
```

Output is deterministic (no timestamps), so regenerating an unchanged spec produces no diff.

## Limitations

What is not supported yet, so you can decide quickly whether this fits:

- **Swagger 2.0 / OpenAPI 2.** The tool stops with a clear message. Convert first, for example with [swagger-converter](https://converter.swagger.io/).
- **External `$ref`** (another file or a URL) raises an error. Bundle the spec into one document first (`redocly bundle` or `swagger-cli bundle`).
- **`oneOf` / `anyOf` examples** use the first variant; `discriminator` mappings are not used.
- **Callbacks, webhooks and links** are not rendered.
- **Server variables** and parameter serialization details (`style`, `explode`) are not rendered.
- **Non-JSON bodies** (XML, form, binary) get the field table but no generated example; an example is shown only when the spec provides one.
- **Markdown and HTML in descriptions** are passed through as written, not sanitized.
- **The output directory is not cleaned.** Renaming a tag leaves the old page behind; delete the directory first if that matters.

## How it works

```
openapi_to_docs/
  cli.py          argparse entry point; generate() loads the spec, builds pages, writes files
  loader.py       JSON/YAML reader with YAML 1.2 scalar rules (18:00 stays a string, not 1080);
                  rejects anything that is not OpenAPI 3.x
  refs.py         Resolver: follows #/... JSON pointers, keeps sibling keys (3.1), detects cycles
  examples.py     example payload for a schema: explicit values first, then type and format defaults
  schema.py       schema -> field rows with dotted paths and readable type labels; allOf merged
  security.py     security schemes and per-endpoint requirements as prose
  markdown.py     small Markdown builder: tables, GitHub-style heading anchors, cross-page links
  generate.py     walks the spec: groups endpoints, renders the index, tag pages and schemas page
examples/         two real public specs and the docs generated from them
tests/            pytest; small fixture specs for $ref resolution, parameter tables,
                  example generation and the CLI (multi-page, single-file, grouping, errors)
```

Design choices:

- **Markdown, not HTML.** It renders on GitHub, GitLab and in any wiki, diffs cleanly in pull requests and needs no build step or hosting. Teams that later adopt MkDocs or Docusaurus can feed these files straight in.
- **Links are resolved after rendering.** Headings get GitHub's anchor rules (`GET /pet/{petId}` becomes `#get-petpetid`, duplicates get `-1`), and every cross-reference is a placeholder until all pages exist, so links are right in both multi-page and single-file mode.
- **The spec's words win.** Descriptions are passed through unchanged, examples from the spec are preferred over generated ones, and tags keep the order the authors declared.
- **Two dependencies worth of trust.** PyYAML for YAML, pytest for tests, nothing else. The whole tool is about 1,200 lines you can read in an afternoon.
- **A test keeps the showcase honest.** `tests/test_cli.py` regenerates `examples/*/docs` and fails if the committed output drifts from what the code produces.

## Development

```bash
pip install -e ".[dev]"
pytest -q
```

To refresh the committed examples after changing the renderer:

```bash
python -m openapi_to_docs examples/petstore/openapi.json -o examples/petstore/docs
python -m openapi_to_docs examples/museum/openapi.yaml -o examples/museum/docs
```

The example specs are the public [Swagger Petstore](https://petstore3.swagger.io/) (Apache 2.0) and Redocly's [Museum API](https://github.com/Redocly/museum-openapi-example) (MIT), included unchanged.

## Author

Alexander Imanuel Widjanarko, Malang, Indonesia. AI engineer and researcher; I build scrapers, automations and integrations that replace manual work, plus the documentation to go with them.
[alexiw.my.id](https://alexiw.my.id) · [LinkedIn](https://www.linkedin.com/in/alexander-imanuel-widjanarko) · [Google Scholar](https://scholar.google.com/citations?user=t97LgJ4AAAAJ&hl=en)

MIT License.
