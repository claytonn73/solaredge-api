#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from solaredge.const import TimeUnit
from utilities import InfluxConnection, get_env, get_logger
from influxdb import InfluxDBClient

logger = get_logger(destination = "syslog")


def add_energy_data(client : SolaredgeClient, connection : InfluxDBClient, time_unit: TimeUnit, measurement_name: str) -> None:
    """Query the solaredge API to get energy details for each site and then load data into influxdb."""    
    client.set_time_unit(time_unit)
    influx_data = [
        {
            'measurement': measurement_name,
            'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
            'tags': {'site_number': site,                 
                     'month': data.date.strftime("%Y %m"),
                     'year': data.date.strftime("%Y"),                     
                    },
            'fields': {
                'generated': float(data.value),
                **({'hour': int(data.date.hour)} if time_unit == "HOUR" else {})
            }
        }
        for site in client.site_list
        for data in client.get_energy(site_id=site).values
    ]
    connection.write_points(influx_data)


def main() -> None:
    """Load historical consumtpion data into influxdb."""
    env = get_env()
    with InfluxConnection(database="solaredge", reset=False).connect() as connection:
        apikey = env.get('solaredge_apikey')
        if not isinstance(apikey, str) or not apikey:
            raise ValueError("Missing or invalid 'solaredge_apikey' in environment variables.")
        with SolaredgeClient(apikey=apikey) as client:
            client.set_datetimes(35, 25)
            client.set_dates(35, 25)
            logger.info("Adding Solaredge daily information to influxdb")
            add_energy_data(client, connection, TimeUnit.DAY, "daily_energy_generated")
            logger.info("Adding Solaredge hourly information to influxdb")
            add_energy_data(client, connection, TimeUnit.HOUR, "hourly_energy_generated")


if __name__ == "__main__":
    main()
