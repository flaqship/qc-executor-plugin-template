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

This project uses [Black](https://black.readthedocs.io/) with a line length of 99.

```bash
uv run black -l 99 src tests
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

The plugin contract is defined by the
[QC Executor framework](https://github.com/flaqship/qc-executor) (this template
targets v0.1.0). Your job is to fill in the abstract methods declared on
[`ExecutorBase`](https://github.com/flaqship/qc-executor/blob/main/src/qc_executor/base/executor_base.py):

| Method | What it should do |
| ------ | ----------------- |
| `_expectation_value` | Return the expectation value of an observable on a circuit. |
| `_expectation_value_derivatives` | Return analytic gradients of the expectation value. |
| `_sample` | Return measurement-shot counts. |
| `_statevector` | Return the full statevector. |
| `_transpile_circuit` | Convert a generic circuit into your backend-native form. |
| `_transpile_operator` | Convert a generic operator into your backend-native form. |
| `get_accepted_backend_types` | List native backend/device classes for auto-detection. |
| `get_accepted_backend_aliases` | List string aliases the factory should route here. |

Replace each `raise NotImplementedError` in `src/qc_executor_mybackend/` with
your implementation, and convert each `pytest.raises(NotImplementedError)` test
in `tests/test_executor.py` into a real assertion.

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
