import unittest
from util.run_bf import run

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


