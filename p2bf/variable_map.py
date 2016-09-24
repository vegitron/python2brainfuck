import p2bf.constants as constants


class VariableMap(object):
    default_length = constants.VARIABLE_STATIC_LENGTH

    def __init__(self):
        self.byte_var_table = {}
        self.space_used = 0

    def variable_exists(self, name):
        return name in self.byte_var_table

    def get_or_create_variable_index(self, name, size=default_length):
        if not self.variable_exists(name):
            self.byte_var_table[name] = self.space_used
            # One byte for the type
            self.space_used += 1 + size

        return self._return_location(self.byte_var_table[name])

    def get_variable_index(self, name):
        if name not in self.byte_var_table:
            raise Exception("Undefined variable: %s" % name)
        return self._return_location(self.byte_var_table[name])

    def _return_location(self, value):
        return {
            "type": value,
            "data": value+1,
            }
