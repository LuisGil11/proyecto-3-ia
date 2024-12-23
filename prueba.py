# Tic tac toe con Q-learning

import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from game_demo import start_game
import random

# Definimos el tablero
board = np.zeros((3,3))

REWARD_WIN = 100
REWARD_BLOCKING = 10
REWARD_DRAW = -3
REWARD_LOSE = -100
REWARD_DEFAULT = 0

# Parámetros de Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.8  # Factor de descuento
epsilon = 0.1  # Tasa de exploración

def generate_states():
    """Genera todos los estados posibles del tablero de Tic-Tac-Toe."""
    all_states = [''.join(p) for p in product(" XO", repeat=9)]
    valid_states = [s for s in all_states if is_valid_state(s)]
    return valid_states

def is_valid_state(state):
    """Verifica si el estado del tablero es válido."""
    x_count = state.count("X")
    o_count = state.count("O")
    return 0 <= x_count - o_count <= 1

def is_winner(state, player):
    """Verifica si el jugador ha ganado en el estado dado."""
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    return any(all(state[i] == player for i in pattern) for pattern in win_patterns)

def build_reward_matrix(states):
    """Construye la matriz R para los estados."""
    N = len(states)
    R = np.full((N, N), -1)  # Inicializa con -1 (movimientos inválidos)
    
    for i, state in enumerate(states):
        for j in range(9):  # Itera sobre las 9 celdas posibles
            if state[j] == " ":  # Si la celda está vacía
                for player in ["X", "O"]:
                    new_state = state[:j] + player + state[j+1:]
                    if new_state in states:
                        k = states.index(new_state)
                        if is_winner(new_state, player):
                            R[i][k] = REWARD_WIN  # Victoria
                        elif is_winner(new_state, "O" if player == "X" else "X"):
                            R[i][k] = REWARD_LOSE  # Derrota
                        else:
                            R[i][k] = REWARD_DEFAULT  # Movimiento válido sin victoria
    return R

# Generar estados y matriz R
states = generate_states()
R = build_reward_matrix(states)

n = len(states)  # Número de estados válidos

# Ejemplo de matriz R para los primeros 10 estados
print(R)

def available_actions(state):
  current_state_row = R[state,]
  av_act = np.where(current_state_row >= 0)[0]
  return av_act

def sample_next_action(state, available_actions_range, epsilon=0.1):
    if np.random.rand() < epsilon:
        # Exploración: elegir una acción aleatoria
        return int(np.random.choice(available_actions_range, 1))
    else:
        # Explotación: elegir la mejor acción (máximo valor Q)
        Q_values = Q[state, available_actions_range]
        return int(available_actions_range[np.argmax(Q_values)])

Q = np.zeros((n, n))

def reward_move(current_state, action):
    current_scenario = states[current_state]
    new_scenario = states[action]
    if is_winner(new_scenario, "O"):
        return REWARD_WIN
    elif is_winner(new_scenario, "X"):
        return REWARD_LOSE
    elif new_scenario.count(" ") == 0:
        return REWARD_DRAW
    else:
        action_index = next(i for i in range(len(current_scenario)) if current_scenario[i] != new_scenario[i])
        hipotetical = current_scenario[:action_index] + "O" + current_scenario[action_index+1:]
        if (is_winner(hipotetical, "X")):
            return REWARD_BLOCKING
    return REWARD_DEFAULT

def update(current_state, action, gamma):

    max_index = np.where(Q[action,] == np.max(Q[action,]))[0]

    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]

    reward = reward_move(current_state, action)
    # Q learning formula
    Q[current_state, action] = reward + gamma * max_value

    isWin = is_winner(states[action], "X")

    return isWin

def canPlay(state):
    return state.count(" ") > 0

def move_is_valid(new_state, current_state):
    differences = [(i, states[current_state][i], states[new_state][i]) for i in range(len(states[current_state])) if states[current_state][i] != states[new_state][i]]
    is_valid = len(differences) == 1 and differences[0][1] == ' ' and (differences[0][2] == 'X' or differences[0][2] == 'O')
    return is_valid

PARTIDAS_POR_EPISODIO = 10

win_rates = []
epsilon_decay = 0.999  # Decaimiento de epsilon
min_epsilon = 0.01  # Valor mínimo de epsilon

for i in range(10000):
    wins = 0
    for j in range(PARTIDAS_POR_EPISODIO):
        current_state = 0 # Estado inicial como arreglo vacío
        machine_turn = np.random.choice([True, False])  # Alternar quién empieza
        while True:
            av_actions = [state for state in available_actions(current_state) if move_is_valid(state, current_state)]
            if len(av_actions) == 0:
                break

            if machine_turn:
                action = sample_next_action(current_state, av_actions, epsilon)
                isWin = update(current_state, action, gamma)
                current_state = action
                if isWin:
                    wins += 1
                    break
            else:
                action = random.choice(av_actions)  # Otro ente juega aleatoriamente
                current_state = action
            machine_turn = not machine_turn  # Alternar turnos

    epsilon = max(min_epsilon, epsilon * epsilon_decay)  # Reducir epsilon
    
    if (i + 1) % 1000 == 0:
        win_rates.append(wins / PARTIDAS_POR_EPISODIO)
        print("Win rate after {} simulations: {:.2f}%".format(i + 1, np.mean(win_rates) * 100))

plt.ion()
plt.plot(win_rates)
plt.xlabel("Simulation")
plt.ylabel("Win rate")
plt.show()

start_game(states, Q)