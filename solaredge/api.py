"""Contains the Solaredge API class and its methods."""

import json
import logging
from datetime import datetime, timedelta  # noqa

import requests

import solaredge.const
from solaredge.const import APIList, Solaredge

# Only export the Solaredge Client
__all__ = ["SolaredgeClient"]


class SolaredgeClient:
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
        self._api = Solaredge
        self._session = requests.Session()                
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
            self._storeddata.inventories.append(self.get_site_inventory(site.id))
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
        return [
            item.SN
            for list in [data.inverters for data in self._storeddata.inventories]
            for item in list
        ]

    def set_datetimes(self, start: int = 1, end: int = 0) -> None:
        """_summary_

        Args:
            start (int, optional): _description_. Defaults to 1.
            end (int, optional): _description_. Defaults to 0.
        """
        self._api.parameters.startTime: str = (
            datetime.now() - timedelta(days=start)
        ).strftime("%Y-%m-%d 00:00:00")
        self._api.parameters.endTime: str = (
            datetime.now() - timedelta(days=end)
        ).strftime("%Y-%m-%d 23:59:59")

    def set_dates(self, start: int = 1, end: int = 0) -> None:
        self._api.parameters.startDate = (
            datetime.now() - timedelta(days=start)
        ).strftime("%Y-%m-%d")
        self._api.parameters.endDate = (datetime.now() - timedelta(days=end)).strftime(
            "%Y-%m-%d"
        )

    def set_time_unit(self, unit: solaredge.const.TimeUnit) -> None:
        """Sets the time unit for the Solaredge API.

        Args:
            unit: The time unit to be set. (Type: solaredge.const.TimeUnit)        """
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
    
    def _set_site_id(self, site_id: str) -> None:
        if site_id is not None:
             self._api.arguments.siteid = site_id        

    def get_site_details(self, site_id: str = None) -> solaredge.const.Site:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteInfo.value)
        return results.details

    def get_data_period(self, site_id: str = None) -> solaredge.const.DataPeriod:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteDataPeriod.value)
        return results.dataPeriod

    def get_site_overview(self, site_id: str = None) -> solaredge.const.OverviewData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteOverview.value)
        return results.overview

    def get_energy(self, site_id: str = None) -> solaredge.const.EnergyData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteEnergy.value)
        return results.energy

    def get_energy_details(self, site_id: str = None) -> solaredge.const.DetailData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.EnergyDetails.value)
        return results.energyDetails

    def get_power(self, site_id: str = None) -> solaredge.const.PowerData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.Power.value)
        return results.power

    def get_power_details(self, site_id: str = None) -> solaredge.const.DetailData:
        """Gets the power details from the Solaredge REST API
        Args:
            site (str): The site ID to be used for the query
        Returns:
            solaredge.const.PowerDetailData
        """
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.PowerDetails.value)
        return results.powerDetails

    def get_power_flow(self, site_id: str = None) -> solaredge.const.SiteCurrentPowerFlow:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.PowerFlow.value)
        return results.SiteCurrentPowerFlow

    def get_storage(self, site_id: str = None) -> solaredge.const.StorageData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.Storage.value)
        return results.storageData

    def get_site_components(self, site_id: str = None) -> list[solaredge.const.ComponentEntry]:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.Components.value)
        for entry in results.reporters.list:
            entry.site = self._api.arguments.siteid
        return results.reporters.list

    def get_site_inventory(self, site_id: str = None) -> solaredge.const.InventoryData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.Inventory.value)
        # Add the site ID to the Inventory data for easier handling
        results.Inventory.site = self._api.arguments.siteid
        return results.Inventory

    def get_inverters(self, site_id: str = None) -> list[solaredge.const.Inverter]:
        results = self.get_site_inventory(site_id)
        # Add the site ID to each inverter entry for easier handling
        for entry in results.inverters:
            entry.site = self._api.arguments.siteid
        return results.inverters

    def get_env_benefits(self, site_id: str = None) -> solaredge.const.EnvBenefits:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteBenefits.value)
        return results.envBenefits

    def get_timeframe_energy(self, site_id: str = None) -> solaredge.const.TimeFrameEnergyData:
        self._set_site_id(site_id)
        results = self._call_api(api=APIList.SiteEnergyTimeframe.value)
        return results.timeFrameEnergy

    def get_inverter_telemetry(self, serial: str = None) -> list[solaredge.const.Telemetry]:
        if serial is not None:
            self._api.arguments.serialnumber = serial
        if self._api.arguments.serialnumber is None:
            return []            
        results = self._call_api(api=APIList.InverterData.value)
        return results.data.telemetries


    def _call_api(self, api: solaredge.const.Endpoint = APIList.Sites.value, sample=False) -> object:
        """Initialise the arguments required to call one of the REST APIs and then call it returning the results."""
        if sample:
            self.logger.info(f"Processing sample json for: {api.name}")
        # Create a dictionary entry for the arguments required by the endpoint
        self.logger.info(f"Calling API endpoint: {api.name}")
        argumentlist = {
            entry.value: getattr(self._api.arguments, entry.value)
            for entry in api.arguments
            if getattr(self._api.arguments, entry.value) is not None
        }            
        # Create parameter list from the api definition where the parameter has been set
        params = {
            entry.value: getattr(self._api.parameters, entry.value)
            for entry in api.parms
            if getattr(self._api.parameters, entry.value) is not None
        }
        # Create a URL from the supplied information        
        url = f"{self._api.url}/{api.endpoint.format(**argumentlist)}"                    
        # Call the API endpoint and return the results parsing with the defined dataclass
        try:
            results = self._session.get(url=url, params=params, timeout=60)
            results.raise_for_status()
            self.logger.debug(
                f"Formatted API results:\n {json.dumps(results.json(), indent=2)}"
            )
            return api.response(**results.json())
        except requests.exceptions.RequestException as err:
            self.logger.error(f"Requests error encountered: {err}")
            raise err        


