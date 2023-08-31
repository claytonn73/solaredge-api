#!/usr/bin/env python3
"""Call the octopus API and print the results."""

import logging
import logging.handlers
import pprint
import sys
from datetime import datetime  # noqa

from solaredge.api import SolaredgeClient
from utilities import get_env


def get_logger():
    """Log message to sysout."""
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    return logger


def main():
    """Call one of the Solaredge Api endpoints and print the formatted results."""
    logger = get_logger() # noqa
    env = get_env()

    with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:
        pprint.pprint(client.get_supported_versions())
        for site in client.get_sites():
            pprint.pprint(site)
        # pprint.pprint(client.get_inverters(site.id))
        # pprint.pprint(client.get_inverter_telemetry())
        # pprint.pprint(list(client._api.constants))


if __name__ == "__main__":
    main()
