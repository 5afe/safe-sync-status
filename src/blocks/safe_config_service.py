import dataclasses
from typing import List
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests import Response


@dataclasses.dataclass
class Chain:
    id: int
    name: str
    transaction_service: str
    l2: bool


def get_chains() -> List[Chain]:
    base_url = settings.SAFE_CONFIG_BASE_URL
    path = "/api/v1/chains/"
    url = urljoin(base=base_url, url=path)

    response = requests.get(url)
    chains = _decode_response(response)

    return chains


def _decode_response(response: Response) -> List[Chain]:
    chains: List[Chain] = []
    for raw_chain in response.json()["results"]:
        chain = Chain(
            id=raw_chain["chainId"],
            name=raw_chain["chainName"],
            transaction_service=raw_chain["transactionService"],
            l2=raw_chain["l2"],
        )
        chains.append(chain)
    return chains
