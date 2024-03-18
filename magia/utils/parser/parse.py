from typing import Literal

from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import Tree

from .SystemVerilogLexer import SystemVerilogLexer
from .SystemVerilogParser import SystemVerilogParser
from .SystemVerilogParserVisitor import SystemVerilogParserVisitor


def parse_sv_code(
        sv_code: str,
        parse_as: Literal["source_text", "concurrent_assertion_item"] = "source_text",
        **kwargs
) -> Tree:
    """
    Parse the given SystemVerilog code and return the AST.
    The parse_as argument can be used to specify the statement type to parse,
    which developer can avoid parsing the whole file just for a specific statement.
    """

    lexer = InputStream(sv_code)
    lexer_grammar = SystemVerilogLexer(lexer)
    stream = CommonTokenStream(lexer_grammar)
    parser = SystemVerilogParser(stream)
    return {
        "source_text": parser.source_text,
        "concurrent_assertion_item": parser.concurrent_assertion_item,
    }[parse_as]()


# ruff: noqa: N802
def flatten_expression(node: Tree) -> str:
    """
    Return a flattened string representation of the given parse tree node.
    """

    class FlattenStatement(SystemVerilogParserVisitor):
        def defaultResult(self) -> str:
            return ""

        def aggregateResult(self, aggregate: str, next_result):
            if next_result and next_result != " ":
                return f"{aggregate} {next_result}".strip()
            return aggregate

        def visitTerminal(self, node):
            return node.getText()

    return FlattenStatement().visit(node)
