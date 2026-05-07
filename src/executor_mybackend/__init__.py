"""MyBackend plugin for the Executor framework.

Replace this module-level docstring and the ``mybackend``/``MyBackend`` names
throughout the package with your backend's name. See README.md for the
full rename checklist.
"""

__version__ = "0.0.1"

try:
    from executor.factory import Executor

    from .mybackend_circuit import MyBackendCircuit
    from .mybackend_executor import MyBackendExecutor
    from .mybackend_operator import MyBackendOperator

    Executor.register("mybackend")(MyBackendExecutor)

    __all__ = [
        "MyBackendCircuit",
        "MyBackendExecutor",
        "MyBackendOperator",
    ]

except ImportError as e:
    import warnings

    warnings.warn(
        f"MyBackend executor plugin not available: {e}. "
        "Install with: pip install executor-mybackend",
        UserWarning,
    )
    raise
