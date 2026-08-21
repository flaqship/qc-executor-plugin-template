"""MyBackend native operator wrapper.

Wraps a generic :class:`qc_executor.quantum_operator.QuantumOperator` for your
backend's expectation-value/sampling routines. Like the circuit wrapper, this
class is intentionally not subclassing
:class:`qc_executor.base.operator_base.QuantumOperatorBase`; subclass it if you
want the full algebraic API contract.

The generic operator carries a Qiskit ``SparsePauliOp`` as its intermediate
representation, reachable via ``operator.qiskit_operator``.
"""

from __future__ import annotations

from qc_executor.quantum_operator import QuantumOperator


class MyBackendOperator:
    """Backend-native operator for MyBackend."""

    @classmethod
    def from_quantum_operator(cls, operator: QuantumOperator) -> "MyBackendOperator":
        """Create a MyBackend native operator from a generic ``QuantumOperator``."""
        return cls(operator)

    def __init__(self, operator: QuantumOperator) -> None:
        self._source_operator = operator
        self._num_qubits = operator.num_qubits
        # TODO: build your backend-native representation from ``operator`` here.

    @property
    def num_qubits(self) -> int:
        """Return the number of qubits the operator acts on."""
        return self._num_qubits
