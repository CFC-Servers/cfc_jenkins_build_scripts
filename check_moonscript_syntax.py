from syntax_checker import SyntaxChecker

class MoonScriptLinter(SyntaxChecker):
    command = "/usr/local/bin/moonc"
    file_pattern = '**/*.moon'

    def get_results(self, stdout, stderr):
        stderr = stderr.decode("utf-8")

        if stderr and stderr[:5] != "Built":
            yield "\n" + stderr


linter = MoonScriptLinter(thread_count=5)
linter.lint_all_files()
results = linter.results

if len(results) > 0:
    linter.err("Moonscript syntax errors have been detected")
    [linter.err(err) for err in results]
    exit(1)

linter.log("No Moonscript syntax errors were detected!")
