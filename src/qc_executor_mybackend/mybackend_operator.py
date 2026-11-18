"""MyBackend native operator.

:class:`~qc_executor.base.operator_base.QuantumOperatorBase` is concrete: it
owns the sparse Pauli representation and the operator algebra. A backend
overrides only :meth:`~MyBackendOperator._build_native`.
"""

from __future__ import annotations
from typing import Any

from qc_executor.base.operator_base import QuantumOperatorBase


class MyBackendOperator(QuantumOperatorBase):
    """Backend-native operator for MyBackend."""

    def _build_native(self) -> Any:
        """Compile :attr:`paulis` and :attr:`coeffs` into MyBackend's native operator."""
        raise NotImplementedError(f"TODO: compile the Pauli terms into a {type(self).__name__}")