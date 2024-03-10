"""Public Plugin."""

from __future__ import annotations

import re
from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, Mapping, NamedTuple

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.utils import is_code_block

if TYPE_CHECKING:
    from markdown_it.token import Token

PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

PATTERNS = {
    # Note '> ' prefix is removed when parsing
    r"^\*\*(?P<title>Note|Warning)\*\*",
    r"^\\?\[!(?P<title>NOTE|TIP|IMPORTANT|WARNING|CAUTION)\\?\]",
}
"""Patterns specific to GitHub Alerts."""


class AdmonState(NamedTuple):
    """Frozen state."""

    parentType: str
    lineMax: int


class AdmonitionData(NamedTuple):
    """AdmonitionData data for rendering."""

    old_state: AdmonState
    meta_text: str
    inline_content: str
    next_line: int


def parse_possible_blockquote_admon_factory(
    patterns: set[str],
) -> Callable[[StateBlock, int, int, bool], AdmonitionData | bool]:
    """Generate the parser function.

    Accepts set of strings that will be compiled into regular expressions.
    They must have a capture group `title`.

    """

    def parse_possible_blockquote_admon(
        state: StateBlock,
        start_line: int,
        end_line: int,
        silent: bool,
    ) -> AdmonitionData | bool:
        if is_code_block(state, start_line):
            return False

        start = state.bMarks[start_line] + state.tShift[start_line]

        # Exit if no match for any pattern
        text = state.src[start:]
        regexes = [
            re.compile(rf"{pat}(?P<inline_content>(?: |<br>)[^\n]+)?")
            for pat in patterns
        ]
        match = next((_m for rx in regexes if (_m := rx.match(text))), None)
        if not match:
            return False

        # Since start is found, we can report success here in validation mode
        if silent:
            return True

        old_state = AdmonState(
            parentType=state.parentType,
            lineMax=state.lineMax,
        )
        state.parentType = "gfm_alert"

        return AdmonitionData(
            old_state=old_state,
            meta_text=match["title"],
            inline_content=match["inline_content"] or "",
            next_line=end_line,
        )

    return parse_possible_blockquote_admon


# FYI: copied from mdformat_admon.factories
@contextmanager
def new_token(state: StateBlock, name: str, kind: str) -> Generator[Token, None, None]:
    """Creates scoped token."""
    yield state.push(f"{name}_open", kind, 1)
    state.push(f"{name}_close", kind, -1)


def format_gfm_alert_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    """Format markup."""
    with new_token(state, PREFIX, "div") as token:
        token.block = True
        token.attrs = {"class": "admonition"}
        token.info = f"[!{admonition.meta_text.upper()}]{admonition.inline_content}"
        token.map = [start_line, admonition.next_line]

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.line = admonition.next_line


def alert_logic(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    """Parse GitHub Alerts."""
    parser_func = parse_possible_blockquote_admon_factory(PATTERNS)
    result = parser_func(state, startLine, endLine, silent)
    if isinstance(result, AdmonitionData):
        format_gfm_alert_markup(state, startLine, admonition=result)
        return True
    return result


def gfm_alert_plugin_factory(
    prefix: str,
    logic: Callable[[StateBlock, int, int, bool], bool],
) -> Callable[[MarkdownIt], None]:
    """Generate the plugin function."""

    def gfm_alert_plugin(md: MarkdownIt) -> None:
        md.block.ruler.before("fence", prefix, logic)

    return gfm_alert_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser to identify Alerts."""
    mdit.use(gfm_alert_plugin_factory("gfm_alert", alert_logic))


def _render_gfm_alert(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode`."""
    title_line = node.info  # TODO: Maybe separate the inline_content?
    elements = [render for child in node.children if (render := child.render(context))]
    # Do not separate the title line from the first row
    return "\n".join([title_line, "\n\n".join(elements)])


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "gfm_alert": _render_gfm_alert,
}
