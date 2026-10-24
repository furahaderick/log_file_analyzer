import logging

import pytest

from src.decorators import log_call, timer


def test_log_call_preserves_return_value(caplog):
    @log_call
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(2, 3)

    assert result == 5


def test_log_call_executes_function_once():
    calls = []

    @log_call
    def work():
        calls.append("called")
        return True

    assert work() is True
    assert calls == ["called"]


def test_timer_preserves_return_value():
    @timer
    def calculate():
        return 42

    assert calculate() == 42


def test_timer_executes_function_once():
    calls = []

    @timer
    def work():
        calls.append(1)

    work()
    assert calls == [1]


def test_decorators_preserve_exceptions():
    @timer
    @log_call
    def fail():
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError, match="Something went wrong"):
        fail()


def test_log_call_logs_function_name(caplog):
    @log_call
    def example_function():
        return "ok"

    with caplog.at_level(logging.INFO):
        example_function()

    assert "example_function" in caplog.text


def test_timer_logs_timing_information(caplog):
    @timer
    def quick_function():
        return None

    with caplog.at_level(logging.INFO):
        quick_function()

    # Adjust this assertion to match the message your timer emits.
    assert "quick_function" in caplog.text
