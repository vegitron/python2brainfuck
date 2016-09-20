import re
from p2bf.emitter import Emitter
from p2bf.variable_map import VariableMap

class BFBuild(object):
    byte_var_table = {}
    current_var_index = 0
    python = ""

    def __init__(self, python, verbose=False):
        self.python = python
        self.vmap = VariableMap()
        self.emit = Emitter(verbose=verbose)

    def process_line(self, line):
        if not re.match("[^ ]", line):
            return
        matches = re.match("print '(.*)'", line)

        if matches:
            self.process_print_static_string(line)
            return

        matches = re.match("print (.+)", line)
        if matches:
            self.process_print_variable(line)
            return

        matches = re.match("([^ ]+)[ ]*=[ ]*'(.)'", line)
        if matches:
            self.process_set_char_variable(line)
            return

        matches = re.match("([^ ]+)[ ]*=[ ]*([^ ]+)", line)
        if matches:
            self.process_set_variable_to_variable(line)
            return

        self.emit.debug("Unparsed line: %s" % line)
        raise Exception("I only know a little bit of python: print '<string literal>', <variable_name> = '<one char>', print <variable_name>.  Sorry!")

    def process_print_variable(self, line):
        matches = re.match("print (.*)", line)

        variable_name = matches.group(1)

        v_index = self.vmap.get_variable_index(variable_name)

        self.emit_move_to_var_index(v_index)
        self.emit.print_current_index()
        self.emit_print_string("\n")

    def process_set_variable_to_variable(self, line):
        matches = re.match("([^ ]+)[ ]*=[ ]*([^ ]+)", line)
        var_target = matches.group(1)
        var_source = matches.group(2)

        source_index = self.vmap.get_variable_index(var_source)
        target_index = self.vmap.get_or_create_variable_index(var_target)

        # Clear out our scratch space.
        self.emit_move_to_var_index(0)
        self.emit_zero_current_index()

        # Clear out the destination space
        self.emit_move_to_var_index(target_index)
        self.emit_zero_current_index()

        # While there's a value at the source, subtract one, and add one to
        # the scratch space and target
        self.emit_move_to_var_index(source_index)
        self.emit.start_loop("Start copying the value into the scratch and destination")

        self.emit.subtract()
        self.emit_move_to_var_index(0)
        self.emit.add()
        self.emit_move_to_var_index(target_index)
        self.emit.add()
        self.emit_move_to_var_index(source_index)
        self.emit.end_loop()

        # While there's a value in the scratch space, subtract one, and add
        # one at the source to restore its value
        self.emit_move_to_var_index(0)
        self.emit.start_loop("Restore the value to the source index")
        self.emit.subtract()
        self.emit_move_to_var_index(source_index)
        self.emit.add()
        self.emit_move_to_var_index(0)
        self.emit.end_loop()

    def process_set_char_variable(self, line):
        matches = re.match("([^ ]+)[ ]*=[ ]*'(.)", line)
        value = matches.group(1)

        variable_name = matches.group(1)
        variable_value = matches.group(2)

        v_index = self.vmap.get_or_create_variable_index(variable_name)

        self.emit_move_to_var_index(v_index)
        self.emit_zero_current_index()
        self.emit_set_current_index_value(ord(variable_value))


    def process_print_static_string(self, line):
        matches = re.match("print '(.*)'", line)
        value = matches.group(1)
        self.emit_print_string(value)
        self.emit_print_string("\n")


    def emit_print_string(self, value):
        self.emit_move_to_var_index(0)

        for char in value:
            next_ord = ord(char)
            self.emit_zero_current_index()
            self.emit_set_current_index_value(next_ord)
            self.emit.print_current_index()

    def emit_zero_current_index(self):
        self.emit.start_loop()
        self.emit.subtract()
        self.emit.end_loop("Set the current index to 0")

    def emit_set_current_index_value(self, value):
        for i in range(value):
            self.emit.add()
        self.emit.debug("Setting value to %s" % value)

    def emit_move_to_var_index(self, index):
        if index > self.current_var_index:
            self.emit.move_index_right_by(index - self.current_var_index, "Move to variable index %s" % index)

        elif index < self.current_var_index:
            self.emit.move_index_left_by(self.current_var_index - index, "Move to variable index %s" % index)
        else:
            self.emit.debug("noop: Already at variable index %s" % index)
        self.current_var_index = index

    def emit_bf(self):
        for line in self.python.split("\n"):
            self.process_line(line)


