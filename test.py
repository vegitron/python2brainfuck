import unittest
import sys
import os

test_path = "%s/t/" % os.path.dirname(os.path.abspath(__file__))
sys.path.append(test_path)


from brainfuck.run import TestBrainFuckRunner

unittest.main()
