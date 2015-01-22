
import random

from music21 import corpus, note, stream
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq


def generate_triples(items):
    """
    Takes a list of of text and uses it
    to generate triples of consecutive items in a list.
    """
    if len(items) < 3:
        return

    for i in range(0, len(items) - 2):
        yield (items[i], items[i+1], items[i+2])


class MarkovMusic(object):
    def __init__(self):
        self.transitions = {}

    def generate_transitions(self, notes):
        for w1, w2, w3 in generate_triples(notes):
            key = (w1, w2)
            try:
                self.transitions[key].append(w3)
            except KeyError:
                self.transitions[key] = [w3]

    def generate_song(self, length = 30):
        w1, w2 = random.choice(self.transitions.keys())
        gen_notes = []
        for i in xrange(length):
            gen_notes.append(w1)
            w1, w2 = w2, random.choice(self.transitions[(w1,w2)])
        return ' '.join(gen_notes)

    def generate_song_file(self, fname, length = 25):
        note_string = self.generate_song(length)
        print note_string
        notes = NoteSeq(note_string)
        midi = Midi(4, tempo=90)
        midi.seq_notes(notes, track=0)
        midi.write(fname)



#Some simple code to parse and do this stuff...
test = MarkovMusic()
test1 = MarkovMusic()
song = corpus.parse('bach/bwv57.8').parts[0]
all_notes = []
all_durations = []
for measure in song.getElementsByClass(stream.Measure):
    for n in measure.getElementsByClass(note.Note):
        #Convert to a pykon object
        new_name = str(n.pitch.name.replace('-', 'b'))
        duration = str(int(n.duration.quarterLength * 4))
        all_notes.append(new_name)
        all_durations.append(duration)
test.generate_transitions(all_notes)
test1.generate_transitions(all_durations)

n = test.generate_song()
d = test1.generate_song()
n = ' '.join([x + y for (x,y) in zip(n.split(),d.split())])
notes = NoteSeq(n)
midi = Midi(4, tempo=150)
midi.seq_notes(notes, track=0)
midi.write("demo.mid")
