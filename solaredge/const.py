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
from datetime import datetime, timedelta, date
from enum import Enum
from typing import List

from dataclasses_json import config, dataclass_json
from solaredge.apiconstruct import baseclass, RESTClient, Endpoint


class TimeUnit(Enum):
    QUARTER_OF_AN_HOUR = "QUARTER_OF_AN_HOUR"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class Unit(Enum):
    WATT = "W"
    WATT_HOUR = "Wh"


class Currency(Enum):
    EUR = "Euro"
    GBP = "Pounds Sterling"
    USD = "US Dollar"


class Order(Enum):
    ASCENDING = "ASC"
    DESCENDING = "DESC"


class SiteStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    DISABLED = "Disabled"
    ALL = "All"


class Property(Enum):
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


class Meters(Enum):
    PRODUCTION = "Production"
    CONSUMPTION = "Consumption"
    SELFCONSUMPTION = "SelfConsumption"
    FEEDIN = "FeedIn"
    PURCHASED = "Purchased"


class Metrics(Enum):
    METRIC = "Metric"
    IMPERIAL = "Imperial"


class InverterMode(Enum):
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


class OperationMode(Enum):
    ON_GRID = 1
    OFF_GRID_PV_BATTERY = 2
    OFF_GRID_GENERATOR = 3


class APIArgs(Enum):
    """Enum containing the set of arguments used by the API endpoints."""
    SITEID = "siteid"
    SERIALNUMBER = "serialnumber"


@dataclass
class APIArguments:
    """Dataclass describing the set of arguments used by the API endpoints."""
    siteid: str = None
    serialnumber: str = None


class APIParms(Enum):
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


@dataclass
class APIParameters:
    """Dataclass describing the set of parameters used by the API endpoints."""
    size: int = 100
    startIndex: int = 0
    searchText: str = None
    sortProperty: Property = None
    sortOrder: Order = Order.ASCENDING.value
    Status: SiteStatus = SiteStatus.ALL.value
    api_key: str = None
    startDate: str = (datetime.now(tz=None) -
                      timedelta(days=1)).strftime('%Y-%m-%d')
    endDate: str = (datetime.now(tz=None)).strftime('%Y-%m-%d')
    startTime: str = (datetime.now(tz=None)-timedelta(days=1)
                      ).strftime('%Y-%m-%d %H:%M:%S')
    endTime: str = datetime.now(tz=None).strftime('%Y-%m-%d %H:%M:%S')
    timeUnit: TimeUnit = TimeUnit.HOUR.value
    meters: Meters = None
    serials: str = None
    systemUnits: Metrics = Metrics.METRIC.value


@dataclass
class Location(baseclass):
    """This dataclass describes the location information provided in multiple API endpoints"""
    country: str
    city: str
    address: str
    address2: str
    zip: str
    timeZone: str
    countryCode: str


@dataclass
class PrimaryModule(baseclass):
    manufacturerName: str
    modelName: str
    maximumPower: float
    temperatureCoef: float


@dataclass
class Uris(baseclass):
    SITE_IMAGE: str
    DATA_PERIOD: str
    DETAILS: str
    OVERVIEW: str


@dataclass
class PublicSettings(baseclass):
    isPublic: bool
    name: str = None


@dataclass
class Site(baseclass):
    """This dataclass describes the site information provided by the Sites API endpoint

    Attributes:
        id: The Site ID which is used as a parameter in other API requests

        name, accountId, status, peakPower, lastUpdateTime, currency,
        installationDate, ptoDate, notes, type, location, primaryModule,
        uris, publicSettings

        alertQuantity and alertSeverity which may not be returned"""
    id: int
    name: str
    accountId: int
    status: SiteStatus
    peakPower: float
    lastUpdateTime: date
    currency: Currency
    installationDate: date
    ptoDate: str
    notes: str
    type: str
    location: Location
    primaryModule: PrimaryModule
    uris: Uris
    publicSettings: PublicSettings
    alertQuantity: int = 0
    alertSeverity: str = None


@dataclass
class SiteList(baseclass):
    """This dataclass describes the list of sites provided by the Sites API endpoint"""
    count: int
    site: list[Site]


@dataclass
class SitesResponse(baseclass):
    """This dataclass describes the response from the Sites API endpoint"""
    sites: SiteList


