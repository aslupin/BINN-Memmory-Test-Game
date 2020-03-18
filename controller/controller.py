machine = 'controller-node'
import _thread
import time
import random
import network
from esp import espnow
from machine import Pin

# config network
w = network.WLAN()
w.active(True)
print('my mac addr:', w.config('mac'))

# config esp32
UNICAST_DISPLAY = b'\xFF' * 6
espnow.init()
espnow.add_peer(UNICAST_DISPLAY)

def genProblen():
    return [str(random.randint(1,3)) for _ in range(3)]

def sendToDisplay():
    global _start
    while _start: 
        global selected_game
        msg = {}
        msg['game'] = selected_game
        msg['data'] = {}
        msg['data']['color'] = 'red'
        msg['data']['value'] = 1
        espnow.send(UNICAST_DISPLAY, str(msg)) 

        # {
        #   game: 1,
        #   data: {
        #        color: red,
        #        value: 1   
        #   }
        # }

        

def strategyGameI(msg):
    global problem_game, player
    strategy = {'1': 'blue', '2': 'green', '3':'red'}
    print("Received from :", msg['player'])
    print("actions are :", msg['action'])
    action = msg['action']
    if(action['color'] == strategy[problem_game[0]]):
        player[msg['player']]['score'] += 1


def strategyGameII(msg):
    return 0

def receive_callback(*dobj):
    global selected_game
    msg = dict(dobj)
    if(selected_game == 1 ):
        strategyGameI(msg)
    elif(selected_game == 2):
        strategyGameII(msg)

    # {
    #     'player' : 1 
    #     'action' : {
    #        'color' : 'red'
    #        'value': 1
    #       }
    # }

def getFromPlayer():
    global _start
    # config espnow
    espnow.init()
    espnow.on_recv(receive_callback)
    while _start:
        pass

# initial

player = {
    '1': { # player 1
        'score' : 0
    },
    '2': { # player 2
        'score' : 0
    }
}

ledBuildIn = Pin(2, Pin.OUT)
ledBuildIn.value(1)

problem_game = []
selected_game = 1 # 1, 2 
_start = False # state for start and end game
isPlay = True  # signal mock  (eg. sensor)
time.sleep(10) # wating for display show problem

# start game !
_thread.start_new_thread(sendToDisplay, ())
_thread.start_new_thread(getFromPlayer, ())
_thread.start_new_thread(getFromPlayer, ())

while True: # main thread was controller 
    print('player 1 score: ' + str(player['1']['score']))
    print('player 2 score: ' + str(player['2']['score']))
    if(player['1']['score'] == 10 or player['2']['score'] == 10):
        isPlay = False
        print(max(player['1']['score'],player['2']['score']))
        problem_game = []

    if(isPlay):
        problem_game = genProblen()
        _start = True
    else:
        _start = False
    pass