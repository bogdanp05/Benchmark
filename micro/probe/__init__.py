from micro.probe.threading import MeasureThread

thread = None


def start_probe(sampling_rate):
    """
    1. if probe already started return
    2. start a thread
    3. create file "measurements_timestamp"
    4. do measurements forever
    :param sampling_rate: the sampling rate for the measurements in seconds (float)
    :return:
    """
    global thread
    if thread:
        print("Probe is already running")
        return

    # create_log()

    thread = MeasureThread(sampling_rate)
    thread.start()


def stop_probe():
    global thread
    if not thread:
        print("Probe is not running")
        return
    thread.stop()
    thread = None
