import coloredlogs, logging
import os
import queue

from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread

# logging setup
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger, isatty=True, fmt='%(levelname)s %(message)s')


class SyntaxChecker:
    command = []
    file_pattern = ""
    def __init__(self, thread_count=5):
        self.thread_count = thread_count
        self.results = []
        self.workpool = queue.Queue()

    def lint_files(self):
        while not self.workpool.empty():
            filename = self.workpool.get()

            command = self.command + [filename]
            print(command)

            p = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()

            for result in self.get_results(stdout, stderr):
                self.results.append(result)


    def get_results(self, stdout, stderr):
        raise NotImplementedEror

    def lint_all_files(self):
        for filename in Path(os.getcwd()).glob(self.file_pattern):
            self.workpool.put(str(filename))

        threads = []

        for t in range(self.thread_count):
            thread = Thread(target=self.lint_files)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def log(self, message):
        logger.info(message)

    def err(self, message):
        logger.error(message)
