"""GitHub Alerts."""

from __future__ import annotations

import re
from collections.abc import Callable
from functools import cached_property

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

from mdformat_gfm_alerts._helpers import get_conf

GFM_ALERTS_PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

GFM_ALERT_OPEN = f"{GFM_ALERTS_PREFIX}_open"
GFM_ALERT_CLOSE = f"{GFM_ALERTS_PREFIX}_close"

DEFAULT_TITLES = ["TIP", "NOTE", "IMPORTANT", "WARNING", "CAUTION"]


class AlertRuleFactory:
    """Identifies blockquote tokens and transforms them to alert tokens."""

    def __init__(
        self,
        titles: list[str] | None = None,
        icons: dict[str, str] | None = None,
        class_prefix: str = "markdown-alert",
        *,
        parse_nested: bool = True,
        match_case_sensitive: bool = False,
        custom_title: bool = False,
    ) -> None:
        if titles is None:
            titles = DEFAULT_TITLES
        self.titles = titles
        if icons is None:
            icons = {}
        self.icons = icons

        self.class_prefix = class_prefix
        self.parse_nested = parse_nested
        self.match_case_sensitive = match_case_sensitive
        self.custom_title = custom_title

    @cached_property
    def patterns(
        self,
    ) -> list[re.Pattern[str]]:
        marker_name_re = "\\w+" if self.titles == ["*"] else "|".join(self.titles)
        flags = 0 if self.match_case_sensitive else re.IGNORECASE
        # Bound the inline-title capture to a single line. The previous `[^\\n\\r]*` was a raw-string trap that
        # excluded `\`, `n`, `r` instead of newlines and leaked body text across line breaks.
        return [
            re.compile(
                r"^(?P<marker>\*\*(?P<title>(Note|Warning))\*\*:?)[ \t]*(?P<inline>[^\n\r]*)",
                flags=flags,
            ),
            re.compile(
                rf"^(?P<marker>\\?\[!(?P<title>({marker_name_re}))\\?\])[ \t]*(?P<inline>[^\n\r]*)",
                flags=flags,
            ),
        ]

    @staticmethod
    def _get_first_inline(tokens: list[Token], start: int, end: int) -> Token | None:
        return next(
            (t for t in tokens[start : end + 1] if t.type == "inline"),
            None,
        )

    @staticmethod
    def _get_first_inline_index(tokens: list[Token], start: int, end: int) -> int:
        for index in range(start, end + 1):
            if tokens[index].type == "inline":
                return index
        return -1

    def _block_to_alerts_if_matched(
        self,
        tokens: list[Token],
        start_index: int,
        end_index: int,
        *,
        custom_title: bool,
    ) -> int:
        first_inline = self._get_first_inline(tokens, start_index, end_index)
        if not first_inline:
            return 0

        match_index = -1
        match = None
        for pattern_index, pattern in enumerate(self.patterns):
            match = pattern.match(first_inline.content)
            if match:
                match_index = pattern_index
                break

        if not match:
            return 0

        title = match.group("title").strip()
        icon = self.icons.get(title.lower(), "")

        # Obsidian's callout spec (open-ended types, fold indicators, custom titles) is where this convention
        # originates. Hugo's alert syntax mirrors just the title/fold grammar, restricted to GFM's five types.
        # This package only replicates the title part, and only when `custom_title` is on, since neither
        # convention is part of GitHub's own GFM alerts spec. The alternate syntaxes never carried that meaning,
        # so keep them on the pre-existing normalize-into-body path.
        is_canonical_unescaped = (
            custom_title and match_index == 1 and "\\" not in match.group("marker")
        )
        inline = match.group("inline") or ""
        if is_canonical_unescaped:
            inline_title = inline.strip()
            first_inline.content = first_inline.content[match.end() :].lstrip()
        else:
            inline_title = ""
            first_inline.content = first_inline.content[
                len(match.group("marker")) :
            ].lstrip()

        open_token = tokens[start_index]
        close_token = tokens[end_index]

        open_token.type = GFM_ALERT_OPEN
        open_token.tag = "div"
        open_token.meta = {
            "title": title,
            "icon": icon,
            "inline_title": inline_title,
        }

        close_token.type = GFM_ALERT_CLOSE
        close_token.tag = "div"

        # An empty leading paragraph would render as a stray `<p></p>` next to the title. Drop it so downstream
        # renderers don't have to filter empty paragraphs out of every alert.
        if is_canonical_unescaped and not first_inline.content:
            inline_index = self._get_first_inline_index(tokens, start_index, end_index)
            if (
                inline_index > 0
                and tokens[inline_index - 1].type == "paragraph_open"
                and inline_index + 1 <= end_index
                and tokens[inline_index + 1].type == "paragraph_close"
            ):
                del tokens[inline_index - 1 : inline_index + 2]
                return 3
        return 0

    def get_rule(self) -> Callable[[StateCore], None]:
        def github_alerts_rule(state: StateCore) -> None:
            # Read lazily, at render time, rather than closing over a value computed when this rule was
            # registered: mdformat runs every extension's `update_mdit` in an unguaranteed order, so a
            # value baked in at registration time could be stale by the time a sibling extension (or the
            # caller) finishes configuring options. By render time every extension has already registered.
            mdformat_opts = state.md.options.get("mdformat")
            custom_title = (
                bool(get_conf(state.md.options, "custom_title"))
                if mdformat_opts is not None
                else self.custom_title
            )

            tokens = state.tokens
            i = 0
            start_indices = []
            while i < len(tokens):
                if tokens[i].type == "blockquote_open":
                    start_indices.append(i)
                elif tokens[i].type == "blockquote_close":
                    start_index = start_indices.pop()
                    if self.parse_nested or not start_indices:
                        removed = self._block_to_alerts_if_matched(
                            tokens,
                            start_index,
                            end_index=i,
                            custom_title=custom_title,
                        )
                        # Rewind past any deletions so the outer cursor stays aligned with the token list.
                        i -= removed
                i += 1

        return github_alerts_rule


