#!/usr/bin/env python3
"""Inverter telemetry from the Solaredge API."""

import logging
import logging.handlers
import os
from datetime import datetime

from dotenv import dotenv_values

from influxconnection import InfluxConnection
from solaredge.api import SolaredgeClient


def get_logger():
    """Log messages to the syslog."""
    logger = logging.getLogger()
    handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON, address='/dev/log')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    log_format = 'python[%(process)d]: [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d \"%(message)s\"'
    handler.setFormatter(logging.Formatter(fmt=log_format))
    return logger


def main():
    """Load historical data into influxdb."""
    global logger
    logger = get_logger()
    env_path = os.path.expanduser('~/.env')
    if os.path.exists(env_path):
        env = dotenv_values(env_path)

    with InfluxConnection(reset=False) as connection:
        with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:

            client.set_datetimes(3, 1)
            client.set_dates(3, 1)
            client.set_time_unit("DAY")

            influx_tags = {
                'site_number': client.site_list[0],
            }
            # Obtain telemetry data and add to influxdb
            telemetry = client.get_inverter_telemetry()
            logger.info("Adding Solaredge information to influxdb")
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
    # args = getopts(sys.argv[1:])
    main()
