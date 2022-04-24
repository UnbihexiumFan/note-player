from array import array
from time import sleep
from math import sin

from tkinter import *
from tkinter.simpledialog import *
import pygame
from pygame.mixer import Sound, get_init, pre_init

tk = Tk()
c = Canvas(tk, width=1000, height=160, bg="#ffffff")
c.pack()



class Note(Sound):
    def __init__(self, frequency, volume=.01):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = 4 * int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

notemap = {
    0:103.825474, # Ab2
    1:110, # A2
    2:116.54094, # Bb2
    3:123.470825, # B2
    4:130.812783, # C3
    5:138.591315, # C#3
    6:146.832384, # D3
    7:155.563492, # Eb3
    8:164.813778, # E3
    9:174.544116, # F3
    10:184.997211, # F#3
    11:195.997718, # G3
    12:207.652349, # Ab3
    13:220, # A3
    14:233.081881, # Bb3
    15:246.941651, # B3
    16:261.625565, # C4
    17:277.182631, # C#4
    18:293.664768, # D4
    19:311.126984, # Eb4
    20:329.627557, # E4
    21:349.228231, # F4
    22:369.994423, # F#4
    23:391.995436, # G4
    24:415.304698, # Ab4
    25:440, # A4
    256:None # Rest
    }

heightmap = {
    0:135, # Ab2
    1:135, # A2
    2:130, # Bb2
    3:130, # B2
    4:125, # C3
    5:125, # C#3
    6:120, # D3
    7:115, # Eb3
    8:115, # E3
    9:110, # F3
    10:110, # F#3
    11:105, # G3
    12:100, # Ab3
    13:100, # A3
    14:55, # Bb3
    15:55, # B3
    16:50, # C4
    17:50, # C#4
    18:45, # D4
    19:40, # Eb4
    20:40, # E4
    21:35, # F4
    22:35, # F#4
    23:30, # G4
    24:25, # Ab4
    25:25 # A4
    }

accmap = {
    # 0 = None, 1 = Sharp, 2 = Natural
    0:0, # Ab2
    1:2, # A2
    2:0, # Bb2
    3:2, # B2
    4:0, # C3
    5:1, # C#3
    6:0, # D3
    7:0, # Eb3
    8:2, # E3
    9:0, # F3
    10:1, # F#3
    11:0, # G3
    12:0, # Ab3
    13:2, # A3
    14:0, # Bb3
    15:2, # B3
    16:0, # C4
    17:1, # C#4
    18:0, # D4
    19:0, # Eb4
    20:2, # E4
    21:0, # F4
    22:1, # F#4
    23:0, # G4
    24:0, # Ab4
    25:2 # A4
    }

tempo = 144

note_seq = [[18,1], [16,1], [14,1], [16,1], [18,1], [18,1], [18,2], [16,1],
            [16,1], [16,2], [18,1], [21,1], [21,2], [18,1], [16,1], [14,1],
            [16,1], [18,1], [18,1], [18,2], [16,1], [16,1], [18,1], [16,1],
            [14,2], [256,2], [16,1], [16,1], [23,1], [23,1], [25,1], [25,1],
            [23,2], [21,1], [21,1], [20,1], [20,1], [18,1], [18,1], [16,2],
            [23,1], [23,1], [21,1], [21,1], [20,1], [20,1], [18,2], [23,1],
            [23,1], [21,1], [21,1], [20,1], [20,1], [18,2], [16,1], [16,1],
            [23,1], [23,1], [25,1], [25,1], [23,2], [21,1], [21,1], [20,1],
            [20,1], [18,1], [18,1], [16,2]]

def list_split(listA, n):
    list_ = []
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]
        list_.append(every_chunk)
    return list_

def play_note(note_id, length):
    if note_id != 256:
        note = Note(notemap[note_id])
        note.play(-1)
    sleep(length/(tempo/60)-(1/tempo))
    if note_id != 256:
        note.stop()
    sleep(1/tempo)

pre_init(44100, -16, 1, 1024)
pygame.init()

