# The main file for this application.
# To run, simply call program with MIDI input port as first argument
# Chad Brown
# Last updated: 05/12/2023
import sys
# import os
# from music21 import converter

from midi_comparator import MidiComparator
from util import readFromFile

def runGame(fileName):
    #let us get the notes as they should be played
    scoreNotes, info = readFromFile(fileName)

    # #generate image of score
    # lily = converter.subConverters.ConverterLilypond()

    # s = converter.parse(f"midi_files/{fileName}")
    # lily.write(s, fmt="png", fp='score0', subformats="png")
    # os.remove('score0')

    #start up game
    game = MidiComparator(scoreNotes, info, f"midi_files/{fileName.split('.')[0]}.png", keepMetronomeOn=True)
    game.run()

if len(sys.argv) < 2:
    print("Program reuires 1 positional argument: the name of the midi file to use.")
    sys.exit()

runGame(sys.argv[1])








