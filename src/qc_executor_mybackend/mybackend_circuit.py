"""MyBackend native circuit.

:class:`~qc_executor.base.circuit_base.QuantumCircuitBase` is concrete: it owns
the circuit IR and the whole builder API. A backend overrides only
:meth:`~MyBackendCircuit.supported_opcodes` and
:meth:`~MyBackendCircuit._build_native`. Gates outside the supported set are
lowered by the framework, or rejected with ``UnsupportedGateError`` when no
decomposition exists.
"""

from __future__ import annotations

from typing import Any, FrozenSet

from qc_executor.base.circuit_base import QuantumCircuitBase
from qc_executor.base.gate_set import OpCode

#: TODO: declare the gates MyBackend executes natively.
SUPPORTED_OPCODES: FrozenSet[OpCode] = frozenset()


class MyBackendCircuit(QuantumCircuitBase):
    """Backend-native circuit for MyBackend."""

    @classmethod
    def supported_opcodes(cls) -> FrozenSet[OpCode]:
        """Return the opcodes MyBackend executes natively."""
        return SUPPORTED_OPCODES

    def _build_native(self) -> Any:
        """Compile the lowered IR into MyBackend's native circuit."""
        ir = self._lowered_ir()  # only supported_opcodes() (plus BARRIER) from here on
        raise NotImplementedError(
            f"TODO: compile {len(ir)} lowered instructions into a {type(self).__name__}"
        )
