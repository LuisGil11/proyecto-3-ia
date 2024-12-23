import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

ia = None
Q = []
possible_states = []

def check_winner():
    """Verifica si hay un ganador o un empate."""
    for row in range(3):
        if buttons[row][0]["text"] == buttons[row][1]["text"] == buttons[row][2]["text"] != "":
            return buttons[row][0]["text"]

    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] != "":
            return buttons[0][col]["text"]

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    for row in buttons:
        for button in row:
            if button["text"] == "":
                return None

    return "Empate"

def on_click(row, col):
    """Maneja el evento de clic en un botón."""
    global current_player

    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        winner = check_winner()

        if winner:
            if winner == "Empate":
                messagebox.showinfo("Fin del juego", "Es un empate!")
            else:
                messagebox.showinfo("Fin del juego", f"{winner} gana!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"
            label_turn["text"] = f"Turno de: {current_player}"
            
            # Verificar si es el turno de la IA antes de que juegue
            if current_player == "O":  # Asumiendo que "O" es la IA
                ia.play(check_state())

def reset_game():
    """Reinicia el juego."""
    global current_player
    current_player = random.choice(["X", "O"])
    print(f"current_player: {current_player}")
    label_turn["text"] = f"Turno de: {current_player}"
    for row in buttons:
        for button in row:
            button["text"] = ""
    if (current_player == "O"):
        ia.play(check_state())

# Crear la ventana principal
root = tk.Tk()
root.title("Tic Tac Toe")

# Variables globales
global current_player
current_player = random.choice(["X", "O"])
buttons = []

# Crear la etiqueta para mostrar el turno
label_turn = tk.Label(root, text=f"Turno de: {current_player}", font=("Arial", 14))
label_turn.pack()

# Crear el tablero de botones
frame = tk.Frame(root)
frame.pack()

for row in range(3):
    button_row = []
    for col in range(3):
        button = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                           command=lambda r=row, c=col: on_click(r, c))
        button.grid(row=row, column=col)
        button_row.append(button)
    buttons.append(button_row)

# Botón para reiniciar el juego
reset_button = tk.Button(root, text="Reiniciar", font=("Arial", 12), command=reset_game)
reset_button.pack(pady=10)

# Iniciar el bucle principal de la interfaz

def check_state():
    state = []
    for row in buttons:
        for button in row:
            state.append(button["text"] if button["text"] != "" else " ")
    return ''.join(state)

class IA:
    def __init__(self, Q_matrix):
        self.Q = Q_matrix
    
    def available_actions(self, state):
        return [i for i in range(9) if state[i] == ' ']

    def play(self, current_state):
        print(current_state)
    
    # Obtener todas las acciones posibles para el estado actual
        possible_actions = self.available_actions(current_state)
        
        # Obtener los valores Q para todas las acciones posibles
        q_values = [self.Q.get((current_state, action), 0) for action in possible_actions]
        
        # Encontrar el valor máximo de Q
        max_q_value = max(q_values)
        
        # Filtrar las acciones que tienen el valor máximo de Q
        best_actions = [action for action, q_value in zip(possible_actions, q_values) if q_value == max_q_value]
        
        # Seleccionar una acción aleatoria de las mejores acciones
        action = random.choice(best_actions)
        
        # Calcular la fila y columna de la acción
        row = action // 3
        col = action % 3
        print(row, col)
        
        # Realizar el movimiento
        on_click(row, col)


def start_game(Q_matrix):
    global ia
    global Q
    global possible_states
    Q = Q_matrix
    ia = IA(Q)
    if (current_player == "O"):
        ia.play(check_state())
    root.mainloop()

def load_Q():
    Q = {}
    with open("./Q_matrix.txt") as file:
        for line in file:
            key, value = line.strip().split(": ")
            state, action = eval(key)
            Q[(state, action)] = float(value)
    return Q

if __name__ == "__main__":
    Q = load_Q()
    start_game(Q)