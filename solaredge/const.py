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

RESTClient: The RESTClient data class represents the configuration for making API requests.
It includes information such as the API URL, authentication method, supported API endpoints, arguments, parameters,
and constants. The Solaredge instance of the RESTClient is configured to interact with the SolarEdge API.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

import dateutil.parser
from dataclasses_json import config, dataclass_json


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


@dataclass(frozen=True)
class Endpoint:
    """Dataclass describing API endpoints and the data they return."""
    response: object
    name: str = None
    endpoint: str = ""
    type: str = "get"
    auth: str = None
    arguments: list = field(default_factory=list)
    parms: list = field(default_factory=list)


@dataclass
class Location:
    """This dataclass describes the location information provided in multiple API endpoints"""
    country: str
    city: str
    address: str
    address2: str
    zip: str
    timeZone: str
    countryCode: str


@dataclass
class PrimaryModule:
    manufacturerName: str
    modelName: str
    maximumPower: float
    temperatureCoef: float


@dataclass
class Uris:
    SITE_IMAGE: str
    DATA_PERIOD: str
    DETAILS: str
    OVERVIEW: str


@dataclass
class PublicSettings:
    isPublic: bool
    name: str = None


@dataclass
class Site:
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
    status: str
    peakPower: float
    lastUpdateTime: datetime
    currency: str
    installationDate: datetime
    ptoDate: str
    notes: str
    type: str
    location: Location
    primaryModule: PrimaryModule
    uris: Uris
    publicSettings: PublicSettings
    alertQuantity: Optional[int] = 0
    alertSeverity: Optional[str] = None

    def __post_init__(self):
        self.publicSettings = PublicSettings(**self.publicSettings)
        self.location = Location(**self.location)
        self.primaryModule = PrimaryModule(**self.primaryModule)
        self.uris = Uris(**self.uris)
        self.installationDate = dateutil.parser.parse(self.installationDate)
        self.lastUpdateTime = dateutil.parser.parse(self.lastUpdateTime)


@dataclass
class SiteList:
    """This dataclass describes the list of sites provided by the Sites API endpoint"""
    count: int
    site: List[Site]

    def __post_init__(self):
        for index, entry in enumerate(self.site):
            if isinstance(entry, dict):
                self.site[index] = Site(**self.site[index])


@dataclass
class SitesResponse:
    """This dataclass describes the response from the Sites API endpoint"""
    sites: SiteList

    def __post_init__(self):
        self.sites = SiteList(**self.sites)


Sites = Endpoint(endpoint="sites/list",
                 name="Site List",
                 parms=[APIParms.API_KEY, APIParms.SIZE, APIParms.START_INDEX, APIParms.SEARCH_TEXT,
                        APIParms.SORT_PROPERTY, APIParms.SORT_ORDER, APIParms.STATUS],
                 response=SitesResponse)


@dataclass
class SiteInfoResponse:
    """This dataclass describes the response from the SiteInfo API endpoint"""
    details: Site

    def __post_init__(self):
        self.details = SiteInfo(**self.details)


SiteInfo = Endpoint(endpoint="site/{siteid}/details",
                    name="Site Details",
                    arguments=[APIArgs.SITEID],
                    parms=[APIParms.API_KEY],
                    response=SiteInfoResponse)


@dataclass
class GasEmissionSaved:
    units: str
    co2: float
    so2: float
    nox: float


@dataclass
class EnvBenefits:
    gasEmissionSaved: GasEmissionSaved
    treesPlanted: float
    lightBulbs: float

    def __post_init__(self):
        self.gasEmissionSaved = GasEmissionSaved(**self.gasEmissionSaved)


@dataclass
class EnvBenefitsResponse:
    envBenefits: EnvBenefits

    def __post_init__(self):
        self.envBenefits = EnvBenefits(**self.envBenefits)


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
class SummaryData:
    energy: float
    revenue: Optional[float] = None


