#!/usr/bin/env python3
"""Inverter telemetry from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from utilities import InfluxConnection, get_env, get_logger


def main():
    """Load historical data into influxdb."""
    logger = get_logger()
    env = get_env()

    with InfluxConnection(database="solaredge", reset=False) as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:

            client.set_datetimes(3, 1)
            client.set_dates(3, 1)
            client.set_time_unit("DAY")

            influx_tags = {
                'site_number': client.site_list[0],
            }
            # Obtain telemetry data and add to influxdb
            telemetry = client.get_inverter_telemetry()
            logger.info("Adding Solaredge inverter telemetry information to influxdb")
            for data in telemetry:
                influx_fields = {
                    'dcvoltage': float(data.dcVoltage or 0.0),
                    'temperature': float(data.temperature),
                    'accurrent': float(data.L1Data.acCurrent),
                    'acvoltage': float(data.L1Data.acVoltage),
                    'acfrequency': float(data.L1Data.acFrequency),
                    'month': data.date.strftime("%b %Y"),
                }
                influx_data = [
                    {
                        'measurement': 'inverter_telemetry',
                        'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                        'tags': influx_tags,
                        'fields': influx_fields,
                    }
                ]
                connection.influxdb.write_points(influx_data)


if __name__ == "__main__":
    main()
