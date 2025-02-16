import tkinter as tk
from tkinter import messagebox

def winReponse(ls, position=None, max=6):

    root = tk.Tk()
    root.title("Button Clicker")
    root.attributes('-topmost', True)  # Assure que la fenêtre soit au premier plan


    # Positionner la fenêtre
    if position:
        x = position["x"]
        y = position["y"]
        root.geometry(f"+{x}+{y}")

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
        root.title("Select Player")
        root.attributes('-topmost', True)  # Ensure the window is on top

        if position:
            x = position["x"]
            y = position["y"]
            root.geometry(f"+{x}+{y}")

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

def retour(io, score, reponse, position=None):
    root = tk.Tk()
    root.title("Message")
    root.attributes('-topmost', True)  # Ensure the window is on top

    if position:
        x = position["x"]
        y = position["y"]
        root.geometry(f"+{x}+{y}")

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
    print(secletPlayer(playerLs))