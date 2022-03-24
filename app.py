from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from oo_minmax_tt import *

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if "player" not in session:
        return render_template("game1.html")
    
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = False
        session["draw"] = False

    if depth() <= 0:
        com_play()
    
    winner = winnerFound(session["board"])
    if(winner[0] == True):
    	session["winner"] = True
    	session["turn"] = winner[1]
    	print("winner found",session["winner"], session["turn"], winner[1])

    if(winner[0] == False and winner[1] == "draw"):
    	session["draw"] = True

    return render_template("game.html", game=session["board"], turn=session["turn"],winnerFound=session["winner"],winner=session["turn"],draw=session["draw"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
	#com_play()
	session["board"][row][col] = session["turn"]
	if(session["turn"] == "X"):
		session["turn"] = "O"
	else:
		session["turn"] = "X"

	com_play()
	return redirect(url_for("index"))
	
	
def com_play():
    if session["turn"] == session["opponent"]:
        b = convertNone(session['board'])
        board = Board(b, session['opponent'])
        move = board.findBestMove()
        b = convert_(session['board'])
        session["board"][move[0]][move[1]] = session["opponent"]
        
        if(session["turn"] == "X"):
            session["turn"] = "O"
        else:
            session["turn"] = "X"
        return redirect(url_for("index"))
	

@app.route("/choose_piece/<int:player>/")
def choose_piece(player):
	if player == 1:
	    session["player"] = 'X'
	    session["opponent"] = 'O'
	else:
	    session["player"] = 'O'
	    session["opponent"] = 'X'
	return redirect(url_for("index"))
	
	
	
@app.route("/reset")
def reset():
	session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
	session["turn"] = "X"
	session["winner"] = False
	session['depth'] = 0
	session["draw"] = False
	session.pop("player")
	session.pop("opponent")
	return redirect(url_for("index"))
	


def convert_(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = None
    return board                

def convertNone(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                board[i][j] = '_'
    return board
    
def depth():
    d = 0
    for i in range(3):
        for j in range(3):
            if session['board'][i][j] != None:
                d = d+1       
    return d



def winnerFound(board):
    print("here at winner")
    print(len(board))
    #check rows
    for i in range(len(board)):
        if (board[i][0] == board[i][1] == board[i][2]):
            if board[i][0] != None:
                return [True, board[i][0]]
    #check cols
    for i in range(len(board)):
        if (board[0][i] == board[1][i] == board[2][i]):
            if board[0][i] != None:
                return [True, board[0][i]]
    #check diagonals
    if(board[0][0] == board[1][1] == board[2][2]):
        if(board[0][0] != None):
            return [True, board[0][0]]
    #check diagonals
    if(board[2][0] == board[1][1] == board[0][2]):
        if(board[2][0] != None):
            return [True, board[2][0]]
    #check if game is drawn
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] == None):
                return [False, board[0][0]]

    #game is drawn since there is no winner 
    #and all boxes are filled
    return [False, "draw"]
