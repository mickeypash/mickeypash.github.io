## Context Managers and Decorators

```
class timing(ContextDecorator):
    """
    This class should be used as a contextmanager or decorator to time a section of
    code. The duration of the timer can then be accessed, i.e.

    https://docs.python.org/3/library/contextlib.html#contextlib.ContextDecorator

    python
    timer = Timer()
    with timer:
        process()

    print(timer.duration)

    """
    def __init__(self):
        self._start_ts = None
        self._end_ts = None

    def __enter__(self):
        self._start_ts = default_timer()

    def __exit__(self, type, value, traceback):
        self._end_ts = default_timer()

    @property
    def duration(self):
        if self._start_ts and self._end_ts:
            return self._end_ts - self._start_ts
        return None
```



https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
2019-07-24