from flask import Flask, request, render_template, jsonify
from gameenv import TicTacToe, Player, load_dict, training, save_dict, get_qvalues

show_qvalues = False
trained = False
env = None
human = "X"
ai = "O"
p1 = None
p2 = None
o_ai = None
x_ai = None
epsilon = alpha = gamma = episodes = ''

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    global trained, env, human, ai, p1, p2, epsilon, alpha, gamma, episodes, o_ai, x_ai

    if trained == True:
        pass
    else:
        trained = False
    
    move = None
    winner = None;
    win_cells = None;

    if request.method == 'POST':
        submit_type = request.form.get('submit_type')

        if submit_type == 'params':
            epsilon = float(request.form.get('epsilon'))
            alpha = float(request.form.get('alpha'))
            gamma = float(request.form.get('gamma'))
            episodes = int(request.form.get('episodes'))

            # AI training
            p1 = Player("X", "ai", epsilon, alpha, gamma)
            p2 = Player("O", "ai", epsilon, alpha, gamma)

            env = TicTacToe([p1, p2])
            training(env, p1,p2, episodes)
            
            save_dict(p1.q_table, "xtable.pkl")
            save_dict(p1.q_table, "otable.pkl")

            x_ai = Player("X", "ai",epsilon=0, q_table=load_dict('xtable.pkl') )
            o_ai = Player("O", "ai", epsilon=0, q_table=load_dict('otable.pkl'))

            trained = True
            #print('AI Trained')

            
        elif submit_type == 'reset' and trained:
            env.reset();
            # switch icons each time game is reset
            human, ai = ("O", "X") if human == "X" else ("X", "O")
            if human == "O":
                env.board[o_ai.step_ai(env)] = ai
                
            qvalues = get_qvalues(x_ai,o_ai,env,human)
            combine2d(env.board, qvalues)

        elif submit_type == 'move' and trained:            
            
            # retrieve location of move
            move = request.form.get('cell')
            print("Form data:", request.form)
            if move:
                row, col = map(int, move.split('-'))
                idx = row * 3 + col
                
                #theres probably better way than checking available actions twice but fuck it
                if env.available_actions(env.board) != []:
                    # check if cell is empty before playing move
                    if env.board[idx] == ' ':
                        env.board[idx] = human

                        # check if user has won before making ai play move
                        winner = env.check_win()
                        if winner == None:
                            if ai == "X":
                                env.board[x_ai.step_ai(env)] = ai
                            else: 
                                env.board[o_ai.step_ai(env)] = ai
                        
                        # retrieve possibilities of ai playing move in each cell
                        qvalues = get_qvalues(x_ai,o_ai,env,human)

                        #the html board is 3x3 while the board in the qtables is 1x9 so convert to 2d list
                        board_2d = combine2d(env.board, qvalues)

                        # check for a winner and update variable accordingly
                        winner = env.check_win()

                        if winner == 0 or winner == 1 or winner == 2:
                            win_cells = env.win_cells
                            env.print_board()
                            env.board = [' ' for i in range(9)]
    
    try:
        board=board_2d
    except(UnboundLocalError, AttributeError):
        try:
            board_2d = [env.board[i:i + 3] for i in range(0, 9, 3)]
        except(UnboundLocalError, AttributeError):
            board_2d = [[' ', ' ', ' '] for i in range(3)]

    print(board_2d)

    return render_template('home.html',
                           move=move,
                           board=board_2d,
                           epsilon=epsilon,
                           alpha=alpha,
                           gamma=gamma,
                           episodes=episodes,
                           winner=winner,
                           cells=win_cells,
                           qvalues_state = show_qvalues)


@app.route('/update_qvalues', methods=['POST'])
def update_qvalues():
    global show_qvalues
    data = request.get_json()
    show_qvalues = data.get('qvalues', False)
    print("Q-values checkbox is now:", show_qvalues)
    return jsonify(success=True)

@app.route('/get_board')
def get_board():
    global env, x_ai, o_ai, human
    if env is None:
        return jsonify(html='<p>Game not started</p>')

    qvalues = get_qvalues(x_ai, o_ai, env, human) if show_qvalues else []

    board_2d = combine2d(env.board, qvalues)

    rendered_board = render_template('board.html', board=board_2d)
    return jsonify(html=rendered_board)

def combine2d(board, qvalues):
    # first, apply taken positions to board_2d
    board_2d = [env.board[i:i + 3] for i in range(0, 9, 3)]

    # then, iterate through empty positions and apply q-values
    if qvalues != [] and show_qvalues:
        for i in range(0, 3):
            for j in range(0, 3):
                if board_2d[i][j] == ' ':
                    board_2d[i][j] = qvalues[0]
                    print(qvalues[0])
                    qvalues.remove(qvalues[0])
                    print(qvalues);

    return board_2d

if __name__ == '__main__':
    app.run(debug=True)