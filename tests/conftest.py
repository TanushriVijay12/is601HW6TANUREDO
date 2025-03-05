# pylint: disable=comparison-with-callable

from decimal import Decimal
from faker import Faker
from calculator.commands.add import AddCommand
from calculator.commands.subtract import SubtractCommand
from calculator.commands.multiply import MultiplyCommand
from calculator.commands.divide import DivideCommand

fake = Faker()

def generate_test_data(num_records):
    operation_mappings = {
        'add': AddCommand(),
        'subtract': SubtractCommand(),
        'multiply': MultiplyCommand(),
        'divide': DivideCommand()
    }
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation = operation_mappings[operation_name]

        if operation_name == 'divide' and b == Decimal('0'):
            expected = "ZeroDivisionError"
        else:
            try:
                expected = operation.execute(a, b)
            except ZeroDivisionError:
                expected = "ZeroDivisionError"

        yield a, b, operation_name, operation, expected

def pytest_addoption(parser):
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    # Check if the test is expecting any of the dynamically generated fixtures
    if {"a", "b", "operation", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        # Generate test data
        parameters = list(generate_test_data(num_records))
        # Modify parameters to fit test functions' expectations
        modified_parameters = [(a, b, operation, expected) for a, b, _, operation, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)
