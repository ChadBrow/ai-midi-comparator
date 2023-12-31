# The main engine of the MIDI comparator, does all the comparing and rel time MIDI reading
# Chad Brown
# Last updated: 06/12/2023
import time as ti
from mido import open_input
import math
import sys
import pygame
import pygame_gui
# import threading
from pyfluidsynth_rip.fluidsynth import Synth

from util import Note
import ui

class MidiComparator:
    def __init__(self, score, scoreInfo, img, keepMetronomeOn=False, pianoFont="grand_piano.sf2"):
        self.time = 0
        self.score = score
        self.info = scoreInfo
        self.keepMetronomeOn = keepMetronomeOn
        self.img = img

        self.metronomeOn = True
        self.tickTime = scoreInfo.tempo / (480 * 1000000) #will likely need to slow this down
        self.tickClock = -960 * scoreInfo.timeSigNum
        self.beat = -4
        self.status = 0 #negative for rushing, pos for dragging

        self.running = False

        try: #open midi input
            self.port = open_input()
        except OSError:
            print("Must connect a midi input device before running.")
            sys.exit()

        self.maxTickDif = 960 #for our comparison func we will only consider notes within one beat
        self.pressedNotes = {}
        self.missedNotes = []
        self.hitNotes = []

        pygame.mixer.init()
        pygame.mixer.music.load("soundfonts/metronome.mp3")
        # midi.init()
        # self.piano = midi.Output(0)
        # self.piano.set_instrument(0)
        # self.paino.set_soundfont("soundfonts/grand_piano.sf2")

        #start up our synths
        #lib = "/opt/homebrew/opt/fluid-synth/lib/libfluidsynth.dylib"
        # fs = Synth()
        self.piano = Synth(gain=1.0)
        # self.metronome = fluidsynth.Synth()
        self.piano.start()
        # self.metronome.start()

        pianoFont = self.piano.sfload("soundfonts/" + pianoFont)
        # pianoFont = self.piano.sfload("pyFluidSynth_rip/example.sf2")
        # # metronomeFont = self.metronome.sfload("soundfonts/metronome.sf2")
        self.piano.program_select(0, pianoFont, 0, 0)

        # self.ui = PygameUI()
    
    def stop(self):
        if not self.running:
            return
        self.running = False

        # exit pygame
        pygame.quit()

        #delete our synths
        self.piano.delete()
        # self.metronome.delete()

        #add all remaining notes to missed notes
        self.missedNotes += self.score

        self.postGameAnalysis()

        sys.exit()
    
    def run(self):
        #here we run the game
        if self.running:
            return
        
        #start ui
        self.ui = ui.PygameUI(self.img)

        #start clock and set timer
        clock = pygame.time.Clock()
        pygame.time.set_timer(ui.TICK, int(self.tickTime * 6000))

        #metronome count in
        # self.countIn()

        #threading because we are going to be doing a lot very quickly
        self.running = True
        while(self.running): #event/render loop
            #handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #check for exit
                    self.stop()
                if event.type == pygame_gui.UI_BUTTON_PRESSED: 
                    #check for quit button pressed
                    if hasattr(event, 'ui_element') and event.ui_element == self.ui.exitButton:
                        self.stop()
                if event.type == ui.TICK: #check for tick
                    if self.tickClock % 480 == 0:
                        if self.metronomeOn:
                            pygame.mixer.music.play()
                        self.ui.beat.set_text(f"Beat: {math.floor(self.beat / self.info.timeSigDen)}.{(self.beat % self.info.timeSigDen) + 1}")
                        self.beat += 1
                    self.tickClock += 6
                if event.type == ui.GOOD: #update status to good
                    self.ui.status.set_text("Status: GOOD")
                if event.type == ui.DRAGGING: #update status to dragging
                    self.ui.status.set_text("Status: DRAGGING")
                if event.type == ui.RUSHING: #update status to rushing
                    self.ui.status.set_text("Status: RUSHING")
                self.ui.manager.process_events(event)
            
            #handle any new MIDI inputs
            for msg in self.port.iter_pending():
                # It actually runs better without being threaded.
                # thread = threading.Thread(target=self.processMessage, args=[msg, self.tickClock])
                # thread.start()
                self.processMessage(msg, self.tickClock)
            
            self.ui.tick(clock.tick()/1000)
        # with ThreadPoolExecutor() as executor: #this is used for threading
        #     #we use blocking scheduler to make sure that we run tick at the exact same increment no matter how long it takes
        #     self.sched = BlockingScheduler({'apscheduler.job_defaults.max_instances': 8})
        #     self.sched.add_job(self.tick, "interval", seconds=self.tickTime, id='clock')
        #     try:
        #         self.sched.start() 
        #     except KeyboardInterrupt: #accept ^C as exit
        #         print("-----------------Post Game Analysis-----------------")
        #         self.stop()    
    
    def printEvent(event):
        print(event.__dict__)
    
    def tick(self):
        if self.metronomeOn:
            pass
        if self.tickClock > self.info.length * 200:
            self.stop()
        if self.tickClock % 480 == 0:
            pygame.mixer.music.play()
        for msg in self.port.iter_pending():
            self.processMessage(msg, self.tickClock)

        self.tickClock += 1

    def processMessage(self, msg, time):
        #only accept note on and off messages
        if msg.type == "note_on" or msg.type == "note_off":
            if msg.velocity == 0:
                #this is a note off message
                self.piano.noteoff(0, msg.note)
                #start by playing the note
                # self.midiPlayer.note_off(msg.note, msg.velocity)
                if msg.note not in self.pressedNotes:
                    #note was released without being pressed. Should never happend
                    return
                #note has been finished. Let's compare it to the score
                note = self.pressedNotes[msg.note]
                note.end = time
                del self.pressedNotes[msg.note] #this note is no longer pressed
                match = self.compare(note)
                #if we get a match then great
                if match:
                    self.hitNotes.append(match)
   
                    #if the last two beats (on average) have dragged or rushed, then we send a message about that
                    #we base this off when notes start because we usually perceive time feel based on when
                    #notes begin
                    runningTotDif = 0
                    numRecentNotes = 0
                    for hitPair in reversed(self.hitNotes):
                        #we only want to look back two beats
                        if hitPair[0].start < self.time - self.maxTickDif:
                            break
                        runningTotDif += hitPair[2]
                        numRecentNotes += 1
                    runningAvgDif = runningTotDif / max(numRecentNotes, 1)

                    if runningAvgDif > 120:
                        if self.status <= 0:
                            #we only want to post pygame event if status has actually changed. 
                            #Otherwise no change is necessary
                            self.status = 1
                            pygame.event.post(pygame.event.Event(ui.DRAGGING))
                    elif runningAvgDif < -60:
                        if self.status >= 0:
                            self.status = -1
                            pygame.event.post(pygame.event.Event(ui.RUSHING))
                    else:
                        if self.status != 0:
                            self.status = 0
                            pygame.event.post(pygame.event.Event(ui.GOOD))
                return
            
            #this is a note on message
            self.piano.noteon(0, msg.note, msg.velocity)
            #start by playing the note
            # self.midiPlayer.note_on(msg.note, msg.velocity)
            self.pressedNotes[msg.note] = Note(msg.note, time, -1, msg.velocity)

    def compare(self, note):
        curBest = None #will contain tuple of (note played, score note, time played - time score, time released dif)
        indexBest = -1
        i = 0

        while i < len(self.score): #use while loop cause we'll be doing some popping
            if self.score[i].start > note.start + self.maxTickDif:
                #we have left the range of acceptable notes
                break
            if self.score[i].start < note.start - self.maxTickDif:
                #this element in score is old enough to be considered a missed note
                self.missedNotes.append(self.score.pop(i))
                i += 1
                continue
            if self.score[i].val != note.val:
                #for now we will assume that the player never hits a wrong note
                #so we will not compare score notes with different vaues from the current note
                #This is NOT a good assumption to make, but we can easily fix this later. Consider this WIP
                i += 1
                continue
            startDif = note.start - self.score[i].start
            if indexBest == -1 or abs(startDif) < abs(curBest[2]):
                #if there is not already a current best match or this new note is a better match
                curBest = (note, self.score[i], startDif, note.end - self.score[i].end)
                indexBest = i
                #if this is a new best match and timeDif > 0 then all subsequent notes in the score that match this note
                #must be worse notes because score is sorted by order of notes so timeDif only goes up. So we can break
                if startDif > 0:
                    break
            i += 1
        
        #pop the note we matched from the score. So long as the maxTickDif isn't too great then this should be alright
        if indexBest > -1:
            self.score.pop(indexBest)

        return curBest
    
    def updateUI(self):
        self.ui.tickNum.set_text(f'Tick: {self.tickClock}')
    
    def postGameAnalysis(self):
        print("Game Over")
        print("Number of notes hit:", len(self.hitNotes))
        print("Number of notes missed:", len(self.missedNotes))

        totalTimeDif = 0
        for notePair in self.hitNotes:
            totalTimeDif += notePair[2]
        avgTimeDif = totalTimeDif / max(len(self.hitNotes), 1)
        print(f"Average time difference: {avgTimeDif * self.tickTime:.4f}s or {avgTimeDif / 480:.4f} beats")
        if avgTimeDif > 120:
            print("You dragged a bit.")
        elif avgTimeDif < -60:
            print("You rushed a bit.")
        else:
            print("You were on time.")
    
    def countIn(self):
        for i in range(2 * self.info.timeSigNum):
            pygame.mixer.music.play()
            ti.sleep(self.info.tempo / 1000000)