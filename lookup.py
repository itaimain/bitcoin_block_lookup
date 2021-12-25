import requests

GENESIS_TS = 1231006505
BASE_API_URL = "https://blockchain.info"


class InvalidBlock(Exception):
    ...


class APIError(Exception):
    ...


def extract_time_from_block(block: dict) -> int:
    blocks = block.get('blocks')
    if 0 == len(blocks):
        raise InvalidBlock(f"Couldn't find blocks, {block=}")

    main_block_data = blocks[0]
    timestamp = main_block_data.get('time')

    if not timestamp:
        raise InvalidBlock(f"No timestamp is available, {block=}")

    return timestamp


def get_block(height: int) -> dict:
    try:
        return requests.get(
            f"{BASE_API_URL}/block-height/{height}?format=json").json()
    except requests.exceptions.RequestException as exp:
        raise APIError(
            f"Error while trying to fetch block at height {height}: {exp}")


def get_latest_block() -> dict:
    try:
        return requests.get(f"{BASE_API_URL}/latestblock?format=json").json()
    except requests.exceptions.RequestException as exp:
        raise APIError(f"Error while trying to the latest block: {exp}")


def get_block_timestamp(height: int) -> int:
    return extract_time_from_block(get_block(height))
