all:
	antlr4 -Dlanguage=Python3 -visitor SystemVerilogLexer.g4
	antlr4 -Dlanguage=Python3 -visitor SystemVerilogParser.g4

clean:
	rm -f *.pyc
	rm -f *.tokens
	rm -f *.interp
	rm -f SystemVerilog*.py
	rm -f *.class