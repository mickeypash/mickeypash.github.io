import signal
import time

# Top answer on StackOverflow
# https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    import pdb; pdb.set_trace()
    self.kill_now = True

if __name__ == '__main__':

  killer = GracefulKiller()
  while not killer.kill_now:

    time.sleep(1)
    print("doing something in a loop ...")

  print("End of the program. I was killed gracefully :)")