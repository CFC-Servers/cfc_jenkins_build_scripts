# A little over-engineered, but it lints all lua files in or below the cwd

import coloredlogs, logging
import os
import queue

from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread

# logging setup
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger, isatty=True)

results = []

def lint_file(workpool, thread_num):
    while not workpool.empty():
        filename = workpool.get()

        command = ["/usr/local/bin/moonc", filename]

        p = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        stderr = stderr.decode("utf-8")

        if stderr and stderr[:5] != "Built":
            results.append("\n" + stderr)

workpool = queue.Queue()

for filename in Path(os.getcwd()).glob('**/*.moon'):
    workpool.put(str(filename))

threads = []
THREAD_COUNT = 5
for t in range(THREAD_COUNT):
    thread = Thread(target=lint_file, args=(workpool,t))
    threads.append(thread)

    thread.start()

for thread in threads:
    thread.join()

if len(results) > 0:
    logger.error("Moonscript syntax errors have been detected")
    [logger.error(err) for err in results]
    exit(1)

logger.info("No Moonscript syntax errors were detected!")
