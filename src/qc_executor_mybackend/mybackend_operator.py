"""MyBackend native operator wrapper.

Wraps a generic :class:`qc_executor.quantum_operator.QuantumOperator` for your
backend's expectation-value/sampling routines. Like the circuit wrapper, this
class is intentionally not subclassing
:class:`qc_executor.base.operator_base.QuantumOperatorBase`; subclass it if you
want the full algebraic API contract.
"""

from __future__ import annotations
from typing import Any

from qc_executor.quantum_operator import QuantumOperatorBase


class MyBackendOperator(QuantumOperatorBase):
    """Backend-native operator for MyBackend."""

    def __init__(self, operator: QuantumOperatorBase) -> None:
        self._source_operator = operator
        self._num_qubits = operator.num_qubits
        # raise NotImplementedError(f"TODO: build your backend-native representation from ``operator`` for {type(self).__name__}")
        return self._build_native()

    # ------------------------------------------------------------------
    # Backend hooks
    # ------------------------------------------------------------------

    def _build_native(self) -> Any:
        """Compile the representation into this backend's native operator."""
        return self.from_quantum_operator(self._source_operator)

    @classmethod
    def from_quantum_operator(cls, operator: QuantumOperatorBase) -> "MyBackendOperator":
        """Create a MyBackend native operator from a generic ``QuantumOperator``."""
        return cls(operator)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def num_qubits(self) -> int:
        """Return the number of qubits the operator acts on."""
        return self._num_qubits
