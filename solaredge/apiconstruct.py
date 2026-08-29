"""This code contains dataclasses which enable the construction of REST API clients

RESTClient: The RESTClient data class represents the configuration for making API requests.
It includes information such as the API URL, authentication method, supported API endpoints, arguments, parameters,
and constants."""

import logging
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date, datetime, time
from enum import Enum
from types import NoneType
from typing import get_args, get_origin

import ciso8601

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class baseclass:
    """This dataclass provides the post_init code to handle the nested dataclasses
    and formatting of datetime entries"""

    def parse_kwargs(self, cls, **kwargs: dict):
        # If the key is in our reserved map, rename it; otherwise keep it as-is
        reserved_map = {"class": "class_", "for": "for_", "from": "from_", "to": "to_", "list": "list_"}

        for key in list(kwargs.keys()):
            if key in reserved_map:
                new_key = reserved_map.get(key, key)
                kwargs[new_key] = kwargs.pop(key)
        # Parse only keywords that are defined in the dataclass definition
        for k in kwargs:
            if k not in cls.__match_args__:
                logger.error("%s got an unexpected keyword argument %s", cls.__name__, k)
        return cls(**{key: value for key, value in kwargs.items() if key in cls.__match_args__})

    def process_enum(self, entry_type: type[Enum], entry_value: str) -> Enum | str:
        """Process an Enum entry type"""
        try:
            return entry_type[entry_value]
        except KeyError:
            return entry_type(entry_value)
        except TypeError:
            return entry_value

    def is_optional(self, entry):
        return type(None) in get_args(entry)

    def _coerce_value(self, field_type, value):
        if field_type is datetime:
            return ciso8601.parse_datetime(value)
        if field_type is date:
            return ciso8601.parse_datetime(value).date()
        if field_type is time:
            return ciso8601.parse_datetime(value).time()
        if is_dataclass(field_type):
            return self.parse_kwargs(field_type, **value)
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            return self.process_enum(field_type, value)
        if get_origin(field_type) is list:
            item_type = get_args(field_type)[0]
            return [self._coerce_value(item_type, item) if item is not None else None for item in value]
        if get_origin(field_type) is dict:
            key_type, value_type = get_args(field_type)
            return {self._convert_key(key_type, k): self._coerce_value(value_type, v) for k, v in value.items()}
        return value

    def _convert_key(self, key_type, key):
        if isinstance(key_type, type) and issubclass(key_type, Enum):
            return getattr(key_type, key)
        return key

    def __post_init__(self):
        for entry in fields(self):
            field_type = entry.type
            value = getattr(self, entry.name)

            if self.is_optional(field_type):
                field_type = next(t for t in get_args(field_type) if t is not NoneType)

            if field_type in (float, str, int, bool) or value in (None, "", [], {}):
                continue

            setattr(self, entry.name, self._coerce_value(field_type, value))


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
    parameters: Enum | None = None
    arguments: Enum | None = None
    auth: str | None = None
    constants: type[Enum] | None = None
