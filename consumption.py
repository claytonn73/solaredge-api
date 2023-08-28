#!/usr/bin/env python3
"""Solar Generation from the Solaredge API."""

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

            client.set_datetimes(7, 1)
            client.set_dates(7, 1)
            client.set_time_unit("DAY")

            influx_tags = {
                'site_number': client.site_list[0],
            }
            logger.info("Adding Solaredge information to influxdb")
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
            logger.info("Adding Solaredge information to influxdb")
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
    # args = getopts(sys.argv[1:])
    main()
