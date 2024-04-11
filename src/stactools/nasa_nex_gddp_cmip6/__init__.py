import stactools.core
from stactools.cli.registry import Registry
from stactools.nasa_nex_gddp_cmip6.stac import (
    create_collection,
    create_item_from_dataset,
)

__version__ = "0.1.0"

__all__ = ["create_collection", "create_item_from_dataset", "__version__"]

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    from stactools.nasa_nex_gddp_cmip6 import commands

    registry.register_subcommand(commands.create_nasanexgddpcmip6_command)
