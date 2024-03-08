# mdformat-gfm-alerts

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

<!-- [![codecov.io][cov-badge]][cov-link]
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-gfm-alerts/branch/main/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-gfm-alerts
 -->

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [GitHub "Alerts"](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts) (and [community discussion](https://github.com/orgs/community/discussions/16925)).

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### Pre-Commit

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.16
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-gfm-alerts
```

### pipx

```sh
pipx install mdformat
pipx inject mdformat mdformat-gfm-alerts
```

## Contributing

See [CONTRIBUTING.md](https://github.com/KyleKing/mdformat-gfm-alerts/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-gfm-alerts/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-gfm-alerts/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-gfm-alerts.svg
[pypi-link]: https://pypi.org/project/mdformat-gfm-alerts
