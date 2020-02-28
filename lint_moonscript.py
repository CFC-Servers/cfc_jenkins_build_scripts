from syntax_checker import SyntaxChecker

class MoonscriptLinter(SyntaxChecker):
    command = ["/usr/local/bin/moonc", "-l"]
    file_pattern = '**/*.lua'

    def get_results(self, stdout, stderr):
        stdout = stdout.decode("utf-8")

        if stdout and len(stdout) > 0:
            for line in stdout.split("\n"):
                if len(line) == 0:
                    continue

                line = "/lua/" + line.split("/lua/")[1]

                yield line


linter = MoonscriptLinter(thread_count=5)
linter.lint_all_files()
results = linter.results

if len(results) > 0:
    linter.err("Moonscript Style Violations have been detected")
    [linter.err(err) for err in results if err and len(err) > 0]
    exit(1)

linter.log("No Moonscript style violations were detected!")
