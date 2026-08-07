# Development

Set up a development environment, run tests, and build the package.

## In this guide

- [Prerequisites](#prerequisites)
- [Clone and install](#clone-and-install)
- [Run the tests](#run-the-tests)
- [Build the package](#build-the-package)
- [Continuous integration](#continuous-integration)

## Prerequisites

- Git
- Python 3.8+
- pip

## Clone and install

```bash
git clone https://github.com/rkriad585/ActiveVPN.git
cd ActiveVPN

python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell
. .venv\Scripts\Activate.ps1

pip install -r requirements.txt pytest build twine
```

## Run the tests

```bash
pytest -q
```

The suite in `tests/` covers:

- `tests/test_detector.py` — process matching, API failover, and verdict scoring (psutil/requests mocked).
- `tests/test_logger.py` — history persistence, clearing, and JSON/CSV/TXT export.

## Build the package

```bash
python -m build
```

Creates `dist/activevpn-<version>.tar.gz` and `dist/activevpn-<version>-py3-none-any.whl`.

```bash
python -m twine check dist/*
```

Validates metadata. To publish, configure `~/.pypirc` with a PyPI token and run:

```bash
python -m twine upload dist/*
```

## Continuous integration

- `.github/workflows/ci.yml` runs `pytest -q` on Ubuntu, Windows, and macOS with Python 3.8 and 3.12 on every push to `main` and every pull request, and builds the docs with `mkdocs build --strict` as a check.
- `.github/workflows/docs.yml` builds the MkDocs site and deploys it to GitHub Pages (`https://rkriad585.github.io/ActiveVPN/`) whenever `docs/`, `mkdocs.yml`, or `pyproject.toml` change on `main`, or on manual `workflow_dispatch`.

## Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/) (4-space indentation).
- Keep the project's tone: descriptive names, minimal comments.
- Update the docs when you change behavior. See [CONTRIBUTING.md](https://github.com/rkriad585/ActiveVPN/blob/main/CONTRIBUTING.md).

---

<a href="../">← Back to Home</a>
