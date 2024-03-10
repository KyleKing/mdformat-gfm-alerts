"""Public Extension."""

from __future__ import annotations

from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render

from .mdit_plugins import gfm_alert_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser to identify Alerts."""
    mdit.use(gfm_alert_plugin)


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
