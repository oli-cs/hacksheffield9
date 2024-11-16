from mido import MidiFile
from turtle import *
import time

file = MidiFile('rick.mid', clip=True)

# Ensure midi file has only one track (+ 1 for metadata)
if len(file.tracks) != 2:
    print("Midi file has more than one track.")
    exit(1)

stream = []

# Get note information directly from the midi stream
for instruction in file.tracks[1]:
    string = str(instruction)
    list = string.split()
    if len(list) >= 3 and list[2][:4] == "note" and list[0] == "note_on":
        print(list[2].split("note=",1)[1])
        stream.append(str(int(list[2].split("note=",1)[1]) % 12))

setup(1920, 1080)
bgcolor("black")
color("white")
width(3) 
up()
goto(-960,0)
down()

loop = 0
for note in stream:
    setheading(0)
    forward(10)

    if int(note) == 0:
        right(90)
        for i in range(6):
            forward(5)
        left(90)
        forward(10)
        left(90)
        for i in range(6):
            forward(5)
        right(90)
        print("6 units down")
    elif int(note) <= 5 and int(note) > 0:
        right(90)
        for i in range(int(note)):
            forward(10)
        left(90)
        forward(10)
        left(90)
        for i in range(int(note)):
            forward(10)
        right(90)
        print(int(note), " units down")
    else:
        left(90)
        for i in range(int(note)-5):
            forward(10)
        right(90)
        forward(10)
        right(90)
        for i in range(int(note)-5):
            forward(10)
        left(90)
        print(int(note)-5, " units up")
    
    loop = loop + 1
    if loop >= 95:
        up()
        forward(1000)
        break

while (1):
    time.sleep(1)

'''
notes =	{
  "A": 9,
  "A#Bb": 10,
  "B": 11,
  "C": 0,
  "C#Db": 1,
  "D": 2,
  "D#Eb": 3,
  "E": 4,
  "F": 5,
  "F#Gb": 6,
  "G": 7,
  "G#Ab": 8,

  "9": "A",
  "10": "A#Bb",
  "11": "B",
  "0": "C",
  "1": "C#Db",
  "2": "D",
  "3": "D#Eb",
  "4": "E",
  "5": "F",
  "6": "F#Gb",
  "7": "G",
  "8": "G#Ab",
}

translatedStream = [notes[index] for index in stream]
'''