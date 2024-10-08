# from collections import defaultdict
import os
import numpy as np

moves = ["rock", "paper", "scissors"]

n_components = 2
n_iter = 20000

ai_win = 0
player_win = 0

observation_sequence = np.array([])

transition_matrix = np.zeros((3, 3))


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def update_transition_matrix(player_move, ai_move):
    transition_matrix[moves.index(player_move), moves.index(ai_move)] += 1


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
    np.save("player_hist.npy", np.array(list(history.values())))


def load_player_hist():
    if os.path.exists("player_hist.npy"):
        return dict(zip(moves, np.load("player_hist.npy")))
    else:
        return {move: 0 for move in moves}

test_moves = [
    "rock", "paper", "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors",
    "paper", "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors", "rock",
    "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors", "rock", "paper",
    "rock", "scissors", "paper", "rock", "scissors", "paper", "rock", "scissors", "paper",
    "paper", "rock", "scissors", "paper", "rock", "scissors", "paper", "rock", "scissors",
    "scissors", "paper", "rock", "scissors", "paper", "rock", "scissors", "paper", "rock",
    "rock", "paper", "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors",
    "paper", "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors", "rock",
    "scissors", "rock", "paper", "scissors", "rock", "paper", "scissors", "rock", "paper",
    "rock", "scissors", "paper", "rock", "scissors", "paper", "rock", "scissors", "paper"
]

def test():
    for move in test_moves:
        test_moves.remove(move)
        return str(move)

def game():
    global player_hist, observation_sequence, rounds, transition_matrix
    player_hist = load_player_hist()

    rounds = 0

    while True:
        player_move = test()

        if player_move == "quit":
            clear()
            exit()

        player_hist[str(player_move)] += 1
        save_player_hist(player_hist)

        if rounds > 0:
            ai_win_rate = ai_win / rounds * 100
            print(f"A.I win rate: {ai_win_rate:.2f}%\n")

        if len(observation_sequence) >= 20:
            transition_matrix /= transition_matrix.sum(axis=1, keepdims=True)

        if len(observation_sequence) >= 20:
            last_20_moves = observation_sequence[-20]
            next_observation = np.random.choice(
                3,
                p=transition_matrix[
                    last_20_moves[0], last_20_moves[1], last_20_moves[2]
                ],
            )


        else:
            next_observation = np.random.randint(0, 3)

        ai_move = moves[next_observation]
        print(f"A.I played {ai_move}\n")
        rounds += 1
        print(str(rounds) + "\n")

        update_transition_matrix(player_move, ai_move)
        is_winner(player_move, ai_move)
        print(f"A.I wins: {ai_win}, player wins: {player_win}\n")

        observation_sequence = np.append(observation_sequence, next_observation)

        if len(test_moves) == 0:
            break
        else:
            continue

game()
