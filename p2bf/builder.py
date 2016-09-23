import re
import ast
from p2bf.emitter import Emitter
from p2bf.variable_map import VariableMap
import p2bf.constants as constants


class BFBuild(object):
    temp_vars = {}
    free_temp_vars = []
    byte_var_table = {}
    current_var_index = 0
    python = ""
    if_depth = 0

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

    def current_if_var(self):
        return "___if_%s" % self.if_depth

    def current_else_var(self):
        return "___else_%s" % self.if_depth

    def process_if_node(self, node):
        test = node.test

        current_if_var = self.current_if_var()
        current_else_var = self.current_else_var()

        self.if_depth += 1
        if_index = self.vmap.get_variable_index(current_if_var)
        else_index = self.vmap.get_variable_index(current_else_var)

        self.emit.debug("At if depth %s" % (self.if_depth-1))
        self.emit_move_to_var_index(if_index)
        self.emit_zero_current_index()
        self.emit_move_to_var_index(else_index)
        self.emit_zero_current_index()
        self.emit.add("Set the else to true by default")

        self._process_assignment_to_variable(current_if_var, test)

        self.emit_move_to_var_index(if_index)
        self.emit.start_loop("If the value at index %s is true:" % if_index)
        # If true value, zero out the if index to make sure we don't keep
        # looping, and zero out the else index so the else doesn't run.
        self.emit_zero_current_index()
        self.emit_move_to_var_index(else_index)
        self.emit_zero_current_index()

        for if_body_node in node.body:
            self.process_node(if_body_node)

        self.emit_move_to_var_index(if_index)
        self.emit.end_loop()

        self.emit_move_to_var_index(else_index)
        self.emit.start_loop("Else")
        self.emit_zero_current_index()
        orelse_len = len(node.orelse)
        if orelse_len:
            else_node = node.orelse[0]
            if orelse_len == 1 and isinstance(else_node, ast.If):
                self.process_if_node(else_node)
            else:
                for else_node in node.orelse:
                    self.process_node(else_node)
        self.emit_move_to_var_index(else_index)
        self.emit.end_loop()
        self.if_depth -= 1

    def get_temp_target_var(self):
        if len(self.free_temp_vars):
            return self.free_temp_vars.pop()
        current_count = len(self.temp_vars)
        var_id = '___tmp_var_%s' % current_count
        self.temp_vars[var_id] = True
        self.vmap.get_or_create_variable_index(var_id)
        return var_id

    def free_temp_target_var(self, variable):
        self.free_temp_vars.append(variable)

    def process_compare(self, target, node):

        if len(node.ops) > 1:
            self.error_on_node(node,
                               "Don't know how to do multiple comparisons")
        if isinstance(node.ops[0], ast.Eq):
            left_var = self.get_temp_target_var()
            comp_var = self.get_temp_target_var()
            self._process_assignment_to_variable(left_var, node.left)
            self._process_assignment_to_variable(comp_var, node.comparators[0])

            target_index = self.vmap.get_variable_index(target)
            left_index = self.vmap.get_variable_index(left_var)
            comp_index = self.vmap.get_variable_index(comp_var)
            # If we subtract one from each temp var until the first one is
            # empty, if the second temp var is empty then they're equal.

            # We set the target to true initially, so it can fail in a loop on
            # the second variable
            self.emit_move_to_var_index(target_index)
            self.emit_zero_current_index()
            self.emit.add()

            self.emit_move_to_var_index(left_index)
            self.emit.start_loop("Emptying tmp left and comp variables")
            self.emit.subtract()
            self.emit_move_to_var_index(comp_index)
            self.emit.subtract()
            self.emit_move_to_var_index(left_index)
            self.emit.end_loop()

            self.emit_move_to_var_index(comp_index)
            self.emit.start_loop("If there's a value here, the values aren't "
                                 "equal!")
            self.emit_zero_current_index()
            self.emit_move_to_var_index(target_index)
            self.emit_zero_current_index()
            self.emit_move_to_var_index(comp_index)
            self.emit.end_loop()
            self.free_temp_target_var(left_var)
            self.free_temp_target_var(comp_var)
        else:
            self.error_on_node(node, "Unknown comparison: %s" % node.ops[0])

    def _process_assignment_to_variable(self, target, node):
            if isinstance(node, ast.Str):
                self.process_string_assignment(target, node.s, node)
            elif isinstance(node, ast.Name):
                self.process_variable_to_variable(target, node.id, node)
            elif isinstance(node, ast.Compare):
                compare_target = self.get_temp_target_var()
                self.process_compare(compare_target, node)
                self.process_variable_to_variable(target,
                                                  compare_target,
                                                  node)
                self.free_temp_target_var(compare_target)

            else:
                print ast.dump(assignment_node)
                self.error_on_node(node, "Unable to set value type")

    def process_assignment_node(self, assignment_node):
        targets = assignment_node.targets
        value = assignment_node.value

        for target in targets:
            if not isinstance(target, ast.Name):
                self.error_on_node(target, "Unknown syntax :(")

            self._process_assignment_to_variable(target.id, value)

    def process_variable_to_variable(self, target, source, source_node):
        source_index = self.vmap.get_variable_index(source)
        target_index = self.vmap.get_or_create_variable_index(target)

        self.emit.debug("Copying value from %s to %s" % (source_index,
                                                         target_index))
        # Clear out our scratch space.
        self.emit_move_to_var_index(self.get_scratch_index())
        self.emit_zero_current_index()

        # Clear out the destination space
        self.emit_move_to_var_index(target_index)
        self.emit_zero_current_index()

        # While there's a value at the source, subtract one, and add one to
        # the scratch space and target
        self.emit_move_to_var_index(source_index)
        self.emit.start_loop("Start copying the value into the "
                             "scratch %s and destination %s")

        self.emit.subtract()
        self.emit_move_to_var_index(self.get_scratch_index())
        self.emit.add()
        self.emit_move_to_var_index(target_index)
        self.emit.add()
        self.emit_move_to_var_index(source_index)
        self.emit.end_loop()

        # While there's a value in the scratch space, subtract one, and add
        # one at the source to restore its value
        self.emit_move_to_var_index(self.get_scratch_index())
        self.emit.start_loop("Restore the value to the source index")
        self.emit.subtract()
        self.emit_move_to_var_index(source_index)
        self.emit.add()
        self.emit_move_to_var_index(self.get_scratch_index())
        self.emit.end_loop()

    def emit_print_variable(self, variable_name):
        v_index = self.vmap.get_variable_index(variable_name)
        self.emit_move_to_var_index(v_index)
        self.emit.print_current_index()

    def emit_print_string(self, value):
        self.emit_move_to_var_index(self.get_scratch_index())

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

    def process_node(self, node):
        if isinstance(node, ast.Assign):
            self.process_assignment_node(node)
        elif isinstance(node, ast.Print):
            self.process_print_node(node)
        elif isinstance(node, ast.If):
            self.process_if_node(node)
        elif isinstance(node, ast.Pass):
            pass
        else:
            print ast.dump(node)
            self.error_on_node(node, "Syntax not supported yet :(")

    def get_scratch_index(self):
        return self.vmap.get_variable_index("___scratch")

    def create_starting_variables(self):
        vmap = self.vmap
        scratch_space_index = vmap.get_or_create_variable_index("___scratch")
        true_index = vmap.get_or_create_variable_index("True")
        false_index = vmap.get_or_create_variable_index("False")
        self.emit.debug("Defining True at index %s" % true_index)
        self.emit_move_to_var_index(true_index)
        self.emit_zero_current_index()
        self.emit.add()
        self.emit.debug("Defining False at index %s" % false_index)
        self.emit_move_to_var_index(false_index)
        self.emit_zero_current_index()

        for i in range(constants.IF_STATEMENT_DEPTH):
            vmap.get_or_create_variable_index("___if_%s" % i)
            vmap.get_or_create_variable_index("___else_%s" % i)

    def emit_bf(self):
        self.create_starting_variables()
        top_node = ast.parse(self.python)
        for node in ast.iter_child_nodes(top_node):
            self.process_node(node)
