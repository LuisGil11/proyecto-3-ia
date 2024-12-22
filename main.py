import matplotlib.pyplot as plt
import numpy as np
import random

# Definir recompensas
REWARD_WIN = 1
REWARD_LOSE = -1
REWARD_DRAW = 0

# Hiperparámetros
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Tasa de exploración
PARTIDAS_POR_EPISODIO = 100

# Inicializar tabla Q
Q = {}

def is_winner(board, player):
    win_patterns = [
        [(0, 0), (0, 1), (0, 2)],  # Filas
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],  # Columnas
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],  # Diagonales
        [(0, 2), (1, 1), (2, 0)]
    ]
    return any(all(board[x][y] == player for x, y in pattern) for pattern in win_patterns)

def board_to_state(board):
    """Convierte un tablero en un string para usar como clave."""
    return ''.join(''.join(row) for row in board)

def available_actions(board):
    """Devuelve las acciones disponibles en el tablero."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def state_to_board(state):
    """Convierte un string de estado a un tablero."""
    return [list(state[i:i+3]) for i in range(0, len(state), 3)]

def update_Q(state, action, reward, next_state):
    """Actualiza la tabla Q usando la fórmula Q-learning."""
    state_action = (state, action)
    if state_action not in Q:
        Q[state_action] = 0
    next_board = state_to_board(next_state)
    max_Q_next = max((Q.get((next_state, a), 0) for a in available_actions(next_board)), default=0)
    Q[state_action] += alpha * (reward + gamma * max_Q_next - Q[state_action])

def play_game():
    """Simula un juego entre la máquina y un jugador aleatorio."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    machine_turn = random.choice([True, False])
    while True:
        state = board_to_state(board)
        if machine_turn:
            actions = available_actions(board)
            if not actions:
                return REWARD_DRAW  # Empate
            if random.random() < epsilon:
                action = random.choice(actions)  # Exploración
            else:
                Q_values = {a: Q.get((state, a), 0) for a in actions}
                action = max(Q_values, key=Q_values.get)  # Explotación
            board[action[0]][action[1]] = "X"
            if is_winner(board, "X"):
                update_Q(state, action, REWARD_WIN, board_to_state(board))
                return REWARD_WIN
        else:
            actions = available_actions(board)
            if not actions:
                return REWARD_DRAW  # Empate
            action = random.choice(actions)
            board[action[0]][action[1]] = "O"
            if is_winner(board, "O"):
                update_Q(state, action, REWARD_LOSE, board_to_state(board))
                return REWARD_LOSE

        machine_turn = not machine_turn

win_rates = []
loss_rates = []
draw_rates = []
for i in range(10000):
    wins = 0
    losses = 0
    draws = 0
    for j in range(PARTIDAS_POR_EPISODIO):
        reward = play_game()
        if reward == REWARD_WIN:
            wins += 1
        if reward == REWARD_LOSE:
            losses += 1
        if reward == REWARD_DRAW:
            draws += 1
    if (i + 1) % 1000 == 0:
        win_rates.append(wins / PARTIDAS_POR_EPISODIO)
        loss_rates.append(losses / PARTIDAS_POR_EPISODIO)
        draw_rates.append(draws / PARTIDAS_POR_EPISODIO)
        print("Win rate after {} simulations: {:.2f}%".format(i + 1, np.mean(win_rates) * 100))
        print("Loss rate after {} simulations: {:.2f}%".format(i + 1, np.mean(loss_rates) * 100))
        print("Draw rate after {} simulations: {:.2f}%".format(i + 1, np.mean(draw_rates) * 100))
        print('\n*******************************************************************************************\n')

plt.ion()
plt.plot(win_rates, label="Win Rate")
plt.plot(loss_rates, label="Loss Rate")
plt.plot(draw_rates, label="Draw Rate")
plt.xlabel("Simulation")
plt.ylabel("Rate")
plt.legend()
plt.show()