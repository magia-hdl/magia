from typing import Literal

from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import Tree

from .SystemVerilogLexer import SystemVerilogLexer
from .SystemVerilogParser import SystemVerilogParser


def parse_sv_code(
        sv_code: str,
        parse_as: Literal["source_text", "concurrent_assertion_item"] = "source_text",
        **kwargs
) -> Tree:
    lexer = InputStream(sv_code)
    lexer_grammar = SystemVerilogLexer(lexer)
    stream = CommonTokenStream(lexer_grammar)
    parser = SystemVerilogParser(stream)
    return {
        "source_text": parser.source_text,
        "concurrent_assertion_item": parser.concurrent_assertion_item,
    }[parse_as]()
