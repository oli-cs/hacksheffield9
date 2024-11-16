ARBITARY_FORWARD_MOVEMENT = 5
NOTE_HEIGHT_MAPPING = {"A":2, "A#Bb":2.5, "B":3, "C":-3,
                        "C#Db":-0.5, "D":-1, "D#Eb":-1.5,
                        "E":-2, "F":-2.5, "F#Gb":0.5, "G":1,
                        "G#Ab":1.5}
SPEED = 200
WAIT_SECS = 0.5

##LEFT IS UP

def write_left() -> None:
    pass

def write_right() -> None:
    pass

def write_forward(scaler:float) -> None:
    pass


def generate_micropython(notes : list):
    with open("maze_solution.py") as file:
        file.write("from microbit import *")
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
            file.write("forward({speed})".format(speed=SPEED))
            distance : int = NOTE_HEIGHT_MAPPING[note]
            if distance > 0:
                file.write("left({speed})".format(speed=SPEED))
                file.write("while accelerometer.is_gesture != 'left':\n        pass")
                file.write("stop()")

                file.write("forward({speed})".format(speed=(SPEED)))
                file.write("sleep({time})".format(WAIT_SECS*distance))
                file.write("stop()")
                
                file.write("right({speed})".format(speed=SPEED))
                file.write("while accelerometer.is_gesture != 'right':\n        pass")
                file.write("stop()")
                
                file.write("forward({speed})".format(speed=(SPEED)))
                file.write("sleep({time})".format(WAIT_SECS))
                file.write("stop()")

                file.write("right({speed})".format(speed=SPEED))
                file.write("while accelerometer.is_gesture != 'right':\n        pass")
                file.write("stop()")

                file.write("forward({speed})".format(speed=(SPEED)))
                file.write("sleep({time})".format(WAIT_SECS*distance))
                file.write("stop()")

                file.write("left({speed})".format(speed=SPEED))
                file.write("while accelerometer.is_gesture != 'left':\n        pass")
                file.write("stop()")
            elif distance < 0:
                distance = abs(distance)
                file.write("right({speed})".format(speed=SPEED))
                file.write("forward({speed})".format(speed=(SPEED*distance)))
                file.write("left({speed})".format(speed=SPEED))
                file.write("forward({speed})".format(speed=(SPEED)))
                file.write("left({speed})".format(speed=SPEED))
                file.write("forward({speed})".format(speed=(SPEED*distance)))
                file.write("right({speed})".format(speed=SPEED))
            else:
                print("distance was zero")
                exit(1)
            

