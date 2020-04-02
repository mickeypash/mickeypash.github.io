import signal
import threading


_EXIT = threading.Event()


def quit(log: logging.Logger):
    def inner_quit(signum: int, _):
        name: str = f"{signum}"
        if signum == signal.SIGINT:
            name = "SIGINT"
        elif signum == signal.SIGTERM:
            name = "SIGTERM"

        log.warning(f"{name} received. Gracefully shutting down.")

        _EXIT.set()

    return inner_quit

if __name__ == "__main__":

    # Handle graceful termination
    signal.signal(signal.SIGINT, quit(log))
    signal.signal(signal.SIGTERM, quit(log))

    while not _EXIT.is_set():
        try:
            time.sleep(1)
            print("doing something in a loop ...")
        except Exception as e:
            log.exception("Error running ingestion batch.", extra={"exception": str(e)})

        finally:
            # Sleep and continue, or until a signal is handled
            _EXIT.wait(5)
