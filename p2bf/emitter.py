import sys

class Emitter(object):
    verbose = False

    def __init__(self, verbose=False):
        self.verbose = verbose

    def subtract(self, message=None):
        sys.stdout.write("-")
        self.debug(message)

    def add(self, message=None):
        sys.stdout.write("+")
        self.debug(message)

    def move_index_right(self, message=None):
        sys.stdout.write(">")
        self.debug(message)

    def move_index_left(self, message=None):
        sys.stdout.write("<")
        self.debug(message)

    def move_index_left_by(self, count, message=None):
        for i in range(count):
            self.move_index_left()
        self.debug(message)

    def move_index_right_by(self, count, message=None):
        for i in range(count):
            self.move_index_right()
        self.debug(message)

    def debug(self, message=None):
        if message and self.verbose:
            print(" %s" % message)

    def print_current_index(self, message=None):
        sys.stdout.write(".")
        self.debug(message)

    def start_loop(self, message=None):
        sys.stdout.write("[")
        self.debug(message)

    def end_loop(self, message=None):
        sys.stdout.write("]")
        self.debug(message)

