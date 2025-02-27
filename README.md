# PHIR: _[PECOS](https://github.com/PECOS-packages/PECOS) High-level Intermediate Representation_

[![PyPI version](https://badge.fury.io/py/phir.svg)](https://badge.fury.io/py/phir)
[![Python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://img.shields.io/badge/python-3.10%2C%203.11%2C%203.12-blue.svg)

`phir` models the [PHIR specification](./spec.md) as a [Pydantic](https://docs.pydantic.dev/latest/) model.
See [our docs](https://cqcl.github.io/phir/).
Included is the tool `phir-cli` that provides validation and pretty printing on the command line.

## Prerequisites

Python >=3.10

## Installation

Just issue `pip install phir` to obtain the latest stable release.

## phir CLI

The package includes a CLI for directly validating PHIR JSON files using the command line.

```sh
❯ phir-cli -h
usage: phir-cli [-h] [-s] [-v] [jsonfile]

Validates and pretty prints valid PHIR

positional arguments:
  jsonfile       json file to validate against PHIR spec

options:
  -h, --help     show this help message and exit
  -s, --schema   dump JSON schema of the PHIR model and exit
  -v, --version  show program's version number and exit
```

## Development

Clone the repository and run:

```sh
uv sync
uv run pre-commit install
```

See `Makefile` for other useful commands.

## Testing

Issue `make tests` from the root directory.
