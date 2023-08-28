#!/usr/bin/env python3
"""Call the octopus API and print the results."""

import logging
import logging.handlers
import os
import pprint
import sys
from datetime import datetime  # noqa

from dotenv import dotenv_values

from solaredge.api import SolaredgeClient


def get_logger():
    """Log message to sysout."""
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    return logger


def main():
    """Call one of the Solaredge Api endpoints and print the formatted results."""
    global logger
    logger = get_logger()
    env_path = os.path.expanduser('~/.env')
    if os.path.exists(env_path):
        env = dotenv_values(env_path)

    with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:
        pprint.pprint(client.get_supported_versions())
        for site in client.get_sites():
            pprint.pprint(site)
        #    pprint.pprint(client.get_inverters(site.id))
        # pprint.pprint(client.get_inverter_telemetry())
        # pprint.pprint(list(client._api.constants))


if __name__ == "__main__":
    main()