@dataclass
class CurrentPower:
    power: float


@dataclass
class OverviewData:
    lastUpdateTime: datetime
    lifeTimeData: SummaryData
    lastYearData: SummaryData
    lastMonthData: SummaryData
    lastDayData: SummaryData
    currentPower: CurrentPower
    measuredBy: str

    def __post_init__(self):
        self.lastUpdateTime = dateutil.parser.parse(self.lastUpdateTime)
        self.lifeTimeData = SummaryData(**self.lifeTimeData)
        self.lastYearData = SummaryData(**self.lastYearData)
        self.lastMonthData = SummaryData(**self.lastMonthData)
        self.lastDayData = SummaryData(**self.lastDayData)
        self.currentPower = CurrentPower(**self.currentPower)


@dataclass
class OverviewResponse:
    overview: OverviewData

    def __post_init__(self):
        self.overview = OverviewData(**self.overview)


SiteOverview = Endpoint(endpoint="site/{siteid}/overview",
                        name="Site Overview",
                        arguments=[APIArgs.SITEID],
                        parms=[APIParms.API_KEY],
                        response=OverviewResponse)


@dataclass
class DataPeriod:
    startDate: datetime
    endDate: datetime

    def __post_init__(self):
        self.startDate = dateutil.parser.parse(self.startDate)
        self.endDate = dateutil.parser.parse(self.endDate)


@dataclass
class SiteDataPeriodResponse:
    dataPeriod: DataPeriod

    def __post_init__(self):
        self.dataPeriod = DataPeriod(**self.dataPeriod)


SiteDataPeriod = Endpoint(endpoint="site/{siteid}/dataPeriod",
                          name="Site Data: Start and End Dates",
                          arguments=[APIArgs.SITEID],
                          parms=[APIParms.API_KEY],
                          response=SiteDataPeriodResponse)


@dataclass
class Value:
    date: datetime
    value: float = 0

    def __post_init__(self):
        self.date = dateutil.parser.parse(self.date)
        if self.value is None:
            self.value = 0


@dataclass
class EnergyData:
    timeUnit: TimeUnit
    unit: str
    measuredBy: str
    values: List[Value]

    def __post_init__(self):
        for index, entry in enumerate(self.values):
            if isinstance(entry, dict):
                self.values[index] = Value(**self.values[index])


@dataclass
class EnergyDataResponse:
    energy: EnergyData

    def __post_init__(self):
        self.energy = EnergyData(**self.energy)


SiteEnergy = Endpoint(endpoint="site/{siteid}/energy",
                      name="Site Energy",
                      arguments=[APIArgs.SITEID],
                      parms=[APIParms.API_KEY, APIParms.START_DATE,
                             APIParms.END_DATE, APIParms.TIME_UNIT],
                      response=EnergyDataResponse)


@dataclass
class EnergyValue:
    date: datetime
    energy: float
    unit: str

    def __post_init__(self):
        self.date = dateutil.parser.parse(self.date)


@dataclass
class TimeFrameEnergyData:
    energy: float
    unit: str
    measuredBy: str
    startLifetimeEnergy: EnergyValue
    endLifetimeEnergy: EnergyValue

    def __post_init__(self):
        self.startLifetimeEnergy = EnergyValue(**self.startLifetimeEnergy)
        self.endLifetimeEnergy = EnergyValue(**self.endLifetimeEnergy)


@dataclass
class TimeFrameEnergyResponse:
    timeFrameEnergy: TimeFrameEnergyData

    def __post_init__(self):
        self.timeFrameEnergy = TimeFrameEnergyData(**self.timeFrameEnergy)


SiteEnergyTimeframe = Endpoint(endpoint="site/{siteid}/timeFrameEnergy",
                               name="Site Energy – Time Period",
                               arguments=[APIArgs.SITEID],
                               parms=[APIParms.API_KEY,
                                      APIParms.START_DATE, APIParms.END_DATE],
                               response=TimeFrameEnergyResponse)


