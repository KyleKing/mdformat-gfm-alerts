from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TypeVar

import mdformat
import pytest
from markdown_it.utils import read_fixture_file

from tests.helpers import print_text

T = TypeVar("T")


def flatten(nested_list: list[list[T]]) -> list[T]:
    return [*chain(*nested_list)]


def with_options(filename, options):
    fixtures = read_fixture_file(Path(__file__).parent / "fixtures" / filename)
    return [(*fix, options) for fix in fixtures]


fixtures = [
    *with_options("gfm_alerts.md", {}),
    *with_options("gfm_alerts_custom_title.md", {"custom_title": True}),
]


@pytest.mark.parametrize(
    ("line", "title", "text", "expected", "options"),
    fixtures,
    ids=[f[1] for f in fixtures],
)
def test_format_fixtures(line, title, text, expected, options):
    output = mdformat.text(text, extensions={"gfm_alerts"}, options=options)
    print_text(output, expected)
    assert output.rstrip() == expected.rstrip()
