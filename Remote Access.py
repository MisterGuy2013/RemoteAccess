import mouse
import keyboard
import websocket
from socket import gethostbyname
import socketio
import requests
import time
import driver
import pyautogui
import base64
from io import BytesIO


room = ""
password = ""

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
    print("message recived, message:", message)
    splitM = message.split(";")
    if(splitM[0] == password):
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


             
        elif(splitD[0] == "WAIT"):
            print("Waiting")
            time.sleep(splitD[4])



        elif(splitD[0] == "SCREEN"):
            print("Screenshot requested")
            image = pyautogui.screenshot()
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            img_str = str(img_str).replace("b'", "")
            img_str = str(img_str).replace("'", "")
            print("Image made, uploading...")
            sio.emit("send", "Uploading Image..")
            sio.emit("send", "IMAGE|" + str(img_str))
            
        else:
             sendErr("ERROR INVALID TYPE:" + splitD[0])
        print("\n")
    else:
        print("Failed Premission Check \n")


@sio.event
def connect():
    print("connected https://RemoteAccess.misterguy2013.repl.co, sid:", sio.sid)


sio.connect('https://RemoteAccess.misterguy2013.repl.co')

sio.emit("join", room)
print("joined:" + room + "\n\n\n")
time.sleep(1)
#socket.emit("send", "bruh")



sio.wait()
print("euheiyfs")
