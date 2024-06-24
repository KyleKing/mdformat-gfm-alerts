"""An mdformat plugin for `gfm_alerts`."""

__version__ = "1.0.1"

from .plugin import RENDERERS, update_mdit

__all__ = ("RENDERERS", "update_mdit")
