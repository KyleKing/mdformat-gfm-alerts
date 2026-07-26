import argparse

import mdformat

from mdformat_gfm_alerts import add_cli_argument_group

_INPUT = "> [!TIP] Custom title\n> Body.\n"
_STRICT = "> [!TIP]\n> Custom title\n> Body.\n"
_GOLDMARK = "> [!TIP] Custom title\n> Body.\n"


def test_goldmark_defaults_to_strict_gfm():
    assert mdformat.text(_INPUT, extensions={"gfm_alerts"}) == _STRICT


def test_goldmark_enabled_via_api_option():
    result = mdformat.text(
        _INPUT, extensions={"gfm_alerts"}, options={"goldmark": True}
    )
    assert result == _GOLDMARK


def test_goldmark_enabled_via_cli_or_toml_plugin_config():
    """Simulates the shape mdformat's CLI/TOML config produces: `options["plugin"]["gfm_alerts"]["goldmark"]`."""
    result = mdformat.text(
        _INPUT,
        extensions={"gfm_alerts"},
        options={"plugin": {"gfm_alerts": {"goldmark": True}}},
    )
    assert result == _GOLDMARK


def test_add_cli_argument_group_registers_goldmark_flag():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group()
    add_cli_argument_group(group)
    args = parser.parse_args(["--goldmark"])
    assert args.goldmark is True


def test_api_option_takes_precedence_over_plugin_config():
    result = mdformat.text(
        _INPUT,
        extensions={"gfm_alerts"},
        options={"goldmark": False, "plugin": {"gfm_alerts": {"goldmark": True}}},
    )
    assert result == _STRICT
