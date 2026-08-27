#!/usr/bin/env python3
"""Inverter telemetry from the Solaredge API."""

from solaredge.api import SolaredgeClient
from solaredge.const import DateFormats, TimeUnit
from utilities import InfluxConnection, get_env, get_logger

logger = get_logger(destination="syslog", level="INFO")


def main() -> None:
    """Load historical telemetry data into influxdb."""
    env = get_env()
    if (apikey := env.get('solaredge_apikey')) is None:
        raise ValueError("Missing required environment variable: solaredge_apikey")
    with InfluxConnection(database="solaredge", reset=False).connect() as connection:
        with SolaredgeClient(apikey=apikey) as client:
            client.set_datetimes(3, 1)
            client.set_time_unit(TimeUnit.DAY)
            if not client.inverter_list:
                logger.warning(
                    "No inverters found from Solaredge API; nothing to write to InfluxDB.")
                return
            influx_data = [
                {
                    'measurement': 'inverter_telemetry',
                    'time': data.date.strftime(DateFormats.DATETIMET.value),
                    'tags': {'inverter_serial': inverter,
                             'month': data.date.strftime(DateFormats.MONTH.value),
                             'year': data.date.strftime(DateFormats.YEAR.value),
                             },
                    'fields': {
                        'dcvoltage': float(data.dcVoltage or 0.0),
                        'temperature': float(data.temperature or 0.0),
                        'accurrent': float(data.L1Data.acCurrent or 0.0),
                        'acvoltage': float(data.L1Data.acVoltage or 0.0),
                        'acfrequency': float(data.L1Data.acFrequency or 0.0),
                        'activepower': float(data.L1Data.activePower or 0.0),
                    },
                }
                for inverter in client.inverter_list
                for data in client.get_inverter_telemetry(inverter)
            ]
            logger.info("Writing %d telemetry points to InfluxDB",
                        len(influx_data))
            connection.write_points(influx_data)


if __name__ == "__main__":
    main()
