import unittest
from p2bf.builder import BFBuild
from p2bf.emitter import Emitter
import StringIO
from util.run_bf import run

class TestOperators(unittest.TestCase):
    def test_equality_true_false(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = True == True\nprint foo"""
        builder = BFBuild(python, emit=emitter).emit_bf()
        memory_space = []
        run(emit_output.getvalue(), stdout=run_output, memory=memory_space)
        self.assertEquals(1, ord(run_output.getvalue()[0]))

        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = True == False\nprint foo"""
        builder = BFBuild(python, emit=emitter).emit_bf()
        memory_space = []
        run(emit_output.getvalue(), stdout=run_output, memory=memory_space)
        self.assertEquals(0, ord(run_output.getvalue()[0]))

    def test_equality_statics(self):
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = "a" == "a"\nprint foo"""
        builder = BFBuild(python, emit=emitter).emit_bf()
        memory_space = []
        run(emit_output.getvalue(), stdout=run_output, memory=memory_space)
        self.assertEquals(1, ord(run_output.getvalue()[0]))

        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """foo = "a" == "b"\nprint foo"""
        builder = BFBuild(python, emit=emitter).emit_bf()
        memory_space = []
        run(emit_output.getvalue(), stdout=run_output, memory=memory_space)
        self.assertEquals(0, ord(run_output.getvalue()[0]))



    def test_equality_in_if(self):
        return
        emit_output = StringIO.StringIO()
        run_output = StringIO.StringIO()
        emitter = Emitter(stdout=emit_output)
        python = """if True == True:\n    print "OK" """
        builder = BFBuild(python, emit=emitter).emit_bf()
        run(emit_output.getvalue(), stdout=run_output)
