
from grin.control_flow_statement import *


class Interpreter:
    def __init__(self, program):
        self.program = program
        self.variables = {}
        self.current_line = 0
        self.gosub_stack = []
        self.line_execution_count = {}
        self.label_map = self._build_label_map()  # Map labels to line indices for faster lookup

    def _build_label_map(self):
        label_map = {}
        for index, statement in enumerate(self.program):
            if statement.label:  # Check for label directly
                label_map[statement.label] = index
        return label_map

    def run(self):
        while self.current_line < len(self.program):
            statement = self.program[self.current_line]
            self._track_execution(statement)

            # Execute the current statement, allowing it to change `self.current_line` if needed
            statement.execute(self)

            # Only move to the next line if no jump occurred in `execute`
            if not hasattr(statement, 'jump_executed') or not statement.jump_executed:
                self.current_line += 1
            else:
                # Reset the jump flag if it was set
                statement.jump_executed = False


    def _track_execution(self, statement):
            if self.current_line not in self.line_execution_count:
                self.line_execution_count[self.current_line] = 0
            self.line_execution_count[self.current_line] += 1
            if self.line_execution_count[self.current_line] > 1000:
                raise GrinRuntimeError("Infinite loop detected")

    def jump_to(self, target):
        try:
            line_offset = int(target)
            self._jump_to_line(line_offset)
        except ValueError:
            if isinstance(target, str):
                if target.startswith('"') and target.endswith('"'):
                    self._jump_to_label(target.strip('"'))
                elif target in self.variables:
                    variable_value = self.variables[target]
                    if isinstance(variable_value, int):
                        self._jump_to_line(variable_value)
                    elif isinstance(variable_value, str):
                        self._jump_to_label(variable_value.strip('"'))
                    else:
                        raise GrinRuntimeError(
                            f"GOTO target variable '{target}' must resolve to an integer or label"
                        )
                else:
                    raise GrinRuntimeError(f"GOTO target variable '{target}' is undefined")
            else:
                raise GrinRuntimeError("GOTO target must be an integer, label, or valid variable")

    def _jump_to_line(self, offset):
        target_line = self.current_line + offset
        if target_line == len(self.program):  # Allow jump to terminate
            self.current_line = len(self.program)
            return
        if not (0 <= target_line < len(self.program)):
            raise GrinRuntimeError(f"Line number out of bounds: {target_line}")
        self.current_line = target_line - 1  # Adjust for 0-based indexing

    def _jump_to_label(self, label):
        if label not in self.label_map:
            raise GrinRuntimeError(f"Label '{label}' not found")
        self.current_line = self.label_map[label] - 1  # Adjust for 0-based indexing

    def _resolve_variable_target(self, variable):
        if variable not in self.variables:
            raise GrinRuntimeError(f"Variable '{variable}' is undefined")
        target_value = self.variables[variable]
        if isinstance(target_value, int):
            self._jump_to_line(target_value)
        elif isinstance(target_value, str):
            self._jump_to_label(target_value.strip('"'))
        else:
            raise GrinRuntimeError(f"Variable '{variable}' must resolve to an integer or a label")


    def evaluate_value(self, value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                pass
            if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")):
                return value[1:-1]
            # If the variable is not found in self.variables, default to 0
            return self.variables.get(value, 0)
        else:
            raise GrinRuntimeError("Unsupported value type")

