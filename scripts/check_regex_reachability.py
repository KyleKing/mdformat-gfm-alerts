"""Assert every regex in the plugin is reachable by the fuzz corpus.

The behavioral guard in 'tests/render/test_security.py' amplifies the render
fixtures, but a regex anchored past a lead-in that no fixture produces (e.g.
``^```math``) is never reached, and the miss is silent. This script closes that
gap: it statically extracts every regex literal from the plugin package,
reconstructs each pattern's leading literal, and checks that at least one
fixture-derived payload contains it. Patterns with no reaching payload are
reported so a fixture can be added.

Run from the repo root: ``python scripts/check_regex_reachability.py``.
Exits non-zero (and is CI-friendly) when a pattern is unreachable.
"""

# ruff:file-ignore[print]

from __future__ import annotations

import ast
import sys
from pathlib import Path

from markdown_it.utils import read_fixture_file

PACKAGE = Path(__file__).parent.parent / "mdformat_gfm_alerts"
FIXTURE_PATH = (
    Path(__file__).parent.parent / "tests" / "render" / "fixtures" / "gfm_alerts.md"
)

_RE_FUNCS = {"compile", "match", "search", "fullmatch", "findall", "finditer", "sub"}
# Metacharacters that end the run of leading literal characters.
_METACHARS = set(".^$*+?()[]{}|")
# Escapes that denote a character class, not a literal.
_CLASS_ESCAPES = set("sSdDwWbBAZ")


def _literal_prefix(pattern: str) -> str:
    r"""Best-effort leading literal of a regex, so anchored patterns are matched.

    Walks the source until the first metacharacter or character class, treating
    ``\x`` as literal ``x`` and expanding a ``{n}`` repeat of the preceding
    literal (so ```` `{3} ```` yields three backticks).
    """
    pattern = pattern.removeprefix("^")
    out: list[str] = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "\\" and i + 1 < len(pattern):
            nxt = pattern[i + 1]
            if nxt in _CLASS_ESCAPES:
                break
            out.append(nxt)
            i += 2
        elif char == "{" and out:
            end = pattern.find("}", i)
            count = pattern[i + 1 : end] if end != -1 else ""
            if not (repeats := count.split(",")[0]).isdigit():
                break
            out.append(out[-1] * (int(repeats) - 1))
            i = end + 1
        elif char in _METACHARS:
            break
        else:
            out.append(char)
            i += 1
    return "".join(out)


def _regex_literal(node: ast.AST) -> str | None:
    """The pattern source if ``node`` is ``re.<func>("literal", ...)``, else None."""
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
        return None
    if node.func.attr not in _RE_FUNCS or not node.args:
        return None
    first = node.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def _iter_regex_literals() -> list[tuple[str, str]]:
    """Every ``(where, pattern_source)`` from ``re.<func>("literal", ...)`` calls."""
    found: list[tuple[str, str]] = []
    for path in PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        found.extend(
            (f"{path.name}:{node.lineno}", pattern)
            for node in ast.walk(tree)
            if (pattern := _regex_literal(node)) is not None
        )
    return found


def _fixture_corpus() -> str:
    if not FIXTURE_PATH.is_file():
        return ""
    return "\n".join(text for _l, _t, text, _e in read_fixture_file(FIXTURE_PATH))


def main() -> int:
    """Report any plugin regex the render fixtures never reach; exit non-zero if so."""
    corpus = _fixture_corpus()
    unreachable: list[tuple[str, str]] = []
    for where, pattern in _iter_regex_literals():
        prefix = _literal_prefix(pattern)
        # An empty prefix matches everywhere (unanchored), so it is trivially reachable.
        if prefix and prefix not in corpus:
            unreachable.append((where, pattern))

    if unreachable:
        print("Regex patterns not reached by any render fixture:")
        for where, pattern in unreachable:
            print(f"  {where}: {pattern!r}  (add a fixture exercising this syntax)")
        return 1

    print("All plugin regexes are reachable by the render fixtures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
