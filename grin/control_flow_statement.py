from grin.statement import Statement
from grin.exception import GrinRuntimeError

class GotoStatement(Statement):
    def __init__(self, target, condition=None, label=None):
        super().__init__(label)
        self.target = target
        self.condition = condition

    def execute(self, interpreter):
        if self.condition is None or self.evaluate_condition(interpreter):
            interpreter.jump_to(self.target)

    def evaluate_condition(self, interpreter):
        if not self.condition or len(self.condition) != 3:
            raise GrinRuntimeError("Invalid or missing condition for GOTO")

        left_value = interpreter.evaluate_value(self.condition[0].text())
        operator = self.condition[1].text()
        right_value = interpreter.evaluate_value(self.condition[2].text())

        # Ensure the types are compatible before comparing
        if isinstance(left_value, (int, float)) and isinstance(right_value, str):
            raise GrinRuntimeError(f"Cannot compare number with string: {left_value} and {right_value}")
        if isinstance(left_value, str) and isinstance(right_value, (int, float)):
            raise GrinRuntimeError(f"Cannot compare string with number: {left_value} and {right_value}")

        # Comparison logic
        if operator == "<":
            return left_value < right_value
        elif operator == "<=":
            return left_value <= right_value
        elif operator == ">":
            return left_value > right_value
        elif operator == ">=":
            return left_value >= right_value
        elif operator == "=":
            return left_value == right_value
        elif operator == "<>":
            return left_value != right_value
        else:
            raise GrinRuntimeError(f"Invalid comparison operator '{operator}'")


class GosubStatement(GotoStatement):
    def execute(self, interpreter):
        # Push the return address (next line) onto the stack
        interpreter.gosub_stack.append(interpreter.current_line + 1)
        # Use the GotoStatement logic to perform the jump
        super().execute(interpreter)


class ReturnStatement(Statement):
    def __init__(self, label = None):
        super().__init__(label)

    def execute(self, interpreter):
        # Check if the gosub_stack is empty
        if not interpreter.gosub_stack:
            raise GrinRuntimeError("RETURN statement without matching GOSUB")

        # If there is a matching GOSUB, pop from the stack
        interpreter.current_line = interpreter.gosub_stack.pop() - 1  # Adjust to continue correctly


class EndStatement(Statement):
    def __init__(self, label=None):
        super().__init__(label)

    def execute(self, interpreter):
        interpreter.current_line = len(interpreter.program)  # Set current_line to end of program



class DotStatement(Statement):
    def __init__(self, label=None):
        super().__init__(label)

    def execute(self, interpreter):
        interpreter.current_line = len(interpreter.program)
