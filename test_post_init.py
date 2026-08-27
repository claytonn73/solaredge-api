import json
import logging
import unittest
from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path

from solaredge.apiconstruct import baseclass


class FixtureState(str, Enum):
    ACTIVE = "active"
    IDLE = "idle"


class FixtureKey(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


@dataclass
class NestedFixture(baseclass):
    occurred_on: date
    at_time: time
    state: FixtureState
    label: str
    level: int
    ok: bool
    amount: float


@dataclass
class ItemFixture(baseclass):
    timestamp: datetime
    count: int


@dataclass
class KeyedFixture(baseclass):
    created_at: datetime
    enabled: bool


@dataclass
class RangeFixture(baseclass):
    window: range


@dataclass
class PostInitFixture(baseclass):
    name: str
    ratio: float
    count: int
    enabled: bool
    optional_created_at: datetime | None
    optional_nested: NestedFixture | None
    optional_state: FixtureState | None
    nullable_text: str | None
    created_at: datetime
    nested: NestedFixture
    tags: list[str] = field(default_factory=list)
    states: list[FixtureState] = field(default_factory=list)
    empty_tags: list[str] = field(default_factory=list)
    items: list[ItemFixture] = field(default_factory=list)
    empty_items: list[ItemFixture] = field(default_factory=list)
    metadata: dict[str, int] = field(default_factory=dict)
    empty_metadata: dict[str, int] = field(default_factory=dict)
    keyed: dict[FixtureKey, KeyedFixture] = field(default_factory=dict)
    empty_keyed: dict[FixtureKey, KeyedFixture] = field(default_factory=dict)


class ParserHarness:
    logger = logging.getLogger(__name__)
    parse_kwargs = baseclass.parse_kwargs


class TestPostInitFixture(unittest.TestCase):
    def test_parse_kwargs_exercises_post_init_conversions(self) -> None:
        payload = json.loads(Path("tests/post_init_fixture.json").read_text(encoding="utf-8"))
        parser = ParserHarness()

        result = parser.parse_kwargs(PostInitFixture, **payload)
        self.assertEqual(result.name, "fixture-root")
        self.assertEqual(result.tags, ["alpha", "beta", "gamma"])
        self.assertTrue(all(isinstance(tag, str) for tag in result.tags))
        self.assertEqual(result.states, [FixtureState.ACTIVE, FixtureState.IDLE])
        self.assertTrue(all(isinstance(state, FixtureState) for state in result.states))
        self.assertEqual(result.empty_tags, [])
        self.assertIsInstance(result.ratio, float)
        self.assertEqual(result.ratio, 3.5)
        self.assertIsInstance(result.count, int)
        self.assertEqual(result.count, 7)
        self.assertIsInstance(result.enabled, bool)
        self.assertTrue(result.enabled)
        self.assertIsNone(result.nullable_text)

        self.assertIsInstance(result.optional_created_at, datetime)
        self.assertEqual(result.optional_created_at.isoformat(), "2024-11-05T18:00:00+00:00")
        self.assertIsInstance(result.optional_nested, NestedFixture)
        self.assertEqual(result.optional_nested.occurred_on.isoformat(), "2024-11-03")
        self.assertEqual(result.optional_nested.at_time.isoformat(), "07:45:30")
        self.assertEqual(result.optional_nested.state, FixtureState.IDLE)
        self.assertEqual(result.optional_nested.label, "optional-nested")
        self.assertEqual(result.optional_state, FixtureState.ACTIVE)

        self.assertIsInstance(result.created_at, datetime)
        self.assertEqual(result.created_at.isoformat(), "2024-11-05T14:23:45+00:00")

        self.assertIsInstance(result.nested, NestedFixture)
        self.assertIsInstance(result.nested.occurred_on, date)
        self.assertEqual(result.nested.occurred_on.isoformat(), "2024-11-04")
        self.assertIsInstance(result.nested.at_time, time)
        self.assertEqual(result.nested.at_time.isoformat(), "06:30:15")
        self.assertEqual(result.nested.state, FixtureState.ACTIVE)
        self.assertEqual(result.nested.label, "nested-label")
        self.assertEqual(result.nested.level, 4)
        self.assertFalse(result.nested.ok)
        self.assertEqual(result.nested.amount, 1.25)

        self.assertEqual(len(result.items), 2)
        self.assertTrue(all(isinstance(item, ItemFixture) for item in result.items))
        self.assertTrue(all(isinstance(item.timestamp, datetime) for item in result.items))
        self.assertEqual(result.items[0].timestamp.isoformat(), "2024-11-05T10:00:00+00:00")
        self.assertEqual(result.items[1].count, 5)
        self.assertEqual(result.empty_items, [])

        self.assertEqual(result.metadata, {"phase": 3, "retries": 1})
        self.assertTrue(all(isinstance(key, str) for key in result.metadata))
        self.assertTrue(all(isinstance(value, int) for value in result.metadata.values()))
        self.assertEqual(result.empty_metadata, {})

        self.assertEqual(set(result.keyed), {FixtureKey.PRIMARY, FixtureKey.SECONDARY})
        self.assertTrue(all(isinstance(value, KeyedFixture) for value in result.keyed.values()))
        self.assertEqual(
            result.keyed[FixtureKey.PRIMARY].created_at.isoformat(),
            "2024-11-05T09:45:00+00:00",
        )
        self.assertFalse(result.keyed[FixtureKey.SECONDARY].enabled)
        self.assertEqual(result.empty_keyed, {})

    def test_range_field_is_left_unchanged(self) -> None:
        result = RangeFixture(window=range(2, 6))

        self.assertIsInstance(result.window, range)
        self.assertEqual(list(result.window), [2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
