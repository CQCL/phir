.PHONY: install dev tests lint docs clean build updateschema

install:
	uv pip install .

dev:
	uv pip install -e .

tests:
	uv run pytest .

lint:
	uv run pre-commit run --all-files

docs:
	uv run sphinx-apidoc -f -o docs/source/ phir
	uv run sphinx-build -M html docs/source/ docs/build/

clean:
	rm -rf *.egg-info dist build docs/build

build: clean
	uv build

updateschema: install
	uv run phir-cli -s > schema.json
