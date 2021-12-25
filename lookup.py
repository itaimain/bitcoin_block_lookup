#!/usr/bin/python
import argparse
import logging
from enum import Enum
from typing import Sequence

from blocks import BlocksVirtualArray
from interpolation import Result
from interpolation import interpolation_nearby_lookup as lookup


class ArgTypeMixin(Enum):
    @classmethod
    def argtype(cls, s: str) -> Enum:
        try:
            return cls[s]
        except KeyError:
            raise argparse.ArgumentTypeError(
                f"{s!r} is not a valid {cls.__name__}")

    def __str__(self):
        return self.name


class LoglevelChoices(ArgTypeMixin, Enum):
    critical = logging.CRITICAL
    error = logging.ERROR
    warning = logging.WARNING
    info = logging.INFO
    debug = logging.DEBUG


def parse_args() -> Sequence:
    parser = argparse.ArgumentParser()
    parser.add_argument('timestamp', type=int, metavar='Timestamp')
    parser.add_argument('-log',
                        '--loglevel',
                        default='warning',
                        type=LoglevelChoices.argtype,
                        choices=LoglevelChoices,
                        help='Provide logging level. Default is warning')
    args = parser.parse_args()
    return args


def lookup_blocks_height_by_timestamp(timestamp: int) -> type[Result]:
    blocks_array = BlocksVirtualArray()
    result = lookup(blocks_array, timestamp)

    count = blocks_array.count
    logging.info(f"API calls {count=}")

    return result


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=args.loglevel.value)
    result = lookup_blocks_height_by_timestamp(args.timestamp)

    print(f'Result is {result.previous_index}')


if '__main__' == __name__:
    main()
