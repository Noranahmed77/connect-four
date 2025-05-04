import tkinter as tk
from tkinter import messagebox
import copy
import math

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 1

    def drop_piece(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False

    def is_winner(self, player):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] == player and self.board[row][col+1] == player and \
                   self.board[row][col+2] == player and self.board[row][col+3] == player:
                    return True

        # Check vertical
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if self.board[row][col] == player and self.board[row+1][col] == player and \
                   self.board[row+2][col] == player and self.board[row+3][col] == player:
                    return True

        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if self.board[row][col] == player and self.board[row+1][col+1] == player and \
                   self.board[row+2][col+2] == player and self.board[row+3][col+3] == player:
                    return True

        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] == player and self.board[row-1][col+1] == player and \
                   self.board[row-2][col+2] == player and self.board[row-3][col+3] == player:
                    return True
        return False

    def is_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def get_valid_moves(self):
        return [col for col in range(self.columns) if self.board[0][col] == 0]

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def copy(self):
        new_game = ConnectFour()
        new_game.board = copy.deepcopy(self.board)
        new_game.current_player = self.current_player
        return new_game

def evaluate_window(window, player):
    score = 0
    opponent = 1 if player == 2 else 2

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4

    return score

def evaluate_board(game, player):
    score = 0
    board = game.board

    # Center column preference
    center_array = [row[3] for row in board]
    center_count = center_array.count(player)
    score += center_count * 3

    # Horizontal evaluation
    for row in range(game.rows):
        for col in range(game.columns - 3):
            window = [board[row][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Vertical evaluation
    for col in range(game.columns):
        for row in range(game.rows - 3):
            window = [board[row+i][col] for i in range(4)]
            score += evaluate_window(window, player)

    # Diagonal evaluation (positive slope)
    for row in range(game.rows - 3):
        for col in range(game.columns - 3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Diagonal evaluation (negative slope)
    for row in range(3, game.rows):
        for col in range(game.columns - 3):
            window = [board[row-i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def greedy_ai(game, player):
    valid_moves = game.get_valid_moves()
    best_score = -math.inf
    best_move = None

    for col in valid_moves:
        temp_game = game.copy()
        temp_game.drop_piece(col)
        temp_game.switch_player()
        score = evaluate_board(temp_game, player)
        if score > best_score:
            best_score = score
            best_move = col

    return best_move

def minimax_ai(game, depth, maximizing_player, player):
    valid_moves = game.get_valid_moves()

    if depth == 0 or game.is_winner(player) or game.is_winner(3 - player) or game.is_full():
        return evaluate_board(game, player), None

    if maximizing_player:
        max_eval = -math.inf
        best_col = None
        for col in valid_moves:
            temp_game = game.copy()
            temp_game.drop_piece(col)
            temp_game.switch_player()
            eval, _ = minimax_ai(temp_game, depth-1, False, player)
            if eval > max_eval:
                max_eval = eval
                best_col = col
        return max_eval, best_col
    else:
        min_eval = math.inf
        best_col = None
        for col in valid_moves:
            temp_game = game.copy()
            temp_game.drop_piece(col)
            temp_game.switch_player()
            eval, _ = minimax_ai(temp_game, depth-1, True, player)
            if eval < min_eval:
                min_eval = eval
                best_col = col
        return min_eval, best_col

def alphabeta_ai(game, depth, alpha, beta, maximizing_player, player):
    valid_moves = game.get_valid_moves()

    if depth == 0 or game.is_winner(player) or game.is_winner(3 - player) or game.is_full():
        return evaluate_board(game, player), None

    if maximizing_player:
        max_eval = -math.inf
        best_col = None
        for col in valid_moves:
            temp_game = game.copy()
            temp_game.drop_piece(col)
            temp_game.switch_player()
            eval, _ = alphabeta_ai(temp_game, depth-1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval
                best_col = col
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_col
    else:
        min_eval = math.inf
        best_col = None
        for col in valid_moves:
            temp_game = game.copy()
            temp_game.drop_piece(col)
            temp_game.switch_player()
            eval, _ = alphabeta_ai(temp_game, depth-1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_col = col
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_col

def a_star_ai(game, player):
    valid_moves = game.get_valid_moves()
    best_score = -math.inf
    best_move = None

    for col in valid_moves:
        temp_game = game.copy()
        temp_game.drop_piece(col)
        temp_game.switch_player()
        score = evaluate_board(temp_game, player)
        if score > best_score:
            best_score = score
            best_move = col

    return best_move

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.master.configure(bg='#E0F0FF')  # Light blue background
        self.game = ConnectFour()
        self.ai_players = {1: None, 2: None}
        self.ai_delay = 500
        self.cell_size = 120  # Increased cell size
        self.colors = {
            'board': '#1F1FFF',    # Dark blue
            'empty': '#CCCCCC',     # Light gray
            'player1': '#FF4444',   # Bright red
            'player2': '#FFFF00',   # Yellow
            'bg': '#E0F0FF',        # Light blue background
            'button_bg': '#4A90E2', # Medium blue
            'button_fg': 'white'
        }
        self.setup_mode_selection()

    def setup_mode_selection(self):
        self.mode_frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.mode_frame.pack(padx=120, pady=120)

        title_font = ('Helvetica', 18, 'bold')
        button_font = ('Helvetica', 14)

        tk.Label(self.mode_frame, text="Select Game Mode:", 
                 font=title_font, bg=self.colors['bg'], fg='navy').pack(pady=10)

        mode_btn_style = {
            'font': button_font,
            'bg': self.colors['button_bg'],
            'fg': self.colors['button_fg'],
            'width': 20,
            'padx': 20,
            'pady': 20
        }

        tk.Button(self.mode_frame, text="AI vs AI",
                 command=lambda: self.setup_ai(True), **mode_btn_style).pack(pady=5)
        tk.Button(self.mode_frame, text="AI vs Human",
                 command=lambda: self.setup_ai(False), **mode_btn_style).pack(pady=5)

    def setup_ai(self, ai_vs_ai):
        self.mode_frame.destroy()
        self.ai_setup_frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.ai_setup_frame.pack(padx=120,pady=120)

        algorithms = ['greedy', 'minimax', 'alphabeta', 'a_star']
        label_style = {'font': ('Helvetica', 20), 'bg': self.colors['bg'], 'fg': 'navy'}
        option_style = {'font': ('Helvetica', 20), 'bg': 'white', 'width': 20}
        btn_style = {
            'font': ('Helvetica', 20, 'bold'),
            'bg': self.colors['button_bg'],
            'fg': self.colors['button_fg'],
            'padx': 10,
            'pady': 5
        }

        if ai_vs_ai:
            tk.Label(self.ai_setup_frame, text="AI 1 Algorithm:", **label_style).grid(row=0, column=0, padx=10, pady=5)
            self.ai1_var = tk.StringVar(value='alphabeta')
            tk.OptionMenu(self.ai_setup_frame, self.ai1_var, *algorithms).grid(row=0, column=1, padx=10, pady=5)

            tk.Label(self.ai_setup_frame, text="AI 2 Algorithm:", **label_style).grid(row=1, column=0, padx=50, pady=50)
            self.ai2_var = tk.StringVar(value='minimax')
            tk.OptionMenu(self.ai_setup_frame, self.ai2_var, *algorithms).grid(row=1, column=1, padx=10, pady=5)

            tk.Button(self.ai_setup_frame, text="Start", command=self.start_ai_vs_ai, **btn_style).grid(row=2, columnspan=2, pady=15)
        else:
            tk.Label(self.ai_setup_frame, text="AI Algorithm:", **label_style).grid(row=0, column=0, padx=10, pady=5)
            self.ai_var = tk.StringVar(value='greedy')
            tk.OptionMenu(self.ai_setup_frame, self.ai_var, *algorithms).grid(row=0, column=1, padx=10, pady=5)

            tk.Button(self.ai_setup_frame, text="Start", command=self.start_ai_vs_human, **btn_style).grid(row=1, columnspan=2, pady=20)

    def start_ai_vs_ai(self):
        self.ai_players[1] = self.ai1_var.get()
        self.ai_players[2] = self.ai2_var.get()
        self.ai_setup_frame.destroy()
        self.setup_board()
        self.master.after(self.ai_delay, self.ai_move)

    def start_ai_vs_human(self):
        self.ai_players[1] = None
        self.ai_players[2] = self.ai_var.get()
        self.ai_setup_frame.destroy()
        self.setup_board()

    def setup_board(self):
        self.canvas = tk.Canvas(self.master, width=700, height=600)
        self.canvas.pack()
        self.draw_board()

        if self.ai_players[self.game.current_player] is not None:
            self.master.after(self.ai_delay, self.ai_move)

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 100
        for row in range(6):
            for col in range(7):
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                if self.game.board[row][col] == 1:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="red", outline="red")
                elif self.game.board[row][col] == 2:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="yellow", outline="yellow")
                else:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="white", outline="white")
        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        if self.ai_players[self.game.current_player] is not None:
            return
        col = event.x // 100
        if col in self.game.get_valid_moves():
            self.make_move(col)

    def make_move(self, col):
        if self.game.drop_piece(col):
            self.draw_board()
            if self.game.is_winner(self.game.current_player):
                messagebox.showinfo("Game Over", f"Player {self.game.current_player} wins!")
                self.master.destroy()
            elif self.game.is_full():
                messagebox.showinfo("Game Over", "Game is a draw!")
                self.master.destroy()
            else:
                self.game.switch_player()
                if self.ai_players[self.game.current_player] is not None:
                    self.master.after(self.ai_delay, self.ai_move)

    def ai_move(self):
        current_player = self.game.current_player
        ai_type = self.ai_players[current_player]

        if ai_type == 'greedy':
            col = greedy_ai(self.game, current_player)
        elif ai_type == 'minimax':
            _, col = minimax_ai(self.game, depth=3, maximizing_player=True, player=current_player)
        elif ai_type == 'alphabeta':
            _, col = alphabeta_ai(self.game, depth=4, alpha=-math.inf, beta=math.inf, 
                                maximizing_player=True, player=current_player)
        elif ai_type == 'a_star':
            col = a_star_ai(self.game, current_player)

        if col is not None and col in self.game.get_valid_moves():
            self.make_move(col)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()