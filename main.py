from collections import defaultdict
import os
import numpy as np
from hmmlearn.hmm import GaussianHMM

moves = ["rock", "paper", "scissors"]

n_components = 2
n_iter = 20000

ai_win = 0
player_win = 0

hmm = GaussianHMM(n_components=n_components, n_iter=n_iter, init_params="kmeans", tol=0.001)
observation_sequence = np.array([])

transition_matrix = defaultdict(lambda: defaultdict(lambda: 0.0))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



def update_transition_matrix(player_move, next_move):
    transition_matrix[player_move][next_move] += 1

def is_winner(player, ai):
    global ai_win
    global player_win

    if player == "rock":
        if ai == "scissors":
            print("PLAYER WINS\n")
            player_win += 1
        elif ai == "paper":
            print("A.I WINS\n")
            ai_win += 1
        else:
            print("TIE\n")

    elif player == "paper":
        if ai == "rock":
            print("PLAYER WINS\n")
            player_win += 1
        elif ai == "scissors":
            print("A.I WINS\n")
            ai_win += 1
        else:
            print("TIE\n")

    elif player == "scissors":
        if ai == "paper":
            print("PLAYER WINS\n")
            player_win += 1
        elif ai == "rock":
            print("A.I WINS\n")
            ai_win += 1
        else:
            print("TIE\n")

def save_player_hist(history):
    if os.path.exists("player.hist"):
        with open("player.hist", "w") as f:
            f.write(str(history))
    else:
        with open("player.hist", "x") as f:
            f.write(str(history))

# def load_player_hist():
#     if os.path.exists("player.hist"):
#         with open("player.hist", "r") as f:
#             hist_str = f.read()
#             hist_dict = {}
#             for item in hist_str.strip().split(","):
#                 parts = item.split(":")
#                 if len(parts) == 2:
#                     move, count = parts
#                     hist_dict[move.strip()] = int(count.strip())
#
#             return defaultdict(int, hist_dict)
#     else:
#         return defaultdict(int)
#

def load_player_hist():
    if os.path.exists("player.hist"):
        with open("player.hist", "r") as f:
            hist_str = f.read()
            hist_dict = {}
            for item in hist_str.strip().split(","):
                parts = item.split(":")
                if len(parts) == 2:
                    move, count = parts
                    try:
                        hist_dict[move.strip()] = int(count.strip())
                    except ValueError:
                        print(f"Invalid count value: {count.strip()}")

            return defaultdict(int, hist_dict)
    else:
        return defaultdict(int)

def game():
    global player_hist, observation_sequence, rounds
    player_hist = load_player_hist()

    rounds = 0

    while True:
        player_move = input(f"Enter your move: {moves} ")

        if player_move == "quit":
            clear()
            exit()

        player_hist[player_move] += 1
        save_player_hist(player_hist)

        if rounds > 0:
            ai_win_rate = ai_win / rounds * 100
            print(f"A.I win rate: {ai_win_rate:.2f}%\n")

        if len(observation_sequence) >= 10:
            observation_sequence_reshaped = observation_sequence.reshape(-1, 1).astype(np.float64)
            hmm.fit(observation_sequence_reshaped)

        if len(observation_sequence) >= 10:
            next_observation = hmm.predict(observation_sequence.reshape(-1, 1).astype(np.float64))[-1]
        else:
            next_observation = np.random.randint(0, 3)

        ai_move = moves[next_observation]
        print(f"A.I played {ai_move}\n")
        rounds += 1
        print(str(rounds) + "\n")

        update_transition_matrix(player_move, ai_move)
        is_winner(player_move, ai_move)
        print(f"A.I wins: {ai_win}, player wins: {player_win}\n")

game()
