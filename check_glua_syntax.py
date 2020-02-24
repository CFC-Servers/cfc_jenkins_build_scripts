from syntax_checker import SyntaxChecker

class GluaSyntaxChecker(SyntaxChecker):
    command = "/usr/bin/luac"
    file_pattern = '**/*.lua'

    def get_results(self, stdout, stderr):
        stderr = stderr.decode("utf-8")

        if stderr and len(stderr) > 0:
            yield stderr


linter = GluaSyntaxChecker(thread_count=5)
linter.lint_all_files()
results = linter.results

if len(results) > 0:
    linter.err("GLua syntax errors have been detected")
    [linter.err(err) for err in results]
    exit(1)

linter.log("No GLua syntax errors were detected!")
