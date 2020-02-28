import atexit
import os
from shutil import copyfile
from syntax_checker import SyntaxChecker

class MoonscriptLinter(SyntaxChecker):
    command = ["/usr/local/bin/moonc", "-l"]
    file_pattern = '**/*.moon'

    def get_results(self, stdout, stderr):
        stderr = stderr.decode()
        stderr = str(stderr)

        if stderr and len(stderr) > 0:
            for line in stderr.split("\n"):
                if len(line) == 0:
                    continue

                yield line

cwd = os.getcwd()

# Get the linter config
linter_config = os.path.dirname(os.path.abspath(__file__)) + "/moonscript_lint_config/lint_config.lua"
copyfile(linter_config, cwd+"/lint_config.lua")

# Init Linter
linter = MoonscriptLinter(thread_count=5)

# Remove linter config before exit
def remove_linting_file():
    linter.log("Removing moonscript linting config..")
    lint_path = cwd + "/lint_config.lua"
    os.remove(lint_path)
atexit.register(remove_linting_file)

# Lint files
linter.lint_all_files()
results = linter.results

if len(results) > 0:
    linter.err("Moonscript Style Violations have been detected")
    for line in results:
        if line[0] == "=":
            continue

        if line[0] == "/":
            # Get relative path instead of absolute
            line = line.replace(cwd, "")

            # Replace leading slash with ./
            line = line.replace("/", "./", 1)

            fileBorderLength = len(line) + 1
            border = "-" * round(fileBorderLength)
            linter.log(border)
            linter.log(line)
            linter.log(border)
            continue


        if line[0] ==  ">":
            linter.log(line)
            linter.log("")
            continue

        linter.err(line)

    exit(1)

linter.log("No Moonscript style violations were detected!")
