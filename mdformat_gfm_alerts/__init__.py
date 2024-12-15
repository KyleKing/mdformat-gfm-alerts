"""An mdformat plugin for `gfm_alerts`."""

__version__ = "1.0.1"

# FYI see source code for available interfaces:
#   https://github.com/executablebooks/mdformat/blob/5d9b573ce33bae219087984dd148894c774f41d4/src/mdformat/plugins.py
from .plugin import RENDERERS, update_mdit

__all__ = ("RENDERERS", "update_mdit")
