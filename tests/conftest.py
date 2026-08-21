"""Shared pytest fixtures for the MyBackend plugin tests."""

import pytest
from qc_executor.factory import Executor

# Importing the plugin package runs Executor.register(), so the factory below
# resolves "mybackend" without any extra wiring.
from qc_executor_mybackend import MyBackendExecutor


@pytest.fixture
def mybackend_executor() -> MyBackendExecutor:
    """Return a freshly-constructed MyBackendExecutor."""
    return Executor.create("mybackend")
