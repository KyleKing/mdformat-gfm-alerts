"""GitHub Alerts."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from markdown_it.token import Token

from mdformat_gfm_alerts._synced.alert_factories import (
    AlertMatch,
    blockquote_to_alert_factory,
    blockquote_to_div_plugin_factory,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from markdown_it.renderer import RendererHTML

GFM_ALERTS_PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

GFM_ALERT_OPEN = f"{GFM_ALERTS_PREFIX}_open"
GFM_ALERT_CLOSE = f"{GFM_ALERTS_PREFIX}_close"

DEFAULT_TITLES = ["TIP", "NOTE", "IMPORTANT", "WARNING", "CAUTION"]

# Pattern for [!NOTE] style alerts
PATTERN_BRACKET = re.compile(
    r"^(?P<marker>\\?\[!(?P<title>(?:TIP|NOTE|IMPORTANT|WARNING|CAUTION))\\?\])\s*(?P<inline>[^\n\r]*)?",
    re.IGNORECASE,
)

# Pattern for **Note**: style alerts
PATTERN_BOLD = re.compile(
    r"^(?P<marker>\*\*(?P<title>(?:Note|Warning))\*\*:?)\s*(?P<inline>[^\n\r]*)?",
    re.IGNORECASE,
)


def _render_alert_open(
    self: RendererHTML,  # noqa: ARG001
    tokens: Sequence[Token],
    idx: int,
    options,  # noqa: ANN001, ARG001
    env,  # noqa: ANN001, ARG001
) -> str:
    meta = tokens[idx].meta
    class_prefix = "markdown-alert"
    return (
        f'<div class="{class_prefix} {class_prefix}-{meta["title"].lower()}">\n'
        f'<p class="{class_prefix}-title">'
        f"{meta['icon']}{meta['title'].title()}</p>\n"
    )


def _render_alert_close(
    self: RendererHTML,  # noqa: ARG001
    tokens: Sequence[Token],  # noqa: ARG001
    idx: int,  # noqa: ARG001
    options,  # noqa: ANN001, ARG001
    env,  # noqa: ANN001, ARG001
) -> str:
    return "</div>\n"


def gfm_alerts_plugin(
    md: MarkdownIt,
    titles: list[str] | None = None,  # noqa: ARG001
    icons: dict[str, str] | None = None,
    class_prefix: str = "markdown-alert",  # noqa: ARG001
    *,
    parse_nested: bool = True,
    match_case_sensitive: bool = False,  # noqa: ARG001
) -> None:
    """Install the GFM alerts plugin.

    Args:
        md: MarkdownIt instance
        titles: List of alert titles to recognize (not yet implemented)
        icons: Dict mapping alert titles to icon strings
        class_prefix: CSS class prefix for alerts
        parse_nested: Whether to parse nested alerts
        match_case_sensitive: Whether to match case sensitively (not yet implemented)

    """
    if icons is None:
        icons = {}

    def _transform_to_alert(
        tokens: list[Token],
        start_index: int,
        end_index: int,
        alert_match: AlertMatch,
    ) -> None:
        """Transform blockquote tokens to GFM alert tokens."""
        # Get first inline token and strip the alert marker
        first_inline = next(
            (t for t in tokens[start_index : end_index + 1] if t.type == "inline"),
            None,
        )
        if first_inline:
            first_inline.content = first_inline.content[
                len(alert_match.marker) :
            ].lstrip()

        # Get icon for this alert type
        icon = icons.get(alert_match.title.lower(), "")

        # Transform open/close tokens
        open_token = tokens[start_index]
        close_token = tokens[end_index]

        open_token.type = GFM_ALERT_OPEN
        open_token.tag = "div"
        open_token.meta = {
            "title": alert_match.title,
            "icon": icon,
        }

        close_token.type = GFM_ALERT_CLOSE
        close_token.tag = "div"

    # Create and register the core rule using the generic factory
    core_rule = blockquote_to_alert_factory(
        GFM_ALERTS_PREFIX,
        [PATTERN_BRACKET, PATTERN_BOLD],
        _transform_to_alert,
        parse_nested=parse_nested,
    )
    md.core.ruler.after("block", GFM_ALERTS_PREFIX, core_rule)

    # Register HTML renderers for alert tokens
    md.add_render_rule(GFM_ALERT_OPEN, _render_alert_open, fmt="html")
    md.add_render_rule(GFM_ALERT_CLOSE, _render_alert_close, fmt="html")

    # Add blockquote-to-div conversion for accessibility
    blockquote_to_div_plugin = blockquote_to_div_plugin_factory(GFM_ALERTS_PREFIX)
    blockquote_to_div_plugin(md)
