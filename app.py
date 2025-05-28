from flask import Flask, request, render_template
from gameenv import TicTacToe, Player, load_dict

app = Flask(__name__)

otable = load_dict('otable.pkl')
p1 = Player("X", "human")
p2 = Player("O", "ai", q_table=otable, epsilon=0)
env = TicTacToe([p1, p2])

@app.route('/', methods=['GET', 'POST'])
def home():
    env.print_board()
    move = None
    epsilon = alpha = gamma = episodes = ''
    winner = -1;

    if request.method == 'POST':
        submit_type = request.form.get('submit_type')

        if submit_type == 'params':
            epsilon = request.form.get('epsilon')
            alpha = request.form.get('alpha')
            gamma = request.form.get('gamma')
            episodes = request.form.get('episodes')

        elif submit_type == 'reset':
            env.reset();

        elif submit_type == 'move':
            # retrieve location of move
            move = request.form.get('cell')
            print("Form data:", request.form)
            if move:
                row, col = map(int, move.split('-'))
                idx = row * 3 + col

                #theres probably better way than checking available actions twice but fuck it
                if env.available_actions(env.board) != []:
                    if env.board[idx] == ' ':
                        env.board[idx] = 'X'
                        if env.available_actions(env.board) != []:
                            env.board[p2.step_ai(env)] = "O"
                        
                        #the html board is 3x3 while the board in the qtables is 1x9 so just convert
                        board_2d = [env.board[i:i + 3] for i in range(0, 9, 3)]

                        # check for a winner and update variable accordingly
                        winner = env.check_win()
                        if winner == 0 or winner == 1 or winner == 2:
                            env.print_board()
                            print("Winner:", winner)
                            env.board = [' ' for i in range(9)]
    
    
    #omg this is such a shit solution to this but im too tired to find anything else to fix when you select a preselcted block
    # if by select a preselected block, you mean selecting a block that has already been chosen, i fixed it. it doesn't allow you to press on it now
    try:
        board=board_2d
    except UnboundLocalError:
        board_2d = [env.board[i:i + 3] for i in range(0, 9, 3)]



    return render_template('home.html',
                           move=move,
                           board=board_2d,
                           epsilon=epsilon,
                           alpha=alpha,
                           gamma=gamma,
                           episodes=episodes,
                           winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
