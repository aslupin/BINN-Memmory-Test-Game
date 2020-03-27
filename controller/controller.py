import ubinascii
from machine import Pin
from esp import espnow
import network
import random
import time
import _thread
import json

machine = 'controller-node'

PIN_SELECT = 17
PIN_RESET = 16

# config network
w = network.WLAN()
w.active(True)
print('my mac addr (Controller):', ubinascii.hexlify(
    w.config('mac'), ':').decode())

# MAC
MAC = {
    'p2': b'\xa4\xcf\x12\x8f\xb8\x74',
    'p1': b'\xA4\xCF\x12\x8F\xB7\x84',
    'display': b'\x24\x0a\xc4\x9f\x50\x58'
}
# config esp32
# BOARDCAST = b'\xFF' * 6
espnow.init()
# espnow.add_peer(UNICAST_DISPLAY)


def getMac(mac):
    return ''.join(["{:02X}".format(x) for x in mac])


def getMsg(msg):
    return msg.decode('utf-8')


def genProblem(amount):
    strategy = {'1': 'blue', '2': 'green', '3': 'red'}
    random.seed(12)
    states = lambda : random.randint(1, 3)
    return [strategy[str(states())] for _ in range(amount)]


def pushSwitch(PIN):
    return Pin(PIN, Pin.IN, Pin.PULL_UP).value()
    # button = Button(pin=Pin(PIN, mode=Pin.IN, pull=Pin.PULL_UP))
    # return button.value()


def sendToPlayer(msg="", player='p1'):
    obj = {}
    obj['msg'] = msg
    espnow.send(MAC[player], str(obj))
    # msg: have to tuple<string> type
    # eg. "'1','2','3'" response will be ('1','2','3')
    # {
    #     msg : 'msg'
    # }


def sendToDisplay():
    msg = {}
    msg['game'] = selected_game
    msg['data'] = problem_game
    espnow.send(MAC['display'], str(msg))

    # {
    #   game: 1,
    #   data: ['red']
    # }


def strategyGame(msg):
    global player
    strategy = {'1': 'blue', '2': 'green', '3': 'red'}
    print("Received from :", msg['player'])
    print("actions are :", msg['action'])
    action = msg['action']
    print(action['color'])
    if (selected_game == 1):
        storage[str(msg['player'])].append(action['color'])
    elif(selected_game == 2):
        if(action['color'] == problem_game[0]):
            player[str(msg['player'])]['score'] += 1
            msg = '"SCORE : ","{}"'.format(player[str(msg['player'])]['score'])
            sendToPlayer(msg=msg, player=msg['player'])
            


def receive_callback(*dobj):
    msg = getMsg(dobj[0][1])
    msg = msg.replace("'", "\"")
    msg = json.loads(msg)
    strategyGame(msg)

    # {
    #     'player' : 1
    #     'action' : {
    #        'color' : 'red'
    #        'value': 1
    #       }
    # }


def getFromPlayer():
    # config espnow
    # espnow.init()
    espnow.on_recv(receive_callback)


# generate problem for game1 and game2


def startGameI():
    print("###### GAME1 ######")
    global problem_game, _start, time_counting, player
    game_state = 10
    problem_game = genProblem(game_state)
    sendToDisplay()
    time.sleep(game_state*0.8)
    print(problem_game)

    # count down before game start
    for count in range(3, 0, -1):
        print("count down :", count)
        msg_p1 = '"COUNT : {}",'.format(str(count))
        msg_p2 = '"COUNT : {}",'.format(str(count))
        sendToPlayer(msg=msg_p1, player='p1')
        sendToPlayer(msg=msg_p2, player='p2')
        time.sleep(1)
    print(time_counting)
    _start = True
    while(time_counting > 0 and _start):
        # SEND SCORES AND TIMING TO OLED ON PLAYER BOARDS.
        msg_p1 = '"TIME LEFT : {}",'.format(str(time_counting))
        msg_p2 = '"TIME LEFT : {}",'.format(str(time_counting))
        sendToPlayer(msg=msg_p1, player='p1')
        sendToPlayer(msg=msg_p2, player='p2')
        print(time_counting)
        time.sleep(1)
        time_counting -= 1
    
    print(storage)

    for key, scores in storage.items():
        for i in range(len(scores)):
            try:
                if (scores[i] == problem_game[i]):
                    print(key)
                    player[key]['score'] += 1
            except:
                continue
    _start = False

    msg_p1 = '"SCORE : {}",'.format(str(player['1']['score']))
    msg_p2 = '"SCORE : {}",'.format(str(player['2']['score']))
    sendToPlayer(msg=msg_p1, player='p1')
    sendToPlayer(msg=msg_p2, player='p2')


def startGameII():
    print("###### GAME2 ######")
    global problem_game, _start, amount_state
    _start = True
    for _ in range(amount_state):
        if (not _start):
            break
        problem_game = genProblem(1)
        sendToDisplay()
        print(problem_game)
        time.sleep(0.7)
    _start = False


# select game

def ledSelect():
    global ledBuildIn
    while(1):
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
        time.sleep(1)


