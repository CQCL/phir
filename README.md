# PHIR: _[PECOS](https://github.com/PECOS-packages/PECOS) High-level Intermediate Representation_

See [PHIR specification](./phir_spec_qasm.md) for more.

## Installation

Clone the repository and run:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
pre-commit install
```

Then install the project using:

```sh
pip install -e .
```

See `Makefile` for other useful commands.

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

## Testing

Just issue `pytest` from the root directory.
