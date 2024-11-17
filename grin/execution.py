from grin.lexing import GrinLexError
from grin.parsing import parse, GrinParseError
from grin.token import GrinTokenKind
from grin.control_flow_statement import GotoStatement, GosubStatement, ReturnStatement, EndStatement, DotStatement
from grin.arithmetic_statement import AddStatement, SubStatement, MultStatement, DivStatement
from grin.statement import LetStatement, PrintStatement, InnumStatement, InstrStatement

def lex_and_parse(lines):
    """
    Lex and parse the given lines of Grin program code.
    Returns a sequence of lists of GrinTokens corresponding to valid statements.
    """
    try:
        return list(parse(lines))  # Uses `parse` from `parsing.py`
    except GrinLexError as lex_err:
        print(f"Lexical Error: {lex_err}")
        exit(1)
    except GrinParseError as parse_err:
        print(f"Parse Error: {parse_err}")
        exit(1)

def tokens_to_statements(tokenized_lines):
    """
    Convert tokenized lines into statement objects.
    """
    statements = []
    for tokens in tokenized_lines:
        # Check if the first token is a label
        label = None
        if len(tokens) > 1 and tokens[0].kind() == GrinTokenKind.IDENTIFIER and tokens[1].kind() == GrinTokenKind.COLON:
            label = tokens[0].text()
            tokens = tokens[2:]  # Skip the label and colon

        # The first remaining token's kind determines the statement type
        if not tokens:
            continue  # Skip empty token lists after label

        if tokens[0].kind() == GrinTokenKind.LET:
            statements.append(LetStatement(tokens[1].text(), tokens[2].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.PRINT:
            statements.append(PrintStatement(tokens[1].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.INNUM:
            statements.append(InnumStatement(tokens[1].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.INSTR:
            statements.append(InstrStatement(tokens[1].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.ADD:
            statements.append(AddStatement(tokens[1].text(), tokens[2].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.SUB:
            statements.append(SubStatement(tokens[1].text(), tokens[2].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.MULT:
            statements.append(MultStatement(tokens[1].text(), tokens[2].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.DIV:
            statements.append(DivStatement(tokens[1].text(), tokens[2].text(), label=label))
        elif tokens[0].kind() == GrinTokenKind.GOTO or tokens[0].kind() == GrinTokenKind.GOSUB:
            target = tokens[1].text()
            condition = None

            # Check for the optional IF condition
            if len(tokens) > 2 and tokens[2].kind() == GrinTokenKind.IF:
                condition = tokens[3:]  # Capture the condition tokens (value, operator, value)

            if tokens[0].kind() == GrinTokenKind.GOTO:
                statements.append(GotoStatement(target, condition, label=label))
            else:
                statements.append(GosubStatement(target, condition, label=label))
        elif tokens[0].kind() == GrinTokenKind.RETURN:
            statements.append(ReturnStatement(label=label))
        elif tokens[0].kind() == GrinTokenKind.END:
            statements.append(EndStatement(label=label))
        elif tokens[0].kind() == GrinTokenKind.DOT:
            statements.append(DotStatement(label=label))
        else:
            raise ValueError(f"Unsupported statement: {tokens[0].kind()}")
    return statements


def load_program_from_stdin():
    """Reads lines from standard input until the end-of-program marker."""
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
            if line.strip() == ".":
                break
        except EOFError:
            break  # Stop on EOF if reached without a dot
    return lines