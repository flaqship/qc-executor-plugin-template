# Contributing to qc-executor-mybackend

Thank you for your interest in contributing! This document covers everything you
need to get started.

## Development Setup

Prerequisites: [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

```bash
git clone https://github.com/your-org/qc-executor-mybackend.git
cd qc-executor-mybackend
uv sync --group dev
```

Run the test suite:

```bash
uv run pytest tests/
```

## Branching Strategy

- `main` – stable, released code
- Feature branches: `feat/<short-description>`
- Bug fixes: `fix/<short-description>`
- Infrastructure / CI: `chore/<short-description>`

Open a PR against `main`. For significant features, open an issue first to
discuss the design.

## Code Style

This project uses [Black](https://black.readthedocs.io/) with a line length of 99
and [isort](https://pycqa.github.io/isort/).

```bash
uv run black -l 99 src tests
uvx isort src tests
```

Linting via [Pylint](https://pylint.readthedocs.io/):

```bash
uv run pylint src/qc_executor_mybackend
```

Both are checked automatically in CI on every PR.

### Docstrings

Use Google-style Python docstrings across the project.

- Use section headers like `Args:`, `Returns:`, and `Raises:`.
- Do not use NumPy-style headers like `Parameters`/`Returns` with dashed
  underlines.
- Keep argument and return types aligned with function signatures.

## Implementing the Executor Contract

The contract is defined by
[QC Executor](https://github.com/flaqship/qc-executor) v0.2.1; see
[Implementing the contract](README.md#implementing-the-contract) for the
methods to fill in on the executor and the native circuit/operator classes.

Register the executor with the factory through the `qc_executor.backends` entry
point in `pyproject.toml` — the template already declares it:

```toml
[project.entry-points."qc_executor.backends"]
mybackend = "qc_executor_mybackend:MyBackendExecutor"
```

## Changelog

Every PR that changes user-facing behaviour should add an entry to
[CHANGELOG.md](CHANGELOG.md) under the `[Unreleased]` section.

## Releasing (Maintainers)

1. Update the version in `src/qc_executor_mybackend/__init__.py`
2. Move the `[Unreleased]` section in `CHANGELOG.md` to a new versioned section
3. Commit: `git commit -m "chore: release vX.Y.Z"`
4. Tag: `git tag vX.Y.Z && git push --tags`
5. Create a GitHub Release – the `publish.yml` workflow will build and upload
   to PyPI automatically (after you've configured trusted publishing — see the
   TODO in `.github/workflows/publish.yml`).
