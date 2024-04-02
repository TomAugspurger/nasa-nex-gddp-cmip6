import json
import pathlib

import numpy as np
import pandas as pd
import pytest
import xarray as xr
from stactools.nasa_nex_gddp_cmip6 import stac

HERE = pathlib.Path(__file__).parent
DATA_DIR = HERE.joinpath("data")


def create_dataset():
    time = xr.DataArray(
        pd.date_range("1950-01-01T12:00:00", periods=365),
        dims=["time"],
        name="time",
        attrs={"axis": "T", "long_name": "time", "standard_name": "time"},
    )
    lat = xr.DataArray(
        np.linspace(-59.875, 89.875, 600),
        dims=["lat"],
        name="lat",
        attrs={
            "units": "degrees_north",
            "axis": "Y",
            "long_name": "latitude",
            "standard_name": "latitude",
        },
    )
    lon = xr.DataArray(
        np.linspace(0.125, 359.875, 1440),
        dims=["lon"],
        name="lon",
        attrs={
            "units": "degrees_east",
            "axis": "X",
            "long_name": "longitude",
            "standard_name": "longitude",
        },
    )

    data = np.empty((time.size, lat.size, lon.size))
    arrays = {}
    attrs = json.loads(DATA_DIR.joinpath("attrs.json").read_text())
    data_vars = [
        "hurs",
        "huss",
        "pr",
        "rlds",
        "rsds",
        "sfcWind",
        "tas",
        "tasmax",
        "tasmin",
    ]
    urls = [
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/huss/huss_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/pr/pr_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/rlds/rlds_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/rsds/rsds_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/sfcWind/sfcWind_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/tas/tas_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/tasmax/tasmax_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
        "https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/tasmin/tasmin_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
    ]

    for data_var, source in zip(data_vars, urls):
        arrays[data_var] = xr.DataArray(
            data,
            coords=[time, lat, lon],
            dims=["time", "lat", "lon"],
            name=data_var,
            attrs=attrs["data_vars"][data_var],
        )
        arrays[data_var].encoding["source"] = source

    result = xr.Dataset(
        arrays, coords={"time": time, "lat": lat, "lon": lon}, attrs=attrs["global"]
    )

    return result


def test_create_item() -> None:
    expected = json.loads((DATA_DIR / "item.json").read_text())
    ds = create_dataset()
    item = stac.create_item_from_dataset(ds)

    assert item.id == "ACCESS-CM2.historical.1950"
    item.validate()
    assert item.to_dict() == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc",
            stac.Parts(
                model="ACCESS-CM2", scenario="historical", year=1950, version="1.0"
            ),
        ),
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950_v1.1.nc",
            stac.Parts(
                model="ACCESS-CM2", scenario="historical", year=1950, version="1.1"
            ),
        ),
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/ssp245/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_ssp245_r1i1p1f1_gn_1950.nc",
            stac.Parts(model="ACCESS-CM2", scenario="ssp245", year=1950, version="1.0"),
        ),
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/ssp126/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_ssp126_r1i1p1f1_gn_1950.nc",
            stac.Parts(model="ACCESS-CM2", scenario="ssp126", year=1950, version="1.0"),
        ),
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/ssp370/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_ssp370_r1i1p1f1_gn_1950.nc",
            stac.Parts(model="ACCESS-CM2", scenario="ssp370", year=1950, version="1.0"),
        ),
        (
            "NEX/GDDP-CMIP6/ACCESS-CM2/ssp585/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_ssp585_r1i1p1f1_gn_2100.nc",
            stac.Parts(model="ACCESS-CM2", scenario="ssp585", year=2100, version="1.0"),
        ),
    ],
)
def test_parts(path: str, expected: stac.Parts) -> None:
    result = stac.Parts.from_path(path)
    assert result == expected


def test_create_collection():
    collection = stac.create_collection()
    collection.validate()