note_id_text = \
"""Note id
0: Very Low Ab
1: Very Low A
2: Very Low Bb
3: Very Low B
4: Low C
5: Low C#
6: Low D
7: Low Eb
8: Low E
9: Low F
10: Low F#
11: Low G
12: Low Ab
13: Low A
14: Low Bb
15: Low B
16: Middle C
17: Middle C#
18: Middle D
19: Middle Eb
20: Middle E
21: Middle F
22: Middle F#
23: Middle G
24: Middle Ab
25: Middle A"""

x = 0
sb = True

class SoundControls():
    def play(event):
        for note in note_seq:
            play_note(note[0], note[1])
    def addrest(event):
        global note_seq
        len_ = askinteger(" ","Note length (beats)", minvalue=1, maxvalue=4)
        if len_:
            note_seq.append([256, len_])
    def addwhole(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 4])
    def addhalf(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 2])
    def adddothalf(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 3])
    def addquarter(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 1])
    def adddotquart(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 1.5])
    def addeighth(event):
        global note_seq
        note_ = askinteger(" ", note_id_text, minvalue=0, maxvalue=25)
        if note_ != None:
            note_seq.append([note_, 0.5])
    def subnote(event):
        global note_seq
        if len(note_seq) > 0:
            note_seq.pop(len(note_seq)-1)
    def load_pres(event):
        global note_seq
        global tempo
        preset = ""
        while preset not in ["#000", "#001", "#002", "#003", "#004", "#005", "#999", None]:
            preset = askstring(" ","Preset:\n\"#000\": Blank\n\"#001\": Mary Ha\
d a Little Lamb and Twinkle Twinkle Little Star\n\"#002\": C pentatonic scale\n\
\"#003\": Chromatic Scale\n\"#004\": Ode to Joy\n\"#005\": Just a note test...\
\n\"#999\": Nothing")
        if preset == "#000":
            note_seq = []
        elif preset == "#001":
            note_seq = [[18,1], [16,1], [14,1], [16,1], [18,1], [18,1], [18,2],
                        [16,1], [16,1], [16,2], [18,1], [21,1], [21,2], [18,1],
                        [16,1], [14,1], [16,1], [18,1], [18,1], [18,2], [16,1],
                        [16,1], [18,1], [16,1], [14,2], [256,2], [23,2], [21,1],
                        [21,1], [20,1], [20,1], [18,1], [18,1], [16,2], [23,1],
                        [23,1], [21,1], [21,1], [20,1], [20,1], [18,2], [23,1],
                        [23,1], [21,1], [21,1], [20,1], [20,1], [18,2], [16,1],
                        [16,1], [23,1], [23,1], [25,1], [25,1], [23,2], [21,1],
                        [21,1], [20,1], [20,1], [18,1], [18,1], [16,2]]
        elif preset == "#002":
            note_seq = [[1, 1], [4, 1], [6, 1], [8, 1], [11, 1], [13, 1],
                        [16, 1], [18, 1], [20, 1], [23, 1], [20, 1], [18, 1],
                        [16, 1], [13, 1], [11, 1], [8, 1], [6, 1], [4, 1],
                        [1, 1], [256, 1], [16,1], [16,1], [23,1], [23,1],
                        [25,1], [25,1]]
        elif preset == "#003":
            note_seq = [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1],
                        [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1],
                        [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1],
                        [19, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1],
                        [25, 1], [25, 1], [24, 1], [23, 1], [22, 1], [21, 1],
                        [20, 1], [19, 1], [18, 1], [17, 1], [16, 1], [15, 1],
                        [14, 1], [13, 1], [12, 1], [11, 1], [10, 1], [9, 1],
                        [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1], [2, 1],
                        [1, 1], [0, 1]]
        elif preset == "#004":
            note_seq = [[10, 2], [11, 1], [13, 1], [13, 1], [11, 1], [10, 1],
                        [8, 1], [6, 2], [8, 1], [10, 1], [10, 1.5], [8, 0.5],
                        [8, 2], [10, 2], [11, 1], [13, 1], [13, 1], [11, 1],
                        [10, 1], [8, 1], [6, 2], [8, 1], [10, 1], [8, 1.5],
                        [6, 0.5], [6, 2], [8, 2], [10, 1], [6, 1], [8, 1],
                        [10, 0.5], [11, 0.5], [10, 1], [6, 1], [8, 1], [10, 0.5],
                        [11, 0.5], [10, 1], [8, 1], [6, 1], [8, 1], [1, 1],
                        [10, 1], [10, 1], [10, 1], [11, 1], [13, 1], [13, 1],
                        [11, 1], [10, 1], [8, 1], [6, 2], [8, 1], [10, 1],
                        [8, 1.5], [6, 0.5], [6, 2]]
        elif preset == "#005":
            note_seq = [[24, 4], [21, 3], [19, 1], [16, 2], [14, 1.5],
                        [12, 0.5], [14, 4]]
        elif preset == "#999":
            tempo = 144
            note_seq = [[13, 0.5], [18, 0.5], [21, 1], [21, 1], [20, 1], [13, 0.5], [18, 0.5], [20, 1], [20, 1], [18, 0.25], [16, 0.75], [13, 0.5], [18, 0.5], [18, 2], [20, 0.5], [16, 1.5], [13, 0.5], [20, 1], [18, 1.5], [13, 0.5], [18, 0.5], [21, 1], [21, 1], [20, 0.75], [13, 0.5], [18, 0.5], [25, 1], [16, 1], [18, 0.25], [16, 0.25], [256, 0.5], [13, 0.5], [18, 0.5], [18, 2], [20, 0.5], [16, 1.5], [13, 0.5], [20, 1], [18, 1.5]]
            SoundControls.play(None)
            note_seq = []

