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

## Run the demos

Install the requirements above, then start any demo with the local Dash server and open
[http://localhost:8050](http://localhost:8050):

```bash
python tree_select_demo.py
python data_list_demo.py
python floating_window_demo.py
```

`DataList` and `FloatingWindow` live on the `dev` branch of the DMC fork. For an editable
checkout in `../dash-mantine-components`, run `npm run build` there after switching
branches so the generated Python components and JavaScript bundle match the branch.
[`demo_page.py`](demo_page.py) provides the layout shared by the `DataList` and
`FloatingWindow` demos.

Floating windows are created only when their example is opened. The app supplies
`validation_layout` with all dynamic windows and corner buttons so Dash can validate
their callback IDs without rendering them on initial load. Its callbacks are registered
on the demo app rather than globally.

## Run the TreeSelect documentation

The TreeSelect component currently lives on the `feat/tree-select-v3` branch of the DMC
fork, which is the branch installed by `requirements.txt`.

The page uses real DMC components inside `MantineProvider`. Each section includes a
live example and expandable source generated from the example function. Examples
cover selection modes, cascading and strict checks, checked strategies, search,
selection limits, controlled expansion and dropdown state, custom rendering, and
standard input props. JSON readouts show the values reported to Dash callbacks.

Custom node, pill, filter, and overflow functions live in
[`assets/tree-select.js`](assets/tree-select.js). Shared data and callbacks are in
[`tree_select_demo.py`](tree_select_demo.py). The feature-branch package must include the generated Python
components and compiled JavaScript bundle.

The app explicitly selects React 19.2.4, bundled with Dash 4.5, as required by DMC 3.
Regression tests cover layout serialization, unique IDs and data values, callback
requests, local assets, and the React version.

For an editable DMC checkout, Mypy may not resolve the editable import hook. Set
`MYPYPATH` to the DMC source root and use `mypy --follow-imports=silent tree_select_demo.py` to
check the app against the generated component types without reporting errors in
the generated dependency itself.
