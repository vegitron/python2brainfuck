import unittest
from p2bf.builder import BFBuild
from p2bf.emitter import Emitter
import StringIO
from util.run_bf import run

class TestPyPrint(unittest.TestCase):

    def test_single_static_output(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """print "Hello" """
        builder = BFBuild(python, emit=emitter).emit_bf()

        run(emit_output.getvalue(), stdout=run_output)

        self.assertEqual(run_output.getvalue(), "Hello\n")

    def test_multi_static_output(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """print "Hello", " ", "World" """
        builder = BFBuild(python, emit=emitter).emit_bf()

        run(emit_output.getvalue(), stdout=run_output)

        self.assertEqual(run_output.getvalue(), "Hello World\n")

