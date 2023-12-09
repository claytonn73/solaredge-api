#!/usr/bin/env python3
"""Call the Solaredge API and print the results."""

import pprint
from datetime import datetime  # noqa
# from cProfile import Profile
# from pstats import SortKey, Stats

from solaredge.api import SolaredgeClient
from utilities import get_env, get_logger


def main():
    """Call one of the Solaredge Api endpoints and print the formatted results."""
    logger = get_logger(destination="stdout") # noqa
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
    # with Profile() as profile:
    #     print(main())
    # (
    #     Stats(profile)
    #     .strip_dirs()
    #     .sort_stats(SortKey.TIME)
    #     .print_stats()
    # )
