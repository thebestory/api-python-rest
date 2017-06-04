"""
The Bestory Project
"""

import logging
import time
import typing

from tbs.config import snowflake as config


logger = logging.getLogger(__name__)

timestamp_bits = 41
machine_id_bits = 10
sequence_number_bits = 12

max_machine_id = -1 ^ (-1 << machine_id_bits)

timestamp_shift = machine_id_bits + sequence_number_bits
machine_id_shift = sequence_number_bits

machine_id_mask = -1 ^ (-1 << machine_id_bits) << machine_id_shift
sequence_number_mask = -1 ^ (-1 << sequence_number_bits)

__default_generator: typing.Iterator[int]


def generate() -> int:
    """Generate next Snowflake ID."""
    return next(__default_generator)


next_snowflake = generate


def timestamp_of_snowflake(snowflake: int) -> int:
    """Get timestamp in ms from config epoch from Snowflake ID."""
    return snowflake >> timestamp_shift


def real_timestamp_of_snowflake(snowflake: int) -> int:
    """Get timestamp in ms from computer epoch - 01.01.1970."""
    return timestamp_of_snowflake(snowflake) + config.EPOCH


def machine_id_of_snowflake(snowflake: int) -> int:
    """Get Machine ID from Snowflake ID."""
    return (snowflake & machine_id_mask) >> machine_id_shift


def sequence_number_of_snowflake(snowflake: int) -> int:
    """Get Sequence Number from Snowflake ID."""
    return snowflake & sequence_number_mask


def first_snowflake_for_timestamp(timestamp: int, machine_id: int=0) -> int:
    """First Snowflake ID for timestamp and Machine ID."""
    return (
        ((timestamp - config.EPOCH) << timestamp_shift) |
        (machine_id << machine_id_shift) |
        0
    )


def generator(machine_id: int=config.MACHINE_ID,
              sleep=lambda x: time.sleep(x / 1000.0),
              now=lambda: int(time.time() * 1000)):
    assert 0 <= machine_id <= max_machine_id

    last_timestamp = -1
    sequence_number = 0

    while True:
        timestamp = now()

        if last_timestamp > timestamp:
            logger.warning(
                "Clock is moving backwards. Waiting until %i" % last_timestamp)
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence_number = (sequence_number + 1) & sequence_number_mask
            if sequence_number == 0:
                logger.warning("Sequence overflow")
                sequence_number = -1 & sequence_number_mask
                sleep(1)
                continue
        else:
            sequence_number = 0

        last_timestamp = timestamp

        yield (
            ((timestamp - config.EPOCH) << timestamp_shift) |
            (machine_id << machine_id_shift) |
            sequence_number
        )


__default_generator = generator()
