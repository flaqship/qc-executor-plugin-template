"""Tests that the plugin registers correctly with the Executor factory.

These are the tests that should keep passing after every change you make to
the plugin — if registration breaks, no other test will be meaningful.
"""

from importlib.metadata import entry_points

from executor.factory import Executor

import executor_mybackend  # noqa: F401  -- import registers the backend
from executor_mybackend import MyBackendExecutor


def test_backend_appears_in_available_backends() -> None:
    """Importing the plugin should expose ``mybackend`` to the factory."""
    assert "mybackend" in Executor.available_backends()


def test_factory_create_returns_mybackend_executor() -> None:
    """``Executor.create("mybackend")`` should return our executor."""
    instance = Executor.create("mybackend")
    assert isinstance(instance, MyBackendExecutor)


def test_entry_point_declared_in_pyproject_toml() -> None:
    """The ``executor.backends`` entry point should be discoverable.

    This test passes once the package is installed (e.g. ``uv sync``);
    it confirms that ``pyproject.toml`` advertises the plugin to other
    code that doesn't ``import executor_mybackend`` explicitly.
    """
    eps = entry_points(group="executor.backends")
    names = {ep.name for ep in eps}
    assert "mybackend" in names, (
        "The 'executor.backends' entry point group does not contain 'mybackend'. "
        "Reinstall the package with `uv sync` after changes to pyproject.toml."
    )
