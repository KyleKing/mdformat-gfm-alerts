"""GitHub Alerts."""

from __future__ import annotations

from markdown_it.rules_block import StateBlock

from mdformat_gfm_alerts.factories import (
    AlertData,
    gfm_alerts_plugin_factory,
    new_token,
    parse_possible_blockquote_admon_factory,
)

GFM_ALERTS_PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

INLINE_SEP = "\n\n"
"""Separator to differentiate the title and inline content (if present)."""

PATTERNS = {
    # Note '> ' prefix is removed when parsing and trailing ":" if found
    r"^\*\*(?P<title>Note|Warning)\*\*:?",
    # FYI: This is intentionally strict. Keep in sync with supported titles
    r"^\\?\[!(?P<title>NOTE|TIP|IMPORTANT|WARNING|CAUTION)\\?\]",
}
"""Patterns specific to GitHub Alerts."""


def format_gfm_alerts_markup(
    state: StateBlock,
    start_line: int,
    admonition: AlertData,
) -> None:
    """Format markup."""
    # To fix #2, when the admonition and text are on the same line, push the content
    #  to the next line. While this is equivalent in the markdown spec, this is
    #  required for Github
    newline = "\n"

    meta = f"[!{admonition.meta_text.upper()}]"
    title_line = f"{meta}{newline}{admonition.inline_content}".rstrip()

    with new_token(state, GFM_ALERTS_PREFIX, "div") as token:
        token.attrs = {
            "class": f"markdown-alert markdown-alert-{admonition.meta_text.lower()}",
        }
        token.block = True
        token.map = [start_line, admonition.next_line]
        token.markup = title_line
        with new_token(state, f"{GFM_ALERTS_PREFIX}_title", "p") as tkn_title:
            tkn_title.attrs = {"class": "markdown-alert-title"}

            tkn_title_txt = state.push("inline", "", 0)
            tkn_title_txt.content = admonition.meta_text.title()

        if admonition.inline_content:
            with new_token(state, f"{GFM_ALERTS_PREFIX}_inline", "p"):
                tkn_inline_txt = state.push("inline", "", 0)
                tkn_inline_txt.content = admonition.inline_content.strip()

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    # FIXME: this isn't actually replacing the block quote outer div?
    #
    # Render as a div for accessibility rather than block quote
    #   Which is because '>' is being misused (https://github.com/orgs/community/discussions/16925#discussioncomment-8729846)
    state.parentType = "div"  # admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.line = admonition.next_line


def alert_logic(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Parse GitHub Alerts."""
    parser_func = parse_possible_blockquote_admon_factory(GFM_ALERTS_PREFIX, PATTERNS)
    result = parser_func(state, start_line, end_line, silent)
    if isinstance(result, AlertData):
        format_gfm_alerts_markup(state, start_line, admonition=result)
        return True
    return result


gfm_alerts_plugin = gfm_alerts_plugin_factory(GFM_ALERTS_PREFIX, alert_logic)
