"""
This code defines a set of data classes and enums that describe the SolarEdge API endpoints and the data they return.

Enums and Constants: The code defines several enums to represent different types of constants used in the SolarEdge API.
These enums include TimeUnit, Unit, Order, SiteStatus, Property, Meters, Metrics, InverterMode, OperationMode, and more.
These enums make the code more readable and help ensure consistent use of values throughout the API interactions.

Data Classes: The code defines various data classes that represent different types of data returned by the SolarEdge API
These data classes include information about sites, energy data, power flow, environmental benefits, battery telemetry,
inventory, component information, and more.

Endpoint Definitions: The code defines endpoint classes using the Endpoint data class.
Each endpoint class represents an API endpoint provided by SolarEdge.
These endpoint classes specify the required parameters, arguments, and response types for each endpoint.

APIArguments and APIParameters: The APIArguments and APIParameters data classes are used to store the arguments and
parameters required for making API requests. These classes have default values and can be customized as needed.

The Solaredge instance of the RESTClient is configured to interact with the SolarEdge API.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, IntEnum, StrEnum
from typing import List, Optional, Type

from solaredge.apiconstruct import (APIArguments, APIParameters, APIResponses,
                                    Endpoint, baseclass)


class TimeUnit(StrEnum):
    """This enum describes the different time units in which data can be returned.
    """

    QUARTER_OF_AN_HOUR = "QUARTER_OF_AN_HOUR"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class Unit(StrEnum):
    """Enumeration of unit types for energy and power measurements.
    """
    WATT = "W"
    KILOWATT = "kW"
    WATT_HOUR = "Wh"
    KILOWATT_HOUR = "kWh"


class Currency(StrEnum):
    """Enumeration of supported currency types for site financial data.
    """
    EUR = "Euro"
    GBP = "Pounds Sterling"
    USD = "US Dollar"


class Order(StrEnum):
    """Enumeration of sorting order options for API queries.
    """
    ASCENDING = "ASC"
    DESCENDING = "DESC"


class SiteStatus(StrEnum):
    """Enumeration representing the status of a site.

    Possible values:
    - `ACTIVE`: The site is in an active state.
    - `PENDING`: The site has been created but no data has been received yet.
    - `DISABLED`: The site is in a disabled state.
    - `ALL`: Special value indicating that all possible statuses should be returned when this is used as a parameter.
    """

    ACTIVE = "Active"
    PENDING = "Pending"
    DISABLED = "Disabled"
    ALL = "All"


class Property(StrEnum):
    """Enumeration of site property fields used in API requests and responses.

    This enum lists the available site attributes that can be referenced for sorting, filtering, or display.
    """
    NAME = "Name"
    COUNTRY = "Country"
    STATE = "State"
    CITY = "City"
    ADDRESS = "Address"
    ZIP = "Zip"
    STATUS = "Status"
    PEAKPOWER = "PeakPower"
    INSTALLATIONDATE = "InstallationDate"
    AMOUNT = "Amount"
    MAXSEVERITY = "MaxSeverity"
    CREATIONTIME = "CreationTime"


class Meters(StrEnum):
    """Enumeration of meter types for site energy and power data.

    This enum specifies the different categories of energy measurement available from the API.
    """
    PRODUCTION = "Production"
    CONSUMPTION = "Consumption"
    SELFCONSUMPTION = "SelfConsumption"
    FEEDIN = "FeedIn"
    PURCHASED = "Purchased"


class Metrics(StrEnum):
    """Enumeration of measurement systems for returned data.

    This enum specifies whether data is provided in metric or imperial units.
    """
    METRIC = "Metric"
    IMPERIAL = "Imperial"


class InverterMode(StrEnum):
    """Enum describing the different modes reported by a Solaredge Inverter.
    The Enum value is the descrption of the response provided by the API."""

    OFF = "Off"
    SLEEPING = "Night mode"
    STARTING = "Pre-production"
    MPPT = "Production"
    THROTTLED = "Forced power reduction"
    SHUTTING_DOWN = "Shutdown procedure"
    FAULT = "Error mode"
    STANDBY = "Maintenance mode"
    LOCKED_STDBY = "Standby mode lock"
    LOCKED_FIRE_FIGHTERS = "Firefighters lock mode"
    LOCKED_FORCE_SHUTDOWN = "Forced shutdown from server"
    LOCKED_COMM_TIMEOUT = "Communication timeout"
    LOCKED_INV_TRIP = "Inverter selflock trip"
    LOCKED_INV_ARC_DETECTED = "Inverter self-lock on arc detection"
    LOCKED_DG = "Inverter lock due to DG mode enable"
    LOCKED_PHASE_BALANCER = "Inverter lock due to phase imbalance (1ph, Australia only)"
    LOCKED_PRE_COMMISSIONING = "Inverter lock due to precommissioning"
    LOCKED_INTERNAL = "Inverter lock due to an undisclosed internal reason"


class OperationMode(IntEnum):
    """Integer-backed enum for solar inverter operation modes.

    This enum maps the numeric mode codes returned by the SolarEdge API to
    named constants.
    """
    ON_GRID = 0
    OFF_GRID_PV_BATTERY = 1
    OFF_GRID_GENERATOR = 2


class APIArgs(StrEnum):
    """Enum containing the set of arguments used by the API endpoints."""

    SITEID = "siteid"
    SERIALNUMBER = "serialnumber"


@dataclass
class apiargs(APIArguments):
    """Dataclass describing the set of arguments used by the API endpoints.

    Attributes:
        siteid: The ID of the site for which to retrieve data.
        serialnumber: The serial number of the inverter for which to retrieve data.
    """

    siteid: Optional[int] = None
    serialnumber: Optional[str] = None


class APIParms(StrEnum):
    """Enum containing the set of parameters used by the API endpoints."""

    SIZE = "size"
    START_INDEX = "startIndex"
    SEARCH_TEXT = "searchText"
    SORT_PROPERTY = "sortProperty"
    SORT_ORDER = "sortOrder"
    STATUS = "Status"
    API_KEY = "api_key"
    START_DATE = "startDate"
    END_DATE = "endDate"
    START_TIME = "startTime"
    END_TIME = "endTime"
    TIME_UNIT = "timeUnit"
    METERS = "meters"
    SERIALS = "serials"
    SYSTEM_UNITS = "systemUnits"


class DateFormats(StrEnum):
    """Enumeration of date and datetime formats used in API requests and responses.

    This enum specifies the string formatting patterns for dates and datetimes.
    """
    DATE = "%Y-%m-%d"
    MONTH = "%Y %m"
    YEAR = "%Y"
    DATETIME = "%Y-%m-%d %H:%M:%S"
    DATETIMET = '%Y-%m-%dT%H:%MZ'


@dataclass
class apiparms(APIParameters):
    """Parameters that may be passed to any SolarEdge endpoint.

    **Important**: the original implementation evaluated ``datetime.now()`` at
    import time, which meant the defaults drifted as soon as the module was
    imported.  By using ``default_factory`` we recompute each time an instance
    is created.
    """
    size: int = 100
    startIndex: int = 0
    searchText: Optional[str] = None
    sortProperty: Optional[Property] = None
    sortOrder: Order = Order.ASCENDING
    Status: SiteStatus = SiteStatus.ALL
    api_key: Optional[str] = None
    startDate: str = field(
        default_factory=lambda: (
            datetime.now() - timedelta(days=1)).strftime(DateFormats.DATE.value)
    )
    endDate: str = field(
        default_factory=lambda: datetime.now().strftime(DateFormats.DATE.value)
    )
    startTime: str = field(
        default_factory=lambda: (
            datetime.now() - timedelta(days=1)).strftime(DateFormats.DATETIME.value)
    )
    endTime: str = field(
        default_factory=lambda: datetime.now().strftime(DateFormats.DATETIME.value)
    )
    timeUnit: TimeUnit = TimeUnit.HOUR
    meters: Optional[Meters] = None
    serials: Optional[str] = None
    systemUnits: Metrics = Metrics.METRIC


@dataclass
class Location(baseclass):
    """This dataclass describes the location information provided in multiple API endpoints

    Attributes:
        country: The country where the site is located.
        city: The city where the site is located.
        address: The street address of the site.
        address2: An optional second line for the street address.
        zip: The postal code for the site.
        timeZone: The time zone of the site.
        state: The state where the site is located - not on details API call
        latitude: The latitude coordinate of the site  - only on details API call
        longitude: The longitude coordinate of the site  - only on details API call
        """

    country: str
    city: str
    address: str
    address2: str
    zip: str
    timeZone: str
    countryCode: str
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class PrimaryModule(baseclass):
    """Describes the primary module (panel) installed at the site.

    Attributes:
        manufacturerName: Manufacturer of the module.
        modelName: Model identifier for the module.
        maximumPower: Maximum power rating (kW or W as returned by API).
        temperatureCoef: Temperature coefficient value for the module.
    """
    manufacturerName: str
    modelName: str
    maximumPower: float
    temperatureCoef: float


@dataclass
class Uris(baseclass):
    """Container for URI templates returned in various API responses.

    These fields contain endpoint fragments or paths that can be used to
    construct full URLs for site images, data periods, details and overview.
    """
    DATA_PERIOD: str
    DETAILS: str
    OVERVIEW: str
    SITE_IMAGE: Optional[str] = None


@dataclass
class PublicSettings(baseclass):
    """Public visibility settings for a site.

    Attributes:
        isPublic: Whether the site is publicly visible.
        name: Optional public display name for the site.
    """
    isPublic: bool
    name: Optional[str] = None


@dataclass
class Site(baseclass):
    """This dataclass describes the site information provided by the Sites API endpoint

    Attributes:
        id: The Site ID which is used as a parameter in other API requests

        name, accountId, status, peakPower, lastUpdateTime, 
        installationDate, ptoDate, notes, type, location, primaryModule,
        uris, publicSettings

        curremcy, alertQuantity and alertSeverity which may not be returned"""

    id: int
    name: str
    accountId: int
    status: SiteStatus
    peakPower: float
    lastUpdateTime: date
    installationDate: date
    highestImpact: int
    ptoDate: str
    notes: str
    type: str
    location: Location
    primaryModule: PrimaryModule
    uris: Uris
    publicSettings: PublicSettings
    alertQuantity: int = 0
    currency: Optional[Currency] = None
    alertSeverity: Optional[str] = None


@dataclass
class SiteList(baseclass):
    """This dataclass describes the list of sites provided by the Sites API endpoint
    
    Attributes: count - count of sites
                site - a list of site information
    """

    count: int
    site: List[Site] = field(default_factory=list)


@dataclass
class SitesResponse(baseclass):
    """
    This dataclass describes the response from the Sites API endpoint

    Attributes: sites - information about the sites returned by the API
    """

    sites: SiteList


Sites = Endpoint(
    endpoint="sites/list",
    name="Site List",
    parms=[
        APIParms.API_KEY,
        APIParms.SIZE,
        APIParms.START_INDEX,
        APIParms.SEARCH_TEXT,
        APIParms.SORT_PROPERTY,
        APIParms.SORT_ORDER,
        APIParms.STATUS,
    ],
    sample="site_list.json",
    response=SitesResponse,
    returns="sites",
)


@dataclass
class SiteInfoResponse(baseclass):
    """This dataclass describes the response from the SiteInfo API endpoint"""

    details: Site


SiteInfo = Endpoint(
    endpoint="site/{siteid}/details",
    name="Site Details",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=SiteInfoResponse,
    returns="details",
)


@dataclass
class GasEmissionSaved(baseclass):
    """This dataclass describes the gas emissions savings returned by the SiteBenefits API

    Attributes:
        units: The unit of measurement for the gas emissions.
        co2: The amount of CO2 emissions saved.
        so2: The amount of SO2 emissions saved.
        nox: The amount of NOx emissions saved.
    """

    units: str
    co2: float
    so2: float
    nox: float


@dataclass
class EnvBenefits(baseclass):
    """This dataclass describes the environmental benefits returned by the SiteBenefits API

    Attributes:
        gasEmissionSaved: The gas emissions savings information.
        treesPlanted: The equivalent number of trees planted.
        lightBulbs: The equivalent number of light bulbs powered.
        """

    gasEmissionSaved: GasEmissionSaved
    treesPlanted: float
    lightBulbs: float


@dataclass
class EnvBenefitsResponse(baseclass):
    """This dataclass describes the initial response for the SiteBenefits API

    Attributes:
        envBenefits: The environmental benefits information.
    """

    envBenefits: EnvBenefits


SiteBenefits = Endpoint(
    endpoint="site/{siteid}/envBenefits",
    name="Site Environmental Benefits",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=EnvBenefitsResponse,
    returns="envBenefits"
)


@dataclass
class Summary(baseclass):
    """This dataclass describes the historical summary data returned by the SiteOverview API"""

    energy: float
    revenue: Optional[float] = None


@dataclass
class CurrentPower(baseclass):
    """This dataclass describes the current power data returned by the SiteOverview API"""

    power: float


@dataclass
class OverviewData(baseclass):
    """This dataclass describes the energy overview data returned by the SiteOverview API"""

    lastUpdateTime: datetime
    lifeTimeData: Summary
    lastYearData: Summary
    lastMonthData: Summary
    lastDayData: Summary
    currentPower: CurrentPower
    measuredBy: str


@dataclass
class OverviewResponse(baseclass):
    """This dataclass describes the initial response for the SiteOverview API"""

    overview: OverviewData


SiteOverview = Endpoint(
    endpoint="site/{siteid}/overview",
    name="Site Overview",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=OverviewResponse,
    returns="overview"
)


@dataclass
class DataPeriod(baseclass):
    """This dataclass describes the data period returned by the SiteDataPeriod API
    Atttributes: startDate, endDate"""

    startDate: datetime
    endDate: datetime


@dataclass
class SiteDataPeriodResponse(baseclass):
    """This dataclass describes the initial response for the SiteDataPeriod API
    Atttributes: dataPeriod"""

    dataPeriod: DataPeriod


SiteDataPeriod = Endpoint(
    endpoint="site/{siteid}/dataPeriod",
    name="Site Data: Start and End Dates",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=SiteDataPeriodResponse,
    returns="dataPeriod"
)


@dataclass
class Value(baseclass):
    """Represents a single timestamped value for energy or power data.

    This dataclass contains a datetime and its associated numeric value, used in various API responses.
    """
    date: datetime
    value: float = 0.0

    def __post_init__(self):
        # Call parent's __post_init__ if it exists
        if hasattr(super(), "__post_init__"):
            super().__post_init__()
        if self.value is None:
            self.value = 0.0


@dataclass
class EnergyData(baseclass):
    """Represents energy data for a site over a specified time period.

    This dataclass contains the time unit, unit type, a list of timestamped values, and the measurement source.
    """
    timeUnit: TimeUnit
    unit: Unit
    values: List[Value] = field(default_factory=list)
    measuredBy: Optional[str] = None


@dataclass
class EnergyDataResponse(baseclass):
    """Represents the response from the Site Energy API endpoint.

    This dataclass contains the energy data for a site, including time unit, unit type, values, and measurement source.
    """
    energy: EnergyData


SiteEnergy = Endpoint(
    endpoint="site/{siteid}/energy",
    name="Site Energy",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_DATE,
           APIParms.END_DATE, APIParms.TIME_UNIT],
    sample="site_energy.json",
    response=EnergyDataResponse,
    returns="energy"
)


@dataclass
class EnergyValue(baseclass):
    """Represents a single timestamped energy value for a site.

    This dataclass contains a datetime, the energy value, and its unit as returned by the API.
    """
    date: datetime
    energy: float
    unit: Unit


@dataclass
class TimeFrameEnergyData(baseclass):
    """Represents energy data for a site over a specific time frame.

    This dataclass contains the total energy, unit, measurement source, and lifetime energy values at the start and end of the period.
    """
    energy: float
    unit: Unit
    measuredBy: str
    startLifetimeEnergy: EnergyValue
    endLifetimeEnergy: EnergyValue


@dataclass
class TimeFrameEnergyResponse(baseclass):
    """Represents the response from the Site Energy Timeframe API endpoint.

    This dataclass contains energy data for a site over a specific time frame, including total energy and lifetime values.
    """
    timeFrameEnergy: TimeFrameEnergyData


SiteEnergyTimeframe = Endpoint(
    endpoint="site/{siteid}/timeFrameEnergy",
    name="Site Energy - Time Period",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_DATE, APIParms.END_DATE],
    response=TimeFrameEnergyResponse,
    returns="timeFrameEnergy"
)


@dataclass
class DataType(baseclass):
    """This dataclass describes a list of information retuened by various API endpoints

    Attrributes: type - the type of data in the list
                 values - a list of values of this type"""

    type: str
    values: List[Value] = field(default_factory=list)


@dataclass
class DetailData(baseclass):
    """This dataclass defines the response to the PowerDetail API request

    Atttributes:
        timeUnit: The granularity of the data returned
        unit: The unit of the data returned
        meters: A list of different types of data that is returned
    """

    timeUnit: TimeUnit
    unit: Unit
    meters: List[DataType] = field(default_factory=list)


@dataclass
class EnergyDetailResponse(baseclass):
    """This dataclass describes the response from the EnergyDetails API endpoint

    Attributes:
        energyDetails: The detailed energy data returned by the API.
    """

    energyDetails: DetailData


EnergyDetails = Endpoint(
    endpoint="site/{siteid}/energyDetails",
    name="Site Energy - Details",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_TIME,
           APIParms.END_TIME, APIParms.TIME_UNIT, APIParms.METERS],
    response=EnergyDetailResponse,
    returns="energyDetails"
)


@dataclass
class PowerDetailsResponse(baseclass):
    """This dataclass describes the response from the Power Details API endpoint
    Attributes:
        powerDetails: The detailed power data returned by the API.
    """

    powerDetails: DetailData


PowerDetails = Endpoint(
    endpoint="site/{siteid}/powerDetails",
    name="Site Power - Details",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_TIME,
           APIParms.END_TIME, APIParms.METERS],
    response=PowerDetailsResponse,
    returns="powerDetails"
)


@dataclass
class PowerData(baseclass):
    """This dataclass describes the power data returned by the PowerData API endpoint.

    Attributes:
        timeUnit: The granularity of the data returned.
        unit: The unit of the data returned.
        measuredBy: The source of the measurement.
        values: A Listof timestamped power values.
    """
    timeUnit: TimeUnit
    unit: Unit
    measuredBy: Optional[str] = None
    values: list[Value] = field(default_factory=list)


@dataclass
class PowerDataResponse(baseclass):
    """This dataclass is the intial response from the PowerData API endpoint"""

    power: PowerData


Power = Endpoint(
    endpoint="site/{siteid}/power",
    name="Site Power",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME],
    response=PowerDataResponse,
    returns="power"
)


@dataclass
class Connection:
    """Represents a power connection between two points in the powerflow.

    The JSON fields are named `from` and `to`, but the dataclass uses
    `from_` and `to_` to avoid using the Python keyword `from`.
    """
    from_: Optional[str] = None
    to_: Optional[str] = None


@dataclass
class PowerDetailInfo(baseclass):
    """This dataclass describes the detailed power information for a site component.

    Attributes:
        status: The operational status of the component.
        currentPower: The current power value for the component.
        chargeLevel: The charge level, if applicable.
        critical: Whether the component is in a critical state.
    """
    status: str
    currentPower: Optional[float] = None
    chargeLevel: Optional[int] = None
    critical: Optional[bool] = None
    timeLeft: Optional[int] = None


@dataclass
class SiteCurrentPowerFlow(baseclass):
    """This dataclass describes the current power flow for a site.

    Attributes:
        unit: The unit of measurement for power values.
        GRID: Detailed power information for the grid connection.
        LOAD: Detailed power information for the site load.
        PV: Detailed power information for the photovoltaic system.
        STORAGE: Detailed power information for the storage system.
        connections: List of power connections between site components.
    """
    unit: Unit
    updateRefreshRate: int
    GRID: PowerDetailInfo
    LOAD: PowerDetailInfo
    PV: PowerDetailInfo
    STORAGE: Optional[PowerDetailInfo] = None
    connections: List[Connection] = field(default_factory=list)


@dataclass
class PowerFlowResponse(baseclass):
    """This dataclass is the intial response from the PowerFlow API endpoint"""

    siteCurrentPowerFlow: SiteCurrentPowerFlow


PowerFlow = Endpoint(
    endpoint="site/{siteid}/currentPowerFlow",
    name="Site Power Flow",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=PowerFlowResponse,
    returns="siteCurrentPowerFlow"
)


@dataclass
class BatteryTelemetry(baseclass):
    """This dataclass describes the telemetry information for a battery.

    Attributes:
        timeStamp: The timestamp of the telemetry reading.
        power: The current power value of the battery.
        batteryState: The operational state of the battery.
        lifeTimeEnergyCharged: Total energy charged over the battery's lifetime.
        lifeTimeEnergyDischarged: Total energy discharged over the battery's lifetime.
        fullPackEnergyAvailable: The available energy in the battery pack.
        internalTemp: The internal temperature of the battery.
        ACGridCharging: The amount of AC grid charging.
    """
    timeStamp: str
    power: int
    batteryState: int
    lifeTimeEnergyCharged: int
    lifeTimeEnergyDischarged: int
    fullPackEnergyAvailable: int
    internalTemp: int
    ACGridCharging: int


@dataclass
class Battery(baseclass):
    """This dataclass describes the battery information and telemetry data returned by the Storage API endpoint.

    Attributes:
        nameplate: The nameplate capacity of the battery.
        serialNumber: The serial number of the battery.
        modelNumber: The model number of the battery.
        telemetryCount: The number of telemetry records.
        telemetries: A list of telemetry data for the battery.
    """
    nameplate: int
    serialNumber: str
    modelNumber: str
    telemetryCount: int
    telemetries: List[BatteryTelemetry] = field(default_factory=list)


@dataclass
class StorageData(baseclass):
    """This dataclass describes the storage data returned by the Storage API endpoint.

    Attributes:
        batteryCount: The number of batteries included in the response.
        batteries: A list of battery information and telemetry data.
    """
    batteryCount: int
    batteries: List[Battery] = field(default_factory=list)


@dataclass
class StorageDataResponse(baseclass):
    """This dataclass describes the response from the Storage API endpoint.

    Attributes:
        storageData: The storage data containing battery information and telemetry.
    """
    storageData: StorageData


Storage = Endpoint(
    endpoint="site/{siteid}/storageData",
    name="Battery Telemetry",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY, APIParms.START_TIME,
           APIParms.END_TIME, APIParms.SERIALS],
    response=StorageDataResponse,
    returns="storageData"
)


@dataclass
class Meter(baseclass):
    """This dataclass describes the meter information provided by the Inventory API Endpoint"""

    name: str
    manufacturer: str
    model: str
    SN: Optional[str] = None


@dataclass
class Sensor(baseclass):
    """This dataclass describes the sensor information provided by the Inventory API Endpoint

    Attributes:
        connectedSolaredgeDeviceSN: The serial number of the connected SolarEdge device.
        connectedTo: The type of device the sensor is connected to.
        id: The unique identifier of the sensor.
        category: The category of the sensor.
        type: The type of sensor."""

    connectedSolaredgeDeviceSN: str
    connectedTo: str
    id: str
    category: str
    type: str


@dataclass
class Gateway(baseclass):
    """This dataclass describes the gatewayinformation provided by the Inventory API Endpoint

    Attributes:
        name: The name of the gateway.
        serialNumber: The serial number of the gateway.
        firmwareVersion: The firmware version of the gateway."""

    name: str
    serialNumber: str
    firmwareVersion: str


@dataclass
class BatteryInventory(baseclass):
    """This dataclass describes the battery inventory information provided by the Inventory API Endpoint.

    Attributes:
        name: The name of the battery.
        manufacturer: The manufacturer of the battery.
        model: The model of the battery.
        firmwareVersion: The firmware version of the battery.
        connectedInverterSn: The serial number of the connected inverter.
        nameplateCapacity: The nameplate capacity of the battery.
        SN: The serial number of the battery.
    """

    name: str
    manufacturer: str
    model: str
    firmwareVersion: str
    connectedInverterSn: str
    nameplateCapacity: float
    SN: str


@dataclass
class Inverter(baseclass):
    """This dataclass describes the inverter information provided by the Inventory API Endpoint

    Attributes:
        SN: The serial number of the inverter which is used in other API requests

        name, manufacturer, model, communicationMethod, cpuVersion, connectedOptimizers"""

    SN: str
    name: str
    manufacturer: str
    model: str
    communicationMethod: str
    dsp1Version: str
    dsp2Version: str
    cpuVersion: str
    connectedOptimizers: int
    partNumber: str
    site: Optional[int] = None


@dataclass
class InventoryData(baseclass):
    """This dataclass describes the information provided by the Inventory API Endpoint

    Attributes:
        meters : A list of the meters that are associated with the site ID
        sensors : A list of the sensors that are associated with the site ID
        batteries : A list of the batteries that are associated with the site ID
        inverters : A list of the inverters that are associated with the site ID
        gateways : A list of the gateways that are associated with the site ID
        site : The site ID is added as an additional attribute but not returned by the API
    """

    meters: List[Meter] = field(default_factory=list)
    sensors: List[Sensor] = field(default_factory=list)
    gateways: List[Gateway] = field(default_factory=list)
    batteries: List[BatteryInventory] = field(default_factory=list)
    inverters: List[Inverter] = field(default_factory=list)
    site: Optional[int] = None


@dataclass
class InventoryResponse(baseclass):
    """This dataclass describes the response from the Inventory API endpoint.

    Attributes:
        Inventory: The inventory data containing meters, sensors, batteries, inverters, gateways, and site information.
    """

    Inventory: InventoryData


Inventory = Endpoint(
    endpoint="site/{siteid}/inventory",
    name="Site Inventory",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=InventoryResponse,
    returns="Inventory"
)


@dataclass
class ComponentEntry(baseclass):
    """This dataclass describes a single component entry provided by the Components API Endpoint.

    Attributes:
        name: The name of the component.
        manufacturer: The manufacturer of the component.
        model: The model of the component.
        serialNumber: The serial number of the component.
        kWpDC: The DC power rating of the component in kilowatts.
        site: The site ID associated with the component, if available.
    """

    name: str
    manufacturer: str
    model: str
    serialNumber: str
    kWpDC: str
    site: Optional[int] = None


@dataclass
class ComponentList(baseclass):
    """This dataclass describes the information provided by the Components API Endpoint

    Attributes:
        count: The total number of components returned by the API.
        list: A list of ComponentEntry objects representing the individual components."""

    count: int
    list: List[ComponentEntry] = field(default_factory=list)


@dataclass
class ComponentsResponse(baseclass):
    """This dataclass describes the response from the Components API endpoint

    Attributes:
        reporters: The list of components returned by the API, encapsulated in a ComponentList object.
    """

    reporters: ComponentList


# This endpoint returns a list of equipment/components for a given site, including details such as name, manufacturer, model, serial number, and kWpDC.
Components = Endpoint(
    endpoint="equipment/{siteid}/list",
    name="Site Components",
    arguments=[APIArgs.SITEID],
    parms=[APIParms.API_KEY],
    response=ComponentsResponse,
    returns="reporters"
)


@dataclass
class LData(baseclass):
    """This dataclass describes the phase information as part of the inverter telemetry.

    Attributes:
        acCurrent: The AC current for the phase.
        acVoltage: The AC voltage for the phase.
        acFrequency: The AC frequency for the phase.
        activePower: The active power for the phase.
        reactivePower: The reactive power for the phase.
        apparentPower: The apparent power for the phase, if available.
        cosPhi: The power factor (cosine of the phase angle) for the phase, if available."""

    acCurrent: float
    acVoltage: float
    acFrequency: float
    activePower: float
    reactivePower: float
    apparentPower: Optional[float] = 0.0
    cosPhi: Optional[float] = 0.0


@dataclass
class Telemetry(baseclass):
    """This dataclass describes the telemetry information provided for the inverter.

    Attributes:
        date: The timestamp of the telemetry reading.
        totalActivePower: The total active power output of the inverter.
        powerLimit: The power limit set for the inverter.
        totalEnergy: The total energy produced by the inverter.
        temperature: The temperature of the inverter.
        inverterMode: The operational mode of the inverter.
        operationMode: The operation mode of the inverter.
        L1Data: The telemetry data for phase L1.
        L2Data: The telemetry data for phase L2, if available.
        L3Data: The telemetry data for phase L3, if available.
        groundFaultResistance: The ground fault resistance, if available.
        vL1To2: The voltage between phases L1 and L2, if available.
        vL2To3: The voltage between phases L2 and L3, if available.
        vL3To1: The voltage between phases L3 and L1, if available.
        dcVoltage: The DC voltage of the inverter, if available."""

    date: datetime
    totalActivePower: float
    powerLimit: float
    totalEnergy: float
    temperature: float
    inverterMode: InverterMode
    operationMode: OperationMode
    L1Data: LData = field(default_factory=lambda: LData(
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    L2Data: Optional[LData] = None
    L3Data: Optional[LData] = None
    groundFaultResistance: Optional[float] = 0.0
    vL1To2: Optional[float] = 0.0
    vL2To3: Optional[float] = 0.0
    vL3To1: Optional[float] = 0.0
    dcVoltage: Optional[float] = 0.0


@dataclass
class InverterInfo(baseclass):
    """This dataclass describes the information provided by the InverterTelemetry API Endpoint

    Attributes:
        count: The total number of telemetry records returned by the API.
        telemetries: A list of Telemetry objects representing the individual telemetry records."""

    count: int
    telemetries: List[Telemetry] = field(default_factory=list)


@dataclass
class InverterResponse(baseclass):
    """This dataclass describes the response from the InverterTelemetry API endpoint

    Attributes:
        data: The inverter telemetry data."""

    data: InverterInfo


InverterTelemetry = Endpoint(
    endpoint="equipment/{siteid}/{serialnumber}/data",
    name="Inverter Technical Data",
    arguments=[APIArgs.SITEID, APIArgs.SERIALNUMBER],
    parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME],
    response=InverterResponse,
    returns="data"
)


class ConstantList(Enum):
    """This enum lists all the defined constant, making it easy to reference them.
    The Enum value is the instance of the constant.
    """

    TimeUnit = TimeUnit
    Unit = Unit
    Order = Order
    SiteStatus = SiteStatus
    Property = Property
    Meters = Meters
    Metrics = Metrics
    InverterMode = InverterMode
    OperationMode = OperationMode
    Endpoint = Endpoint
    DateFormats = DateFormats


class APIList(Enum):
    """This enum lists all the defined API endpoints, making it easy to reference them.
    The Enum value is the instance of the Endpoint class that describes the endpoint.
    """

    Sites = Sites
    SiteInfo = SiteInfo
    SiteBenefits = SiteBenefits
    SiteOverview = SiteOverview
    SiteDataPeriod = SiteDataPeriod
    SiteEnergy = SiteEnergy
    SiteEnergyTimeframe = SiteEnergyTimeframe
    EnergyDetails = EnergyDetails
    Power = Power
    PowerDetails = PowerDetails
    PowerFlow = PowerFlow
    Storage = Storage
    Inventory = Inventory
    Components = Components
    InverterData = InverterTelemetry


@dataclass
class responses(APIResponses):
    """Maps API endpoints to their response classes.

    This dataclass is used by the `RESTClient` configuration to know which
    dataclass should be used to parse each API endpoint's JSON response.
    """
    Sites: SitesResponse
    SiteInfo: SiteInfoResponse
    SiteBenefits: EnvBenefitsResponse
    SiteImage: str
    SiteOverview: OverviewResponse
    SiteDataPeriod: SiteDataPeriodResponse
    SiteEnergy: EnergyDataResponse
    SiteEnergyTimeframe: TimeFrameEnergyResponse
    EnergyDetails: EnergyDetailResponse
    Power: PowerDataResponse
    PowerDetails: PowerDetailsResponse
    PowerFlow: PowerFlowResponse
    Storage: StorageDataResponse
    Inventory: InventoryResponse
    Components: ComponentsResponse
    InverterTelemetry: InverterResponse


@dataclass
class SummaryData:
    """This dataclass is used to store data returned by multiple calls to the REST API."""

    sites: List[Site] = field(default_factory=list)
    inventories: List[InventoryData] = field(default_factory=list)
    components: List[ComponentEntry] = field(default_factory=list)


@dataclass
class RESTClient:
    """This dataclass defines the set of information necessary to use a REST API.

    Attributes:
        url: The URL used for the REST API
        auth: The type of authorisation used
        apis: A list of the API Endpoints
        apiargs: A dataclass describing the set of arguments used by the endpoints
        apiparms: A dataclass describing the set of parameters used by the endpoints
        constants: A list of constants
    """

    url: str
    apilist: Type[Enum]
    arguments: apiargs
    parameters: apiparms
    constants: Type[Enum]
    responses: Type[responses]
    auth: Optional[Type[Enum]] = None


# This instance of RESTClient describes the SolarEdge API
Solaredge = RESTClient(
    url="https://monitoringapi.solaredge.com",
    auth=None,
    apilist=APIList,
    arguments=apiargs(),
    parameters=apiparms(),
    constants=ConstantList,
    responses=responses
)
