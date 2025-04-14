import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import json
import subprocess

# === Core Directories ===
SKIN_DIR = "skins"
GAMES_DIR = "games"
PLAYERS_DIR = "players"
THUMBNAILS_DIR = "thumbnails"
SETTINGS_FILE = "settings.json"
ACHIEVEMENTS_FILE = "achievements.json"

# === Load and Save Helpers ===
def load_json(file_path, default):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

# === Flash Player Detection ===
def is_potential_flash_player(file_name):
    """Checks if a file name contains 'Player' (case-insensitive)."""
    return "player" in file_name.lower()

def move_to_players(file_path):
    """Moves a file to the players directory."""
    if not os.path.exists(PLAYERS_DIR):
        os.makedirs(PLAYERS_DIR)
    shutil.move(file_path, os.path.join(PLAYERS_DIR, os.path.basename(file_path)))

# === Flash Player Launcher ===
def launch_flash_game(path, player=None):
    if not os.path.exists(PLAYERS_DIR):
        messagebox.showerror("Error", "Players directory not found.")
        return

    exe_files = [os.path.join(PLAYERS_DIR, f) for f in os.listdir(PLAYERS_DIR) if f.endswith(".exe")]

    if not exe_files:
        messagebox.showerror("Error", "No Flash Player executables found in the players directory.")
        return

    # Launch the first player found or the specified one
    for exe in exe_files:
        try:
            subprocess.Popen([exe, path], shell=True)
            return
        except Exception as e:
            print(f"Failed to launch {exe}: {e}")
            continue

    messagebox.showerror("Error", "Failed to launch the game with any available Flash Player.")

# === App ===
class AchiwaApp:
    def __init__(self, root):
        # Load settings and achievements
        self.settings = load_json(SETTINGS_FILE, {"theme": "default"})
        self.achievements = load_json(ACHIEVEMENTS_FILE, {})
        
        # Initialize the root window
        self.root = root
        self.root.title("Achiwa Launcher")
        self.root.geometry("500x500")
        self.build_ui()

    def build_ui(self):
        # Game Selector
        self.game_var = tk.StringVar()
        tk.Label(self.root, text="Select Game:").pack(pady=10)
        self.game_menu = ttk.Combobox(self.root, textvariable=self.game_var)
        self.game_menu.pack()
        self.refresh_games()
        
        # Launch Button
        launch_btn = tk.Button(self.root, text="Launch Game", command=self.launch_selected_game)
        launch_btn.pack(pady=20)

        # Theme Selector Placeholder
        tk.Label(self.root, text="Themes and Customizer coming soon!").pack(pady=10)
        # Placeholder for future theme UI

    def refresh_games(self):
        # Refresh the list of available games
        games = [f for f in os.listdir(GAMES_DIR) if f.endswith(".swf") or f.endswith(".exe")]
        
        # Check for potential Flash Player executables in the games folder
        for game in games:
            game_path = os.path.join(GAMES_DIR, game)
            if is_potential_flash_player(game):
                result = messagebox.askyesno(
                    "Potential Flash Player Detected",
                    f"'{game}' appears to be a Flash Player executable. Would you like to move it to the 'players' folder?"
                )
                if result:  # User confirms
                    move_to_players(game_path)
                    games.remove(game)  # Remove from the list after moving

        self.game_menu["values"] = games
        if games:
            self.game_var.set(games[0])  # Auto-select the first game

    def launch_selected_game(self):
        selected_game = self.game_var.get()
        if not selected_game:
            messagebox.showerror("Error", "No game selected.")
            return

        game_path = os.path.join(GAMES_DIR, selected_game)
        if not os.path.exists(game_path):
            messagebox.showerror("Error", f"Game file not found: {selected_game}")
            return

        launch_flash_game(game_path)

# === Run ===
if __name__ == "__main__":
    # Ensure required folders exist
    for folder in [SKIN_DIR, GAMES_DIR, PLAYERS_DIR, THUMBNAILS_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    root = tk.Tk()
    app = AchiwaApp(root)
    root.mainloop()