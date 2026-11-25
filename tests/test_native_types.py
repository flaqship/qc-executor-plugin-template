"""Tests for the native circuit and operator types.

These hold for any ``SUPPORTED_OPCODES`` you declare. The ``native`` stub tests
assert ``NotImplementedError``; replace them with real assertions once
``_build_native`` is implemented.
"""

from __future__ import annotations

import numpy as np
import pytest
from qc_executor import QuantumCircuit, QuantumOperator
from qc_executor.base.circuit_base import QuantumCircuitBase
from qc_executor.base.decompose import UnsupportedGateError
from qc_executor.base.gate_set import GATE_DEFS, OpCode
from qc_executor.base.operator_base import QuantumOperatorBase

from qc_executor_mybackend import MyBackendCircuit, MyBackendOperator

_STRUCTURAL = {OpCode.BARRIER, OpCode.BLOCK_BEGIN, OpCode.BLOCK_END}


def test_native_types_subclass_framework_bases() -> None:
    assert issubclass(MyBackendCircuit, QuantumCircuitBase)
    assert issubclass(MyBackendOperator, QuantumOperatorBase)


# ----------------------------------------------------------------------
# Circuit
# ----------------------------------------------------------------------


def test_circuit_from_generic() -> None:
    generic = QuantumCircuit(2)
    generic.h(0)
    generic.cx(0, 1)

    native = MyBackendCircuit.from_quantum_circuit(generic)

    assert isinstance(native, MyBackendCircuit)
    assert native.ir == generic.ir
    assert native.ir is not generic.ir  # copied, so edits don't leak back
    assert MyBackendCircuit.from_quantum_circuit(native) is native
    # Inherited methods rebuild via the constructor and must keep the type.
    assert isinstance(native.invert(), MyBackendCircuit)


def test_supported_opcodes_pass_through_lowering() -> None:
    """Every declared opcode reaches ``_build_native`` unchanged."""
    declared = MyBackendCircuit.supported_opcodes() - _STRUCTURAL
    if not declared:
        pytest.skip("SUPPORTED_OPCODES is empty; declare MyBackend's native gates")

    defs = [GATE_DEFS[opcode] for opcode in declared]
    native = MyBackendCircuit(max(d.num_qubits for d in defs), max(d.num_clbits for d in defs))
    for opcode, gate in zip(declared, defs):
        native.ir.append(
            opcode,
            range(gate.num_qubits),
            (0.1,) * gate.num_params,
            range(gate.num_clbits),
        )

    assert native._lowered_ir() is native.ir


def test_undeclared_gate_is_lowered(monkeypatch) -> None:
    """An undeclared gate is decomposed into the declared set.

    CZ is an example; swap it for a gate your backend lacks. RX, RY, RZ and CX
    have no decomposition rule, so they cannot serve as the example.
    """
    if not MyBackendCircuit.supported_opcodes():
        basis = frozenset({OpCode.RX, OpCode.RY, OpCode.RZ, OpCode.CX})
        monkeypatch.setattr(MyBackendCircuit, "supported_opcodes", classmethod(lambda _: basis))
    supported = MyBackendCircuit.supported_opcodes()
    if OpCode.CZ in supported:
        pytest.skip("CZ is native to MyBackend; pick another example gate")

    native = MyBackendCircuit(2)
    native.cz(0, 1)
    lowered = {instruction.opcode for instruction in native._lowered_ir()}

    assert OpCode.CZ not in lowered
    assert lowered <= supported | {OpCode.BARRIER}


def test_undeclared_non_unitary_instructions_are_rejected() -> None:
    if OpCode.RESET in MyBackendCircuit.supported_opcodes():
        pytest.skip("MyBackend declares RESET as native")

    native = MyBackendCircuit(1)
    native.reset(0)

    with pytest.raises(UnsupportedGateError, match="reset"):
        _ = native.native


def test_circuit_native_stub() -> None:
    with pytest.raises(NotImplementedError, match="TODO"):
        _ = MyBackendCircuit(1).native


# ----------------------------------------------------------------------
# Operator
# ----------------------------------------------------------------------


def test_operator_from_generic() -> None:
    generic = QuantumOperator(["ZI", "XX"], [1.0, 0.5])

    native = MyBackendOperator.from_quantum_operator(generic)

    assert isinstance(native, MyBackendOperator)
    assert native.paulis == generic.paulis
    assert np.allclose(native.coeffs_array, generic.coeffs_array)
    assert MyBackendOperator.from_quantum_operator(native) is native
    assert isinstance(native.adjoint(), MyBackendOperator)


def test_operator_native_stub() -> None:
    with pytest.raises(NotImplementedError, match="TODO"):
        _ = MyBackendOperator(["Z"], [1.0]).native
