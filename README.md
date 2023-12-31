# ai-midi-comparator

Grand piano sound font courtesy of: https://musical-artifacts.com/artifacts/1660

### Installing

There are many libraries that need to be installed before you can run this program

1. mido (I used version 1.3.0)
`pip install mido`
2. pygame (I used version 2.1.2)
`pip install pygame`
3. pygame_gui (I used version 0.6.9)
`pip install pygame_gui`
<!-- 4. music21 (I used version 9.1.0)
`pip install music21` -->

<!-- You will also need some additional software in order for music21 to work. -->

<!-- You will need to install at least lilypond (I used version 2.24.3).

Click [here](https://lilypond.org/doc/v2.24/Documentation/learning/installing) for install instructions. I used Brew on Mac to install. -->

<!-- Lilypond will throw some errors during execution, but you should be able to ignore these. If music21 throws errors regarding mscore or Musescore that keep the program from executing, you might need to install Musescore 3 or 4 and run `python3 -m music21.configure` or some equivalent. Click [here](https://musescore.org/en/handbook/4/download-and-installation) for instructions on installing Musescore. I used version 4.1.1. -->

You will also need fluidsynth in order for pyfluidsynth to work. Pyfluid synth itself does not need to  be downloaded because the program contains a slightly modified version of its source code. I used version 2.3.4 of fluidsynth. You can find instructions for downloading it [here](https://www.fluidsynth.org/download/). I used brew to install it: `brew install fluid-synth`.



### Running the program

Simply run main.py and pass in the name of the midi file you want to play along with. This midi file as well as a png file with the same name should be saved in test_files. For example to play along with Test2.mid in test_files enter `python3 main.py Test2.mid`.

**This program does a require a midi device to be plugged into a midi port in order to run. I have yet to find an application that can act as an alternative to a Midi keyboard, but I will update the ReadMe if I do.**
