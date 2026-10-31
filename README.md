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

The page uses real DMC components inside `MantineProvider`. Each section includes a
live example and expandable source generated from the example function. Examples
cover selection modes, cascading and strict checks, checked strategies, search,
selection limits, controlled expansion and dropdown state, custom rendering, and
standard input props. JSON readouts show the values reported to Dash callbacks.

Custom node, pill, filter, and overflow functions live in
[`assets/tree-select.js`](assets/tree-select.js). Shared data and callbacks are in
[`app.py`](app.py). The feature-branch package must include the generated Python
components and compiled JavaScript bundle.

The app explicitly selects React 19.2.4, bundled with Dash 4.5, as required by DMC 3.
Regression tests cover layout serialization, unique IDs and data values, callback
requests, local assets, and the React version.

For an editable DMC checkout, Mypy may not resolve the editable import hook. Set
`MYPYPATH` to the DMC source root and use `mypy --follow-imports=silent app.py` to
check the app against the generated component types without reporting errors in
the generated dependency itself.
