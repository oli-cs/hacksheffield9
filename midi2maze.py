from mido import MidiFile

file = MidiFile('test.mid', clip=True)

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
        stream.append(list[2].split("note=",1)[1])

# Ensure the midi file contains a maximum of twelve notes
streamSet = set(stream)
if len(streamSet) > 12:
    print("Midi file comtains more than tweleve notes")
    exit(1)

# Create a dictionary with an index for each note.
# Convert each note to its dictionary value.
streamDict = {note: index for index, note in enumerate(streamSet)}
stream = [streamDict[note] for note in stream]

