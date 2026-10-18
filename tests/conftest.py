from pathlib import Path

import pytest

from openapi_to_docs.loader import load_spec

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_path():
    def _path(name: str) -> Path:
        return FIXTURES / name
    return _path


@pytest.fixture
def spec(fixture_path):
    def _spec(name: str) -> dict:
        return load_spec(fixture_path(name))
    return _spec
