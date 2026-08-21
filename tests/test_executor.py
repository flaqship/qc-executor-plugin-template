"""Stub tests for MyBackendExecutor abstract methods.

Each abstract method is asserted to raise ``NotImplementedError`` so the suite
is green on a fresh template clone. As you implement each method, replace the
``pytest.raises(NotImplementedError)`` block with a real assertion against the
returned value.
"""

from __future__ import annotations

import pytest
from qc_executor.factory import Executor

from qc_executor_mybackend import MyBackendExecutor


def test_remote_property_is_local(mybackend_executor) -> None:
    """Default template assumes a local backend. Override if remote."""
    assert mybackend_executor.remote is False


def test_get_accepted_backend_types(mybackend_executor) -> None:
    """Backend-type list is empty in the template; populate with your SDK's classes."""
    assert mybackend_executor.get_accepted_backend_types() == []


def test_get_accepted_backend_aliases(mybackend_executor) -> None:
    """Alias list is empty in the template; populate with your backend's short names."""
    assert mybackend_executor.get_accepted_backend_aliases() == []


def test_factory_forwards_configuration() -> None:
    """The factory should pass constructor kwargs straight through to the plugin."""
    executor = Executor.create("mybackend", shots=1024, seed=42)
    assert isinstance(executor, MyBackendExecutor)
    config = executor.get_config()
    assert config["shots"] == 1024
    assert config["seed"] == 42


def test_switch_backend_preserves_configuration() -> None:
    """``switch_backend`` round-trips this plugin's configuration."""
    executor = Executor.create("mybackend", shots=1024, seed=42)
    switched = executor.switch_backend("mybackend", shots=2048)
    assert isinstance(switched, MyBackendExecutor)
    assert switched.get_config()["shots"] == 2048
    assert switched.get_config()["seed"] == 42


def test_expectation_value_stub(mybackend_executor) -> None:
    """``expectation_value`` should raise until you implement ``_expectation_value``."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.expectation_value(circuit=None, observable=None)


def test_expectation_value_derivatives_stub(mybackend_executor) -> None:
    """``expectation_value_derivatives`` should raise until you implement it."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.expectation_value_derivatives(circuit=None, observable=None)


def test_sample_stub(mybackend_executor) -> None:
    """``sample`` should raise until you implement ``_sample``."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.sample(circuit=None)


def test_statevector_stub(mybackend_executor) -> None:
    """``statevector`` should raise until you implement ``_statevector``."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.statevector(circuit=None)


def test_transpile_circuit_stub(mybackend_executor) -> None:
    """``transpile_circuit`` should raise until you implement ``_transpile_circuit``."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.transpile_circuit(circuit=None)


def test_transpile_operator_stub(mybackend_executor) -> None:
    """``transpile_operator`` should raise until you implement ``_transpile_operator``."""
    with pytest.raises(NotImplementedError):
        mybackend_executor.transpile_operator(operator=None)
