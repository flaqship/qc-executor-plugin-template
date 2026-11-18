# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `tests/test_native_types.py`: conversion, gate lowering and rejection tests
  for the native circuit and operator.

### Changed

- Target QC Executor v0.2.1 (was v0.1.0).
- `MyBackendCircuit` / `MyBackendOperator` subclass `QuantumCircuitBase` /
  `QuantumOperatorBase` and override only `supported_opcodes()` /
  `_build_native()`. They build on the shared IR instead of Qiskit objects.
- `_transpile_circuit` / `_transpile_operator` are implemented via the inherited
  `from_quantum_circuit()` / `from_quantum_operator()`.
- `max_cache_size` defaults to 4096 (was unbounded), matching `ExecutorBase`.

### Deprecated
### Removed

- Dedicated circuit/operator caches; `ExecutorBase` caches circuit conversion.

### Fixed
### Security