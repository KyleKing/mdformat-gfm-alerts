"""GitHub Alerts."""

from __future__ import annotations

from markdown_it.rules_block import StateBlock

from ..factories import (
    AlertData,
    gfm_alert_plugin_factory,
    new_token,
    parse_possible_blockquote_admon_factory,
)

PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

PATTERNS = {
    # Note '> ' prefix is removed when parsing
    r"^\*\*(?P<title>Note|Warning)\*\*",
    r"^\\?\[!(?P<title>NOTE|TIP|IMPORTANT|WARNING|CAUTION)\\?\]",
}
"""Patterns specific to GitHub Alerts."""


def format_gfm_alert_markup(
    state: StateBlock,
    start_line: int,
    admonition: AlertData,
) -> None:
    """Format markup."""
    with new_token(state, PREFIX, "div") as token:
        token.block = True
        token.attrs = {"class": f"admonition {admonition.meta_text.lower()}"}
        token.info = f"[!{admonition.meta_text.upper()}]{admonition.inline_content}"
        token.map = [start_line, admonition.next_line]

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    # Render as a div for accessibility rather than block quote
    #   Which is because '>' is being misused (https://github.com/orgs/community/discussions/16925#discussioncomment-8729846)
    state.parentType = "div"
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
    if isinstance(result, AlertData):
        format_gfm_alert_markup(state, startLine, admonition=result)
        return True
    return result


gfm_alert_plugin = gfm_alert_plugin_factory(PREFIX, alert_logic)
