# Auxiliary file that defines a class used to store info about scores
# Chad Brown
# Last updated: 05/11/2023

class ScoreInfo:
    def __init__(self, tempo, length, timeSigNum, timeSigDen=None, key=None):
        self.tempo = tempo
        self.length = length #in ticks
        self.timeSigNum = timeSigNum
        self.timeSigDen = timeSigDen if timeSigDen else 4

class Note:
    def __init__(self, val, start, end, vel):
        self.val = val
        self.start = start
        self.end = end
        self.vel = vel #velocity. How loud it is (roughly)
    
    def __str__(self):
        return f"({self.val}, {self.start}, {self.end}, {self.vel})"