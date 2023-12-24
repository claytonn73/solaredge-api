#!/usr/bin/env python3
"""Inverter telemetry from the Solaredge API."""

from datetime import datetime

from solaredge.api import SolaredgeClient
from utilities import InfluxConnection, get_env, get_logger

def main() -> None:
    """Load historical telemetry data into influxdb."""
    logger = get_logger(destination = "syslog")
    env = get_env()

    with InfluxConnection(database="solaredge", reset=False).connect() as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:

            client.set_datetimes(3, 1)
            client.set_dates(3, 1)
            client.set_time_unit("DAY")

            # Obtain telemetry data and add to influxdb
            logger.info("Adding Solaredge inverter telemetry information to influxdb")
            influx_data = [
                {
                    'measurement': 'inverter_telemetry',
                    'time': datetime.strftime(data.date, '%Y-%m-%dT%H:%MZ'),
                    'tags': {'inverter_serial': inverter},
                    'fields': {
                        'dcvoltage': float(data.dcVoltage or 0.0),
                        'temperature': float(data.temperature),
                        'accurrent': float(data.L1Data.acCurrent),
                        'acvoltage': float(data.L1Data.acVoltage),
                        'acfrequency': float(data.L1Data.acFrequency),
                        'month': data.date.strftime("%b %Y"),
                    },
                }
                for inverter in client.inverter_list                    
                for data in client.get_inverter_telemetry(inverter)
            ]
            connection.write_points(influx_data)


if __name__ == "__main__":
    main()

