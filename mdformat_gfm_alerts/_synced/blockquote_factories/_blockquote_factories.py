"""Blockquote to Div Conversion Factories.

Adapted from the implementation in `mdformat-obsidian`:
<https://github.com/KyleKing/mdformat-obsidian/blob/main/mdformat_obsidian/mdit_plugins/_obsidian_callouts.py>

This provides utilities for converting blockquotes containing specific content to divs
for accessibility purposes, while maintaining mdformat compatibility.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

if TYPE_CHECKING:
    from collections.abc import Sequence


def blockquote_to_div_plugin_factory(
    content_prefix: str,
) -> Callable[[MarkdownIt], None]:
    """Create a plugin that converts blockquotes containing specific content to divs.

    This is useful for accessibility when blockquotes are repurposed for semantic
    content (like callouts, alerts, admonitions) rather than actual quotations.

    The blockquote tokens remain in the AST for mdformat compatibility, but are
    rendered as <div> elements in HTML when they contain the specified content type.

    Args:
        content_prefix: The prefix of the content tokens to detect (e.g., "obsidian_callout")

    Returns:
        A plugin function that can be applied to a MarkdownIt instance
    """

    def _render_blockquote_open_with_content(
        self: RendererHTML,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Render blockquote as div when it contains specific content for accessibility."""
        # Check if next token is the specified content type
        if idx + 1 < len(tokens) and tokens[idx + 1].type == f"{content_prefix}_open":
            # Use div instead of blockquote for accessibility
            return "<div>\n"
        # Otherwise use default blockquote rendering
        return self.renderToken(tokens, idx, options, env)

    def _render_blockquote_close_with_content(
        self: RendererHTML,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Close div when blockquote contained specific content."""
        # Find the matching blockquote_open by walking backwards
        level = 1
        j = idx - 1
        while j >= 0 and level > 0:
            token_type = tokens[j].type
            j -= 1

            if token_type == "blockquote_close":  # noqa: S105
                level += 1
                continue

            if token_type != "blockquote_open":  # noqa: S105
                continue

            level -= 1
            if level > 0:
                continue

            # Check if content follows the opening blockquote
            if j + 1 < len(tokens) and tokens[j + 1].type == f"{content_prefix}_open":
                return "</div>\n"
            break

        # Otherwise use default blockquote rendering
        return self.renderToken(tokens, idx, options, env)

    def blockquote_to_div_plugin(md: MarkdownIt) -> None:
        """Install the blockquote-to-div conversion plugin."""
        # Override blockquote rendering to use div for content (accessibility)
        md.add_render_rule(
            "blockquote_open", _render_blockquote_open_with_content, fmt="html"
        )
        md.add_render_rule(
            "blockquote_close", _render_blockquote_close_with_content, fmt="html"
        )

    return blockquote_to_div_plugin
