"""Public Plugin."""

from typing import Mapping

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.utils import is_code_block

# PLANNED: fix capitalization or whitespace if incorrect?
LABELS = ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")
TAG_STARTS = {"> **", "> [!"}  # Useful for quickly checking potential matches
TAGS = [
    *[f"> **{label}**" for label in ("Note", "Warning")],  # 2022 Syntax
    *[f"> [!{label}]" for label in LABELS],  # 2023 Syntax
]
MAXTAG = max(map(len, TAGS))


def _gfm_alert_rule(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
) -> bool:
    if is_code_block(state, startLine):
        return False

    prefix = state.src.lstrip()[:MAXTAG]
    if (
        # Check for pattern first before confirming for all possible matches
        any(prefix.startswith(short) for short in TAG_STARTS)
        and any(prefix.startswith(tag) for tag in TAGS)
    ):
        # TODO: Implement proper HTML output
        return True

    return False


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser to identify Alerts."""
    # FIXME: This is being run indefinitely!!
    mdit.block.ruler.after(
        "fence",  # TODO: What should this be?
        "gfm_alert",
        _gfm_alert_rule,
        {"alt": ["blockquote"]},
    )


def _render_gfm_alert(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode`."""
    breakpoint()
    return node.child.render(context)

    # prefix = node.markup.split(" ")[0]
    # title = node.info.strip()
    # title_line = f"{prefix} {title}"
    #
    # elements = [render for child in node.children if (render := child.render(context))]
    # separator = "\n\n"
    #
    # # Then indent to either 3 or 4 based on the length of the prefix
    # #   For reStructuredText, '..' should be indented 3-spaces
    # #       While '!!!', , '...', '???', '???+', etc. are indented 4-spaces
    # indent = " " * (min(len(prefix), 3) + 1)
    # content = textwrap.indent(separator.join(elements), indent)
    #
    # return title_line + "\n" + content if content else title_line


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {"gfm_alert": _render_gfm_alert}
