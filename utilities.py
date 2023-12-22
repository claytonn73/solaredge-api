#!/usr/bin/env python3
"""Utility functions used in various scripts."""
import logging
import logging.handlers
import os
from contextlib import contextmanager

import influxdb
from dotenv import dotenv_values


def get_logger(destination: str = "stdout"):
    """Creates a logger instance of the desired type"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handlers = {
        "stdout": logging.StreamHandler(),
        "syslog": logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON, 
                                                 address='/dev/log')
    }
    handler = handlers.get(destination)
    if destination == "syslog":
        log_format = 'python[%(process)d]: [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)d \"%(message)s\"'
        handler.setFormatter(logging.Formatter(fmt=log_format))
    logger.addHandler(handler)
    return logger


def get_env() -> dict:
    """Reads environment variables from the users home directory"""
    env_path = os.path.expanduser('~/.env')
    return dotenv_values(env_path) if os.path.exists(env_path) else {}


class InfluxConnection:
    """Connect to influxdb and return connection."""

    def __init__(self, database: str, reset: bool = False):
        """Connect to influxdb."""
        self.database = database
        self.reset = reset

    @contextmanager
    def connect(self):
        """Context manager that ensures the InfluxDB connection is closed."""
        try:
            influxdb_client = influxdb.InfluxDBClient(host='localhost', port=8086)
            if self.reset:
                influxdb_client.drop_database(self.database)
                influxdb_client.create_database(self.database)
            influxdb_client.switch_database(self.database)
            yield influxdb_client
        except (influxdb.exceptions.InfluxDBClientError, influxdb.exceptions.InfluxDBServerError) as err:
            raise SystemExit(err) from err
        finally:
            influxdb_client.close()
