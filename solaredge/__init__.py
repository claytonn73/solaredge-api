"""Solaredge API client ."""
import logging
from .api import SolaredgeClient # noqa F401

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