Sites = Endpoint(endpoint="sites/list",
                 name="Site List",
                 parms=[APIParms.API_KEY, APIParms.SIZE, APIParms.START_INDEX, APIParms.SEARCH_TEXT,
                        APIParms.SORT_PROPERTY, APIParms.SORT_ORDER, APIParms.STATUS],
                 sample="site_list.json",
                 response=SitesResponse)


@dataclass
class SiteInfoResponse(baseclass):
    """This dataclass describes the response from the SiteInfo API endpoint"""
    details: Site


SiteInfo = Endpoint(endpoint="site/{siteid}/details",
                    name="Site Details",
                    arguments=[APIArgs.SITEID],
                    parms=[APIParms.API_KEY],
                    response=SiteInfoResponse)


@dataclass
class GasEmissionSaved(baseclass):
    units: str
    co2: float
    so2: float
    nox: float


@dataclass
class EnvBenefits(baseclass):
    gasEmissionSaved: GasEmissionSaved
    treesPlanted: float
    lightBulbs: float


@dataclass
class EnvBenefitsResponse(baseclass):
    envBenefits: EnvBenefits


SiteBenefits = Endpoint(endpoint="site/{siteid}/envBenefits",
                        name="Site Environmental Benefits",
                        arguments=[APIArgs.SITEID],
                        parms=[APIParms.API_KEY],
                        response=EnvBenefitsResponse)

SiteImage = Endpoint(endpoint="site/{siteid}/siteimage/{name}",
                     name="Site Image",
                     arguments=[APIArgs.SITEID],
                     parms=[APIParms.API_KEY],
                     response=str)


@dataclass
class SummaryData(baseclass):
    energy: float
    revenue: float = None


@dataclass
class CurrentPower(baseclass):
    power: float


@dataclass
class OverviewData(baseclass):
    lastUpdateTime: datetime
    lifeTimeData: SummaryData
    lastYearData: SummaryData
    lastMonthData: SummaryData
    lastDayData: SummaryData
    currentPower: CurrentPower
    measuredBy: str


@dataclass
class OverviewResponse(baseclass):
    overview: OverviewData


SiteOverview = Endpoint(endpoint="site/{siteid}/overview",
                        name="Site Overview",
                        arguments=[APIArgs.SITEID],
                        parms=[APIParms.API_KEY],
                        response=OverviewResponse)


@dataclass
class DataPeriod(baseclass):
    startDate: datetime
    endDate: datetime


@dataclass
class SiteDataPeriodResponse(baseclass):
    dataPeriod: DataPeriod


SiteDataPeriod = Endpoint(endpoint="site/{siteid}/dataPeriod",
                          name="Site Data: Start and End Dates",
                          arguments=[APIArgs.SITEID],
                          parms=[APIParms.API_KEY],
                          response=SiteDataPeriodResponse)


@dataclass
class Value(baseclass):
    date: datetime
    value: float = float(0)

    def __post_init__(self):
        super().__post_init__()
        if self.value is None:
            self.value = float(0)


@dataclass
class EnergyData(baseclass):
    timeUnit: TimeUnit
    unit: str
    measuredBy: str
    values: List[Value]


@dataclass
class EnergyDataResponse(baseclass):
    energy: EnergyData


SiteEnergy = Endpoint(endpoint="site/{siteid}/energy",
                      name="Site Energy",
                      arguments=[APIArgs.SITEID],
                      parms=[APIParms.API_KEY, APIParms.START_DATE,
                             APIParms.END_DATE, APIParms.TIME_UNIT],
                      sample="site_energy.json",
                      response=EnergyDataResponse)


@dataclass
class EnergyValue(baseclass):
    date: datetime
    energy: float
    unit: str


@dataclass
class TimeFrameEnergyData(baseclass):
    energy: float
    unit: str
    measuredBy: str
    startLifetimeEnergy: EnergyValue
    endLifetimeEnergy: EnergyValue


@dataclass
class TimeFrameEnergyResponse(baseclass):
    timeFrameEnergy: TimeFrameEnergyData