def selectSwitch():
    global select
    btn_select = pushSwitch(PIN_RESET)
    while (btn_select == 1):
        btn_select = pushSwitch(PIN_RESET)
        if (btn_select == 0):
            print("select game!!")
            select = True
        time.sleep(0.2)


def selectGame():
    global selected_game, _start, select
    select = False  # initial selecting state
    _thread.start_new_thread(selectSwitch, ())
    _thread.start_new_thread(ledSelect, ())
    print("select game:", selected_game)
    while (not select):
        # selected_game is 1 or 2
        if(pushSwitch(PIN_SELECT) == 0):
            selected_game = (selected_game + 1) % 3
            if (selected_game == 0):
                selected_game = 1
            print("select game:", selected_game)
            time.sleep(0.2)


# reset game

def reset():
    global _start
    reset = False
    while (not reset):
        btn_reset = pushSwitch(PIN_RESET)
        if(btn_reset == 0):
            reset = True
        time.sleep(0.1)
    _start = False
    print('reset')
    _thread.exit()

# Connecting Display, P1, P2


def connectDevice(device):
    espnow.add_peer(MAC[device])
    mac = MAC[device]
    while(signal[device] == False):  # bug on staging
        espnow.send(mac, 'connecting')
        time.sleep(1)


def callBackConnect(*dobj):
    mac = getMac(dobj[0][0])
    msg = getMsg(dobj[0][1])
    print('connect with', mac, msg)
    if (mac == getMac(MAC['p1']) and msg == 'connected'):
        signal['p1'] = True
    elif (mac == getMac(MAC['p2']) and msg == 'connected'):
        signal['p2'] = True
    elif (mac == getMac(MAC['display']) and msg == 'connected'):
        signal['display'] = True


def connectMain():
    # P1 = 'p1'
    _thread.start_new_thread(connectDevice, ['p1'])
    _thread.start_new_thread(connectDevice, ['p2'])
    _thread.start_new_thread(connectDevice, ['display'])


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
ledBuildIn.off()

# SIGNAL
# set true for mockup
signal = {
    'p1': False,
    'p2': False,
    'display': False,
}
devicesConnect = False  # signal mock  (eg. sensor)

initial_time = 5
time_counting = initial_time  # timing of game1
amount_state = 10  # state of game2

problem_game = []
selected_game = 1  # selected, 1, 2
select = False  # state for select or not select game
_start = False  # state for start and end game
# time.sleep(3)  # wating for display show problem
selected_game = 1
# storage for save ans from player
storage = {
    '1': [],  # player1
    '2': []  # player2
}

print('wait for connection')
espnow.on_recv(callBackConnect)
connectMain()

while (signal['p1'] != True or signal['p2'] != True or signal['display'] != True):

    ledBuildIn.on()
    time.sleep(0.5)
    ledBuildIn.off()
    time.sleep(0.5)

    for device, ready in signal.items():
        if (not ready):
            print('wait', device)
            time.sleep(1)


devicesConnect = True
ledBuildIn.on()
print('connecting')

while True:  # main thread was controller
    score_p1 = str(player['1']['score'])
    score_p2 = str(player['2']['score'])
    # if(_start and selected_game == 2):
    #     print('player 1 score: ' + score_p1)
    #     print('player 2 score: ' + score_p2)
    #     # SEND SCORES TO OLED ON PLAYER BOARDS.
    #     msg = '"SCORE : ","{}"'.format(score_p1)
    #     sendToPlayer(msg=msg, player='p1')
    #     msg = '"SCORE : ","{}"'.format(score_p2)
    #     sendToPlayer(msg=msg, player='p2')
    #     time.sleep(0.5)

    if ((not _start and select)):  # when end game
        print('player 1 score: ' + str(player['1']['score']))
        print('player 2 score: ' + str(player['2']['score']))

        max_score = max(player['1']['score'], player['2']['score'])
        if(max_score == player['1']['score']):
            msg_p1 = '"SCORE : ","{}","YOU WIN!"'.format(score_p1)
            msg_p2 = '"SCORE : ","{}","YOU LOSE!"'.format(score_p2)
            sendToPlayer(msg=msg_p1, player='p1')
            sendToPlayer(msg=msg_p2, player='p2')
        else:
            msg_p1 = '"SCORE : ","{}","YOU LOSE!"'.format(score_p1)
            msg_p2 = '"SCORE : ","{}","YOU WIN!"'.format(score_p2)
            sendToPlayer(msg=msg_p1, player='p1')
            sendToPlayer(msg=msg_p2, player='p2')

        print('Game is end')
        time.sleep(1.5)

        # re init global value
        _start = False
        selected_game == 1
        select = False
        problem_game = []
        storage = {
            '1': [],  # player1
            '2': []  # player2
        }
        time_counting = initial_time

    if (devicesConnect and not _start and not select):
        # select game
        print("Select Game")
        while(select == False):
            selectGame()
        # count before game start
        # for _ in range(3):
            # time.sleep(1)
        # start game !
        
        if(selected_game == 1):
            _thread.start_new_thread(startGameI, ())
        if(selected_game == 2):
            _thread.start_new_thread(startGameII, ())
        _start = True
        print('start game!')
        _thread.start_new_thread(getFromPlayer, ())
        # _thread.start_new_thread(reset, ())
