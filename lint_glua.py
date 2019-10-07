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

        command = ["/var/lib/jenkins/build_scripts/glualint", filename]

        p = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        stdout = stdout.decode("utf-8")

        if stdout and len(stdout) > 0:
            for line in stdout.split("\n"):
                line = "/lua/" + line.split("/lua/")[1]

                results.append(line)

workpool = queue.Queue()

for filename in Path(os.getcwd()).glob('**/*.lua'):
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
    logger.error("GLua Style Violations have been detected")
    [logger.error(err) for err in results if err and len(err) > 0]
    exit(1)

logger.info("No GLua style violations were detected!")

