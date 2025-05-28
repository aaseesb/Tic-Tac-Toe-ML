from flask import Flask, request, render_template
from gameenv import TicTacToe, Player, load_dict, training, save_dict
import os

trained = False
env = None
human = "X"
p1 = None
p2 = None
epsilon = alpha = gamma = episodes = ''

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    global trained, env, human, p1, p2, epsilon, alpha, gamma, episodes

    #env.print_board()
    if trained == True:
        pass
    else:
        trained = False
    move = None
    
    winner = -1;
    win_direction = None;
    win_cells = None;
    board = []

    print(win_cells)

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
            print('AI Trained')

            

        elif submit_type == 'reset' and trained:
            env.reset();
            human = "O" if human == "X" else "X"
            if human == "O":
                env.board[p2.step_ai(env)] = "X"
            
            

        elif submit_type == 'move' and trained:
            # retrieve location of move
            move = request.form.get('cell')
            print("Form data:", request.form)
            if move:
                row, col = map(int, move.split('-'))
                idx = row * 3 + col

                #theres probably better way than checking available actions twice but fuck it
                if env.available_actions(env.board) != []:

                    if env.board[idx] == ' ':
                        if human == "X":
                            env.board[idx] = 'X'
                            if env.available_actions(env.board) != []:
                                env.board[p2.step_ai(env)] = "O"
                        if human == "O":
                            env.board[idx] = "O"
                            if env.available_actions(env.board) != []:
                                env.board[p2.step_ai(env)] = "X"
                        
                        #the html board is 3x3 while the board in the qtables is 1x9 so just convert
                        board_2d = [env.board[i:i + 3] for i in range(0, 9, 3)]

                        # check for a winner and update variable accordingly
                        winner = env.check_win()

                        # this probably isn't the best place to put this
                        win_cells = env.win_cells
                        if win_cells:
                            win_direction = check_win_direction(win_cells);

                        if winner == 0 or winner == 1 or winner == 2:
                            env.print_board()
                            print("Winner:", winner)
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
                           direction=win_direction)

def check_win_direction(cells):
    if cells == (0, 4, 8):
        return 'down-right'
    elif cells == (2, 4, 6):
        return 'down-left'
    elif cells in [(0,1,2),(3,4,5),(6,7,8)]:
        return 'horizontal'
    else:
        return 'vertical'

if __name__ == '__main__':
    app.run(debug=True)