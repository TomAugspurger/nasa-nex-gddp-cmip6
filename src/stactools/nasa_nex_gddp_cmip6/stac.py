import dataclasses
import importlib
import importlib.resources
import json
import logging
import pathlib
import re
from typing import Any, Literal

import pystac
import xarray as xr
import xstac

logger = logging.getLogger(__name__)

HERE = pathlib.Path(".")
VERSION = Literal["1.0", "1.1", "1.2"]
SCENARIO = Literal["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
VARIABLE = Literal[
    "hurs", "huss", "pr", "rlds", "rsds", "sfcWind", "tas", "tasmax", "tasmin"
]
MODEL = Literal[
    "ACCESS-CM2",
    "ACCESS-ESM1-5",
    "BCC-CSM2-MR",
    "CESM2",
    "CESM2-WACCM",
    "CMCC-CM2-SR5",
    "CMCC-ESM2",
    "CNRM-CM6-1",
    "CNRM-ESM2-1",
    "CanESM5",
    "EC-Earth3",
    "EC-Earth3-Veg-LR",
    "FGOALS-g3",
    "GFDL-CM4",
    "GFDL-CM4_gr2",
    "GFDL-ESM4",
    "GISS-E2-1-G",
    "HadGEM3-GC31-LL",
    "HadGEM3-GC31-MM",
    "IITM-ESM",
    "INM-CM4-8",
    "INM-CM5-0",
    "IPSL-CM6A-LR",
    "KACE-1-0-G",
    "KIOST-ESM",
    "MIROC-ES2L",
    "MIROC6",
    "MPI-ESM1-2-HR",
    "MPI-ESM1-2-LR",
    "MRI-ESM2-0",
    "NESM3",
    "NorESM2-LM",
    "NorESM2-MM",
    "TaiESM1",
    "UKESM1-0-LL",
]


@dataclasses.dataclass
class Parts:
    """
    Construct metadata from
    """

    PATH_XPR = re.compile(
        r"(?P<variable>\w+)_day_"
        r"(?P<model>[^_]+)_"
        r"(?P<scenario>(historical|ssp245|ssp585|ssp126|ssp370))"
        r"_[^_]+_g(n|r)\d*_"
        r"(?P<year>\d{4})_"
        r"?v?(?P<version>(\d.\d|)?)\.nc$"
    )

    model: str
    scenario: str
    year: int
    version: VERSION

    @classmethod
    def from_path(cls, path: str) -> "Parts":
        # this should probably be a regex

        m = cls.PATH_XPR.search(path)
        if not m:
            raise ValueError(f"Unexpected path format: {path}")

        g: dict[str, int | str] = m.groupdict()
        if g["version"] == "":
            # default to 1.0
            g["version"] = "1.0"
        g.pop("variable")
        g["year"] = int(g["year"])
        assert g["version"] in {"1.0", "1.1", "1.2"}

        return cls(**g)  # type: ignore[arg-type]

    @property
    def item_id(self) -> str:
        parts = [self.model, self.scenario, str(self.year)]
        return ".".join(parts)


def asset_key(path):
    *_, variable, _ = path.split("/")
    return variable


def create_item_from_dataset(
    ds: xr.Dataset, xarray_to_stac_options: dict[str, Any] | None = None
) -> pystac.Item:
    paths = [data_var.encoding["source"] for data_var in ds.data_vars.values()]
    if not paths:
        raise ValueError(
            "No paths found in dataset. Set the source href in the `encoding` for "
            "each variable."
        )

    all_parts = [Parts.from_path(path) for path in paths]
    item_ids = set([p.item_id for p in all_parts])
    if len(item_ids) != 1:
        raise ValueError(
            f"Multiple item IDs derived from paths. {item_ids}. Verify that the "
            "paths are consistent."
        )

    parts = all_parts[0]

    template = pystac.Item(
        "item",
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [180.0, -90.0],
                    [180.0, 90.0],
                    [-180.0, 90.0],
                    [-180.0, -90.0],
                    [180.0, -90.0],
                ]
            ],
        },
        bbox=[-180, -90, 180, 90],
        datetime=None,
        properties={"start_datetime": None, "end_datetime": None},
    )

    xarray_to_stac_options = xarray_to_stac_options or {}
    xarray_to_stac_options.setdefault("reference_system", 4326)
    xarray_to_stac_options.setdefault("template", template)
    item = xstac.xarray_to_stac(ds, **xarray_to_stac_options)
    item.id = parts.item_id

    for path, part in zip(paths, all_parts):
        key = asset_key(path)
        asset = pystac.Asset(
            path,
            media_type="application/netcdf",
            roles=["data"],
        )
        asset.extra_fields["cmip6:variable"] = key
        asset.extra_fields["nasa-nex-gddp-cmip6:version"] = part.version

        item.add_asset(key, asset)

    for k, v in dataclasses.asdict(parts).items():
        if k == "version":
            # This is asset-specific
            continue
        item.properties[f"cmip6:{k}"] = v

    return item


def create_collection():
    data = json.loads(
        importlib.resources.files("stactools.nasa_nex_gddp_cmip6")
        .joinpath("collection.json")
        .read_text()
    )
    return pystac.Collection.from_dict(data)
