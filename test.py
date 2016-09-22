import unittest
import sys
import os

test_path = "%s/t/" % os.path.dirname(os.path.abspath(__file__))
sys.path.append(test_path)


from brainfuck.run import TestBrainFuckRunner
from py2b.print_statement import TestPyPrint
from py2b.variable_assignment import TestVariableAssignment
from py2b.if_statements import TestIfStatements

unittest.main()
