from typing import Any, Optional, Sequence

import requests

from exceptions import APIError, InvalidBlock
import logging

BASE_API_URL = "https://blockchain.info"

GENESIS_TS = 1231006505


class Block:
    height: int
    timestamp: int

    def __init__(self,
                 raw: Optional[dict] = None,
                 height: Optional[int] = None,
                 timestamp: Optional[int] = None,
                 latest=False):
        if raw:
            self.height = self.extract_blocks_index(raw, latest)
            self.timestamp = self.extract_time_from_block(raw, latest)
        elif height is None or timestamp is None:
            raise AttributeError(
                "Creating a block requires a raw block dictionary or a height and a timestamp"
            )
        else:
            self.height = height
            self.timestamp = timestamp

    @staticmethod
    def __extract_prop_from_block(block: dict, prop: str, last=False) -> Any:
        if last:
            main_block_data = block
        else:
            blocks = block.get('blocks', [])
            if 0 == len(blocks):
                raise InvalidBlock(f"Couldn't find blocks, {block=}")

            main_block_data = blocks[0]
        value = main_block_data.get(prop)

        if not value:
            raise InvalidBlock(f"No {value} is available, {block=}")

        return value

    @staticmethod
    def extract_time_from_block(block: dict, last=False) -> int:
        return Block.__extract_prop_from_block(block, 'time', last)

    @staticmethod
    def extract_blocks_index(block: dict, last=False) -> int:
        return Block.__extract_prop_from_block(block, 'height', last)


class BlocksVirtualArray(Sequence):
    genesis_block: Block
    latest_block: Block
    __counter: int

    def __init__(self) -> None:
        self.__counter = 0
        self.genesis_block = Block(height=0, timestamp=GENESIS_TS)
        self.latest_block = self.__get_latest_block()

    def __getitem__(self, index: int) -> int:
        if index < 0:
            index = self.__len__() + index

        if self.latest_block.height == index:
            return self.latest_block.timestamp

        if 0 == index:
            return self.genesis_block.timestamp

        return self.__get_block(index).timestamp

    def __len__(self):
        return self.latest_block.height + 1

    def __get_block(self, height: int) -> Block:
        logging.info(f'get block {height}')

        try:
            block = Block(
                requests.get(
                    f"{BASE_API_URL}/block-height/{height}?format=json").json(
                    ))
            self.__counter += 1
            return block
        except requests.exceptions.RequestException as exp:
            raise APIError(
                f"Error while trying to fetch block at height {height}: {exp}")

    def __get_latest_block(self) -> Block:
        logging.info('get latest block')

        try:
            block = Block(
                requests.get(f"{BASE_API_URL}/latestblock?format=json").json(),
                latest=True)
            self.__counter += 1
            return block
        except requests.exceptions.RequestException as exp:
            raise APIError(f"Error while trying to the latest block: {exp}")

    @property
    def count(self):
        return self.__counter