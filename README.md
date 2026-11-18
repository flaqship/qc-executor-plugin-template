# qc-executor-mybackend

> **Template repository** for building a third-party backend plugin for
> [QC Executor](https://github.com/flaqship/qc-executor).
>
> Click **Use this template** on GitHub to start a new plugin repo from this
> scaffold, then walk through the [Rename Checklist](#rename-checklist) below.
>
> Targets QC Executor **v0.2.1**.

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

# 4. Declare SUPPORTED_OPCODES, replace each `raise NotImplementedError`
#    in src/, and turn the matching stub tests into real assertions.
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

Three classes make up a plugin:

- `MyBackendExecutor` subclasses
  [`ExecutorBase`](https://github.com/flaqship/qc-executor/blob/main/src/qc_executor/base/executor_base.py).
  Its public methods (`expectation_value`, `sample`, …) normalise parameters,
  cache results and convert inputs, then call your underscore methods.
- `MyBackendCircuit` / `MyBackendOperator` subclass `QuantumCircuitBase` /
  `QuantumOperatorBase`, which hold the framework-independent circuit IR and
  Pauli representation. You only compile that into your SDK's objects.

| Class | Method | Returns | Notes |
| ----- | ------ | ------- | ----- |
| Circuit | `supported_opcodes` | `frozenset[OpCode]` | Gates your backend runs natively; others are lowered or rejected. |
| Circuit | `_build_native` | SDK circuit | Compile `self._lowered_ir()`. |
| Operator | `_build_native` | SDK operator | Compile `paulis` / `coeffs`. |
| Executor | `_expectation_value` | `float \| np.ndarray` | Expectation value of an observable on a circuit. |
| Executor | `_expectation_value_derivatives` | `float \| np.ndarray \| dict` | Analytic gradients with respect to circuit parameters. |
| Executor | `_sample` | `dict \| list[dict]` | Measurement-shot counts (bitstring → count). |
| Executor | `_statevector` | `np.ndarray` | Full statevector of the circuit. |
| Executor | `_transpile_circuit` / `_transpile_operator` | native type | Implemented; extend for device mapping. |
| Executor | `get_accepted_backend_types` | `list[type]` | Native backend classes; powers auto-detection. |
| Executor | `get_accepted_backend_aliases` | `list[str]` | Short names the factory should route here. |

If a native class needs its own state, keep the base constructor signature and
add only keyword-only arguments: inherited methods such as `copy()` rebuild
instances through it.

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

`tests/test_registration.py` is the gate: if registration breaks, nothing else
matters. Stub tests assert `NotImplementedError`; turn them into real assertions
as you implement. The gate pass-through test is skipped until you declare
`SUPPORTED_OPCODES`.

## Depending on QC Executor

QC Executor is published on PyPI as
[`qc-executor`](https://pypi.org/project/qc-executor/); this template pins it in
`pyproject.toml`:

```toml
dependencies = [
   "qc-executor>=0.2.1",
]
```

If your plugin needs one of its optional backends for
comparison in tests, add the matching extra, for example
`qc-executor[qulacs]>=0.2.1`.

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
