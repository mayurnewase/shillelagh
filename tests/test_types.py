from shillelagh.db import connect
from shillelagh.types import Binary
from shillelagh.types import Date
from shillelagh.types import DateFromTicks
from shillelagh.types import Time
from shillelagh.types import TimeFromTicks
from shillelagh.types import Timestamp
from shillelagh.types import TimestampFromTicks


def test_types():
    connection = connect(":memory:")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE test_types (
            type_date DATE,
            type_time TIME,
            type_timestamp TIMESTAMP,
            type_binary BLOB
        )
    """
    )
    cursor.execute(
        "INSERT INTO test_types VALUES (?, ?, ?, ?)",
        (
            Date(2020, 1, 1),
            Time(0, 0, 0),
            Timestamp(2020, 1, 1, 0, 0, 0),
            Binary("🦥"),
        ),
    )
    cursor.execute("SELECT * FROM test_types")
    row = cursor.fetchone()
    assert row == (
        "2020-01-01",
        "00:00:00+00:00",
        "2020-01-01T00:00:00+00:00",
        b"\xf0\x9f\xa6\xa5",
    )

    cursor.execute(
        "INSERT INTO test_types VALUES (?, ?, ?, ?)",
        (
            DateFromTicks(1),
            TimeFromTicks(2),
            TimestampFromTicks(3),
            Binary("🦥"),
        ),
    )
    cursor.execute("SELECT * FROM test_types")
    rows = cursor.fetchall()
    assert rows == [
        (
            "2020-01-01",
            "00:00:00+00:00",
            "2020-01-01T00:00:00+00:00",
            b"\xf0\x9f\xa6\xa5",
        ),
        (
            "1970-01-01",
            "00:00:02+00:00",
            "1970-01-01T00:00:03+00:00",
            b"\xf0\x9f\xa6\xa5",
        ),
    ]
