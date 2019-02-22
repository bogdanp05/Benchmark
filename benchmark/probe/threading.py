import threading
import time


class MeasureThread(threading.Thread):
    """
    Used for measuring the system params
    """

    def __init__(self, sampling_rate):
        threading.Thread.__init__(self)
        self._keep_running = True
        self._sampling_rate = sampling_rate

    def run(self):
        """
        Continuously takes a snapshot from the stacktrace (only the main-thread). Filters everything before the
        endpoint has been called (i.e. the Flask library).
        Directly computes the histogram, since this is more efficient for performance
        :return:
        """
        print("Probe started")
        while self._keep_running:
            current_time = time.time()

            print(current_time)

            elapsed = time.time() - current_time
            if self._sampling_rate > elapsed:
                time.sleep(self._sampling_rate - elapsed)
        print("Probe stopped")

    def stop(self):
        self._keep_running = False

