
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import subprocess

# === Core Directories ===
SKIN_DIR = "skins"
GAMES_DIR = "games"
SETTINGS_FILE = "settings.json"

# === Load Settings ===
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return {"theme": "default"}

        save_settings(settings)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# === Load Theme ===
def load_theme(name):
    path = os.path.join(SKIN_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "background": "#1e1e1e", "foreground": "#dcdcdc",
        "accent": "#00bcd4", "font": "Consolas"
    }

# === Flash Player Fallback Rotation ===
FLASH_PLAYERS = [
    "players/Macromedia Flash Player 3.0/flashplayer.exe",
    "players/Macromedia Flash Player 4.0/flashplayer.exe",
    "players/Macromedia Flash Player 8.0/flashplayer.exe",
    "players/Adobe Flash Player 9.0/flashplayer.exe"
]

def launch_flash_game(path):
    for player in FLASH_PLAYERS:
        if os.path.exists(player):
            try:
                subprocess.Popen([player, path], shell=True)
                return
            except:
                continue
    messagebox.showerror("Error", "No flash player succeeded.")

# === App ===
class AchiwaApp:
    def __init__(self, root):
        self.settings = load_settings()
        self.theme = load_theme(self.settings["theme"])
        self.root = root
        self.root.title("AchiwaOS")
        self.root.configure(bg=self.theme["background"])
        self.root.geometry("700x500")

        self.build_ui()
        self.apply_theme()

    def build_ui(self):
        # Skin Dropdown
        self.skin_var = tk.StringVar(value=self.settings["theme"])
        skins = [f.replace(".json", "") for f in os.listdir(SKIN_DIR)]
        tk.Label(self.root, text="Theme:", bg=self.theme["background"],
                 fg=self.theme["foreground"]).pack(pady=5)
        skin_menu = ttk.Combobox(self.root, values=skins, textvariable=self.skin_var)
        skin_menu.pack()
        skin_menu.bind("<<ComboboxSelected>>", self.change_skin)

        # Game Selector
        self.game_var = tk.StringVar()
        tk.Label(self.root, text="Select Game:", bg=self.theme["background"],
                 fg=self.theme["foreground"]).pack(pady=10)
        self.game_menu = ttk.Combobox(self.root, textvariable=self.game_var)
        self.game_menu.pack()
        self.refresh_games()

        # Launch Button
        launch_btn = tk.Button(self.root, text="Launch Game",
                               command=self.launch_selected_game,
                               bg=self.theme["accent"], fg=self.theme["background"])
        launch_btn.pack(pady=20)

    def refresh_games(self):
        swfs = [f for f in os.listdir(GAMES_DIR) if f.endswith(".swf")]
        self.game_menu["values"] = swfs
        if swfs:
            self.game_var.set(swfs[0])

    def launch_selected_game(self):
        game = self.game_var.get()
        if game:
            launch_flash_game(os.path.join(GAMES_DIR, game))

    def change_skin(self, _):
        self.settings["theme"] = self.skin_var.get()
        save_settings(self.settings)
        self.theme = load_theme(self.skin_var.get())
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.theme["background"])
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button)):
                widget.configure(bg=self.theme["background"], fg=self.theme["foreground"])
            if isinstance(widget, ttk.Combobox):
                widget.configure(background=self.theme["background"], foreground=self.theme["foreground"])

# === Run ===
if __name__ == "__main__":
    if not os.path.exists(SKIN_DIR): os.makedirs(SKIN_DIR)
    if not os.path.exists(GAMES_DIR): os.makedirs(GAMES_DIR)
    root = tk.Tk()
    app = AchiwaApp(root)
    root.mainloop()
player_dropdown.bind('<<ComboboxSelected>>', save_player_selection)
        save_settings(settings)

# --- Flash Player Dropdown [FINAL FIX] ---
player_frame = tk.Frame(root, bg=THEME['background'])
player_frame.grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))
tk.Label(player_frame, text='Select Flash Player:', bg=THEME['background'], fg=THEME['accent'], font=(THEME['font'], 10)).grid(row=0, column=0, sticky='w')
player_dropdown = ttk.Combobox(player_frame, values=get_flash_players(), state='readonly', width=60)
player_dropdown.set(settings.get('player', ''))
player_dropdown.grid(row=0, column=1, sticky='w', padx=(10, 0))

def save_player_selection(event):
    selected = player_dropdown.get()
    settings['player'] = selected
    save_settings(settings)
    logging.info(f"Flash player selected: {selected}")
