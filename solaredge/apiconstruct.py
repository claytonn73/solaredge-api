"""This code contains dataclasses which enable the construction of REST API clients

RESTClient: The RESTClient data class represents the configuration for making API requests.
It includes information such as the API URL, authentication method, supported API endpoints, arguments, parameters,
and constants."""

import logging
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date, datetime, time
from enum import Enum
from typing import Type, get_args, get_origin, Any

import ciso8601

logger = logging.getLogger(__name__)

@dataclass
class baseclass:
    """This dataclass provides the post_init code to handle the nested dataclasses
    and formatting of datetime entries"""

    def parse_kwargs(self, cls, **kwargs: dict):
        # If the key is in our reserved map, rename it; otherwise keep it as-is                
        reserved_map = {'class': 'class_', 'for': 'for_', 'from': 'from_', 'to': 'to_', 'list': 'list_'}

        for key in list(kwargs.keys()):           
            if key in reserved_map:
                new_key = reserved_map.get(key, key)
                kwargs[new_key] = kwargs.pop(key)
        #Parse only keywords that are defined in the dataclass definition
        for k in kwargs:
            if k not in cls.__match_args__:
                logger.error("%s got an unexpected keyword argument %s", cls.__name__, k)
        return cls(**{k: kwargs[k] for k in kwargs if k in cls.__match_args__})



    def process_enum(self, entry_type : type[Enum] , entry_value: str) -> Enum | str:
        """Process an Enum entry type"""
        try:
            return entry_type[entry_value]
        except KeyError:
            return entry_type(entry_value)
        except TypeError:
            return entry_value

    def is_optional(self, field):
        return type(None) in get_args(field)

    def __post_init__(self) -> None:

        for entry in fields(self):
            if (entry_value := getattr(self, entry.name)) is None:
                continue
            entry_type = entry.type
            if self.is_optional(entry_type):
                entry_type = next(
                    field_type for field_type in get_args(entry_type)
                    if field_type is not type(None)
                )
            # Order of checks is based on frequency of data within API responses
            # If the entry type is datetime then convert it from a string to a datetime object
            if entry_type is datetime:
                setattr(self, entry.name, ciso8601.parse_datetime(entry_value))
            elif entry_type in {float, str, int, bool}:
                continue
            elif entry_type is range or isinstance(entry_value, range):
                continue
            # If the entry type is date then convert it from a string to a date object
            elif entry_type is date:
                setattr(self, entry.name, ciso8601.parse_datetime(entry_value).date())
            # If the entry type is time then convert it from a string to a time object
            elif entry_type is time:
                setattr(self, entry.name, ciso8601.parse_datetime(entry_value).time())
            # If the entry type is a list
            elif get_origin(entry_type) is list:
                list_type : type = get_args(entry_type)[0]
                # If the type of the list entry is a dataclass then parse each entry of the list into the dataclass
                if (is_dataclass(list_type)) and (bool(entry_value)):
                    for index, data in enumerate(entry_value):
                        entry_value[index] = self.parse_kwargs(list_type, **(data))
                # If the type of the list entry is an Enum then convert it to an Enum entry
                elif issubclass(list_type, Enum):
                    setattr(
                        self,
                        entry.name,
                        [self.process_enum(list_type, data) for data in entry_value],
                    )
            # If the entry type is a dataclass and the entry is not null then parse the entry into the dataclass
            elif (is_dataclass(entry_type)) and (bool(entry_value)):
                setattr(
                    self, entry.name, self.parse_kwargs(entry_type, **(entry_value))
                )
            # If the entry type is an Enum then convert it to an Enum entry
            elif issubclass(entry_type, Enum):
                setattr(self,entry.name, self.process_enum(entry_type, entry_value))
            # If the entry type is a dict and the entry is not null
            elif (get_origin(entry_type) is dict) and (bool(entry_value)):
                # Create a new dict in case we have to change the index
                new_dict = {}
                for index, data in enumerate(entry_value):
                    # if the dict value is a dataclass
                    if is_dataclass(entry_type.__args__[1]):
                        entry_value[data] = self.parse_kwargs(
                            entry_type.__args__[1], **(entry_value[data])
                        )
                    # if the dict index is an enum
                    if issubclass(entry_type.__args__[0], Enum):
                        new_dict[getattr(entry_type.__args__[0], data)] = entry_value[
                            data
                        ]
                    else:
                        new_dict[data] = entry_value[data]
                setattr(self, entry.name, new_dict)


@dataclass(frozen=True)
class Endpoint:
    """Dataclass describing API endpoints and the data they return."""

    response: object
    returns: str | None = None
    sample: str | None = None
    name: str | None = None
    endpoint: str = ""
    type: str = "get"
    auth: str | None = None
    arguments: list = field(default_factory=list)
    parms: list = field(default_factory=list)


@dataclass
class APIArguments:
    """Dataclass describing the set of arguments used by the API endpoints."""


@dataclass
class APIParameters:
    """Dataclass describing the set of parameters used by the API endpoints."""

@dataclass
class APIResponses:
    """Dataclass describing the set of parameters used by the API endpoints."""


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
    responses: type[APIResponses]    
    apilist: type[Enum]    
    parameters: Any | None = None
    arguments: Any | None = None
    auth: str | None = None
    constants: type[Enum] | None = None
