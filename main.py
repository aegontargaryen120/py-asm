#!/opt/homebrew/bin/python3.15
import sys

class Section:
    def __init__(self, name=".text"):
        self.name = name
        self.body = []


    def db(self, name, value):
        self.body.append(f"    {name} db {', '.join(value)}")


    def add(self, line):
        self.body.append(line)


    def render(self):
        return "\n".join(self.body)


class Program:
    def __init__(self, name="output.asm"):
        self.name = name
        self.header = []
        self.sections = []


    def add(self, line):
        self.header.append(line)


    def section(self, name):
        section = Section(name)
        self.sections.append(section)
        return section


    def generate(self):
        with open(self.name, "w") as f:
            body = ""
            body += "\n".join(self.header)
            body += "\n"

            for section in self.sections:
                body += f"section {section.name}\n"
                body += section.render() + "\n"

            f.write(body)


try:
    if sys.argv[1] == "generate":
        file = Program("output.asm")
        file.add("global _main")
        file.add("extern _printf")
        data = file.section(".data")
        data.db("message", ['"Hello, world!"',"10", "0"])
        text = file.section(".text")
        text.add("_main:")
        text.add("    push rbp")
        text.add("    mov rbp, rsp\n")
        text.add("    lea rdi, [rel message]")
        text.add("    xor eax, eax")
        text.add("    call _printf\n")
        text.add("    xor eax, eax")
        text.add("    pop rbp")
        text.add("    ret")
        file.generate()

    else:
        print(f"Usage: {sys.argv[0]} generate")
except IndexError:
    print("Usage: ./main.py generate")

