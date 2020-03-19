import ubinascii
from machine import Pin
from esp import espnow
import network
import random
import time
import _thread
machine = 'controller-node'

PIN_SELECT = 17
PIN_RESET = 16

# config network
w = network.WLAN()
w.active(True)
print('my mac addr (Controller):', ubinascii.hexlify(
    w.config('mac'), ':').decode())

# config esp32
UNICAST_DISPLAY = b'\xFF' * 6
espnow.init()
espnow.add_peer(UNICAST_DISPLAY)


def genProblem(amount):
    return [str(random.randint(1, 3)) for _ in range(amount)]


def pushSwitch(PIN):
    return Pin(PIN, Pin.IN, Pin.PULL_UP).value()


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


def strategyGame(msg):
    global problem_game, player
    strategy = {'1': 'blue', '2': 'green', '3': 'red'}
    print("Received from :", msg['player'])
    print("actions are :", msg['action'])
    action = msg['action']
    if(action['color'] == strategy[problem_game[0]]):
        player[msg['player']]['score'] += 1


def receive_callback(*dobj):
    global selected_game
    msg = dict(dobj)
    strategyGame(msg)

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

# generate problem for game1 and game2


def startGameI():
    global problem_game, _start, time_counting
    problem_game = genProblem(3)
    for _ in range(time_counting):
        time.sleep(1)
    _start = False


def startGameII():
    global problem_game, _start, amount_state
    for _ in range(amount_state):
        problem_game = genProblem(1)
        time.sleep(0.5)
    _start = False


# select game

def ledSelect():
    global selected_game, ledBuildIn
    if (selected_game == 1):
        ledBuildIn.value(0)
        time.sleep(0.5)
        ledBuildIn.value(1)
        time.sleep(0.5)
    if (selected_game == 2):
        ledBuildIn.value(0)
        time.sleep(0.25)
        ledBuildIn.value(1)
        time.sleep(0.25)
        ledBuildIn.value(0)
        time.sleep(0.25)
        ledBuildIn.value(1)
        time.sleep(0.25)


def selectGame():
    select = False
    global selected_game, _start
    while (not select):
        selected_game = (selected_game +
                         (pushSwitch(PIN_SELECT) == 0)) % 3
        if (selected_game == 3):
            selected_game = 1
        if (pushSwitch(PIN_RESET) == 0):
            select = True
        print("select game:", selected_game)
        time.sleep(0.5)
        ledSelect()

# reset game


def reset():
    global reset, _start
    while (not reset):
        reset = pushSwitch(PIN_RESET) == 0
        _start = False
    print('reset')


# initial
player = {
    '1': {  # player 1
        'score': 0
    },
    '2': {  # player 2
        'score': 0
    }
}

ledBuildIn = Pin(2, Pin.OUT)
ledBuildIn.value(1)

time_counting = 10  # game1
amount_state = 20  # game2


problem_game = []
selected_game = 0  # 0 : none selected, 1, 2
_start = False  # state for start and end game
isPlay = True  # signal mock  (eg. sensor)
reset = False  # state when reset btn is push
time.sleep(3)  # wating for display show problem
print('main')
while True:  # main thread was controller
    if(_start):
        print('player 1 score: ' + str(player['1']['score']))
        print('player 2 score: ' + str(player['2']['score']))
        time.sleep(0.5)
    if(not _start and selected_game != 0):
        isPlay = False
        _start = False
        reset = False
        print(max(player['1']['score'], player['2']['score']))
        time.sleep(1.5)
        selected_game == 0
        problem_game = []
    if (isPlay and not _start and not reset):
        # select game
        print("Select Game")
        while(selected_game == 0):
            selectGame()
        # start game !
        if(selected_game == 1):
            _thread.start_new_thread(startGameI, ())
        if(selected_game == 2):
            _thread.start_new_thread(startGameII, ())
        _start = True
        time.sleep(5)
        print('start game!')
        _thread.start_new_thread(sendToDisplay, ())
        _thread.start_new_thread(getFromPlayer, ())
        _thread.start_new_thread(reset, ())
    pass
