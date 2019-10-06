import coloredlogs, logging
import os

from pathlib import Path
from subprocess import Popen, PIPE

# logging setup
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

results = []
for filename in Path(os.getcwd()).glob('**/*.lua'):
    filename = str(filename)

    output = None

    command = ["/usr/bin/luac", filename]

    p = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    stderr = stderr.decode("utf-8")

    results.append(stderr or None)

results = [r for r in results if r]

if len(results) > 0:
    logger.error("GLua syntax errors have been detected")
    [logger.error(err) for err in results]
    exit(1)

