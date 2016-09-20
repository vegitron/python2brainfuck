#!/usr/bin/env python
import sys
import tty
import termios


def run(program, memory=[]):
    memory.append(0)
    loop_stack = []
    index = 0
    max_seen_index = 0
    plen = len(program)

    pindex = 0
    while pindex < plen:
        character = program[pindex]

        if character == ">":
            index += 1
            if index > max_seen_index:
                memory.append(0)
                max_seen_index = index

        elif character == "<":
            index -= 1
            if index < 0:
                raise Exception("Negative pointer index at char %s" % pindex)
            pass
        elif character == "+":
            memory[index] += 1
        elif character == "-":
            memory[index] -= 1
        elif character == ".":
            sys.stdout.write(chr(memory[index]))
            sys.stdout.flush()
        elif character == ",":
            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                tty.setraw(sys.stdin.fileno())
                val = sys.stdin.read(1)
                memory[index] = ord(val)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        elif character == "[":
            if memory[index] == 0:
                inner_bracket_depth = 0
                more = True
                while more:
                    pindex += 1

                    if pindex >= plen:
                        raise Exception("Unfinished loop at end of program")

                    character = program[pindex]

                    if character == "[":
                        inner_bracket_depth += 1
                    elif character == "]":
                        inner_bracket_depth -= 1
                        if inner_bracket_depth < 0:
                            more = False
            else:
                loop_stack.append([pindex])
        elif character == "]":
            if not len(loop_stack):
                raise Exception("Extra loop ending at char %s" % pindex)

            current_loop = loop_stack[len(loop_stack)-1]
            if memory[index] != 0:
                pindex = current_loop[0]
            else:
                loop_stack.pop()

        else:
            pass

        pindex += 1

    if len(loop_stack):
        raise Exception("Unfinished loop at end of program")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: bf.py <script name>"
        sys.exit(1)

    bf = open(sys.argv[1])

    program = ""
    buff = bf.read(1024)
    pparts = []
    while (buff):
        pparts.append(buff)
        buff = bf.read(1024)

    program = "".join(pparts)

    run(program)
