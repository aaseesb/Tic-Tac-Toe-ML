from flask import Flask, jsonify, request, render_template
from gameenv import TicTacToe, Player

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    epsilon = None
    alpha = None
    gamma = None
    episodes = None

    # Handle POST request (form submission)
    if request.method == 'POST':
        epsilon = request.form.get('epsilon')
        alpha = request.form.get('alpha')
        gamma = request.form.get('gamma')
        episodes = request.form.get('episodes')

    return render_template('home.html', epsilon=epsilon, alpha=alpha, gamma=gamma, episodes=episodes)

if __name__ == "__main__":
    app.run(debug=True)