def gfm_alerts_plugin(
    md: MarkdownIt,
    titles: list[str] | None = None,
    icons: dict[str, str] | None = None,
    class_prefix: str = "markdown-alert",
    *,
    parse_nested: bool = True,
    match_case_sensitive: bool = False,
    custom_title: bool = False,
) -> None:
    github_alerts_rule = AlertRuleFactory(
        titles=titles,
        icons=icons,
        class_prefix=class_prefix,
        parse_nested=parse_nested,
        match_case_sensitive=match_case_sensitive,
        custom_title=custom_title,
    ).get_rule()

    md.core.ruler.after("block", GFM_ALERTS_PREFIX, github_alerts_rule)

    def render_alert_open(
        self: RendererProtocol,  # ruff: ignore[unused-function-argument]
        tokens: list[Token],
        idx: int,
        options,  # ruff: ignore[missing-type-function-argument, unused-function-argument]
        env,  # ruff: ignore[missing-type-function-argument, unused-function-argument]
    ) -> str:
        meta = tokens[idx].meta
        inline_title = meta.get("inline_title", "")
        if inline_title:
            title_html = md.renderInline(inline_title)
        else:
            title_html = meta["title"].title()
        return (
            f'<div class="{class_prefix} {class_prefix}-{meta["title"].lower()}">\n'
            f'<p class="{class_prefix}-title">'
            f"{meta['icon']}{title_html}</p>\n"
        )

    def render_alert_close(
        self: RendererProtocol,  # ruff: ignore[unused-function-argument]
        tokens: list[Token],  # ruff: ignore[unused-function-argument]
        idx: int,  # ruff: ignore[unused-function-argument]
        options,  # ruff: ignore[missing-type-function-argument, unused-function-argument]
        env,  # ruff: ignore[missing-type-function-argument, unused-function-argument]
    ) -> str:
        return "</div>"

    md.add_render_rule("gfm_alert_open", render_alert_open)
    md.add_render_rule("gfm_alert_close", render_alert_close)
