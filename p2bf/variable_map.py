class VariableMap(object):
    byte_var_table = {}

    def variable_exists(self, name):
        return name in self.byte_var_table

    def get_or_create_variable_index(self, name):
        if not self.variable_exists(name):
            # Intentionally leaving cell 0 empty
            self.byte_var_table[name] = len(self.byte_var_table)+1

        return self.byte_var_table[name]

    def get_variable_index(self, name):
        if name not in self.byte_var_table:
            raise Exception("Undefined variable: %s" % name)
        return self.byte_var_table[name]

