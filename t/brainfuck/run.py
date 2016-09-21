import unittest
from util.run_bf import run
import StringIO


class TestBrainFuckRunner(unittest.TestCase):
    def test_memory(self):
        memory_space = []
        run("", memory=memory_space)
        self.assertEqual(memory_space[0], 0)

        memory_space = []
        run("++", memory=memory_space)
        self.assertEqual(memory_space[0], 2)

        memory_space = []
        run("++-", memory=memory_space)
        self.assertEqual(memory_space[0], 1)

    def test_pointer(self):
        memory_space = []
        run(">-", memory=memory_space)
        self.assertEqual(memory_space[0], 0)
        self.assertEqual(memory_space[1], -1)

        memory_space = []
        run(">>>+", memory=memory_space)
        self.assertEqual(memory_space[0], 0)
        self.assertEqual(memory_space[1], 0)
        self.assertEqual(memory_space[2], 0)
        self.assertEqual(memory_space[3], 1)

        memory_space = []
        run(">>><<+", memory=memory_space)
        self.assertEqual(memory_space[0], 0)
        self.assertEqual(memory_space[1], 1)
        self.assertEqual(memory_space[2], 0)
        self.assertEqual(memory_space[3], 0)

    def test_loop(self):
        memory_space = []
        run("+++[->+<]", memory=memory_space)
        self.assertEqual(memory_space[0], 0)
        self.assertEqual(memory_space[1], 3)

        memory_space = []
        run(">++>+>+++>++[[-]<]", memory=memory_space)
        self.assertEqual(memory_space[0], 0)
        self.assertEqual(memory_space[1], 0)
        self.assertEqual(memory_space[2], 0)
        self.assertEqual(memory_space[3], 0)
        self.assertEqual(memory_space[4], 0)

    def test_skipped_loop(self):
        memory_space = []
        run("[+++[]++++]>+", memory=memory_space)
        self.assertEquals(memory_space[0], 0)
        self.assertEquals(memory_space[1], 1)

    def test_print(self):
        # Hello world from https://en.wikipedia.org/wiki/Brainfuck
        output = StringIO.StringIO()
        run("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>"
            "++.<<+++++++++++++++.>.+++.------.--------.>+.>.", stdout=output)
        self.assertEquals(output.getvalue(), "Hello World!\n")

    def test_read_input(self):
        class Input(object):
            index = -1
            def get_input(self):
                self.index += 1
                return "Hello"[self.index]

        memory_space = []
        run(",>,>,>,>,", input_reader=Input(), memory=memory_space)
        self.assertEqual(chr(memory_space[0]), "H")
        self.assertEqual(chr(memory_space[1]), "e")
        self.assertEqual(chr(memory_space[2]), "l")
        self.assertEqual(chr(memory_space[3]), "l")
        self.assertEqual(chr(memory_space[4]), "o")
