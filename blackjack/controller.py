import flask, jsonpickle, shelve
from game import Game
shelves = shelve.open("shelves")
app = flask.Flask(__name__)


@app.route("/", methods=['GET','POST'])
def landerPage():
    if flask.request.method == "POST":
        userInput = flask.request.form
        npcCount = int(userInput["npcCount"])
        game = Game(npcCount + 1)#+1 for add person players to game
        game.players[0].ID = userInput["playerName"]
        shelves["game"] = game
        return flask.redirect("/game")
    return flask.render_template("lander.html")

@app.route("/game", methods=['GET','POST'])
def GameLoop():
    game = shelves["game"]
    #if players are done
    if game.IsNpcTurn():
        game.FinishGame()  # finish npc play
        shelves["game"] = game#save changes
    json = jsonpickle.encode(game)
    # if game not active game is over
    gameOver = not game.isActive
    sendToClient = {"json": json, "gameOver":gameOver}
    if flask.request.method == 'GET':
        return flask.render_template("game.html",dict=sendToClient)
    #POST
    return flask.render_template('game.html', dict=sendToClient)

@app.route("/hit",methods=['GET','POST'])
def Hit():
    if flask.request.method == "POST":
        game = shelves["game"]#load
        if not game.isActive:
            return flask.redirect("/game")
        playerIndex = int(flask.request.form["playerIndex"])
        player = game.players[playerIndex]
        game.Hit(player)
        shelves["game"] = game#save
        return flask.redirect("/game")

@app.route("/hold",methods=["POST"])
def Hold():
    if flask.request.method == "POST":
        game = shelves["game"]
        playerIndex = int(flask.request.form["playerIndex"])
        player = game.players[playerIndex]
        player.Hold()
        shelves["game"] = game
        return flask.redirect("/game")

@app.route("/restart",methods=["POST"])
def Restart():
    game = shelves["game"]
    game.RestartGame()
    shelves["game"] = game
    return flask.redirect("/game")




