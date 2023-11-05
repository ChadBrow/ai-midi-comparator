class MidiInputHandler:
    def __init__(self, port, offset):
        self.port = port
        self._absTime = 0 - offset

    def __call__(self, event, data=None):
        print(event.__dict__)
        # message, deltatime = event
        # self._absTime += deltatime
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))