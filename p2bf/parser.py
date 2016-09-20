class Parser(object):
    def parse_content(self, content):
        for line in content.split("\n"):
            self.process_line(line)
