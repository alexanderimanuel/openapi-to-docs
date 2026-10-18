"""Walk the spec and build the Markdown pages."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .examples import example_for, merge_all_of
from .markdown import Document, Slugger, filename_slug, finalize, link
from .refs import Resolver
from .schema import code, describe, field_rows, is_structured, one_line, type_label
from .security import requirement_text, scheme_details

HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")
INDEX = "README.md"
SCHEMAS_PAGE = "schemas.md"
PROJECT_URL = "https://github.com/alexanderimanuel/openapi-to-docs"


@dataclass
class Options:
    single_file: bool = False
    group_by: str = "tag"  # "tag" or "path"
    schemas: bool = True
    max_depth: int = 4
    title: str | None = None
    source_name: str = "openapi spec"


@dataclass
class Endpoint:
    method: str
    path: str
    operation: dict
    path_item: dict


@dataclass
class Group:
    name: str
    description: str = ""
    external_docs: dict | None = None
    endpoints: list[Endpoint] = field(default_factory=list)
    filename: str = ""


def collect_endpoints(doc: dict, resolver: Resolver) -> list[Endpoint]:
    """Every (method, path) in the spec, in document order."""
    endpoints: list[Endpoint] = []
    for path, raw_item in (doc.get("paths") or {}).items():
        item = resolver.deref(raw_item)
        if not isinstance(item, dict):
            continue
        for method, operation in item.items():
            if method in HTTP_METHODS and isinstance(operation, dict):
                endpoints.append(Endpoint(method, str(path), operation, item))
    return endpoints


def group_endpoints(endpoints: list[Endpoint], doc: dict, group_by: str) -> list[Group]:
    """One group per tag (declared tags first, in their order) or per first path segment."""
    if group_by == "tag" and not any(ep.operation.get("tags") for ep in endpoints):
        group_by = "path"  # nothing is tagged, so group by resource instead

    groups: dict[str, Group] = {}
    if group_by == "tag":
        for tag in doc.get("tags") or []:
            if isinstance(tag, dict) and tag.get("name"):
                groups[tag["name"]] = Group(tag["name"], tag.get("description") or "", tag.get("externalDocs"))
        for ep in endpoints:
            tags = ep.operation.get("tags") or ["Other"]
            name = str(tags[0])
            groups.setdefault(name, Group(name)).endpoints.append(ep)
    else:
        for ep in endpoints:
            segment = ep.path.strip("/").split("/")[0] if ep.path.strip("/") else ""
            name = segment.strip("{}") or "root"
            groups.setdefault(name, Group(name)).endpoints.append(ep)

    result = [g for g in groups.values() if g.endpoints]
    taken = Slugger(reserved=[filename_slug(INDEX[:-3]), filename_slug(SCHEMAS_PAGE[:-3])])
    for group in result:
        group.filename = taken.slug(filename_slug(group.name)) + ".md"
    return result


class Generator:
    def __init__(self, doc: dict, options: Options | None = None):
        self.doc = doc
        self.options = options or Options()
        self.resolver = Resolver(doc)
        self.info = doc.get("info") or {}
        components = doc.get("components") or {}
        self.schemas: dict = components.get("schemas") or {}
        self.security_schemes: dict = {
            name: self.resolver.deref(s) for name, s in (components.get("securitySchemes") or {}).items()
        }
        self.endpoints = collect_endpoints(doc, self.resolver)
        self.groups = group_endpoints(self.endpoints, doc, self.options.group_by)

    # --- entry point -----------------------------------------------------------------------------

    def build(self) -> dict[str, str]:
        """Return {filename: markdown}. Single-file mode returns one entry, keyed by INDEX."""
        opts = self.options
        if opts.single_file:
            doc = Document(INDEX)
            self.render_index(doc, pages=False)
            for group in self.groups:
                self.render_group(doc, group, level=2)
            if opts.schemas and self.schemas:
                self.render_schemas(doc, level=2)
            self.render_footer(doc)
            return finalize([doc])

        index = Document(INDEX)
        self.render_index(index, pages=True)
        self.render_footer(index)
        docs = [index]
        for group in self.groups:
            page = Document(group.filename)
            self.render_group(page, group, level=1)
            docs.append(page)
        if opts.schemas and self.schemas:
            page = Document(SCHEMAS_PAGE)
            self.render_schemas(page, level=1)
            docs.append(page)
        return finalize(docs)

    # --- helpers ---------------------------------------------------------------------------------

    def schema_link(self, name: str) -> str:
        return link(f"schema:{name}", name)

    def title(self) -> str:
        return self.options.title or self.info.get("title") or "API"

    def auth_text(self, operation: dict) -> str | None:
        security = operation["security"] if "security" in operation else self.doc.get("security")
        return requirement_text(security, self.security_schemes)

    @staticmethod
    def json_like(media_type: str) -> bool:
        return "json" in media_type.lower()

    def media_groups(self, content: dict) -> list[tuple[list[str], dict]]:
        """Media types that share one schema are documented once, e.g. JSON + XML + form."""
        groups: dict[str, tuple[list[str], dict]] = {}
        for media_type, media in content.items():
            media = self.resolver.deref(media) if isinstance(media, dict) else {}
            key = json.dumps(media.get("schema"), sort_keys=True, default=str)
            if key in groups:
                groups[key][0].append(media_type)
            else:
                groups[key] = ([media_type], media)
        ordered = sorted(groups.values(), key=lambda g: not any(self.json_like(m) for m in g[0]))
        return ordered

    def explicit_example(self, media: dict) -> tuple[Any, str | None]:
        """Example given in the spec: (value, external url). (None, None) when there is none."""
        if "example" in media:
            return media["example"], None
        examples = media.get("examples")
        if isinstance(examples, dict) and examples:
            first = self.resolver.deref(next(iter(examples.values())))
            if isinstance(first, dict):
                if "value" in first:
                    return first["value"], None
                if first.get("externalValue"):
                    return None, str(first["externalValue"])
        return None, None

    # --- index -----------------------------------------------------------------------------------

    def render_index(self, doc: Document, *, pages: bool) -> None:
        info = self.info
        doc.heading(1, self.title())

        meta = []
        if info.get("version"):
            meta.append(f"Version `{info['version']}`")
        if info.get("termsOfService"):
            meta.append(f"[Terms of service]({info['termsOfService']})")
        contact = info.get("contact") or {}
        if contact.get("email"):
            meta.append(f"Contact: [{contact.get('name') or contact['email']}](mailto:{contact['email']})")
        elif contact.get("url"):
            meta.append(f"Contact: [{contact.get('name') or contact['url']}]({contact['url']})")
        lic = info.get("license") or {}
        if lic.get("name"):
            meta.append(f"License: [{lic['name']}]({lic['url']})" if lic.get("url") else f"License: {lic['name']}")
        if meta:
            doc.para(" · ".join(meta))
        if info.get("summary"):
            doc.para(f"*{one_line(info['summary'])}*")
        if info.get("description"):
            doc.para(str(info["description"]))
        ext = self.doc.get("externalDocs") or {}
        if ext.get("url"):
            doc.para(f"More information: [{ext.get('description') or ext['url']}]({ext['url']})")

        servers = [s for s in (self.doc.get("servers") or []) if isinstance(s, dict) and s.get("url")]
        if servers:
            doc.heading(2, "Servers")
            doc.table(["URL", "Description"], [[f"`{s['url']}`", one_line(s.get("description"))] for s in servers])

        doc.heading(2, "Authentication")
        if self.security_schemes:
            lines: list[str] = []
            for name, scheme in self.security_schemes.items():
                lines += scheme_details(name, scheme)
            doc.block([("- " + ln if not ln.startswith("  ") else ln) for ln in lines])
            default = requirement_text(self.doc.get("security"), self.security_schemes)
            if default:
                doc.para(f"Unless an endpoint says otherwise, requests need: {default}.")
            else:
                doc.para("Each endpoint lists the scheme it accepts under **Auth**.")
        else:
            doc.para("This spec declares no security schemes.")

        doc.heading(2, "Endpoints")
        if not self.groups:
            doc.para("This spec declares no paths.")
        for group in self.groups:
            if pages:
                doc.heading(3, f"[{group.name}]({group.filename})")
            else:
                doc.para(f"**{link(f'group:{group.name}', group.name)}**")
            if group.description:
                doc.para(one_line(group.description))
            rows = []
            for ep in group.endpoints:
                path_link = link(f"op:{ep.method} {ep.path}", f"`{ep.path}`")
                summary = one_line(ep.operation.get("summary") or "")
                if ep.operation.get("deprecated"):
                    summary = f"{summary} (deprecated)".strip()
                rows.append([f"`{ep.method.upper()}`", path_link, summary])
            doc.table(["Method", "Path", "Summary"], rows)

        if pages and self.options.schemas and self.schemas:
            doc.heading(2, "Schemas")
            doc.para(", ".join(self.schema_link(name) for name in self.schemas))

    def render_footer(self, doc: Document) -> None:
        doc.rule()
        doc.para(f"Generated from `{self.options.source_name}` with [openapi-to-docs]({PROJECT_URL}).")

    # --- endpoints -------------------------------------------------------------------------------

    def render_group(self, doc: Document, group: Group, level: int) -> None:
        doc.heading(level, group.name, key=f"group:{group.name}")
        if level == 1:
            doc.para(f"Part of the [{self.title()}]({INDEX}) documentation.")
        if group.description:
            doc.para(str(group.description))
        ext = group.external_docs or {}
        if ext.get("url"):
            doc.para(f"[{ext.get('description') or ext['url']}]({ext['url']})")
        for ep in group.endpoints:
            self.render_endpoint(doc, ep, level + 1)

    def render_endpoint(self, doc: Document, ep: Endpoint, level: int) -> None:
        op = ep.operation
        doc.heading(level, f"{ep.method.upper()} {ep.path}", key=f"op:{ep.method} {ep.path}")
        if op.get("deprecated"):
            doc.para("> **Deprecated.** This endpoint may be removed in a future version.")
        summary = str(op.get("summary") or "").strip()
        description = str(op.get("description") or "").strip()
        if summary:
            doc.para(f"**{summary}**")
        if description and description.rstrip(".") != summary.rstrip("."):
            doc.para(description)

        facts: list[str] = []
        auth = self.auth_text(op)
        if auth:
            facts.append(f"**Auth:** {auth}")
        if op.get("operationId"):
            facts.append(f"**Operation ID:** `{op['operationId']}`")
        ext = op.get("externalDocs") or {}
        if ext.get("url"):
            facts.append(f"**More:** [{ext.get('description') or ext['url']}]({ext['url']})")
        doc.bullets(facts)

        params = self.merged_parameters(ep)
        if params:
            doc.heading(level + 1, "Parameters")
            doc.table(["Name", "In", "Type", "Required", "Description"],
                      [self.parameter_row(p) for p in params])

        body = self.resolver.deref(op.get("requestBody"))
        if isinstance(body, dict) and body.get("content"):
            doc.heading(level + 1, "Request body")
            flag = "**Required.**" if body.get("required") else "Optional."
            doc.para(f"{flag} {one_line(body.get('description'))}".strip())
            self.render_content(doc, body["content"], mode="request")

        doc.heading(level + 1, "Responses")
        responses = op.get("responses") or {}
        if not responses:
            doc.para("No responses documented.")
        for code in sorted(responses, key=self.response_order):
            response = self.resolver.deref(responses[code])
            if not isinstance(response, dict):
                continue
            doc.para(f"**{code}**: {one_line(response.get('description')) or 'No description.'}")
            headers = response.get("headers") or {}
            if headers:
                rows = []
                for name, header in headers.items():
                    header = self.resolver.deref(header)
                    if not isinstance(header, dict):
                        header = {}
                    htype = type_label(header["schema"], self.resolver, self.schema_link) if "schema" in header else "string"
                    rows.append([f"`{name}`", htype, one_line(header.get("description"))])
                doc.table(["Header", "Type", "Description"], rows)
            if response.get("content"):
                self.render_content(doc, response["content"], mode="response")

    @staticmethod
    def response_order(code: Any) -> tuple:
        text = str(code)
        if text.isdigit():
            return (0, int(text), text)
        if text.lower() == "default":
            return (2, 0, text)
        return (1, 0, text)

    def merged_parameters(self, ep: Endpoint) -> list[dict]:
        """Path-level parameters, overridden by operation-level ones with the same name and location."""
        merged: dict[tuple, dict] = {}
        for raw in list(ep.path_item.get("parameters") or []) + list(ep.operation.get("parameters") or []):
            param = self.resolver.deref(raw)
            if isinstance(param, dict):
                merged[(param.get("name"), param.get("in"))] = param
        order = {"path": 0, "query": 1, "header": 2, "cookie": 3}
        return sorted(merged.values(), key=lambda p: order.get(p.get("in"), 9))

    def parameter_row(self, param: dict) -> list[str]:
        schema = param.get("schema")
        if schema is None and isinstance(param.get("content"), dict) and param["content"]:
            schema = next(iter(param["content"].values())).get("schema")
        node = self.resolver.deref(schema) if schema is not None else {}
        node = merge_all_of(node, self.resolver) if isinstance(node, dict) else {}
        details = {k: v for k, v in node.items() if k != "description"}
        details["description"] = param.get("description")
        if param.get("deprecated"):
            details["deprecated"] = True
        text = describe(details)
        example = param.get("example", node.get("example"))
        if example is None and isinstance(param.get("examples"), dict) and param["examples"]:
            first = self.resolver.deref(next(iter(param["examples"].values())))
            example = first.get("value") if isinstance(first, dict) else None
        if example is not None:
            text = f"{text} Example: {code(example)}".strip()
        required = "yes" if param.get("required") or param.get("in") == "path" else "no"
        type_text = type_label(schema, self.resolver, self.schema_link) if schema is not None else "string"
        return [f"`{param.get('name', '')}`", str(param.get("in", "")), type_text, required, text]

    def render_content(self, doc: Document, content: dict, *, mode: str) -> None:
        for media_types, media in self.media_groups(content):
            label = "Content type" if len(media_types) == 1 else "Content types"
            doc.para(f"{label}: " + ", ".join(f"`{m}`" for m in media_types))
            schema = media.get("schema")
            if schema is not None:
                self.render_schema_table(doc, schema, mode=mode)

            value, external = self.explicit_example(media)
            explicit = value is not None
            if external:
                doc.para(f"Example: see {external}")
                continue
            if not explicit and schema is not None and is_structured(schema, self.resolver)                     and any(self.json_like(m) for m in media_types):
                value = example_for(schema, self.resolver, mode)
            if value is None:
                continue
            doc.para("Example:")
            if isinstance(value, str) and not any(self.json_like(m) for m in media_types):
                doc.code_block(value)
            else:
                doc.code_block(json.dumps(value, indent=2, ensure_ascii=False, default=str), "json")

    def render_schema_table(self, doc: Document, schema: Any, *, mode: str | None) -> None:
        node = self.resolver.deref(schema)
        label = type_label(schema, self.resolver, self.schema_link)
        if is_structured(schema, self.resolver):
            rows = field_rows(schema, self.resolver, self.schema_link, mode=mode, max_depth=self.options.max_depth)
            if rows:
                doc.table(["Field", "Type", "Required", "Description", "Example"],
                          [[f"`{r.name}`", r.type, "yes" if r.required else "no", r.description, r.example]
                           for r in rows])
                return
        detail = describe({k: v for k, v in node.items() if k != "description"}) if isinstance(node, dict) else ""
        doc.para(f"Type: {label}. {detail}".strip())

    # --- schemas ---------------------------------------------------------------------------------

    def render_schemas(self, doc: Document, level: int) -> None:
        doc.heading(level, "Schemas")
        if level == 1:
            doc.para(f"Data models used by the [{self.title()}]({INDEX}) endpoints.")
        for name, schema in self.schemas.items():
            doc.heading(level + 1, str(name), key=f"schema:{name}")
            node = self.resolver.deref(schema)
            if isinstance(node, dict) and node.get("description"):
                doc.para(str(node["description"]))
            if isinstance(node, dict) and node.get("deprecated"):
                doc.para("> **Deprecated.**")
            self.render_schema_table(doc, schema, mode=None)
            value = example_for(schema, self.resolver)
            if value is not None:
                doc.para("Example:")
                doc.code_block(json.dumps(value, indent=2, ensure_ascii=False, default=str), "json")
