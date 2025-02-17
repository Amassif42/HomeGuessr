import tkinter as tk
from tkinter import messagebox

def set_window_position(root, position):
    root.update_idletasks()  # Ensure the window dimensions are calculated
    if position:
        x = position["x"]
        y = position["y"]

        wwidth = root.winfo_width()
        wheight = root.winfo_height()

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate new position
        new_x = x - (wwidth // 2)
        new_y = y - (wheight // 2)

        # Ensure the window is within screen bounds
        if new_x < 0:
            new_x = 0
        elif new_x + wwidth > screen_width:
            new_x = screen_width - wwidth

        if new_y < 0:
            new_y = 0
        elif new_y + wheight > screen_height:
            new_y = screen_height - wheight

        root.geometry(f"+{new_x}+{new_y}")

def on_mouse_move(root):
    """Retourne la position actuelle de la souris sous forme de dictionnaire."""
    return {"x": root.winfo_pointerx(), "y": root.winfo_pointery()}

def winReponse(ls, position=None, max=6):

    root = tk.Tk()
    root.title("HoneGuessr")
    root.attributes('-topmost', True)  # Assure que la fenêtre soit au premier plan

    # Positionner la fenêtre
    set_window_position(root, position)

    clicked_button = tk.IntVar(value=-1)

    def on_button_click(button_id):
        clicked_button.set(button_id)
        root.destroy()

    if len(ls) > max:

        defaultText = "Choisissez une option"

        options = [defaultText] + [i for i in ls]
        print(options)
        selected_option = tk.StringVar(root)
        selected_option.set(options[0])  # Set default value

        dropdown = tk.OptionMenu(root, selected_option, *options)
        dropdown.pack(padx=10, pady=10)

        def on_select(*args):
            if selected_option.get() != defaultText:
                on_button_click(options.index(selected_option.get())-1)

        selected_option.trace("w", on_select)
    else:
        # Create buttons dynamically
        for i, e in enumerate(ls):
            button = tk.Button(root, text=e, command=lambda i=i: on_button_click(i))
            button.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()
    return clicked_button.get()

def secletPlayer(playerLs, position=None):
    print(position)
    selected_players = []

    def on_select(*args):
        selected_player = selected_option.get()
        if selected_player != defaultText:
            selected_players.append(selected_player)
            playerLs.remove(selected_player)
            root.destroy()

    def on_next():
        nonlocal playerLs
        playerLs=[]
        root.destroy()

    def on_close():
        nonlocal selected_players
        selected_players = []
        root.destroy()

    while playerLs:
        root = tk.Tk()
        root.title("Player selection")
        root.attributes('-topmost', True)  # Ensure the window is on top

        if position:
            print("test")
            set_window_position(root, position)

        defaultText = "Choisissez un joueur"
        options = [defaultText] + playerLs
        selected_option = tk.StringVar(root)
        selected_option.set(options[0])  # Set default value

        dropdown = tk.OptionMenu(root, selected_option, *options)
        dropdown.pack(padx=10, pady=10)

        message = "Liste des joueurs sélectionnés:\n"
        for player in selected_players:
            message += player + " "
        label = tk.Label(root, text=message)
        label.pack(padx=10, pady=10)

        selected_option.trace_add("write", on_select)

        next_button = tk.Button(root, text="Valider", command=on_next)
        next_button.pack(padx=10, pady=10)

        root.protocol("WM_DELETE_WINDOW", on_close)

        root.mainloop()

    return selected_players

def retour(io, score, reponse):
    root = tk.Tk()
    root.title("Info")
    root.attributes('-topmost', True)  # Ensure the window is on top

    position = on_mouse_move(root)

    if position:
        set_window_position(root, position)

    message = "Félicitation 🎉🎉" if io else "Echéque ):"
    message += f"\n La réponse était {reponse}"
    message += f"\n Votre score est de {score}"
    label = tk.Label(root, text=message)
    label.pack(padx=10, pady=10)

    def on_next():
        root.destroy()

    button = tk.Button(root, text="Next", command=on_next)
    button.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    playerLs = ["player1", "player2", "player3", "player4", "player5", "player6", "player7", "player8", "player9", "player10"]
    p = {"x": 500, "y": 500}
    print(secletPlayer(playerLs, p))