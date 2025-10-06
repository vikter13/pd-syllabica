import sys
from subprocess import Popen, PIPE
import time

a = Popen(["find", "/"])
while a.poll() is None:
    print(1, file=sys.stderr)
    time.sleep(.1)

