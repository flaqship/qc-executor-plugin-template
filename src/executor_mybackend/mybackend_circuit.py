"""MyBackend native circuit wrapper.

Wraps a generic :class:`executor.quantum_circuit.QuantumCircuit` and exposes it
in a form your backend can execute. Most in-tree backends keep this class
standalone (not subclassing :class:`executor.base.circuit_base.QuantumCircuitBase`)
and only implement the methods their executor actually needs. You can opt in to
the full base-class contract by changing the class declaration to
``class MyBackendCircuit(QuantumCircuitBase):`` — that gives you the gate-level
abstract methods, but you must then implement every gate.
"""

from __future__ import annotations

from executor.quantum_circuit import QuantumCircuit


class MyBackendCircuit:
    """Backend-native circuit for MyBackend."""

    @classmethod
    def from_quantum_circuit(cls, circuit: QuantumCircuit) -> "MyBackendCircuit":
        """Create a MyBackend native circuit from a generic ``QuantumCircuit``."""
        return cls(circuit)

    def __init__(self, circuit: QuantumCircuit) -> None:
        self._source_circuit = circuit
        self._num_qubits = circuit.num_qubits
        # TODO: build your backend-native representation from ``circuit`` here.

    @property
    def num_qubits(self) -> int:
        """Return the number of qubits in the circuit."""
        return self._num_qubits
