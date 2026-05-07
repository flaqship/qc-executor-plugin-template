"""MyBackend executor implementation — the meat of a plugin.

Subclass of :class:`executor.base.executor_base.ExecutorBase`. Replace each
``raise NotImplementedError`` with the actual backend logic. Tests in
``tests/test_executor.py`` assert that these stubs raise; convert each test to
a real assertion as you implement the corresponding method.
"""

from __future__ import annotations

from typing import List

import numpy as np
from executor.base.circuit_base import QuantumCircuitBase
from executor.base.executor_base import ExecutorBase
from executor.base.operator_base import QuantumOperatorBase

from .mybackend_circuit import MyBackendCircuit
from .mybackend_operator import MyBackendOperator


class MyBackendExecutor(ExecutorBase):
    """Executor plugin for MyBackend.

    Args:
        shots (int | None, optional): Number of shots for sampling.
        seed (int | None, optional): Random seed for reproducibility.
        log_file (str | None, optional): Path to the log file.
        log_level (str, optional): Logging level.
        caching (bool | None, optional): Whether to use in-memory caching.
        cache_dir (str, optional): Directory for caching.
        max_cache_size (int | None, optional): Maximum number of entries kept
            in each in-memory cache.
    """

    _native_circuit_class = MyBackendCircuit
    _native_operator_class = MyBackendOperator

    def __init__(
        self,
        shots: int | None = None,
        seed: int | None = None,
        log_file: str | None = None,
        log_level: str = "WARNING",
        caching: bool | None = None,
        cache_dir: str = "cache",
        max_cache_size: int | None = None,
    ):
        super().__init__(
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
        raise NotImplementedError

    @property
    def remote(self) -> bool:
        """Return True if execution accesses a remote backend."""
        return False

    @classmethod
    def get_accepted_backend_types(cls) -> List[type]:
        """Backend object types this executor accepts for auto-detection.

        Return the native backend/device classes from your SDK so that callers
        can pass an instance directly to :meth:`executor.factory.Executor.create`
        and have it routed here.
        """
        return []

    @classmethod
    def get_accepted_backend_aliases(cls) -> List[str]:
        """String aliases the factory should route to this executor.

        Return any short names callers might pass instead of ``"mybackend"``.
        """
        return []

    def _expectation_value(
        self,
        circuit: QuantumCircuitBase | List[QuantumCircuitBase],
        observable: QuantumOperatorBase | List[QuantumOperatorBase],
        **parameters,
    ) -> float | np.ndarray:
        raise NotImplementedError("TODO: implement _expectation_value for MyBackend")

    def _expectation_value_derivatives(
        self,
        circuit: QuantumCircuitBase | List[QuantumCircuitBase],
        observable: QuantumOperatorBase | List[QuantumOperatorBase],
        *derivative,
        **parameters,
    ) -> float | np.ndarray | dict:
        raise NotImplementedError("TODO: implement _expectation_value_derivatives for MyBackend")

    def _sample(
        self, circuit: QuantumCircuitBase | List[QuantumCircuitBase], **parameters
    ) -> dict | List[dict]:
        raise NotImplementedError("TODO: implement _sample for MyBackend")

    def _statevector(
        self, circuit: QuantumCircuitBase | List[QuantumCircuitBase], **parameters
    ) -> np.ndarray:
        raise NotImplementedError("TODO: implement _statevector for MyBackend")

    def _transpile_circuit(self, circuit: QuantumCircuitBase) -> QuantumCircuitBase:
        raise NotImplementedError("TODO: implement _transpile_circuit for MyBackend")

    def _transpile_operator(self, operator: QuantumOperatorBase) -> QuantumOperatorBase:
        raise NotImplementedError("TODO: implement _transpile_operator for MyBackend")
