import src.parser as parser
import src.linter as linter

# Test block chunking
blocks = parser.chunk("main.cider")
linter.lint(blocks)
