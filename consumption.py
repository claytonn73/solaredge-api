#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from utilities import InfluxConnection, get_env, get_logger


def main():
    """Load historical data into influxdb."""
    logger = get_logger(destination = "syslog")
    env = get_env()

    with InfluxConnection(database="solaredge", reset=False) as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:

            client.set_datetimes(7, 1)
            client.set_dates(7, 1)

            for site in client.site_list:
                
                influx_tags = {
                    'site_number': site,
                }            
                influx_data = []
                logger.info("Adding Solaredge daily information to influxdb")
                # Obtain daily energy figures and add to influxdb
                client.set_time_unit("DAY")                                
                energy = client.get_energy(id=site)
                for data in energy.values:
                    influx_fields = {
                        'generated': float(data.value),
                        'month': data.date.strftime("%b %Y"),
                    }
                    influx_data.append(
                        {
                            'measurement': 'daily_energy_generated',
                            'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                            'tags': influx_tags,
                            'fields': influx_fields,
                        }
                    )
                connection.influxdb.write_points(influx_data)

                influx_data = []
                logger.info("Adding Solaredge hourly information to influxdb")
                # Obtain hourly energy figures and add to influxdb
                client.set_time_unit("HOUR")                
                energy = client.get_energy(id=site)
                for data in energy.values:
                    influx_fields = {
                        'generated': float(data.value),
                        'month': data.date.strftime("%b %Y"),
                        'hour': int(data.date.hour),
                    }
                    influx_data.append(
                        {
                            'measurement': 'hourly_energy_generated',
                            'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                            'tags': influx_tags,
                            'fields': influx_fields,
                        }
                    )
                connection.influxdb.write_points(influx_data)


if __name__ == "__main__":
    main()
