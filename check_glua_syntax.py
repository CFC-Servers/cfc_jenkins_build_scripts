from syntax_checker import SyntaxChecker

logger = logging.getLogger(__name__)

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
    logger.error("GLua syntax errors have been detected")
    [logger.error(err) for err in results]
    exit(1)

logger.info("No GLua syntax errors were detected!")
