#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from utilities import InfluxConnection, get_env, get_logger


def add_energy_data(client, connection, site, time_unit, measurement_name, logger):
    logger.info(f"Adding Solaredge {time_unit.lower()} information to influxdb")
    client.set_time_unit(time_unit)
    energy = client.get_energy(site_id=site)
    influx_data = [
        {
            'measurement': measurement_name,
            'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
            'tags': {'site_number': site},
            'fields': {
                'generated': float(data.value),
                'month': data.date.strftime("%b %Y"),
                **({'hour': int(data.date.hour)} if time_unit == "HOUR" else {})
            }
        }
        for data in energy.values
    ]
    connection.write_points(influx_data)

def main() -> None:
    """Load historical data into influxdb."""
    logger = get_logger(destination = "syslog")
    env = get_env()
    with InfluxConnection(database="solaredge", reset=False).connect() as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:
            client.set_datetimes(7, 1)
            client.set_dates(7, 1)
            for site in client.site_list:
                add_energy_data(client, connection, site, "DAY", "daily_energy_generated", logger)
                add_energy_data(client, connection, site, "HOUR", "hourly_energy_generated", logger)


if __name__ == "__main__":
    main()
