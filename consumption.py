#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

from influxdb import InfluxDBClient

from solaredge.api import SolaredgeClient
from solaredge.const import DateFormats, TimeUnit
from utilities import InfluxConnection, get_env, get_logger

logger = get_logger(destination="syslog", level="INFO")


def add_energy_data(client: SolaredgeClient, connection: InfluxDBClient, time_unit: TimeUnit, measurement_name: str) -> None:
    """Query the solaredge API to get energy details for each site and then load data into influxdb."""
    client.set_time_unit(time_unit)
    influx_data = [
        {
            'measurement': measurement_name,
            'time': data.date.strftime(DateFormats.DATETIMET.value),
            'tags': {'site_number': site,
                     'month': data.date.strftime(DateFormats.MONTH.value),
                     'year': data.date.strftime(DateFormats.YEAR.value),
                     },
            'fields': {
                'generated': float(data.value),
                **({'hour': int(data.date.hour)} if time_unit == TimeUnit.HOUR else {})
            }
        }
        for site in client.site_list
        for data in client.get_energy(site_id=site).values
    ]
    logger.info("Adding %d Solaredge %s datapoints to influxdb",
                len(influx_data), time_unit.value)
    connection.write_points(influx_data)


def main() -> None:
    """Load historical consumption data into influxdb."""
    env = get_env()
    apikey = env.get('solaredge_apikey')
    if not isinstance(apikey, str) or not apikey:
        raise ValueError("Missing or invalid 'solaredge_apikey' in environment variables.")
    with InfluxConnection(database="solaredge", reset=False).connect() as connection, SolaredgeClient(apikey=apikey) as client:
        client.set_datetimes(3, 1)
        add_energy_data(client, connection, TimeUnit.DAY,
                        "daily_energy_generated")
        add_energy_data(client, connection, TimeUnit.HOUR,
                        "hourly_energy_generated")


if __name__ == "__main__":
    main()
