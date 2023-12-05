# ai-midi-comparitor

Grand piano sound font courtesy of: https://musical-artifacts.com/artifacts/1660

### Installing

There are many libraries that need to be installed before you can this program

1. mido (I used version 1.3.0)
`pip install mido`
2. pygame (I used version 2.1.2)
`pip install pygame`
3. pygame_gui (I used version 0.6.9)
`pip install pygame_gui`
4. music21 (I used version 9.1.0)
`pip install music21`

You will also need some additional software in order for music21 to work.

You will need to install at least lilypond (I used version 2.24.3).

Click [here](https://lilypond.org/doc/v2.24/Documentation/learning/installing) for install instructions. I used Brew on Mac to install.

Lilypond will throw some errors during execution, but you should be able to ignore these. If music21 throws errors regarding mscore or Musescore that keep the program from executing, you might need to install Musescore 3 or 4 and run `python3 -m music21.configure` or some equivalent. Click [here](https://musescore.org/en/handbook/4/download-and-installation) for instructions on installing Musescore. I used version 4.1.1.

### Running the program

Simply run main.py and pass in the name of the midi file you want to play along with. This midi file should be saved in test_files. For example to play along with Test2.mid in test_files enter `python3 main.py Test2.mid`.