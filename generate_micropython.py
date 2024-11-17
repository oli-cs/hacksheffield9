ARBITARY_FORWARD_MOVEMENT = 5
NOTE_HEIGHT_MAPPING = {"A":0.4, "A#Bb":0.5, "B":0.6, "C":-0.6,
                        "C#Db":-0.1, "D":-0.2, "D#Eb":-0.3,
                        "E":-0.4, "F":-0.5, "F#Gb":0.1, "G":0.2,
                        "G#Ab":0.3}
SPEED = 600
TURN = 0.3575
WAIT_SECS = 0.5

##LEFT IS UP

def write_left(file) -> None:
    file.write("right({speed})\n".format(speed=SPEED))
    file.write("sleep({turn})\n".format(turn=TURN))
    file.write("stop()\n")
    return

def write_right(file) -> None:
    file.write("right({speed})\n".format(speed=SPEED))
    file.write("sleep({turn})\n".format(turn=TURN))
    file.write("stop()\n")

def write_forward(file,scaler:float) -> None:
    file.write("forward({speed})\n".format(speed=(SPEED)))
    file.write("sleep({time})\n".format(time=WAIT_SECS*scaler))
    file.write("stop()\n")

def generate_micropython(notes : list):
    with open("output/maze_solution.py","w") as file:
        file.write("from microbit import *\n")
        file.write("""from time import sleep
def forward(speed):
    if (speed > 1023) or (speed < 1):
        display.scroll("Speed must be a number 1-1023")
    else:
        pin12.write_analog(speed)
        pin8.write_digital(0)
        pin16.write_analog(speed)
        pin14.write_digital(0)

def left(speed):
    if (speed > 1023) or (speed < 1):
        display.scroll("Speed must be a number 1-1023")
    else:
        pin12.write_analog(speed)
        pin8.write_digital(0)
        pin16.write_analog(1023)
        pin14.write_analog(1023)

def right(speed):
    if (speed > 1023) or (speed < 1):
        display.scroll("Speed must be a number 1-1023")
    else:
        pin16.write_analog(speed)
        pin14.write_digital(0)
        pin12.write_analog(1023)
        pin8.write_analog(1023)

def stop(brake=True):
    if brake==True:
        pin12.write_analog(1023)
        pin8.write_analog(1023)
        pin16.write_analog(1023)
        pin14.write_analog(1023)
    else:
        pin12.write_digital(0)
        pin8.write_digital(0)
        pin16.write_digital(0)
        pin14.write_digital(0)
""")
        for note in notes:
            file.write("forward({speed})\n".format(speed=SPEED))
            distance : int = NOTE_HEIGHT_MAPPING[note]
            if distance > 0:
                write_left(file)
                write_forward(file,distance)
                write_right(file)

                write_forward(file,1)
                
                write_right(file)
                write_forward(file,distance)
                write_left(file)
                file.write("\n\n")

            elif distance < 0:
                distance = abs(distance)
                write_right(file)
                write_forward(file,distance)
                write_left(file)

                write_forward(file,1)
                
                write_left(file)
                write_forward(file,distance)
                write_right(file)
                file.write("\n\n")

            else:
                print("distance was zero")
                exit(1)