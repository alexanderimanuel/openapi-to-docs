"""Readable text for security schemes and per-endpoint security requirements."""

from __future__ import annotations

from .schema import one_line

FLOW_NAMES = {
    "implicit": "Implicit",
    "password": "Password",
    "clientCredentials": "Client credentials",
    "authorizationCode": "Authorization code",
}


def scheme_summary(scheme: dict) -> str:
    """Short label used next to an endpoint: `API key in header api_key`, `HTTP bearer (JWT)` ..."""
    kind = scheme.get("type")
    if kind == "apiKey":
        return f"API key in {scheme.get('in', 'header')} `{scheme.get('name', '?')}`"
    if kind == "http":
        text = f"HTTP {scheme.get('scheme', 'basic')}"
        if scheme.get("bearerFormat"):
            text += f" ({scheme['bearerFormat']})"
        return text
    if kind == "oauth2":
        flows = list((scheme.get("flows") or {}).keys())
        names = ", ".join(FLOW_NAMES.get(f, f).lower() for f in flows)
        return f"OAuth 2.0, {names} flow" if len(flows) == 1 else ("OAuth 2.0" + (f", {names} flows" if flows else ""))
    if kind == "openIdConnect":
        return "OpenID Connect"
    if kind == "mutualTLS":
        return "mutual TLS"
    return str(kind or "unknown scheme")


def scheme_details(name: str, scheme: dict) -> list[str]:
    """Bullet lines for the Authentication section of the index page."""
    lines = [f"**`{name}`**: {scheme_summary(scheme)}."]
    if scheme.get("description"):
        lines[0] += " " + one_line(scheme["description"])
    kind = scheme.get("type")
    if kind == "oauth2":
        for flow_name, flow in (scheme.get("flows") or {}).items():
            urls = [f"{label} {flow[key]}" for key, label in (("authorizationUrl", "authorize at"),
                                                                ("tokenUrl", "token at"),
                                                                ("refreshUrl", "refresh at")) if flow.get(key)]
            lines.append(f"  - {FLOW_NAMES.get(flow_name, flow_name)} flow: " + ", ".join(urls) if urls
                         else f"  - {FLOW_NAMES.get(flow_name, flow_name)} flow")
            scopes = flow.get("scopes") or {}
            if scopes:
                lines.append("  - Scopes: " + ", ".join(
                    f"`{s}` ({one_line(d)})" if d else f"`{s}`" for s, d in scopes.items()))
    elif kind == "openIdConnect" and scheme.get("openIdConnectUrl"):
        lines.append(f"  - Discovery document: {scheme['openIdConnectUrl']}")
    return lines


def requirement_text(security: list[dict] | None, schemes: dict) -> str | None:
    """`[{"a": []}, {"b": ["x"]}]` -> "`a` (...) or `b` (...; scopes `x`)". None when unspecified."""
    if security is None:
        return None
    if not security:
        return "none required"
    alternatives: list[str] = []
    for requirement in security:
        if not requirement:
            alternatives.append("none (optional)")
            continue
        parts: list[str] = []
        for name, scopes in requirement.items():
            scheme = schemes.get(name)
            detail = scheme_summary(scheme) if isinstance(scheme, dict) else "scheme not declared in components"
            if scopes:
                detail += "; scopes " + ", ".join(f"`{s}`" for s in scopes)
            parts.append(f"`{name}` ({detail})")
        alternatives.append(" and ".join(parts))
    return " or ".join(alternatives)
