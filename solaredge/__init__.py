"""Solaredge API client ."""

import logging

from .api import SolaredgeClient

# Only export the Solaredge Client
__all__ = ["SolaredgeClient"]

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
