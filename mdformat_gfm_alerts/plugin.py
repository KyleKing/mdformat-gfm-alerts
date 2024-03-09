"""Public Plugin."""

from __future__ import annotations

from re import Pattern, compile
from typing import Callable, Mapping, NamedTuple

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdformat_admon.factories._factories import RenderType, default_render, new_token
from mdit_py_plugins.utils import is_code_block

PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

PATTERNS = {
    # Note '> ' prefix is removed when parsing
    compile(r"^\*\*(?P<title>Note|Warning)\*\*"),
    compile(r"^\\?\[!(?P<title>NOTE|TIP|IMPORTANT|WARNING|CAUTION)\\?\]"),
}


class AdmonState(NamedTuple):
    """Frozen state."""

    parentType: str
    lineMax: int


class AdmonitionData(NamedTuple):
    """AdmonitionData data for rendering."""

    old_state: AdmonState
    meta_text: str
    next_line: int


def search_alert_end(state: StateBlock, start_line: int, end_line: int) -> int:
    """Search for the end of the block."""
    next_line = start_line
    while True:
        next_line += 1
        if next_line >= end_line:
            break  # unclosed block should be auto closed by end of document.
        if not state.src[next_line].lstrip().startswith(">"):
            break

    return next_line


def parse_possible_blockquote_admon_factory(
    patterns: set[Pattern],
) -> Callable[[StateBlock, int, int, bool], AdmonitionData | bool]:
    """Accepts set of compiled regular expressions with a capture group `title`."""

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
        match = next((_m for pat in patterns if (_m := pat.match(text))), None)
        if not match:
            return False
        admon_meta_text = match["title"]

        # Since start is found, we can report success here in validation mode
        if silent:
            return True

        old_state = AdmonState(
            parentType=state.parentType,
            lineMax=state.lineMax,
        )
        state.parentType = "gfm_alert"

        next_line = search_alert_end(state, start_line, end_line)

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = next_line
        return AdmonitionData(
            old_state=old_state,
            meta_text=admon_meta_text,
            next_line=next_line,
        )

    return parse_possible_blockquote_admon


def format_gfm_alert_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    """Format markup."""
    title = f"[!{admonition.meta_text.upper()}]"

    with new_token(state, PREFIX, "div") as token:
        token.block = True
        token.attrs = {"class": "admonition"}
        token.info = title  # admonition.meta_text
        token.map = [start_line, admonition.next_line]

        with new_token(state, f"{PREFIX}_title", "p") as tkn_title:
            tkn_title.attrs = {"class": "admonition-title"}
            tkn_title.map = [start_line, start_line + 1]

            tkn_inline = state.push("inline", "", 0)
            tkn_inline.content = title
            tkn_inline.map = [start_line, start_line + 1]
            tkn_inline.children = []

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
    parser = parse_possible_blockquote_admon_factory(PATTERNS)
    result = parser(state, startLine, endLine, silent)
    if isinstance(result, AdmonitionData):
        format_gfm_alert_markup(state, startLine, admonition=result)
        return True
    return result


def gfm_alert_plugin_factory(
    prefix: str,
    logic: Callable[[StateBlock, int, int, bool], bool],
) -> Callable[[MarkdownIt, None | RenderType], None]:
    def gfm_alert_plugin(md: MarkdownIt, render: None | RenderType = None) -> None:
        render = render or default_render

        md.add_render_rule(f"{prefix}_open", render)
        md.add_render_rule(f"{prefix}_close", render)
        md.add_render_rule(f"{prefix}_title_open", render)
        md.add_render_rule(f"{prefix}_title_close", render)

        md.block.ruler.before("fence", prefix, logic)

    return gfm_alert_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser to identify Alerts."""
    mdit.use(gfm_alert_plugin_factory("gfm_alert", alert_logic))


def _render_gfm_alert(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode`."""
    prefix = node.markup.split(" ")[0]
    title = node.info.strip()
    title_line = f"{prefix} {title}"

    elements = [render for child in node.children if (render := child.render(context))]
    separator = "\n\n"

    content = separator.join(elements)

    return title_line + "\n" + content if content else title_line


def tbd(node: RenderTreeNode, context: RenderContext) -> str:
    title = ""
    # breakpoint()
    return title


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "gfm_alert": _render_gfm_alert,
    "gfm_alert_title": tbd,
}
