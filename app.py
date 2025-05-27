from flask import Flask, jsonify, request, render_template
from gameenv import TicTacToe, Player

app = Flask(__name__)

env = TicTacToe()
xagent = agent()

@app.route('/')
def home():
    return render_template('home.html')