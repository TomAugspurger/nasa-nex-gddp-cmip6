# stactools-nasa-nex-gddp-cmip6

[![PyPI](https://img.shields.io/pypi/v/stactools-nasa-nex-gddp-cmip6?style=for-the-badge)](https://pypi.org/project/stactools-nasa-nex-gddp-cmip6/)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/stactools-packages/nasa-nex-gddp-cmip6/continuous-integration.yml?style=for-the-badge)

- Name: nasa-nex-gddp-cmip6
- Package: `stactools.nasa_nex_gddp_cmip6`
- [stactools-nasa-nex-gddp-cmip6 on PyPI](https://pypi.org/project/stactools-nasa-nex-gddp-cmip6/)
- Owner: @githubusername
- [Dataset homepage](http://example.com)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `nasa-nex-gddp-cmip6:custom`: A custom attribute
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/nasa-nex-gddp-cmip6/main/examples/collection.json)
- [Browse a notebook demonstrating the example item and collection](https://github.com/stactools-packages/nasa-nex-gddp-cmip6/tree/main/docs/example.ipynb)

A short description of the package and its usage.

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-nasa-nex-gddp-cmip6
```

## Command-line usage

Description of the command line functions

```shell
stac nasa-nex-gddp-cmip6 create-item source destination
```

Use `stac nasa-nex-gddp-cmip6 --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e '.[dev]'
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```

If you've updated the STAC metadata output, update the examples:

```shell
scripts/update-examples
```