@dataclass
class MeterData:
    type: str
    values: List[Value]

    def __post_init__(self):
        for index, entry in enumerate(self.values):
            if isinstance(entry, dict):
                self.values[index] = Value(**self.values[index])


@dataclass
class EnergyDetailData:
    timeUnit: TimeUnit
    unit: str
    meters: List[MeterData]

    def __post_init__(self):
        for index, entry in enumerate(self.meters):
            if isinstance(entry, dict):
                self.meters[index] = MeterData(**self.meters[index])


@dataclass
class EnergyDetailResponse:
    energyDetails: EnergyDetailData

    def __post_init__(self):
        self.energyDetails = EnergyDetailData(**self.energyDetails)


EnergyDetails = Endpoint(endpoint="site/{siteid}/energyDetails",
                         arguments=[APIArgs.SITEID],
                         parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME,
                                APIParms.TIME_UNIT, APIParms.METERS],
                         response=EnergyDetailResponse)


@dataclass
class PowerData:
    timeUnit: TimeUnit
    unit: str
    measuredBy: str
    values: List[Value]

    def __post_init__(self):
        for index, entry in enumerate(self.values):
            if isinstance(entry, dict):
                self.values[index] = Value(**self.values[index])


@dataclass
class PowerDataResponse:
    power: PowerData

    def __post_init__(self):
        self.power = PowerData(**self.power)


Power = Endpoint(endpoint="site/{siteid}/power",
                 arguments=[APIArgs.SITEID],
                 parms=[APIParms.API_KEY, APIParms.START_TIME, APIParms.END_TIME],
                 response=PowerDataResponse)


@dataclass
class PowerType:
    type: str
    values: List[Value]

    def __post_init__(self):
        for index, entry in enumerate(self.values):
            if isinstance(entry, dict):
                self.values[index] = Value(**self.values[index])


@dataclass
class PowerDetailData:
    """ This dataclass defines the response to the PowerDetail API request

    Atttributes:
        timeUnit: The granularity of the data returned
        unit: The unit of the data returned
        meters: A list of different types of data that is returned
        """
    timeUnit: TimeUnit
    unit: str
    meters: List[PowerType]

    def __post_init__(self):
        for index, entry in enumerate(self.meters):
            if isinstance(entry, dict):
                self.meters[index] = PowerType(**self.meters[index])


@dataclass
class PowerDetailsResponse:
    """This dataclass describes the response from the Power Details API endpoint"""
    powerDetails: PowerDetailData

    def __post_init__(self):
        self.powerDetails = PowerDetailData(**self.powerDetails)


PowerDetails = Endpoint(endpoint="site/{siteid}/powerDetails",
                        arguments=[APIArgs.SITEID],
                        parms=[APIParms.API_KEY, APIParms.START_TIME,
                               APIParms.END_TIME, APIParms.METERS],
                        response=PowerDetailsResponse)


@dataclass_json
@dataclass
class Connection:
    from_: str = field(metadata=config(field_name="from"))
    to_: str = field(metadata=config(field_name="to"))


@dataclass
class PowerDetailInfo:
    status: str
    currentPower: float
    chargeLevel: int
    critical: bool


@dataclass
class SiteCurrentPowerFlow:
    unit: str
    connections: List[Connection]
    GRID: PowerDetailInfo
    LOAD: PowerDetailInfo
    PV: PowerDetailInfo
    STORAGE: PowerDetailInfo

    def __post_init__(self):
        self.GRID = PowerDetailInfo(**self.GRID)
        self.LOAD = PowerDetailInfo(**self.LOAD)
        self.PV = PowerDetailInfo(**self.PV)
        self.STORAGE = PowerDetailInfo(**self.STORAGE)
        for index, entry in enumerate(self.connections):
            if isinstance(entry, dict):
                self.connections[index] = Connection(**self.connections[index])


