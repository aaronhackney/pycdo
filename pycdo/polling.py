import logging
from subprocess import call
import time

log = logging.getLogger(__name__)


class Polling:
    def poll(self, fn: callable, retries, poll_interval_ms, *args) -> bool:
        """Pass a function and then poll the functions until an expected value is returned or retires exhausted

        Args:
            fn: The function we wish to poll
            retries (int):Number of times to re-try
            poll_interval_ms (int): Number of milliseconds inbetween polling attempts. Defaults to 2000.
            args (list, optional): these are the paramters for the callable function parameter
        """
        i = 0
        while i < retries:
            result = fn(*args)
            if result:
                return True
            i += 1
            time.sleep(poll_interval_ms * 0.001)
        return False
