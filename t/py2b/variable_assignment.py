import unittest
from p2bf.builder import BFBuild
from p2bf.emitter import Emitter
import StringIO
from util.run_bf import run

class TestVariableAssignment(unittest.TestCase):
    def test_single_assignment(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """v1 = "a" """
        builder = BFBuild(python, emit=emitter).emit_bf()

        print emit_output.getvalue()
        run(emit_output.getvalue(), stdout=run_output)

    def test_multi_assignment(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """v3 = v2 = v1 = "a" """
        builder = BFBuild(python, emit=emitter).emit_bf()

        print emit_output.getvalue()
        run(emit_output.getvalue(), stdout=run_output)

    def test_variable_to_variable(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """v1 = "a"\nv2 = v1 """
        builder = BFBuild(python, emit=emitter).emit_bf()

        print emit_output.getvalue()
        run(emit_output.getvalue(), stdout=run_output)

