"""Shared pytest fixtures for the MyBackend plugin tests."""

import pytest
from executor.factory import Executor

import executor_mybackend  # noqa: F401  -- import registers the backend
from executor_mybackend import MyBackendExecutor


@pytest.fixture
def mybackend_executor() -> MyBackendExecutor:
    """Return a freshly-constructed MyBackendExecutor."""
    return Executor.create("mybackend")
