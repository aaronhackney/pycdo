import logging
import time

log = logging.getLogger(__name__)


class Polling:
    def poll(self, fn: callable, retries: int = 5, poll_interval_ms: int = 2000):
        """Pass a function and then poll the functions until an expected value is returned or retires exhausted

        Args:
            fn: The function we wish to poll
            retries (int, optional):Number of times to re-try. Defaults to 5.
            poll_interval_ms (int, optional): Number of milliseconds inbetween polling attempts. Defaults to 2000.
        """
        i = 0
        while i < retries:
            result = fn
            if result:
                print("DONE!")
                return True
            i += 1
            time.sleep(poll_interval_ms * 0.001)
        return False