SiteEnergyTimeframe = Endpoint(endpoint="site/{siteid}/timeFrameEnergy",
                               name="Site Energy - Time Period",
                               arguments=[APIArgs.SITEID],
                               parms=[APIParms.API_KEY,
                                      APIParms.START_DATE, APIParms.END_DATE],
                               response=TimeFrameEnergyResponse)


@dataclass
class DataType(baseclass):
    type: str
    values: List[Value]


@dataclass
class DetailData(baseclass):
    """ This dataclass defines the response to the PowerDetail API request

    Atttributes:
        timeUnit: The granularity of the data returned
        unit: The unit of the data returned
        meters: A list of different types of data that is returned
        """
    timeUnit: TimeUnit
    unit: str
    meters: List[DataType]


@dataclass
class EnergyDetailResponse(baseclass):
    energyDetails: DetailData


EnergyDetails = Endpoint(endpoint="site/{siteid}/energyDetails",
                         name="Site Energy - Details",
                         arguments=[APIArgs.SITEID],
                         parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME,
                                APIParms.TIME_UNIT, APIParms.METERS],
                         response=EnergyDetailResponse)


@dataclass
class PowerDetailsResponse(baseclass):
    """This dataclass describes the response from the Power Details API endpoint"""
    powerDetails: DetailData


PowerDetails = Endpoint(endpoint="site/{siteid}/powerDetails",
                        name="Site Power - Details",
                        arguments=[APIArgs.SITEID],
                        parms=[APIParms.API_KEY, APIParms.START_TIME,
                               APIParms.END_TIME, APIParms.METERS],
                        response=PowerDetailsResponse)


@dataclass
class PowerData(baseclass):
    timeUnit: TimeUnit
    unit: str
    measuredBy: str
    values: List[Value]


@dataclass
class PowerDataResponse(baseclass):
    power: PowerData


Power = Endpoint(endpoint="site/{siteid}/power",
                 name="Site Power",
                 arguments=[APIArgs.SITEID],
                 parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME],
                 response=PowerDataResponse)


@dataclass_json
@dataclass
class Connection:
    from_: str = field(metadata=config(field_name="from"))
    to_: str = field(metadata=config(field_name="to"))


@dataclass
class PowerDetailInfo(baseclass):
    status: str
    currentPower: float
    chargeLevel: int
    critical: bool


@dataclass
class SiteCurrentPowerFlow(baseclass):
    unit: str
    connections: List[Connection]
    GRID: PowerDetailInfo
    LOAD: PowerDetailInfo
    PV: PowerDetailInfo
    STORAGE: PowerDetailInfo


@dataclass
class PowerFlowResponse(baseclass):
    siteCurrentPowerFlow: SiteCurrentPowerFlow


PowerFlow = Endpoint(endpoint="site/{siteid}/currentPowerFlow",
                     name="Site Power Flow",
                     arguments=[APIArgs.SITEID],
                     parms=[APIParms.API_KEY],
                     response=PowerFlowResponse)


@dataclass
class BatteryTelemetry(baseclass):
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
    nameplate: int
    serialNumber: str
    modelNumber: str
    telemetryCount: int
    telemetries: List[BatteryTelemetry]


@dataclass
class StorageData(baseclass):
    batteryCount: int
    batteries: List[Battery]


@dataclass
class StorageDataResponse(baseclass):
    storageData: StorageData


Storage = Endpoint(endpoint="site/{siteid}/storageData",
                   name="Battery Telemetry",
                   arguments=[APIArgs.SITEID],
                   parms=[APIParms.API_KEY, APIParms.START_TIME,
                          APIParms.END_TIME, APIParms.SERIALS],
                   response=StorageDataResponse)


@dataclass
class Meter(baseclass):
    name: str
    manufacturer: str
    model: str
    SN: str = None


@dataclass
class Sensor(baseclass):
    """This dataclass describes the sensor information provided by the Inventory API Endpoint"""
    connectedSolaredgeDeviceSN: str
    connectedTo: str
    id: str
    category: str
    type: str


@dataclass
class Gateway(baseclass):
    """This dataclass describes the gatewayinformation provided by the Inventory API Endpoint"""
    name: str
    serialNumber: str
    firmwareVersion: str


