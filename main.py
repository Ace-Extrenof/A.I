from collections import defaultdict
import os
import random
import numpy as np
from numpy import astype
from hmmlearn.hmm import GaussianHMM

moves = ["rock", "paper", "scissors"]

n_components = 2
n_iter = 20000

hmm = GaussianHMM(n_components=n_components, n_iter=n_iter, init_params="kmeans", tol=0.001)
observation_sequence = np.array([])

transition_matrix = defaultdict(lambda: defaultdict(lambda: 0.0))

def update_transition_matrix(player_move, next_move):
    transition_matrix[player_move][next_move] += 1

def is_winner(player, ai):
    if player == "rock":
        if ai == "paper":
            print("A.I WINS")
    elif player == "paper":
        if ai == "scissors":
            print("A.I WINS")
    elif player == "scissors":
        if ai == "rock":
            print("A.I WINS")

def save_player_hist(history):
    if os.path.exists("player.hist"):
        with open("player.hist", "w") as f:
            f.write(str(history))
    else:
        with open("player.hist", "x") as f:
            f.write(str(history))

def load_player_hist():
    if os.path.exists("player.hist"):
        with open("player.hist", "r") as f:
            return eval(f.read())
    else:
        return defaultdict(int)

def game():
    global player_hist, observation_sequence
    player_hist = defaultdict(int)

    while True:
        player_move = input(f"Enter your move: {moves} ")

        if player_move == "quit":
            exit()

        player_hist[player_move] += 1
        save_player_hist(player_hist)


        if len(observation_sequence) >= 10:
            observation_sequence_reshaped = observation_sequence.reshape(-1, 1).astype(np.float64)
            hmm.fit(observation_sequence_reshaped)

        if len(observation_sequence) >= 10:
            next_observation = hmm.predict(observation_sequence.reshape(-1, 1).astype(np.float64))[-1]
        else:
            next_observation = np.random.randint(0, 3)

        ai_move = moves[next_observation]
        print(f"A.I played {ai_move}")

        update_transition_matrix(player_move, ai_move)
        is_winner(player_move, ai_move)

game()
