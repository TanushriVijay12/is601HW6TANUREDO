from decimal import Decimal, InvalidOperation
from calculator import Calculator
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Default to 'production' if not set
print(f"Running in {ENVIRONMENT} mode")

def calculate_and_print(a, b, operation_name):
    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        calculator = Calculator()
        if operation_name in calculator.commands:
            result = calculator.commands[operation_name].execute(a_decimal, b_decimal)
            print(f"The result of {a} {operation_name} {b} is equal to {result}")
        else:
            raise ValueError(f"Unknown operation: {operation_name}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ValueError as e:
        print(e)

def main():
    import sys
    if len(sys.argv) == 4:
        # Command-line mode
        _, a, b, operation_name = sys.argv
        calculate_and_print(a, b, operation_name)
    else:
        # Interactive REPL mode
        calculator = Calculator()
        calculator.run()

if __name__ == '__main__':
    main()