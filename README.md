# mdformat-gfm-alerts

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [GFM Alerts](https://github.com/orgs/community/discussions/16925)

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### Pre-Commit

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.19
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-gfm-alerts
```

### pipx/uv

```sh
pipx install mdformat
pipx inject mdformat mdformat-gfm-alerts
```

Or with uv:

```sh
uv tool run --from mdformat-gfm-alerts mdformat
```

## HTML Rendering

To generate HTML output, `gfm_alerts_plugin` can be imported from `mdit_plugins`. For more guidance on `MarkdownIt`, see the docs: <https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser>

```py
from markdown_it import MarkdownIt

from mdformat_gfm_alerts.mdit_plugins import gfm_alerts_plugin

md = MarkdownIt()
md.use(gfm_alerts_plugin)

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

[ci-badge]: https://github.com/kyleking/mdformat-gfm-alerts/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-gfm-alerts/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-gfm-alerts.svg
[pypi-link]: https://pypi.org/project/mdformat-gfm-alerts
