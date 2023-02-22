import random
import launchpad
import chess
import chess.engine
import math
import time

def boardLED():
    lp.LedAllOn(0)

    for i in range(8):
        for j in range(8):
            if (i+j)%2!=0:
                lp.LedCtrlRawByCode(((i+1)*10)+(j+1), 3)

def makemove(board, f, t):
    try:
        f = convertlc(f)
        t = convertlc(t)
        move = chess.Move.from_uci(f+t)
        movep = chess.Move.from_uci(f+t+"q")
        legal = move in board.legal_moves
        if legal == True:
            board.push(move)
        else:
            legal = movep in board.legal_moves
            if legal == True:
                p = pickp()
                movep = chess.Move.from_uci(f+t+p)
                board.push(movep)
            else:
                error()
    except:
        error()

def error():
    lp.LedAllOn(72)
    time.sleep(1)

def pickp():
    for i in range(4):
        lp.LedCtrlRawByCode(i+91, 13)
    p = getloc()
    return 'r' if p == 91 else 'n' if p == 92 else 'b' if p == 93 else 'q' if p == 94 else error()
    
def convertlc(l):
    return chr(l%10+96)+str(math.floor(l/10))

def convertcl(c):
    return (int(c[1])*10)+ord(c[0])-96

def showoptions(loc):
    moves = board.legal_moves
    loc = convertlc(loc)
    amoves = False

    for i in range(8):
        for j in range(8):
            des = convertlc((i+1)*10+j+1)
            if loc != des:
                move = chess.Move.from_uci(loc+des)
                movep = chess.Move.from_uci(loc+des+'q')
                legal = (move in moves) or (movep in moves)
                if legal:
                    des = convertcl(des)
                    lp.LedCtrlRawByCode(des, 17)
                    amoves = True
                    if (detectpiece(des) != None and detectpiece(des).color != board.turn) or (detectpiece(des) == None and (8*math.floor((des-11)/10))+(des%10)-1 == board.ep_square):
                        lp.LedCtrlRawByCode(des, 72)
                        
    return amoves

def detectpiece(loc):
    loc =  (8*math.floor((loc-11)/10))+(loc%10)-1
    return board.piece_at(loc)

def getloc():
    buts = []
    while len(buts) == 0:
        buts = lp.ButtonStateRaw()
    if buts[1] == 0:
        buts = [];
        return getloc()
    else:
        return buts[0]

def playermove():
    boardLED()

    loc1 = getloc()
    if detectpiece(loc1) != None and detectpiece(loc1).color == board.turn and showoptions(loc1):
        lp.LedCtrlRawByCode(loc1, 36)
        showoptions(loc1)
        loc2 = getloc()
        makemove(board, loc1, loc2)
    else:
        error()

    print(board)

def cpumove():
    boardLED()
    print(board.legal_moves())
    move = random.choice(board.legal_moves())
    print(move)

def win():
    boardLED()

    for i in range(50):
        for j in range(8):
            for k in range(8):
                p = (j+1)*10+k+1
                if detectpiece(p) != None and detectpiece(p).color != board.turn:
                    lp.LedCtrlRawByCode(p, random.randrange(0,127))

        time.sleep(0.2)

def pvp():
    while not board.is_checkmate():
        playermove()

    win()

def pve(dif):
    while not board.is_checkmate():
        if board.turn == True:
            playermove()
        else:
            cpumove()
    win()

lp = launchpad.LaunchpadLPX()

if lp.Open(1, "LPX"):
    print("Launchpad X")
    mode = "Pro"

board = chess.Board()


pvp()