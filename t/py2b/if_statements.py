import unittest
from p2bf.builder import BFBuild
from p2bf.emitter import Emitter
import StringIO
from util.run_bf import run

class TestIfStatements(unittest.TestCase):
    def test_if_true(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """if True:\n    print "OK" """
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
        self.assertEqual(run_output.getvalue(), "OK\n")

    def test_if_false(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """if False:\n    print "BAD" """
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
        self.assertEqual(run_output.getvalue(), "")

    def test_other_var_true(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = 'A'\nif foo:\n    print "OK" """
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
        self.assertEqual(run_output.getvalue(), "OK\n")

    def test_plain_string_true(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """if 'A':\n    print "OK" """
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
        self.assertEqual(run_output.getvalue(), "OK\n")

