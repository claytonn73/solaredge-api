"""Connection to a local influxdb."""
import influxdb


class InfluxConnection:
    """Connect to influxdb and return connection."""

    def __init__(self, reset: bool = False):
        """Connect to influxdb."""
        try:
            self.influxdb = influxdb.InfluxDBClient(host='localhost', port=8086)
            if reset is True:
                self.influxdb.drop_database('solaredge')
                self.influxdb.create_database('solaredge')
            self.influxdb.switch_database('solaredge')
        except (influxdb.exceptions.InfluxDBClientError, influxdb.exceptions.InfluxDBServerError) as err:
            raise SystemExit(err)

    def __enter__(self):
        """Return the connection."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close connection to influxdb."""
        self.influxdb.close()
