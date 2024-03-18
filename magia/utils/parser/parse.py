from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import Tree

from .SystemVerilogLexer import SystemVerilogLexer
from .SystemVerilogParser import SystemVerilogParser


def parse_sv_code(sv_code: str, **kwargs) -> Tree:
    lexer = InputStream(sv_code)
    lexer_grammar = SystemVerilogLexer(lexer)
    stream = CommonTokenStream(lexer_grammar)
    parser = SystemVerilogParser(stream)
    return parser.source_text()
