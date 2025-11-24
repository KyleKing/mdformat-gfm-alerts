# Blockquote Factories

This code provides utilities for converting blockquotes to divs for accessibility when they contain specific content types.

The key insight is that blockquotes containing certain types of content (like callouts, alerts, or admonitions) should be rendered as `<div>` elements instead of `<blockquote>` elements for better accessibility, since the `>` syntax is being repurposed for semantic content rather than actual quotations.

## Usage

Use the `blockquote_to_div_plugin_factory` to create a plugin that will automatically convert blockquotes containing specific token types to divs during HTML rendering.

```python
from mdformat_plugin_template._synced.blockquote_factories import (
    blockquote_to_div_plugin_factory,
)


def my_plugin(md: MarkdownIt) -> None:
    # Your plugin logic here that creates tokens like "my_prefix_open"

    # Add blockquote-to-div conversion for accessibility
    blockquote_to_div_plugin = blockquote_to_div_plugin_factory("my_prefix")
    blockquote_to_div_plugin(md)
```

This will ensure that blockquotes containing your custom content are rendered as `<div>` elements in HTML output while maintaining compatibility with mdformat's AST structure.
