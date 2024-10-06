from collections import defaultdict
import os
import numpy as np
import random

moves = ["rock", "paper", "scissors"]

alpha = 0.1
gamma = 0.95
epsilon = 1

ai_win = 0
player_win = 0

Q = defaultdict(lambda: np.zeros(len(moves)))

observation_sequence = np.array([])

transition_matrix = np.zeros((3, 3))

move_history = []

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def update_transition_matrix(player_move, last_player_move):
    if last_player_move:
        transition_matrix[moves.index(last_player_move), moves.index(player_move)] += 1

def predict_player_move():
    if len(move_history) < 2:
        return random.choice(moves)

    last_move = move_history[-1]
    second_last_move = move_history[-2]

    last_move_idx = moves.index(last_move)
    second_last_move_idx = moves.index(second_last_move)

    next_move_probabilities = transition_matrix[last_move_idx] + transition_matrix[second_last_move_idx]

    if np.sum(next_move_probabilities) > 0:
        next_move_probabilities = next_move_probabilities / np.sum(next_move_probabilities)
        predicted_move = moves[np.argmax(next_move_probabilities)]
    else:
        predicted_move = random.choice(moves)
        return predicted_move

def counter_move(player_move):
    if player_move == "rock":
        return "paper"
    elif player_move == "paper":
        return "scissors"
    elif player_move == "scissors":
        return "rock"

def choose_ai_move():
    if random.uniform(0, 1) > epsilon:
        return random.choice(moves)
    else:
        predicted_move = predict_player_move()
        if predicted_move is not None:
            return counter_move(predicted_move)
        else:
            return random.choice(moves)

def is_winner(player, ai):
    global ai_win
    global player_win

    if player == "rock":
        if ai == "scissors":
            print("PLAYER WINS\n")
            player_win += 1
            return 1
        elif ai == "paper":
            print("A.I WINS\n")
            ai_win += 1
            return -1
        else:
            print("TIE\n")
            return 0

    elif player == "paper":
        if ai == "rock":
            print("PLAYER WINS\n")
            player_win += 1
            return 1
        elif ai == "scissors":
            print("A.I WINS\n")
            ai_win += 1
            return -1
        else:
            print("TIE\n")
            return 0

    elif player == "scissors":
        if ai == "paper":
            print("PLAYER WINS\n")
            player_win += 1
            return 1
        elif ai == "rock":
            print("A.I WINS\n")
            ai_win += 1
            return -1
        else:
            print("TIE\n")
            return 0

def save_transition_matrix():
    np.save("transition_matrix.npy", transition_matrix)

def load_transition_matrix():
    if os.path.exists("transition_matrix.npy"):
        return np.load("transition_matrix.npy")
    else:
        return np.zeros((3, 3))

def save_player_hist(history):
    np.save("player_hist.npy", np.array(list(history.values())))


def load_player_hist():
    if os.path.exists("player_hist.npy"):
        return dict(zip(moves, np.load("player_hist.npy")))
    else:
        return {move: 0 for move in moves}


def update_q_table(player_move, ai_move, reward):
    state = moves.index(player_move)
    action = moves.index(ai_move)
    next_state = state

    # idk the hell this is but some random ass *magic* formula I got from the internet
    Q[state][action] = Q[state][action] + alpha * (
        reward + gamma * np.max(Q[next_state]) - Q[state][action]
    )

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
    global player_hist, observation_sequence, rounds, transition_matrix, epsilon, alpha
    player_hist = load_player_hist()

    last_player_move = None

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

        ai_move = choose_ai_move()

        print(f"A.I played {ai_move}\n")
        rounds += 1

        reward = is_winner(player_move, ai_move)
        update_q_table(player_move, ai_move, reward)

        update_transition_matrix(player_move, ai_move)
        is_winner(player_move, ai_move)
        print(f"A.I wins: {ai_win}, player wins: {player_win}       {rounds}\n")

        if last_player_move:
            update_transition_matrix(player_move, last_player_move)

        move_history.append(player_move)

        if len(move_history) > 3:
            move_history.pop(0)
            last_player_move = player_move

            epsilon = max(0.05, epsilon * 0.99)
            alpha = max(0.01, alpha * 0.99)

        if len(test_moves) == 0:
            break
        else:
            continue

game()
