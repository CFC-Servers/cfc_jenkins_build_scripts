from syntax_checker import SyntaxChecker

class GluaLinter(SyntaxChecker):
    command = "/var/lib/jenkins/build_scripts/glualint"
    file_pattern = '**/*.lua'

    def get_results(self, stdout, stderr):
        stdout = stdout.decode("utf-8")

        if stdout and len(stdout) > 0:
            for line in stdout.split("\n"):
                if len(line) == 0:
                    continue

                line = "/lua/" + line.split("/lua/")[1]

                yield line


linter = GluaLinter(thread_count=5)
linter.lint_all_files()
results = linter.results

if len(results) > 0:
    logger.error("GLua Style Violations have been detected")
    [logger.error(err) for err in results if err and len(err) > 0]
    exit(1)

logger.info("No GLua style violations were detected!")



