# The main file for this application.
# To run, simply call program with MIDI input port as first argument
# Chad Brown
# Last updated: 05/12/2023
import sys
import os
from music21 import converter

from midi_comparator import MidiComparator
from util import readFromFile

def runGame(fileName):
    #let us get the notes as they should be played
    scoreNotes, info = readFromFile(fileName)

    #generate image of score
    lily = converter.subConverters.ConverterLilypond()

    s = converter.parse("test_files/Test2.mid")
    lily.write(s, fmt="png", fp='score0', subformats="png")
    os.remove('score0')

    #start up game
    game = MidiComparator(scoreNotes, info, 'score0.png', keepMetronomeOn=True)
    game.run()

runGame('Test2.mid')