class ScreenControls():
    def left(event):
        global x
        if x > 0:
            x -= 1
    def right(event):
        global x
        x += 1
    def showbars(event):
        global sb
        sb = not sb

c.bind_all("<KeyPress-q>", SoundControls.addquarter)
c.bind_all("<KeyPress-h>", SoundControls.addhalf)
c.bind_all("<KeyPress-t>", SoundControls.adddothalf)
c.bind_all("<KeyPress-w>", SoundControls.addwhole)
c.bind_all("<KeyPress-k>", SoundControls.adddotquart)
c.bind_all("<KeyPress-e>", SoundControls.addeighth)
c.bind_all("<KeyPress-r>", SoundControls.addrest)
c.bind_all("<KeyPress-s>", SoundControls.subnote)
c.bind_all("<KeyPress-p>", SoundControls.load_pres)
c.bind_all("<KeyPress-space>", SoundControls.play)
c.bind_all("<KeyPress-Left>", ScreenControls.left)
c.bind_all("<KeyPress-Right>", ScreenControls.right)
c.bind_all("<KeyPress-b>", ScreenControls.showbars)

while True:
    c.delete("all")
    c.create_line(10, 30, 990, 30)
    c.create_line(10, 40, 990, 40)
    c.create_line(10, 50, 990, 50)
    c.create_line(10, 60, 990, 60)
    c.create_line(10, 70, 990, 70)
    c.create_line(10, 100, 990, 100)
    c.create_line(10, 110, 990, 110)
    c.create_line(10, 120, 990, 120)
    c.create_line(10, 130, 990, 130)
    c.create_line(10, 140, 990, 140)
    c.create_line(20, 110, 20, 105, 25, 100, 30, 105, 30, 120, 15, 135, width=1.5)
    c.create_line(35, 103, 35, 107, width=1.5)
    c.create_line(35, 113, 35, 117, width=1.5)
    c.create_line(20, 35, 25, 30, 30, 35, 30, 45, 15, 50, 30, 55, 30, 65, 25, 70, 20, 65, width=1.5)
    c.create_line(15, 30, 15, 70, width=1.5)
    c.create_rectangle(10, 30, 12, 70, fill="#000000")
    c.create_text(40, 55, text="♭")
    c.create_text(47, 40, text="♭")
    c.create_text(54, 60, text="♭")
    c.create_text(40, 130, text="♭")
    c.create_text(47, 115, text="♭")
    c.create_text(54, 135, text="♭")
    if sb:
        c.create_text(70, 40, text="4", font=("Default", 15))
        c.create_text(70, 60, text="4", font=("Default", 15))
        c.create_text(70, 110, text="4", font=("Default", 15))
        c.create_text(70, 130, text="4", font=("Default", 15))
    offset = 80
    note_seq_ = list(list_split(note_seq, 54))
    measures = 0
    if x < len(note_seq_):
        bef_notes = []
        for line in note_seq_[:x]:
            bef_notes += line
        for note in bef_notes:
            measures += note[1]
        for note in note_seq_[x]:
            if note[0] != 256:
                notey = heightmap[note[0]]
                noteacc = accmap[note[0]]
                nleng = note[1]
                if noteacc == 2:
                    c.create_text(offset+13, notey-6, text="♮")
                elif noteacc == 1:
                    c.create_text(offset+13, notey-6, text="♯")
                if nleng == 4:
                    c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5)
                elif nleng == 2:
                    c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5)
                    c.create_line(offset+10, notey, offset+10, notey-25, width=1.5)
                elif nleng == 3:
                    c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5)
                    c.create_line(offset+10, notey, offset+10, notey-25, width=1.5)
                    c.create_line(offset+13, notey-1, offset+15, notey+1, width=1.5)
                elif nleng == 1:
                    c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5, fill="#000000")
                    c.create_line(offset+10, notey, offset+10, notey-25, width=1.5)
                elif nleng == 1.5:
                    c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5, fill="#000000")
                    c.create_line(offset+10, notey, offset+10, notey-25, width=1.5)
                    c.create_line(offset+13, notey-1, offset+13, notey+1, width=1.5)
                elif nleng == 0.5:
                    if measures % 1 == 0 and offset < 981 and note_seq_[x][int((offset-80)/17+1)][1] == 0.5:
                        c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5, fill="#000000")
                        c.create_line(offset+10, notey, offset+10, notey-25, offset+27, heightmap[note_seq_[x][int((offset-80)/17+1)][0]]-25, width=1.5)
                    elif measures % 1 == 0.5 and offset > 80 and note_seq_[x][int((offset-80)/17-1)][1] == 0.5:
                        c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5, fill="#000000")
                        c.create_line(offset+10, notey, offset+10, notey-25, width=1.5)
                    else:
                        c.create_oval(offset, notey+4, offset+10, notey-4, width=1.5, fill="#000000")
                        c.create_line(offset+10, notey, offset+10, notey-25, offset+13, notey-10, width=1.5)
            elif note[0] == 256:
                nleng = note[1]
                if nleng == 4:
                    c.create_rectangle(offset, 54, offset+10, 50, fill="#000000")
                    c.create_rectangle(offset, 124, offset+10, 120, fill="#000000")
                elif nleng == 2:
                    c.create_rectangle(offset, 46, offset+10, 50, fill="#000000")
                    c.create_rectangle(offset, 116, offset+10, 120, fill="#000000")
                elif nleng == 3:
                    c.create_rectangle(offset, 46, offset+10, 50, fill="#000000")
                    c.create_rectangle(offset, 116, offset+10, 120, fill="#000000")
                    c.create_line(offset+15, 49, offset+13, 51, width=1.5)
                    c.create_line(offset+15, 119, offset+13, 121, width=1.5)
                elif nleng == 1:
                    c.create_line(offset, 35, offset+5, 40, offset, 50, offset+5, 55, offset, 55, offset+3, 60, width=1.5)
                    c.create_line(offset, 105, offset+5, 110, offset, 120, offset+5, 125, offset, 125, offset+3, 130, width=1.5)
            measures += nleng
            if sb and measures % 4 == 0 and offset < 980:
                c.create_line(offset+14, 20, offset+14, 150)
            offset += 17
    tk.update()
