from grin.exception import *

class Statement:
    """Base class for all statements."""
    def __init__(self, label=None):
        self.label = label

    def execute(self, interpreter):
        raise NotImplementedError("Subclasses should implement this method.")

class LetStatement(Statement):
    """Assigns a value to a variable."""
    def __init__(self, variable, value, label=None):
        super().__init__(label)
        # Validate that the variable is a valid string identifier
        if not isinstance(variable, str) or not variable.isidentifier():
            raise GrinRuntimeError(
                f"Variable name '{variable}' is invalid. "
                f"Variables must be strings (valid identifiers, starting with a letter or underscore)."
            )
        self.variable = variable
        self.value = value

    def execute(self, interpreter):
        # Evaluate the new value and assign it to the variable in the interpreter’s context.
        value = interpreter.evaluate_value(self.value)
        interpreter.variables[self.variable] = value
class PrintStatement(Statement):
    """Prints the value of the given variable or literal."""
    def __init__(self, variable, label=None):
        super().__init__(label)
        self.variable = variable

    def execute(self, interpreter):
        value = interpreter.evaluate_value(self.variable)

        print(value)

class InnumStatement(Statement):
    def __init__(self, variable, label=None):
        super().__init__(label)
        self.variable = variable

    def execute(self, interpreter):
        try:
            user_input = input().strip()
            value = float(user_input)
            interpreter.variables[self.variable] = int(value) if value.is_integer() else value
        except ValueError:
            raise GrinRuntimeError(f"Invalid input for INNUM: '{user_input}' must be a number.")

class InstrStatement(Statement):
    def __init__(self, variable, label=None):
        super().__init__(label)
        self.variable = variable

    def execute(self, interpreter):
        interpreter.variables[self.variable] = input().strip()

