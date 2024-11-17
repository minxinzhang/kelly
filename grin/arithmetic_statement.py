from grin.statement import Statement
from grin.exception import GrinRuntimeError
import math


class AddStatement(Statement):
    def __init__(self, variable, value, label=None):
        super().__init__(label)
        self.variable = variable
        self.value = value

    def execute(self, interpreter):
        current_value = interpreter.variables.get(self.variable, 0)
        operand = interpreter.evaluate_value(self.value)

        # Check if both are strings (for concatenation)
        if isinstance(current_value, str) and isinstance(operand, str):
            result = current_value + operand

        # If both are numbers, handle type-based addition
        elif isinstance(current_value, (int, float)) and isinstance(operand, (int, float)):
            result = current_value + operand

        # If one is a number and the other is a string, it's an invalid operation
        elif isinstance(current_value, (int, float)) and isinstance(operand, str):
            raise GrinRuntimeError("Unsupported types for ADD operation: cannot add number and string")
        elif isinstance(current_value, str) and isinstance(operand, (int, float)):
            raise GrinRuntimeError("Unsupported types for ADD operation: cannot add string and number")

        # Raise error for unsupported types
        else:
            raise GrinRuntimeError("Unsupported types for ADD operation")

        interpreter.variables[self.variable] = result



class SubStatement(Statement):
    def __init__(self, variable, value, label=None):
        super().__init__(label)
        self.variable = variable
        self.value = value

    def execute(self, interpreter):
        current_value = interpreter.variables.get(self.variable, 0)
        operand = interpreter.evaluate_value(self.value)

        # Ensure both operands are of numeric types (int or float)
        if isinstance(current_value, (int, float)) and isinstance(operand, (int, float)):
            result = current_value - operand
        else:
            raise GrinRuntimeError("Unsupported types for SUB operation: operands must be int or float")

        interpreter.variables[self.variable] = result




class MultStatement(Statement):
    def __init__(self, variable, value, label=None):
        super().__init__(label)
        self.variable = variable
        self.value = value

    def execute(self, interpreter):
        current_value = interpreter.variables.get(self.variable, 0)
        multiplier = interpreter.evaluate_value(self.value)

        # Integer * Integer => Integer
        if isinstance(current_value, int) and isinstance(multiplier, int):
            result = current_value * multiplier

        # Float * Float, Float * Integer, Integer * Float => Float
        elif isinstance(current_value, (int, float)) and isinstance(multiplier, (int, float)):
            result = float(current_value) * float(multiplier)

        # String * Integer or Integer * String => String repetition
        elif isinstance(current_value, str) and isinstance(multiplier, int):
            if multiplier < 0:
                raise GrinRuntimeError("Negative multiplication of a string is not allowed")
            result = current_value * multiplier
        elif isinstance(current_value, int) and isinstance(multiplier, str):
            if current_value < 0:
                raise GrinRuntimeError("Negative multiplication of a string is not allowed")
            result = multiplier * current_value

        # Raise error for unsupported types
        else:
            raise GrinRuntimeError("Unsupported types for MULT operation")

        interpreter.variables[self.variable] = result



class DivStatement(Statement):
    def __init__(self, variable, value, label=None):
        super().__init__(label)
        self.variable = variable
        self.value = value

    def execute(self, interpreter):
        current_value = interpreter.variables.get(self.variable, 0)
        divisor = interpreter.evaluate_value(self.value)
        if not isinstance(current_value, (int, float)) or not isinstance(divisor, (int, float)):
            raise GrinRuntimeError(
                "Unsupported operand types for DIV statement; operands must be int or float")
        # Check for division by zero
        if divisor == 0:
            raise GrinRuntimeError("Division by zero")

        # Integer division with floor adjustment for mixed signs
        if isinstance(current_value, int) and isinstance(divisor, int) or current_value == int(current_value) and divisor == int(divisor):
            if current_value * divisor < 0:
                result = int(math.floor(current_value / divisor))  # Apply floor division for mixed signs
            else:
                result = int(current_value // divisor) # Standard integer division for same-sign integers
        elif isinstance(current_value, (int, float)) and isinstance(divisor, (int, float)):
            # Float division if either operand is a float
            result = current_value / divisor
        else:
            raise GrinRuntimeError("Unsupported operand types for DIV statement")

        interpreter.variables[self.variable] = result
