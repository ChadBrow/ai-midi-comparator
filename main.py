# The main file for this application.
# To run, simply call program with MIDI input port as first argument
# Chad Brown
# Last updated: 05/11/2023

# from html.entities import name2codepoint
import sys
from mido import MidiFile
# from rtmidi.midiutil import open_midiinput

from midi_comparator import MidiComparator
from score_info import ScoreInfo

def readFromFile():
    #open are midi file
    file = MidiFile('test_files/Test2.mid')

    # for i, track in enumerate(file.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         print(msg)

    #get first track and info about the tack. Any input midi file should have only one track
    track = file.tracks[0]
    trackStartTime = track.pop(0).time #unsure if this will ever be needed, but we do have this info
    timeSignature = track.pop(0)
    keySignature = track.pop(0)
    lenNote = track.pop(0).tempo #midi file represent tempo not as beats per minute but as microseconds (10^-6 s) per quarter note

    #now we can start reading 
    # note: all time values are given in ticks. MIDI has 480 ticks per beat (quarter note) 
    # or tempo/480 microseconds per tick
    print(timeSignature.numerator, '=', lenNote)
    # print(track)
    notes = [] #this list'll keep track of all the notes in order of when they're first pressed
    notesCurrentlyActive = {} #this dict will keep track of all the unended notes as well as their index in the list
    l = 0 #keeps track of len(notes)
    time = 0 #keeps track of time
    for msg in track:
        time += msg.time

        if msg.type == "note_on":
            if msg.velocity < 1: #for some reason mido likes to express note_off as note_on w/ zero velocity
                if msg.note not in notesCurrentlyActive:
                    continue #note is released without being pressed. Should never happen
                notes[notesCurrentlyActive[msg.note]][2] = time
                del notesCurrentlyActive[msg.note]
                continue
            if msg.note in notesCurrentlyActive:
                continue #note is pressed again when it is already pressed. Should never happen
            notesCurrentlyActive[msg.note] = l
            notes.append([msg.note, time, -1])
            l += 1

    print(notes)
    info = ScoreInfo(lenNote, time, timeSigNum=timeSignature)
    return notes, info

# #make sure user input MIDI port
# if len(sys.argv) < 2:
#     sys.exit()
# livePort = sys.argv[1]
# print(livePort)

#let us get the notes as they should be played
scoreNotes, info = readFromFile()

#start up game
game = MidiComparator(scoreNotes, info, keepMetronomeOn=True)
game.run()
