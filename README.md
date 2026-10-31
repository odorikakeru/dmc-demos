# dmc-demos

This repository contains demos and documentation for new features being developed in
[odorikakeru/dash-mantine-components](https://github.com/odorikakeru/dash-mantine-components),
a fork of Dash Mantine Components.

Examples here may also be used to demonstrate and reproduce bugs or other problems
encountered while developing that project.

## Component documentation

- [TreeSelect](docs/tree-select.md)

## Set up

Create and activate a virtual environment, then install the development requirements.
This installs the runtime requirements, including Dash and this repository's fork, as
well as Ruff, Mypy, and pytest:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Code quality

All Python code must pass Ruff checks and formatting:

```bash
ruff check .
ruff format --check .
```

Mypy checks annotated code and also checks function bodies without annotations:

```bash
mypy path/to/python/files
```

Run the test suite with:

```bash
pytest
```

## Run the TreeSelect documentation

Install the requirements above, then start the local Dash server:

```bash
python app.py
```

Open [http://localhost:8050](http://localhost:8050) to view the TreeSelect guide. The
component currently lives on the `feat/tree-select-v3` branch of the DMC fork, which is
the branch installed by `requirements.txt`.

The current feature branch has a packaging issue: importing
`dash_mantine_components` fails because its generated `_imports_` module is missing.
The page shows this limitation and omits the live component preview until the fork
provides a working package.
