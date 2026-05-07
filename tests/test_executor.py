"""Stub tests for MyBackendExecutor abstract methods.

Each abstract method is asserted to raise ``NotImplementedError`` so the suite
is green on a fresh template clone. As you implement each method, replace the
``pytest.raises(NotImplementedError)`` block with a real assertion against the
returned value.
"""

from __future__ import annotations

import pytest


def test_remote_property_is_local(mybackend_executor) -> None:
    """Default template assumes a local backend. Override if remote."""
    assert mybackend_executor.remote is False


def test_get_accepted_backend_types(mybackend_executor) -> None:
    """Backend-type list is empty in the template; populate with your SDK's classes."""
    assert mybackend_executor.get_accepted_backend_types() == []


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
