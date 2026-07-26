# mdformat-gfm-alerts

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [GFM Alerts](https://github.com/orgs/community/discussions/16925). For the JS markdown-it equivalent, see [antfu/markdown-it-github-alerts](https://github.com/antfu/markdown-it-github-alerts)

## Scope

By default, this package targets the alert syntax GitHub itself renders: `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, and `[!CAUTION]` alone on their own line, per [GitHub's alerts spec](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts). Custom titles (`[!TIP] Title`) and fold indicators aren't part of that spec, so trailing text on the marker line is folded into the alert body rather than treated as a title, matching how GitHub itself would render it.

Some other renderers (Hugo, Obsidian) recognize custom titles as an extension to this syntax. Pass `--goldmark` (or the `goldmark` option, see [Configuration](#configuration)) to preserve an inline title on the canonical `[!TYPE]` line instead of folding it into the body. This package still won't support Obsidian's open-ended callout types or fold indicators; for that:

- [mdformat-hugo](https://github.com/gaborbernat/mdformat-hugo) bundles this package alongside Hugo-specific shortcode and markdown-attribute formatting
- [mdformat-obsidian](https://github.com/kyleking/mdformat-obsidian) fully supports GFM-style alerts plus custom titles, folding, and Obsidian's open-ended callout types

## Configuration

`--goldmark` (CLI), `goldmark = true` under `[plugin.gfm_alerts]` (`.mdformat.toml`), or `options={"goldmark": True}` (API) preserves an inline custom title on the canonical `[!TYPE]` line instead of folding it into the body:

```md
<!-- Strict GFM (default): -->
> [!TIP]
> Custom title
> Body.

<!-- With --goldmark: -->
> [!TIP] Custom title
> Body.
```

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 1.0.0
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-gfm-alerts
```

### uvx

```sh
uvx --with=mdformat-gfm-alerts mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-gfm-alerts
```

## HTML Rendering

To generate HTML output, `gfm_alerts_plugin` can be imported from `mdit_plugins`. For more guidance on `MarkdownIt`, see the docs: <https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser>

```py
from markdown_it import MarkdownIt

from mdformat_gfm_alerts.mdit_plugins import gfm_alerts_plugin

md = MarkdownIt()
md.use(gfm_alerts_plugin)  # pass goldmark=True to preserve inline custom titles

text = """
> [!WARNING]
> This is the warning text
"""
md.render(text)
# <div class="markdown-alert markdown-alert-warning">
# <p class="markdown-alert-title">Warning</p>
# <p>This is the warning text</p>
# </div>
```

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-gfm-alerts/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-gfm-alerts/actions/workflows/tests.yml/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-gfm-alerts/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-gfm-alerts.svg
[pypi-link]: https://pypi.org/project/mdformat-gfm-alerts
