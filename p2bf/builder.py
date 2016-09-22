import re
import ast
from p2bf.emitter import Emitter
from p2bf.variable_map import VariableMap


class BFBuild(object):
    byte_var_table = {}
    current_var_index = 0
    python = ""

    def __init__(self, python, verbose=False, emit=None):
        self.python = python
        self.vmap = VariableMap()
        if emit:
            self.emit = emit
        else:
            self.emit = Emitter(verbose=verbose)

    def error_on_node(self, node, error):
        raise Exception("Error on line %s: %s" % (node.lineno, error))

    def process_print_node(self, print_node):
        if print_node.dest:
            self.error_on_node(node, "Don't know how to do print destinations")

        values = print_node.values
        for value in values:
            if isinstance(value, ast.Str):
                self.emit_print_string(value.s)
            elif isinstance(value, ast.Name):
                if not isinstance(value.ctx, ast.Load):
                    self.error_on_node(node, "Don't know what this variable"
                                             "context is")

                self.emit_print_variable(value.id)
        if print_node.nl:
            self.emit_print_string("\n")

    def process_string_assignment(self, target, value, value_node):
        if len(value) > 1:
            self.error_on_node(value_node,
                               "Can only set single chars right now")

        v_index = self.vmap.get_or_create_variable_index(target)

        self.emit_move_to_var_index(v_index)
        self.emit_zero_current_index()
        self.emit_set_current_index_value(ord(value))

    def process_assignment_node(self, assignment_node):
        targets = assignment_node.targets
        value = assignment_node.value

        for target in targets:
            if not isinstance(target, ast.Name):
                self.error_on_node(target, "Unknown syntax :(")

            if isinstance(value, ast.Str):
                self.process_string_assignment(target.id, value.s, value)
            elif isinstance(value, ast.Name):
                self.process_variable_to_variable(target.id, value.id, value)
            else:
                self.error_on_node(value, "Unable to set value type")

    def process_variable_to_variable(self, target, source, source_node):
        source_index = self.vmap.get_variable_index(source)
        target_index = self.vmap.get_or_create_variable_index(target)

        # Clear out our scratch space.
        self.emit_move_to_var_index(0)
        self.emit_zero_current_index()

        # Clear out the destination space
        self.emit_move_to_var_index(target_index)
        self.emit_zero_current_index()

        # While there's a value at the source, subtract one, and add one to
        # the scratch space and target
        self.emit_move_to_var_index(source_index)
        self.emit.start_loop("Start copying the value into the "
                             "scratch and destination")

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

    def emit_print_variable(self, variable_name):
        v_index = self.vmap.get_variable_index(variable_name)
        self.emit_move_to_var_index(v_index)
        self.emit.print_current_index()

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
            self.emit.move_index_right_by(index - self.current_var_index,
                                          "Move to variable index %s" % index)

        elif index < self.current_var_index:
            self.emit.move_index_left_by(self.current_var_index - index,
                                         "Move to variable index %s" % index)
        else:
            self.emit.debug("noop: Already at variable index %s" % index)
        self.current_var_index = index

    def emit_bf(self):
        top_node = ast.parse(self.python)
        for node in ast.iter_child_nodes(top_node):
            if isinstance(node, ast.Assign):
                self.process_assignment_node(node)
            elif isinstance(node, ast.Print):
                self.process_print_node(node)
            else:
                self.error_on_node(node, "Syntax not supported yet :(")
