import logging
import pytest
from main import calculate_and_print, main

# Ensure that pytest captures the log output
@pytest.fixture(autouse=True)
def caplog(caplog):
    """Capture logs during tests."""
    with caplog.at_level(logging.INFO):  # You can change this to logging.DEBUG if needed
        yield caplog

# Parameterize the test function to cover different operations and scenarios, including errors
@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "Cannot divide by zero."),
    ("9", "3", 'unknown', "Unknown operation: unknown"),
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),
    ("5", "b", 'subtract', "Invalid number input: 5 or b is not a valid number.")
])
def test_calculate_and_print(a_string, b_string, operation_string, expected_string, caplog):
    calculate_and_print(a_string, b_string, operation_string)

    # Assert that the expected string is in the log output captured by caplog
    assert expected_string in caplog.text


def test_repl_loop_exit(monkeypatch, capsys):
    '''Test that the REPL loop exits when 'exit' is entered'''
    # Simulate user input of 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    main()
    captured = capsys.readouterr()
    assert "Exiting calculator. Goodbye!" in captured.out
