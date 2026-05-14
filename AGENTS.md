# AGENTS.md

Guidelines for AI coding agents working in this repository.

## Project overview

**bmi-topography** is a Python library that fetches and caches land elevation
data from the [OpenTopography](https://opentopography.org/) REST API. It
exposes a [Basic Model Interface (BMI)](https://bmi.csdms.io) so the data
source can be composed with other BMI-compliant models and components.

Key source files:

| File | Role |
|------|------|
| `bmi_topography/topography.py` | Core `Topography` class — API requests, caching, data loading |
| `bmi_topography/bmi.py` | `BmiTopography` — BMI wrapper |
| `bmi_topography/cli.py` | Click-based CLI |
| `bmi_topography/api_key.py` | `ApiKey` — credential management (env var, file, user prompt) |
| `bmi_topography/bbox.py` | `BoundingBox` — coordinate validation |
| `bmi_topography/config.py` | YAML config loader |
| `bmi_topography/errors.py` | Custom exceptions |

## Environment setup

```bash
conda env create --file=environment.yml
conda activate bmi-topography
pip install -e .
```

Or with pip only:

```bash
pip install -e .
```

Python 3.10 or later is required.

## Running tests

Tests are managed with **nox**. The most common sessions:

```bash
nox -s test            # unit tests with coverage
nox -s test-bmi        # BMI interface tests
nox -s test-cli        # CLI tests
nox -s lint            # pre-commit linters
nox -s check-notebooks # run example Jupyter notebooks
nox -s build-docs      # build Sphinx docs
```

To run pytest directly (skips coverage and nox overhead):

```bash
pytest tests/
```

### API key

Most tests that call the live OpenTopography API are guarded behind the
`hasuserkey` marker and are skipped in CI unless `OPENTOPOGRAPHY_API_KEY` is
set. Set `NO_FETCH=1` to skip any actual network requests locally.

## Code style

The project enforces formatting and linting through **pre-commit** hooks. Run
them before committing:

```bash
pre-commit run --all-files
```

Tools in use:

- **Black** — code formatting (line length 88)
- **isort** — import sorting (multi-line mode 3, line length 88)
- **Flake8** — linting (ignores E203, E501, W503, W605; max complexity 18)
- **pyupgrade** — modernise syntax to Python 3.10+
- **blackdoc** — format doctest examples
- **nbQA + nbstripout** — notebook hygiene

Do not manually wrap lines at 79 characters; Black owns line length.

## Contribution conventions

- Target Python 3.10 and later; use modern syntax (`pyupgrade --py310-plus`).
- Exceptions belong in `errors.py`; do not raise bare `Exception`.
- Dataset names are validated against the `DEM` and `USGS_DEM` enums/lists in
  `topography.py` — update those lists when adding new dataset support.
- New CLI options go in `cli.py` using Click; mutually exclusive options use
  the existing `MutuallyExclusiveOption` helper class.
- Keep `CHANGES.md` updated with notable changes under the `[Unreleased]`
  section.

## CI

GitHub Actions runs on every push and pull request:

| Workflow | What it runs |
|----------|-------------|
| `test.yml` | `nox -s test` on Ubuntu/macOS/Windows × Python 3.11–3.14 |
| `lint.yml` | `nox -s lint` |
| `docs.yml` | `nox -s build-docs` |
| `test-notebooks.yml` | `nox -s check-notebooks` |

All workflows must pass before merging. Coverage is reported to Coveralls.

## What to avoid

- Do not commit notebooks with cell outputs; `nbstripout` strips them, but
  verify before committing.
- Do not hardcode API keys anywhere in source or tests.
- Do not add network calls to tests unless they are guarded by the
  `hasuserkey` marker or `NO_FETCH`.
