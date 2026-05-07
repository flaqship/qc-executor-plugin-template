# executor-mybackend

> **Template repository** for building a third-party backend plugin for the
> [Executor](https://github.com/flaqship/Executor) framework.
>
> Click **Use this template** on GitHub to start a new plugin repo from this
> scaffold, then walk through the [Rename Checklist](#rename-checklist) below.

---

## What this is

[Executor](https://github.com/flaqship/Executor) is an abstraction layer that
lets one user-facing API drive multiple quantum backends. Backends are
discovered at runtime via the `executor.backends` Python entry point, so any
PyPI package that ships an `ExecutorBase` subclass and declares the entry point
is automatically picked up.

This template gives you a working scaffold for such a package: registration
plumbing, abstract methods stubbed, CI configured, and instructions for getting
to a published PyPI release.

## Quick start

```bash
# 1. Click "Use this template" on GitHub, then clone your new repo:
git clone https://github.com/your-org/executor-mybackend.git
cd executor-mybackend

# 2. Walk through the Rename Checklist below.

# 3. Install dev dependencies and run the green-on-arrival test suite:
uv sync --group dev
uv run pytest tests/

# 4. Replace each `raise NotImplementedError` in src/executor_mybackend/
#    with your real implementation, and convert each
#    `pytest.raises(NotImplementedError)` in tests/test_executor.py
#    into a real assertion as you go.
```

## Rename Checklist

Every occurrence of `mybackend` / `MyBackend` / `executor-mybackend` /
`executor_mybackend` should become your backend's name. Suggested order:

1. **Pick names**:
   - PyPI distribution name — for example `executor-acmesim` (kebab-case).
   - Import name — for example `executor_acmesim` (snake-case, must be a valid
     Python identifier).
   - Short backend name — for example `acmesim` (used in `Executor.create("acmesim")`).
2. **Rename the source package directory:**
   `src/executor_mybackend/` → `src/executor_<your-name>/`.
3. **Rename module files** inside `src/executor_<your-name>/`:
   `mybackend_executor.py`, `mybackend_circuit.py`, `mybackend_operator.py`.
4. **Find-and-replace** across the repo:
   - `MyBackend` → `<YourBackend>` (PascalCase, used in class names)
   - `mybackend` → `<your-backend>` (used in registration strings, docs)
   - `executor_mybackend` → `executor_<your-name>` (import path)
   - `executor-mybackend` → `executor-<your-name>` (PyPI distribution name)
5. **Update author / homepage / contact info** in `pyproject.toml`,
   `SECURITY.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/config.yml`.
6. **Update the `LICENSE`** copyright line with your name and year (or replace
   the file entirely if you want a different license).
7. **Run the tests** — `uv sync --group dev && uv run pytest tests/`. Everything
   should still be green; the registration test confirms your renamed plugin
   loads correctly.

## Implementing the contract

`MyBackendExecutor` in `src/executor_mybackend/mybackend_executor.py` subclasses
[`ExecutorBase`](https://github.com/flaqship/Executor/blob/main/src/executor/base/executor_base.py).
Replace each stub:

| Method | Returns | Notes |
| ------ | ------- | ----- |
| `_expectation_value` | `float \| np.ndarray` | Expectation value of an observable on a circuit. |
| `_expectation_value_derivatives` | `float \| np.ndarray \| dict` | Analytic gradients with respect to circuit parameters. |
| `_sample` | `dict \| list[dict]` | Measurement-shot counts (bitstring → count). |
| `_statevector` | `np.ndarray` | Full statevector of the circuit. |
| `_transpile_circuit` | `QuantumCircuitBase` | Convert a generic circuit into your backend-native form. |
| `_transpile_operator` | `QuantumOperatorBase` | Convert a generic operator into your backend-native form. |
| `get_accepted_backend_types` | `list[type]` | Native backend classes; powers auto-detection. |

For worked examples, see the in-tree backends in the parent repo:
[Qulacs](https://github.com/flaqship/Executor/tree/main/src/executor/qulacs) (smallest),
[PennyLane](https://github.com/flaqship/Executor/tree/main/src/executor/pennylane),
[Qiskit](https://github.com/flaqship/Executor/tree/main/src/executor/qiskit).

## Testing your plugin

```bash
uv sync --group dev
uv run pytest tests/ -v
```

`tests/test_registration.py` confirms the plugin discovers correctly via
entry points; treat its passing as a gate. `tests/test_executor.py` starts as
stub assertions of `NotImplementedError` and should be tightened into real
assertions as you implement methods.

## Switching the executor dependency to PyPI

The template currently pulls the `executor` framework from git:

```toml
dependencies = [
    "executor @ git+https://github.com/flaqship/Executor.git",
]
```

Once Executor is published to PyPI under its real distribution name, swap this
for a version pin:

```toml
dependencies = [
    "<executor-distribution-name>>=<version>",
]
```

(The PyPI name `executor` is currently held by an unrelated package, so
Executor will publish under a different name. Watch the parent repo's release
notes for the announcement.)

## Publishing to PyPI

1. Reserve your project name on [PyPI](https://pypi.org/account/register/).
2. Configure
   [trusted publishing](https://docs.pypi.org/trusted-publishers/) for this
   repo: add the workflow `publish.yml`, the GitHub environment `release`, and
   the project name on the PyPI side.
3. Update the `url:` line in `.github/workflows/publish.yml` to point at your
   PyPI project page.
4. Cut a release: bump the version in `src/executor_<your-name>/__init__.py`,
   tag, and create a GitHub Release. The `publish.yml` workflow will build and
   upload automatically.

## License

Apache 2.0 — see [LICENSE](LICENSE). Replace with your preferred license if
desired; if you do, also update the classifier in `pyproject.toml`.
