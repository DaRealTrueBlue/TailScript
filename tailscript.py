import sys
import time

class TailScript:
    def __init__(self):
        self.variables = {}

    def run(self, code: str):
        lines = code.splitlines()
        i = 0
        while i < len(lines):
            line_number = i + 1
            line = lines[i].strip()

            if not line or line.startswith("#"):  # skip empty lines & comments
                i += 1
                continue

            try:
                # handle blocks (if/else/every)
                if line.startswith("if "):
                    i = self.handle_if_block(lines, i)
                elif line.startswith("every "):
                    i = self.handle_every_block(lines, i)
                else:
                    self.run_line(line)
                    i += 1
            except Exception as e:
                print(f"❌ Error on line {line_number}: {e}")
                break

    # --- line execution ---
    def run_line(self, line: str):
        # typo correction
        if line.startswith("pritn "):
            print("⚠ Did you mean 'print'?")
            line = "print " + line[6:]

        if line.startswith("print "):
            value = line[6:]
            print(self.resolve(value))
            return

        if line.startswith("set "):
            parts = line.split(" to ", 1)
            if len(parts) != 2:
                raise Exception("Use: set name to value")
            name = parts[0][4:].strip()
            value = parts[1].strip()
            self.variables[name] = self.resolve(value)
            return

        if line.startswith("wait "):
            self.handle_wait(line)
            return

        if line.startswith("ask "):
            self.handle_ask(line)
            return

        if line.startswith("increase "):
            self.handle_increase(line)
            return

        if line.startswith("decrease "):
            self.handle_decrease(line)
            return

        raise Exception(f"I don't understand '{line}'")

    # --- resolve value ---
    def resolve(self, value: str):
        # Handle string literals
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        
        # Handle arithmetic expressions
        if ' plus ' in value:
            parts = value.split(' plus ')
            return self.resolve(parts[0].strip()) + self.resolve(parts[1].strip())
        if ' minus ' in value:
            parts = value.split(' minus ')
            return self.resolve(parts[0].strip()) - self.resolve(parts[1].strip())
        if ' times ' in value:
            parts = value.split(' times ')
            return self.resolve(parts[0].strip()) * self.resolve(parts[1].strip())
        if ' divided by ' in value:
            parts = value.split(' divided by ')
            return self.resolve(parts[0].strip()) // self.resolve(parts[1].strip())
        
        # Handle numbers (including negatives)
        if value.lstrip('-').isdigit():
            return int(value)
        
        # Handle variables
        if value in self.variables:
            return self.variables[value]
        
        raise Exception(f"I don't know what '{value}' is")

    # --- wait command ---
    def handle_wait(self, line: str):
        # wait 10 seconds / wait 2 minutes
        parts = line.split()
        if len(parts) != 3:
            raise Exception("Use: wait <number> <seconds|minutes>")
        amount = int(parts[1])
        unit = parts[2]
        if unit.startswith("second"):
            time.sleep(amount)
        elif unit.startswith("minute"):
            time.sleep(amount * 60)
        else:
            raise Exception("Unit must be seconds or minutes")

    # --- if / else block ---
    def handle_if_block(self, lines, index):
        condition_line = lines[index].strip()
        if not condition_line.startswith("if "):
            raise Exception("Invalid if syntax")
        
        # parse condition with multiple operators
        condition = condition_line[3:]
        cond = False
        
        if " is greater than " in condition:
            parts = condition.split(" is greater than ")
            cond = self.resolve(parts[0].strip()) > self.resolve(parts[1].strip())
        elif " is less than " in condition:
            parts = condition.split(" is less than ")
            cond = self.resolve(parts[0].strip()) < self.resolve(parts[1].strip())
        elif " is not " in condition:
            parts = condition.split(" is not ")
            cond = self.resolve(parts[0].strip()) != self.resolve(parts[1].strip())
        elif " is " in condition:
            parts = condition.split(" is ")
            cond = self.resolve(parts[0].strip()) == self.resolve(parts[1].strip())
        else:
            raise Exception("Invalid if condition. Use: is, is not, is greater than, or is less than")

        # collect block lines
        block_lines = []
        index += 1
        else_block = []
        while index < len(lines):
            line = lines[index]
            if line.strip().startswith("else"):
                index += 1
                break
            if line.startswith("    "):
                block_lines.append(line[4:])
                index += 1
            else:
                break
        # collect else block
        while index < len(lines):
            line = lines[index]
            if line.startswith("    "):
                else_block.append(line[4:])
                index += 1
            else:
                break

        # run appropriate block
        if cond:
            for l in block_lines:
                self.run_line(l)
        else:
            for l in else_block:
                self.run_line(l)
        return index

    # --- ask command ---
    def handle_ask(self, line: str):
        # ask "What is your name?" and save to name
        if " and save to " not in line:
            raise Exception("Use: ask \"question\" and save to variable")
        parts = line.split(" and save to ")
        question = parts[0][4:].strip()
        var_name = parts[1].strip()
        
        if question.startswith('"') and question.endswith('"'):
            question = question[1:-1]
        
        response = input(question + " ")
        # Try to convert to number if possible
        if response.isdigit():
            self.variables[var_name] = int(response)
        else:
            self.variables[var_name] = response

    # --- increase command ---
    def handle_increase(self, line: str):
        # increase age by 1
        parts = line.split(" by ")
        if len(parts) != 2:
            raise Exception("Use: increase variable by amount")
        var_name = parts[0][9:].strip()
        amount = self.resolve(parts[1].strip())
        
        if var_name not in self.variables:
            raise Exception(f"Variable '{var_name}' doesn't exist")
        
        self.variables[var_name] += amount

    # --- decrease command ---
    def handle_decrease(self, line: str):
        # decrease age by 1
        parts = line.split(" by ")
        if len(parts) != 2:
            raise Exception("Use: decrease variable by amount")
        var_name = parts[0][9:].strip()
        amount = self.resolve(parts[1].strip())
        
        if var_name not in self.variables:
            raise Exception(f"Variable '{var_name}' doesn't exist")
        
        self.variables[var_name] -= amount

    # --- every <n> minutes do block ---
    def handle_every_block(self, lines, index):
        header = lines[index].strip()
        parts = header.split()
        if len(parts) < 4 or parts[2] != "do":
            raise Exception("Use: every <number> <minutes|seconds> do")
        amount = int(parts[1])
        unit = parts[2]
        index += 1
        block_lines = []
        while index < len(lines) and lines[index].startswith("    "):
            block_lines.append(lines[index][4:])
            index += 1
        # simple demo: just run once
        for l in block_lines:
            self.run_line(l)
        return index

# ---- main program ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a .tail file")
        print("Example: tailscript hello.tail")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith(".tail"):
        print("❌ TailScript files must end with .tail")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)

    TailScript().run(code)
