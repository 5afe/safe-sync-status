import dataclasses
from typing import Any, List

from django.http import HttpResponse
from django.template import loader

from . import safe_config_service, safe_transaction_service
from .safe_config_service import Chain


@dataclasses.dataclass
class BlockTemplateTableRow:
    master_copy_version: str
    service_block: int
    rpc_block: int
    block_difference: int


@dataclasses.dataclass
class BlockTemplateContainer:
    chain: Chain
    table_rows: List[BlockTemplateTableRow]


def index(request: Any) -> HttpResponse:
    template = loader.get_template("blocks/index.html")

    chains = safe_config_service.get_chains()
    containers: List[BlockTemplateContainer] = []
    for chain in chains:
        master_copies = safe_transaction_service.get_master_copies(chain)
        ethereum_rpc = safe_transaction_service.get_ethereum_rpc(chain)

        table_rows: List[BlockTemplateTableRow] = []
        for master_copy in master_copies:
            row = BlockTemplateTableRow(
                master_copy_version=master_copy.version,
                service_block=master_copy.last_indexed_block_number,
                rpc_block=ethereum_rpc.block_number,
                block_difference=ethereum_rpc.block_number
                - master_copy.last_indexed_block_number,
            )
            table_rows.append(row)

        container = BlockTemplateContainer(
            chain=chain,
            table_rows=table_rows,
        )
        containers.append(container)

    context = {
        "containers": containers,
    }

    return HttpResponse(template.render(context, request))