@dataclass
class Battery(baseclass):
    """This dataclass describes the battery information provided by the Inventory API Endpoint"""
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
    cpuVersion: str
    connectedOptimizers: int


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
    meters: list[Meter]
    sensors: list[Sensor]
    gateways: list[Gateway]
    batteries: list[Battery]
    inverters: list[Inverter]
    site: str = None


@dataclass
class InventoryResponse(baseclass):
    """This dataclass describes the response from the Inventory API endpoint"""
    Inventory: InventoryData


Inventory = Endpoint(endpoint="site/{siteid}/inventory",
                     name="Site Inventory",
                     arguments=[APIArgs.SITEID],
                     parms=[APIParms.API_KEY],
                     response=InventoryResponse)


@dataclass
class ComponentEntry(baseclass):
    """This dataclass describes the component data provided by the Components API Endpoint"""
    name: str
    manufacturer: str
    model: str
    serialNumber: str
    kWpDC: str
    site: str = None


@dataclass
class ComponentList(baseclass):
    """This dataclass describes the information provided by the Components API Endpoint"""
    count: int
    list: list[ComponentEntry]


@dataclass
class ComponentsResponse(baseclass):
    """This dataclass describes the response from the Components API endpoint"""
    reporters: ComponentList


Components = Endpoint(endpoint="equipment/{siteid}/list",
                      name="Site Components",
                      arguments=[APIArgs.SITEID],
                      parms=[APIParms.API_KEY],
                      response=ComponentsResponse)


@dataclass
class LData(baseclass):
    """This dataclass describes the phase information as part of the inverter telemetry."""
    acCurrent: float
    acVoltage: float
    acFrequency: float
    apparentPower: float
    activePower: float
    reactivePower: float
    cosPhi: float


@dataclass
class Telemetry(baseclass):
    """This dataclass describes the telemetry information provided for the inverter."""
    date: datetime
    totalActivePower: float
    powerLimit: float
    totalEnergy: float
    temperature: float
    inverterMode: InverterMode
    operationMode: int
    groundFaultResistance: float = 0
    vL1To2: float = 0
    vL2To3: float = 0
    vL3To1: float = 0
    dcVoltage: float = 0
    L1Data: LData = None
    L2Data: LData = None
    L3Data: LData = None


@dataclass
class InverterInfo(baseclass):
    """This dataclass describes the information provided by the InverterTelemetry API Endpoint"""
    count: int
    telemetries: List[Telemetry]


@dataclass
class InverterResponse(baseclass):
    """This dataclass describes the response from the InverterTelemetry API endpoint"""
    data: InverterInfo


InverterTelemetry = Endpoint(endpoint="equipment/{siteid}/{serialnumber}/data",
                             name="Inverter Technical Data",
                             arguments=[APIArgs.SITEID, APIArgs.SERIALNUMBER],
                             parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME],
                             response=InverterResponse)


@dataclass
class Version(baseclass):
    release: str


@dataclass
class VersionResponse(baseclass):
    version: Version


CurrentVersion = Endpoint(endpoint="version/current",
                          name="Current Version",
                          parms=[APIParms.API_KEY],
                          response=VersionResponse)


@dataclass
class VersionsResponse(baseclass):
    supported: List[Version]


SupportedVersions = Endpoint(endpoint="version/supported",
                             name="Supported Vesions",
                             parms=[APIParms.API_KEY],
                             response=VersionsResponse)


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


class APIList(Enum):
    """This enum lists all the defined API endpoints, making it easy to reference them.
    The Enum value is the instance of the Endpoint class that describes the endpoint.
    """
    Sites = Sites
    SiteInfo = SiteInfo
    SiteBenefits = SiteBenefits
    SiteImage = SiteImage
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
    CurrentVersion = CurrentVersion
    SupportedVersions = SupportedVersions


@dataclass
class SummaryData:
    """This dataclass is used to store data returned by multiple calls to the REST API."""
    sites: list[Site] = field(default_factory=list)
    inventories: list[InventoryData] = field(default_factory=list)
    components: list[ComponentEntry] = field(default_factory=list)


# This instance of RESTClient describes the SolarEdge API
Solaredge = RESTClient(
    url="https://monitoringapi.solaredge.com",
    auth=None,
    apilist=APIList,
    arguments=APIArguments(),
    parameters=APIParameters(),
    constants=ConstantList
)
