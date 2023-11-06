import time
import threading

def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

class MidiComparitor:
    def __init__(self, score, scoreInfo, keepMetronomeOn=False):
        self.time = 0
        self.score = score
        self.info = scoreInfo
        self.keepMetronomeOn = keepMetronomeOn

        self.metronomeOn = True
        self.tickTime = scoreInfo.tempo / 480
    
    def printEvent(event):
        print(event.__dict__)
    
    def run(self):
        if self.metronomeOn:
            pass

        self.time += self.tickTime
        