import dataclasses
from typing import List
from urllib.parse import urljoin

import requests
from requests import Response

from .safe_config_service import Chain


@dataclasses.dataclass
class MasterCopy:
    version: str
    last_indexed_block_number: int


@dataclasses.dataclass
class EthereumRpc:
    block_number: int


def get_ethereum_rpc(chain: Chain) -> EthereumRpc:
    base_url = chain.transaction_service
    if chain.l2:
        path = "/api/v1/about/ethereum-rpc/"
    else:
        path = "/api/v1/about/ethereum-tracing-rpc/"
    url = urljoin(base=base_url, url=path)

    response = requests.get(url)
    ethereum_rpc = _decode_ethereum_rpc(response)

    return ethereum_rpc


def _decode_ethereum_rpc(response: Response) -> EthereumRpc:
    json = response.json()
    return EthereumRpc(block_number=json["block_number"])


def get_master_copies(chain: Chain) -> List[MasterCopy]:
    base_url = chain.transaction_service
    path = "/api/v1/about/master-copies/"
    url = urljoin(base=base_url, url=path)

    response = requests.get(url)
    master_copies = _decode_response_master_copies(response)

    return master_copies


def _decode_response_master_copies(response: Response) -> List[MasterCopy]:
    master_copies: List[MasterCopy] = []
    for raw_master_copy in response.json():
        master_copy = MasterCopy(
            version=raw_master_copy["version"],
            last_indexed_block_number=raw_master_copy["lastIndexedBlockNumber"],
        )
        master_copies.append(master_copy)
    return master_copies
