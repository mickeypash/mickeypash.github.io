"""Control the termination of loops that run forever
Have your loop run as such:
    def work():
        while loopcontrol.RUN_FOREVER:
            do_work()
And where you call the work() function wrap it in:
    with loopcontrol.graceful_termination():
        work()
It will toggle the RUN_FOREVER boolean so the current iteration runs till the end
before it exits.
"""

import contextlib
import logging
import signal
import sys

RUN_FOREVER = True


logger = logging.getLogger(__name__)


@contextlib.contextmanager
def graceful_termination():
    signal.signal(signal.SIGTERM, handle_graceful_termination)
    signal.signal(signal.SIGINT, handle_graceful_termination)
    yield
    if not RUN_FOREVER:
        logger.info("Goodbye")
        sys.exit()


def handle_graceful_termination(signum, frame):
    global RUN_FOREVER
    signalname = signum
    if signum == signal.SIGTERM:
        signalname = 'SIGTERM'
    elif signum == signal.SIGINT:
        signalname = 'SIGINT'
    logger.warning("{} received. Gracefully shutting down.".format(signalname))
    RUN_FOREVER = False