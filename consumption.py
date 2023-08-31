#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from utilities import InfluxConnection, get_env, get_logger


def main():
    """Load historical data into influxdb."""
    logger = get_logger()
    env = get_env()

    with InfluxConnection(database="solaredge", reset=False) as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:

            client.set_datetimes(7, 1)
            client.set_dates(7, 1)
            client.set_time_unit("DAY")

            influx_tags = {
                'site_number': client.site_list[0],
            }
            logger.info("Adding Solaredge daily information to influxdb")
            # Obtain half hour cost figures and add to influxdb
            energy = client.get_energy()

            for data in energy.values:
                influx_fields = {
                    'generated': float(data.value),
                    'month': data.date.strftime("%b %Y"),
                }
                influx_data = [
                    {
                        'measurement': 'daily_energy_generated',
                        'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                        'tags': influx_tags,
                        'fields': influx_fields,
                    }
                ]
                connection.influxdb.write_points(influx_data)

            client.set_time_unit("HOUR")

            influx_tags = {
                'site_number': client.site_list[0],
            }
            logger.info("Adding Solaredge hourly information to influxdb")
            # Obtain half hour cost figures and add to influxdb
            energy = client.get_energy()
            for data in energy.values:
                influx_fields = {
                    'generated': float(data.value),
                    'month': data.date.strftime("%b %Y"),
                    'hour': int(data.date.hour),
                }
                influx_data = [
                    {
                        'measurement': 'hourly_energy_generated',
                        'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                        'tags': influx_tags,
                        'fields': influx_fields,
                    }
                ]
                connection.influxdb.write_points(influx_data)


if __name__ == "__main__":
    main()
