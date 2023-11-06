import time
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from concurrent.futures import ThreadPoolExecutor
from mido import open_input

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

class GameClock(threading.Thread):
    def __init__(self, comparator):
        self.comparator = comparator
        self.stopped = threading.Event()
        self.tickClock = 0
        self.timeClock = 0
        self.tickTime = self.comparator.tickTime
    
    def stop(self):
        self.stopped.set()
    
    def run(self):
        print("Running")
        self.startTime = time.time()
        print(self.startTime)
        while not self.stopped.wait(self.tickTime):
            self.tickClock += 1
            self.comparator.tick(self.tickClock)

class MidiComparator:
    def __init__(self, score, scoreInfo, keepMetronomeOn=False):
        self.time = 0
        self.score = score
        self.info = scoreInfo
        self.keepMetronomeOn = keepMetronomeOn

        self.metronomeOn = True
        self.tickTime = scoreInfo.tempo / (480 * 1000000) #will likely need to slow this down
        self.tickClock = 0

        self.running = False

        self.port = open_input()
    
    def stop(self):
        if not self.running:
            return
        self.sched.shutdown()
        del self.sched
        self.running = False
    
    def run(self):
        #here we run the game
        if self.running:
            return
        #threading because we are going to be doing a lot very quickly
        with ThreadPoolExecutor() as executor:
            #we use blocking scheduler to make sure that we run tick at the exact same increment no matter how long it takes
            self.sched = BlockingScheduler({'apscheduler.job_defaults.max_instances': 6})
            self.sched.add_job(self.tick, "interval", seconds=self.tickTime)
            try:
                self.sched.start()
                self.running = True
            except KeyboardInterrupt: #accept ^C as exit
                print("Exiting prematurly.")
            finally:
                # clock.stop()
                self.stop()
                print("Exit.")
    
    def printEvent(event):
        print(event.__dict__)
    
    def tick(self):
        if self.metronomeOn:
            pass
        # print("Tick---------")
        # print(time.time())
        # print(self.tickClock)
        for msg in self.port.iter_pending():
            print(msg)
        self.tickClock += 1