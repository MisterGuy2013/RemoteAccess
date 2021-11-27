import mouse
import keyboard
import websocket
from socket import gethostbyname
'''
python-engineio==3.13.2
python-socketio==4.6.0
socketio broswer == max!!!
'''
import socketio
import requests
import time
import driver
import pyautogui
import base64
from io import BytesIO


global room, username, password, verify
room = ""
username = ""
password = ""
verify = "undefined"

print("starting...")
time.sleep(0.25)
print( mouse.get_position())
time.sleep(0.1)


ip = gethostbyname('RemoteAccess.misterguy2013.repl.co')
print(ip)


#sio = socketio.Client(logger=True, engineio_logger=True)
sio = socketio.Client()

def connect():
    print("Connected to " + str(ip))

def connect_error(data):
    print("Error")

def disconnect():
    print("Disconnect")

def sendErr(error):
    print(error)
    sio.emit("send", error)

'''
Guide on responces

PASSWORD|MAIN_ACTION(can be MOUSE, KEY, or WAIT)    \n
|SUB_ACTION(can be CLICK, MOVE, PRESS, HOLD)   \n
|IDENTIFIER(can be LEFT, RIGHT, a key, or a position)   \n
|DURATION(How long this should happen)

'''
@sio.on('recieve')
def catch_all(message):
    global username, verify, password
    print("message recived, message:", message)
    splitM = message.split(";")
    if(len(splitM) == 3 and not splitM[2] == verify and splitM[0] == username):
        splitD = splitM[1].split("|")
        if(splitD[0] == "PASSWORD"):
            if(splitD[1] == password):
                print("Verified:" + splitM[2])
                verify = splitM[2]
            else:
                print(splitM[2], " failed verification")
        elif(splitD[0] == "HELP"):
            print("help requested")
            sio.emit("send", "Use | to separte parts of your message, there are three main groups, MOUSE, KEY, SCREEN, and WAIT. MOUSE subcatigory 1 MOUSE|CLICK, and then MOUSE|CLICK|LEFT/RIGHT/MIDDLE. MOUSE Subcatigory 2, MOUSE|MOVE + position + duration in seconds, example MOUSE|MOVE|100,100|1. MOUSE Subcatigory 3, position MOUSE|POSITION. <br> SCREEN, SCREEN will upload a screenshot of the computer in its current state along with the screen size, SCREEN has no sub paramiters.")
    elif(splitM[0] == username and len(splitM) == 3 and splitM[2] == verify):
        print("Password Confirmed, Continuing...")
        splitD = splitM[1].split("|")

        
        if(splitD[0] == "MOUSE"):
             print("Mouse Value Change Detected")
             if(splitD[1] == "CLICK"):
                 print("Click detected")
                 if(splitD[2] == "LEFT"):
                     print("Left Click detected")
                     mouse.click(button="left")
                 elif(splitD[2] == "RIGHT"):
                    print("Right Click detected")
                    mouse.click(button="right")
                 elif(splitD[2] == "MIDDLE"):
                    print("Middle Click detected")
                    mouse.click(button="middle")
                 else:
                    sendErr("Error, button:" +splitD[2] + "not found")

             elif(splitD[1] == "POSITION"):
                print("Position Requested, position:" + str(mouse.get_position()))
                sio.emit("send", "Mouse Position: " + str(mouse.get_position()))
             elif(splitD[1] == "MOVE"):
                print("Move Mouse Requested")
                splitPos = splitD[2].split(",")
                mouse.move(splitPos[0], splitPos[1], duration=float(splitD[3]))
             else:
                 sendErr("Error, " + splitD[1] + "is unknown")

                 
        elif(splitD[0] == "KEY"):
             print("Key Press Detected")
             if(splitD[1] == "TYPE"):
                 print("typing:" + splitD[2] + " for " +splitD[3] + "seconds")
                 keyboard.write(splitD[2], delay=float(splitD[3]))
             elif(splitD[1] == "PRESS"):
                 print("pressing:" + splitD[2] + " for " +splitD[3] + "seconds")
                 keyboard.press(splitD[2])
                 time.sleep(float(splitD[3]))
                 keyboard.release(splitD[2])
             else:
                 sendErr("Error, " + splitD[1] + " is unknown")

        elif(splitD[0] == "WAIT"):
            print("Waiting")
            time.sleep(splitD[3])



        elif(splitD[0] == "SCREEN"):
            print("Screenshot requested")
            image = pyautogui.screenshot()
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            img_str = str(img_str).replace("b'", "")
            img_str = str(img_str).replace("'", "")
            img_size = image.size
            print("Image made, size:" + str(img_size) + "uploading...")
            sio.emit("send", "Uploading Image... Size:" + str(img_size))
            sio.emit("send", "IMAGE|" + str(img_str))

        elif(splitD[0] == "HELP"):
            print("help requested")
            sio.emit("send", "Use | to separte parts of your message, there are three main groups, MOUSE, KEY, SCREEN, and WAIT. MOUSE subcatigory 1 MOUSE|CLICK, and then MOUSE|CLICK|LEFT/RIGHT/MIDDLE. MOUSE Subcatigory 2, MOUSE|MOVE + position + duration in seconds, example MOUSE|MOVE|100,100|1. MOUSE Subcatigory 3, position MOUSE|POSITION. <br> SCREEN, SCREEN will upload a screenshot of the computer in its current state along with the screen size, SCREEN has no sub paramiters.")
        else:
             sendErr("ERROR INVALID TYPE:" + splitD[0])
        print("\n")
    elif(splitM[0] == "undefined"):
        print("Self Message recived\n")
    else:
        print("Failed Premission Check \n")


@sio.event
def connect():
    print("connected https://RemoteAccess.misterguy2013.repl.co, sid:", sio.sid)


sio.connect('https://RemoteAccess.misterguy2013.repl.co')
c = "computer"
sio.emit("join", room)
print("joined:" + room + "\n\n\n")
time.sleep(1)
#socket.emit("send", "bruh")



sio.wait()
print("euheiyfs")