@dataclass
class PowerFlowResponse:
    siteCurrentPowerFlow: SiteCurrentPowerFlow

    def __post_init__(self):
        self.siteCurrentPowerFlow = PowerFlowResponse(
            **self.siteCurrentPowerFlow)


PowerFlow = Endpoint(endpoint="site/{siteid}/currentPowerFlow",
                     name="Site Power Flow",
                     arguments=[APIArgs.SITEID],
                     parms=[APIParms.API_KEY],
                     response=PowerFlowResponse)


@dataclass
class BatteryTelemetry:
    timeStamp: str
    power: int
    batteryState: int
    lifeTimeEnergyCharged: int
    lifeTimeEnergyDischarged: int
    fullPackEnergyAvailable: int
    internalTemp: int
    ACGridCharging: int


@dataclass
class Battery:
    nameplate: int
    serialNumber: str
    modelNumber: str
    telemetryCount: int
    telemetries: List[BatteryTelemetry]

    def __post_init__(self):
        for index, entry in enumerate(self.telemetries):
            if isinstance(entry, dict):
                self.telemetries[index] = BatteryTelemetry(
                    **self.telemetries[index])


@dataclass
class StorageData:
    batteryCount: int
    batteries: List[Battery]

    def __post_init__(self):
        for index, entry in enumerate(self.batteries):
            if isinstance(entry, dict):
                self.batteries[index] = Battery(**self.batteries[index])


@dataclass
class StorageDataResponse:
    storageData: StorageData

    def __post_init__(self):
        self.storageData = StorageData(**self.storageData)


Storage = Endpoint(endpoint="site/{siteid}/storageData",
                   name="Battery Telemetry",
                   arguments=[APIArgs.SITEID],
                   parms=[APIParms.API_KEY, APIParms.START_TIME,
                          APIParms.END_TIME, APIParms.SERIALS],
                   response=StorageDataResponse)


@dataclass
class Meter:
    name: str
    manufacturer: str
    model: str
    SN: str = None


@dataclass
class Sensor:
    """This dataclass describes the sensor information provided by the Inventory API Endpoint"""
    connectedSolaredgeDeviceSN: str
    connectedTo: str
    id: str
    category: str
    type: str


@dataclass
class Gateway:
    """This dataclass describes the gatewayinformation provided by the Inventory API Endpoint"""
    name: str
    serialNumber: str
    firmwareVersion: str


@dataclass
class Battery:
    """This dataclass describes the battery information provided by the Inventory API Endpoint"""
    name: str
    manufacturer: str
    model: str
    firmwareVersion: str
    connectedInverterSn: str
    nameplateCapacity: float
    SN: str


@dataclass
class Inverter:
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
class InventoryData:
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

    def __post_init__(self):
        for index, entry in enumerate(self.meters):
            if isinstance(entry, dict):
                self.meters[index] = Meter(**self.meters[index])
        for index, entry in enumerate(self.sensors):
            if isinstance(entry, dict):
                self.sensors[index] = Sensor(**self.sensors[index])
        for index, entry in enumerate(self.gateways):
            if isinstance(entry, dict):
                self.gateways[index] = Gateway(**self.gateways[index])
        for index, entry in enumerate(self.batteries):
            if isinstance(entry, dict):
                self.batteries[index] = Battery(**self.batteries[index])
        for index, entry in enumerate(self.inverters):
            if isinstance(entry, dict):
                self.inverters[index] = Inverter(**self.inverters[index])


@dataclass
class InventoryResponse:
    """This dataclass describes the response from the Inventory API endpoint"""
    Inventory: InventoryData

    def __post_init__(self):
        self.Inventory = InventoryData(**self.Inventory)


Inventory = Endpoint(endpoint="site/{siteid}/inventory",
                     name="Site Inventory",
                     arguments=[APIArgs.SITEID],
                     parms=[APIParms.API_KEY],
                     response=InventoryResponse)


