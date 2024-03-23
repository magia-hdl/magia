from pathlib import Path

from magia.utils.parser import SystemVerilogParser, SystemVerilogParserVisitor, flatten_expression, parse_sv_code


def test_smoke():
    """
    Smoke test on the SystemVerilog parser.
    """
    with open(Path(__file__).parent / "test_code.sv") as f:
        sv_code = f.read()
    tree = parse_sv_code(sv_code)
    assert tree is not None


def test_parse_sva():
    """
    Test parsing a SystemVerilog SVA statement.

    The SVA parser must be able to extract:
    - The assertion name.
    - The assertion type (Assert / Assume / Cover).
    - The clocking event.
    - The disable iff expression.
    - The assertion property.
    """
    statement = "a1: assert property (@(posedge clk) disable iff (rst_n) (a |-> b));"
    tree = parse_sv_code(statement, parse_as="concurrent_assertion_item")

    class TreeVerifier(SystemVerilogParserVisitor):
        def visitConcurrent_assertion_item(self, ctx):  # noqa: N802
            assert ctx.identifier().getText() == "a1", "Except an assertion named as 'a1'."
            return self.visitChildren(ctx)

        def visitConcurrent_assertion_statement(  # noqa: N802
                self,
                ctx: SystemVerilogParser.Concurrent_assertion_statementContext
        ):
            assert ctx.getChild(0) == ctx.KW_ASSERT(), "Expect an 'assert' keyword at the beginning of the statement."
            return self.visitChildren(ctx)

        def visitProperty_spec(self, ctx: SystemVerilogParser.Property_specContext):  # noqa: N802
            assert flatten_expression(ctx.clocking_event()) == "@ ( posedge clk )", "Expect a clocking event."
            assert ctx.getToken(SystemVerilogParser.KW_DISABLE, 0) is not None, "Expect a 'disable' keyword."
            assert ctx.getToken(SystemVerilogParser.KW_IFF, 0) is not None, "Expect a 'iff' keyword."
            assert flatten_expression(ctx.expression_or_dist()) == "rst_n", "Expect a disable iff expression."
            assert flatten_expression(ctx.property_expr()) == "( a |-> b )", "Property statement mismatch."
            return True

    TreeVerifier().visit(tree)
