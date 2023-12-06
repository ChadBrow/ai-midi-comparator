# Auxiliary file that defines a class used to store info about scores
# Chad Brown
# Last updated: 05/12/2023
from mido import MidiFile

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

def readFromFile(fileName):
    #open are midi file
    file = MidiFile(f'midi_files/{fileName}')

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
                notes[notesCurrentlyActive[msg.note]].end = time
                del notesCurrentlyActive[msg.note]
                continue
            if msg.note in notesCurrentlyActive:
                continue #note is pressed again when it is already pressed. Should never happen
            notesCurrentlyActive[msg.note] = l
            notes.append(Note(msg.note, time, -1, msg.velocity))
            l += 1

    info = ScoreInfo(lenNote, time, timeSignature.numerator, timeSigDen=timeSignature.denominator)
    return notes, info