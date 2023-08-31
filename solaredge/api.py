"""Contains the Solaredge API class and its methods."""

import json
import logging
from dataclasses import asdict  # noqa F401
from datetime import datetime, timedelta # noqa

import dateutil.parser  # noqa
import requests

import solaredge.const
from solaredge.const import APIList, Solaredge  # noqa F401
from solaredge.errors import APIKeyError  # noqa

# Only export the Solaredge Client
__all__ = ["SolaredgeClient"]


class SolaredgeClient():
    """This class enables queries to be performed using the Solaredge REST API"""

    def __init__(self, apikey: str) -> None:
        """Initialise the API client and get basic information on the sites for the API key provided.
        Args:
            apikey (str): The apikey for the Solaredge account.
        """
        assert apikey is not None
        # Create a logger instance for messages from the API client
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialising Solaredge API Client")
        self._session = requests.Session()
        self._api = Solaredge
        # Solaredge API uses the API key as a parameter
        self._api.parameters.api_key = apikey
        # Create a dataclass for locally stored information that is retained for the session
        self._storeddata = solaredge.const.SummaryData()
        # Store the site information
        self._storeddata.sites = self.get_sites()
        for site in self._storeddata.sites:
            self.logger.info(f"Found a site with id: {site.id}")
            # Set the site ID - with a single site this will remain set
            self._api.arguments.siteid = site.id
            # Store the inventory information for each site
            self._storeddata.inventories.append(
                self.get_site_inventory(site.id))
        for data in self._storeddata.inventories:
            for inverter in data.inverters:
                self.logger.info(f"Found an inverter with SN: {inverter.SN}")
                # Set the Inverter serial number so with a single inverter it is preset
                self._api.arguments.serialnumber = inverter.SN

    def __enter__(self) -> object:
        """Entry function for the Solaredge Client."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Exit function for the Solaredge Client."""
        self._session.close()

    def close(self) -> None:
        """Close the requests session."""
        self._session.close()

    @property
    def site_list(self) -> list[str]:
        return [site.id for site in self._storeddata.sites]

    @property
    def inverter_list(self) -> list[str]:
        return [item.SN for list in [data.inverters for data in self._storeddata.inventories] for item in list]

    def set_datetimes(self, start: int = 1, end: int = 0) -> None:
        self._api.parameters.startTime: str = (datetime.now()-timedelta(days=start)).strftime('%Y-%m-%d 00:00:00')
        self._api.parameters.endTime: str = (datetime.now()-timedelta(days=end)).strftime('%Y-%m-%d 23:59:59')

    def set_dates(self, start: int = 1, end: int = 0) -> None:
        self._api.parameters.startDate = (datetime.now()-timedelta(days=start)).strftime('%Y-%m-%d')
        self._api.parameters.endDate = (datetime.now()-timedelta(days=end)).strftime('%Y-%m-%d')

    def set_time_unit(self, unit: solaredge.const.TimeUnit) -> None:
        self._api.parameters.timeUnit = unit

    def get_current_version(self) -> solaredge.const.Version:
        results = self._call_api(api=APIList.CurrentVersion.value)
        return results.version

    def get_supported_versions(self) -> list[solaredge.const.Version]:
        results = self._call_api(api=APIList.SupportedVersions.value)
        return results.supported

    def get_sites(self) -> list[solaredge.const.Site]:
        results = self._call_api(api=APIList.Sites.value)
        return results.sites.site

    def get_site_details(self, id: str = None) -> solaredge.const.Site:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteInfo.value)
        return results.details

    def get_data_period(self, id: str = None) -> solaredge.const.DataPeriod:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteDataPeriod.value)
        return results.dataPeriod

    def get_site_overview(self, id: str = None) -> solaredge.const.OverviewData:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteOverview.value)
        return results.overview

    def get_energy(self, id: str = None) -> solaredge.const.EnergyData:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteEnergy.value)
        return results.energy

    def get_energy_details(self, id: str = None) -> solaredge.const.DetailData:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.EnergyDetails.value)
        return results.energyDetails

    def get_power(self, id: str = None) -> solaredge.const.PowerData:
        if id is not None:
            self._api.arguments.siteid = id
        results = self._call_api(api=APIList.Power.value)
        return results.power

    def get_power_details(self, site: str = None) -> solaredge.const.DetailData:
        """Gets the power details from the Solaredge REST API

        Args:
            site (str): The site ID to be used for the query

        Returns:
            solaredge.const.PowerDetailData
        """
        if site is not None:
            self._api.arguments.siteid = site
        results = self._call_api(api=APIList.PowerDetails.value)
        return results.powerDetails

    def get_power_flow(self, id: str) -> solaredge.const.SiteCurrentPowerFlow:
        self._api.arguments.siteid = id
        results = self._call_api(api=APIList.PowerFlow.value)
        return results.SiteCurrentPowerFlow

    def get_storage(self, id: str) -> solaredge.const.StorageData:
        self._api.arguments.siteid = id
        results = self._call_api(api=APIList.Storage.value)
        return results.storageData

    def get_site_components(self, site: str = None) -> list[solaredge.const.ComponentEntry]:
        if site is not None:
            self._api.arguments.siteid = site
        results = self._call_api(api=APIList.Components.value)
        for entry in results.reporters.list:
            entry.site = self._api.arguments.siteid
        return results.reporters.list

    def get_site_inventory(self, id: str) -> solaredge.const.InventoryData:
        self._api.arguments.siteid = id
        results = self._call_api(api=APIList.Inventory.value)
        # Add the site ID to the Inventory data for easier handling
        results.Inventory.site = id
        return results.Inventory

    def get_inverters(self, id: str) -> list[solaredge.const.Inverter]:
        results = self.get_site_inventory(id)
        # Add the site ID to each inverter entry for easier handling
        for entry in results.inverters:
            entry.site = id
        return results.inverters

    def get_env_benefits(self, id: str) -> solaredge.const.EnvBenefits:
        self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteBenefits.value)
        return results.envBenefits

    def get_timeframe_energy(self, id: str) -> solaredge.const.TimeFrameEnergyData:
        self._api.arguments.siteid = id
        results = self._call_api(api=APIList.SiteEnergyTimeframe.value)
        return results.timeFrameEnergy

    def get_inverter_telemetry(self, serial: str = None) -> list[solaredge.const.Telemetry]:
        if serial is not None:
            self._api.arguments.serialnumber = serial
        if self._api.arguments.serialnumber is not None:
            results = self._call_api(api=APIList.InverterData.value)
            return results.data.telemetries
        else:
            return None

    def _call_api(self, api: solaredge.const.Endpoint = APIList.Sites.value) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        # Create a dictionary entry for the arguments required by the endpoint
        self.logger.info(f"Calling API endpoint: {api.name}")
        argumentlist = {}
        for entry in api.arguments:
            argumentlist.update({entry.value: getattr(self._api.arguments, entry.value)})
        # Create a parameter string including any parameters for the endpoint which have a defined value
        parm_string = ""
        for entry in api.parms:
            if getattr(self._api.parameters, entry.value) is not None:
                if parm_string == "":
                    parm_string = f"?{entry.value}={getattr(self._api.parameters, entry.value)}"
                else:
                    parm_string += f"&{entry.value}={getattr(self._api.parameters, entry.value)}"
        # Create a URL from the supplied information
        url = "{}/{}/{}".format(self._api.url,
                                api.endpoint.format(**argumentlist),
                                parm_string)
        # Call the API endpoint and return the results parsing with the defined dataclass
        return api.response(**self._rest_request(url))

    def _rest_request(self, url: str) -> json:
        """Use the requests module to call the REST API and check the response."""
        try:
            self.logger.debug(f"Issuing HTTP request: {url}")
            results = self._session.get(url=url, timeout=60)
            self.logger.debug(f'Response received: {results}')
            results.raise_for_status()
            # Check the REST API response status
            if results.status_code != requests.codes.ok:
                self.logger.error(f"API Error encountered for URL: {url} Status Code: {results.status_code}")
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
        self.logger.debug(
            f"Formatted API results:\n {json.dumps(results.json(), indent=2)}")
        return results.json()
