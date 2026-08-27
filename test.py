#!/usr/bin/env python3
"""Call the Solaredge API and print the results."""

import logging
import pprint
# from datetime import datetime  # noqa

from solaredge.api import SolaredgeClient
# from solaredge.const import DateFormats, TimeUnit
from utilities import get_env, get_logger

logger = get_logger(destination="stdout")
logger.setLevel(logging.DEBUG)


def main() -> None:
    """Call one of the Solaredge Api endpoints and print the formatted results."""
    env = get_env()
    if (api_key := env.get('solaredge_apikey')) is None:
        raise ValueError("solaredge environment variable is not set")
    with SolaredgeClient(apikey=api_key) as client:
        client.set_datetimes(3, 1)
        # help(client)

        # for site in client.site_list:
        #    for data in client.get_energy(site_id=site).values:
        #        logger.info(f"Site: {site} - Energy Data: {data}")
        for site in client.get_sites():
            pprint.pprint(client.get_energy(site.id), width=120)
            # pprint.pprint(client.get_site_inventory(site.id))
            # pprint.pprint(client.get_site_components(site.id))
            # pprint.pprint(client.get_power_flow(site.id))
        # pprint.pprint(client.get_inverter_telemetry())
        # pprint.pprint(client._api)


if __name__ == "__main__":
    main()