@dataclass
class ComponentEntry:
    """This dataclass describes the component data provided by the Components API Endpoint"""
    name: str
    manufacturer: str
    model: str
    serialNumber: str
    kWpDC: str
    site: str = None


@dataclass
class ComponentList:
    """This dataclass describes the information provided by the Components API Endpoint"""
    count: int
    list: list[ComponentEntry]

    def __post_init__(self):
        for index, entry in enumerate(self.list):
            if isinstance(entry, dict):
                self.list[index] = ComponentEntry(**self.list[index])


@dataclass
class ComponentsResponse:
    """This dataclass describes the response from the Components API endpoint"""
    reporters: ComponentList

    def __post_init__(self):
        self.reporters = ComponentList(**self.reporters)


Components = Endpoint(endpoint="equipment/{siteid}/list",
                      name="Site Components",
                      arguments=[APIArgs.SITEID],
                      parms=[APIParms.API_KEY],
                      response=ComponentsResponse)


@dataclass
class LData:
    """This dataclass describes the phase information as part of the inverter telemetry."""
    acCurrent: float
    acVoltage: float
    acFrequency: float
    apparentPower: float
    activePower: float
    reactivePower: float
    cosPhi: float


@dataclass
class Telemetry:
    """This dataclass describes the telemetry information provided for the inverter."""
    date: datetime
    totalActivePower: float
    powerLimit: float
    totalEnergy: float
    temperature: float
    inverterMode: InverterMode
    operationMode: int
    groundFaultResistance: Optional[float] = 0
    vL1To2: float = 0
    vL2To3: float = 0
    vL3To1: float = 0
    dcVoltage: float = 0
    L1Data: LData = None
    L2Data: LData = None
    L3Data: LData = None

    def __post_init__(self):
        self.date = dateutil.parser.parse(self.date)
        if self.L1Data is not None:
            self.L1Data = LData(**self.L1Data)
        if self.L3Data is not None:
            self.L2Data = LData(**self.L2Data)
        if self.L3Data is not None:
            self.L3Data = LData(**self.L3Data)


@dataclass
class InverterInfo:
    """This dataclass describes the information provided by the InverterTelemetry API Endpoint"""
    count: int
    telemetries: List[Telemetry]

    def __post_init__(self):
        for index, entry in enumerate(self.telemetries):
            if isinstance(entry, dict):
                self.telemetries[index] = Telemetry(
                    **self.telemetries[index])


@dataclass
class InverterResponse:
    """This dataclass describes the response from the InverterTelemetry API endpoint"""
    data: InverterInfo

    def __post_init__(self):
        self.data = InverterInfo(**self.data)


InverterTelemetry = Endpoint(endpoint="equipment/{siteid}/{serialnumber}/data",
                             name="Inverter Technical Data",
                             arguments=[APIArgs.SITEID, APIArgs.SERIALNUMBER],
                             parms=[APIParms.API_KEY,
                                    APIParms.START_TIME, APIParms.END_TIME],
                             response=InverterResponse)


@dataclass
class Version:
    release: str


@dataclass
class VersionResponse:
    version: Version

    def __post_init__(self):
        self.version = Version(**self.version)


CurrentVersion = Endpoint(endpoint="version/current",
                          name="Current Version",
                          parms=[APIParms.API_KEY],
                          response=VersionResponse)


@dataclass
class VersionsResponse:
    supported: List[Version]

    def __post_init__(self):
        for index, entry in enumerate(self.supported):
            if isinstance(entry, dict):
                self.supported[index] = Version(**self.supported[index])


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
    auth: str
    apilist: Enum
    arguments: APIArguments
    parameters: APIParameters
    constants: Enum


# This instance of RESTClient describes the SolarEdge API
Solaredge = RESTClient(
    url="https://monitoringapi.solaredge.com",
    auth=None,
    apilist=APIList,
    arguments=APIArguments(),
    parameters=APIParameters(),
    constants=ConstantList
)
