# qc-executor-mybackend

> **Template repository** for building a third-party backend plugin for
> [QC Executor](https://github.com/flaqship/qc-executor).
>
> Click **Use this template** on GitHub to start a new plugin repo from this
> scaffold, then walk through the [Rename Checklist](#rename-checklist) below.
>
> Targets QC Executor **v0.1.0**.

---

## What this is

[QC Executor](https://github.com/flaqship/qc-executor) is an abstraction layer
that lets one user-facing API drive multiple quantum backends. Backends are
discovered at runtime via the `qc_executor.backends` Python entry point, so any
PyPI package that ships an `ExecutorBase` subclass and declares the entry point
is automatically picked up.

This template gives you a working scaffold for such a package: registration
plumbing, abstract methods stubbed, CI configured, and instructions for getting
to a published PyPI release.

## Quick start

```bash
# 1. Click "Use this template" on GitHub, then clone your new repo:
git clone https://github.com/your-org/qc-executor-mybackend.git
cd qc-executor-mybackend

# 2. Walk through the Rename Checklist below.

# 3. Install dev dependencies and run the green-on-arrival test suite:
uv sync --group dev
uv run pytest tests/

# 4. Replace each `raise NotImplementedError` in src/qc_executor_mybackend/
#    with your real implementation, and convert each
#    `pytest.raises(NotImplementedError)` in tests/test_executor.py
#    into a real assertion as you go.
```

## Rename Checklist

Every occurrence of `mybackend` / `MyBackend` / `qc-executor-mybackend` /
`qc_executor_mybackend` should become your backend's name. Suggested order:

1. **Pick names**:
   - PyPI distribution name — for example `qc-executor-acmesim` (kebab-case).
     Prefixing with `qc-executor-` keeps plugins discoverable alongside the
     framework.
   - Import name — for example `qc_executor_acmesim` (snake-case, must be a
     valid Python identifier).
   - Short backend name — for example `acmesim` (used in `Executor.create("acmesim")`).
2. **Rename the source package directory:**
   `src/qc_executor_mybackend/` → `src/qc_executor_<your-name>/`.
3. **Rename module files** inside `src/qc_executor_<your-name>/`:
   `mybackend_executor.py`, `mybackend_circuit.py`, `mybackend_operator.py`.
4. **Find-and-replace** across the repo:
   - `MyBackend` → `<YourBackend>` (PascalCase, used in class names)
   - `mybackend` → `<your-backend>` (used in registration strings, docs)
   - `qc_executor_mybackend` → `qc_executor_<your-name>` (import path)
   - `qc-executor-mybackend` → `qc-executor-<your-name>` (PyPI distribution name)

   Note that `qc_executor` / `qc-executor` on their own refer to the framework
   and must **not** be renamed.
5. **Update author / homepage / contact info** in `pyproject.toml`,
   `SECURITY.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/config.yml`.
6. **Update `LICENSE.txt`** — fill in the `Copyright [yyyy] [name of copyright
   owner]` line with your name and year (or replace the file entirely if you
   want a different license).
7. **Run the tests** — `uv sync --group dev && uv run pytest tests/`. Everything
   should still be green; the registration test confirms your renamed plugin
   loads correctly.

## Implementing the contract

`MyBackendExecutor` in `src/qc_executor_mybackend/mybackend_executor.py`
subclasses
[`ExecutorBase`](https://github.com/flaqship/qc-executor/blob/main/src/qc_executor/base/executor_base.py).
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
| `get_accepted_backend_aliases` | `list[str]` | Short names the factory should route here. |

The public wrappers (`expectation_value`, `sample`, …) live on `ExecutorBase`
and handle parameter normalisation and result caching before delegating to your
underscore-prefixed implementations — implement only the latter.

A generic `QuantumCircuit` carries a Qiskit circuit as its intermediate
representation (`circuit.qiskit_circuit`), and a generic `QuantumOperator`
carries a Qiskit `SparsePauliOp` (`operator.qiskit_operator`). Build your native
form from those in the circuit/operator wrappers.

### Backend object convention

If your backend selects a device/simulator object or named target, the
constructor parameter is always called `backend` — the factory forwards
auto-detected objects and registered aliases through it:

```python
Executor.create("mybackend", shots=1024)          # by registered name
Executor.create(my_native_device_object)          # via get_accepted_backend_types()
Executor.create("my-alias")                       # via get_accepted_backend_aliases()
```

For worked examples, see the in-tree backends in the framework repo:
[Qulacs](https://github.com/flaqship/qc-executor/tree/main/src/qc_executor/qulacs) (smallest),
[PennyLane](https://github.com/flaqship/qc-executor/tree/main/src/qc_executor/pennylane),
[Qiskit](https://github.com/flaqship/qc-executor/tree/main/src/qc_executor/qiskit),
[Pauli propagation](https://github.com/flaqship/qc-executor/tree/main/src/qc_executor/pauli_propagation).

## Testing your plugin

```bash
uv sync --group dev
uv run pytest tests/ -v
```

`tests/test_registration.py` confirms the plugin discovers correctly via
entry points; treat its passing as a gate. `tests/test_executor.py` starts as
stub assertions of `NotImplementedError` and should be tightened into real
assertions as you implement methods.

## Depending on QC Executor

QC Executor is published on PyPI as
[`qc-executor`](https://pypi.org/project/qc-executor/); this template pins it in
`pyproject.toml`:

```toml
dependencies = [
    "qc-executor>=0.1.0",
]
```

The framework only requires Qiskit (used as the common intermediate
representation). If your plugin needs one of its optional backends for
comparison in tests, add the matching extra, for example
`qc-executor[qulacs]>=0.1.0`.

## Publishing to PyPI

1. Reserve your project name on [PyPI](https://pypi.org/account/register/).
2. Configure
   [trusted publishing](https://docs.pypi.org/trusted-publishers/) for this
   repo: add the workflow `publish.yml`, the GitHub environment `release`, and
   the project name on the PyPI side.
3. Update the `url:` line in `.github/workflows/publish.yml` to point at your
   PyPI project page.
4. Cut a release: bump the version in `src/qc_executor_<your-name>/__init__.py`,
   tag, and create a GitHub Release. The `publish.yml` workflow will build and
   upload automatically.

## License

Apache 2.0 — see [LICENSE.txt](LICENSE.txt). Replace with your preferred license
if desired; if you do, also update the classifier in `pyproject.toml`.
