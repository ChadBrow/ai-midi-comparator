# Auxiliary file that defines a class used to store info about scores
# Chad Brown
# Last updated: 05/11/2023

class ScoreInfo:
    def __init__(self, tempo, length, timeSigNum=None, timeSigDen=None, key=None):
        self.tempo = tempo
        self.length = length #in ticks