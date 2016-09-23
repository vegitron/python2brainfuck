import unittest
from p2bf.builder import BFBuild
from p2bf.emitter import Emitter
import StringIO
from util.run_bf import run

class TestOperators(unittest.TestCase):
    def test_equality(self):
        return
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = True == True"""
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
