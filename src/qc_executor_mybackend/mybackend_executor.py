"""MyBackend executor implementation — the meat of a plugin.

Subclass of :class:`qc_executor.base.executor_base.ExecutorBase`. Replace each
``raise NotImplementedError`` with the actual backend logic. Tests in
``tests/test_executor.py`` assert that these stubs raise; convert each test to
a real assertion as you implement the corresponding method.
"""

from __future__ import annotations

from typing import Any, List

import numpy as np
from qc_executor.base.circuit_base import QuantumCircuitBase
from qc_executor.base.executor_base import ExecutorBase
from qc_executor.base.operator_base import QuantumOperatorBase

from .mybackend_circuit import MyBackendCircuit
from .mybackend_operator import MyBackendOperator


class MyBackendExecutor(ExecutorBase):
    """Executor plugin for MyBackend.

    Args:
        backend (Any, optional): Backend-native device/simulator object or its
            string name. The framework convention is that this parameter is
            always called ``backend``; the factory forwards auto-detected
            objects and aliases through it. Drop the parameter if your backend
            has nothing to select.
        shots (int | None, optional): Number of shots for sampling.
        seed (int | None, optional): Random seed for reproducibility.
        log_file (str | None, optional): Path to the log file.
        log_level (str, optional): Logging level.
        caching (bool | None, optional): Whether to use in-memory caching.
        cache_dir (str, optional): Directory for caching.
        max_cache_size (int | None, optional): Maximum number of entries kept
            in each in-memory cache; ``None`` makes them unbounded.

    Note:
        ``ExecutorBase`` already caches circuit conversion (keyed by circuit
        content), so no dedicated circuit cache is needed here. Operator
        conversion is *not* cached by the base class; if converting an
        operator is expensive for your backend, cache it inside
        :meth:`_transpile_operator`, keyed by ``(operator, options)``.
    """

    _native_circuit_class = MyBackendCircuit
    _native_operator_class = MyBackendOperator

    def __init__(
        self,
        backend: Any = None,
        shots: int | None = None,
        seed: int | None = None,
        log_file: str | None = None,
        log_level: str = "WARNING",
        caching: bool | None = None,
        cache_dir: str = "cache",
        max_cache_size: int | None = 4096,
    ):
        super().__init__(
            backend=backend,
            shots=shots,
            seed=seed,
            log_file=log_file,
            log_level=log_level,
            caching=caching,
            cache_dir=cache_dir,
            max_cache_size=max_cache_size,
        )

    @property
    def shots(self) -> int | None:
        """Return the number of shots."""
        return self._shots

    @shots.setter
    def shots(self, value: int | None) -> None:
        """Set the number of shots."""
        raise NotImplementedError(f"TODO: implement shots setter for {type(self).__name__}")

    @property
    def remote(self) -> bool:
        """Return True if execution accesses a remote backend."""
        return False

    @classmethod
    def get_accepted_backend_types(cls) -> List[type]:
        """Backend object types this executor accepts for auto-detection.

        Return the native backend/device classes from your SDK so that callers
        can pass an instance directly to
        :meth:`qc_executor.factory.Executor.create` and have it routed here.
        """
        return []

    @classmethod
    def get_accepted_backend_aliases(cls) -> List[str]:
        """String aliases the factory should route to this executor.

        Return any short names callers might pass instead of ``"mybackend"``.
        Each alias is forwarded to ``__init__`` as ``backend=<alias>``, and
        aliases must be unique across all registered backends.
        """
        return []

    def _expectation_value(
        self,
        circuit: QuantumCircuitBase | List[QuantumCircuitBase],
        observable: QuantumOperatorBase | List[QuantumOperatorBase],
        **parameters,
    ) -> float | np.ndarray:
        raise NotImplementedError(f"TODO: implement _expectation_value for {type(self).__name__}")

    def _expectation_value_derivatives(
        self,
        circuit: QuantumCircuitBase | List[QuantumCircuitBase],
        observable: QuantumOperatorBase | List[QuantumOperatorBase],
        *derivative,
        **parameters,
    ) -> float | np.ndarray | dict:
        raise NotImplementedError(
            f"TODO: implement _expectation_value_derivatives for {type(self).__name__}"
        )

    def _sample(
        self, circuit: QuantumCircuitBase | List[QuantumCircuitBase], **parameters
    ) -> dict | List[dict]:
        raise NotImplementedError(f"TODO: implement _sample for {type(self).__name__}")

    def _statevector(
        self, circuit: QuantumCircuitBase | List[QuantumCircuitBase], **parameters
    ) -> np.ndarray:
        raise NotImplementedError(f"TODO: implement _statevector for {type(self).__name__}")

    def _transpile_circuit(self, circuit: QuantumCircuitBase) -> MyBackendCircuit:
        # Add device-specific steps (e.g. qubit mapping) here if your backend needs them.
        return MyBackendCircuit.from_quantum_circuit(circuit)

    def _transpile_operator(
        self, operator: QuantumOperatorBase, **options: Any
    ) -> MyBackendOperator:
        # The base class does not cache operator conversion (only results, when
        # ``caching=True``). Add a cache here if conversion is expensive.
        return MyBackendOperator.from_quantum_operator(operator, **options)
