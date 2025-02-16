
import gui
import files
import browser

import random
import os

# récupère url dans le .env
URL = os.getenv("URL")

# demande un entier positif a l'utilisateur
def askInt(message, default):
    while True:
        try:
            v = input(message)
            if v == "":
                print(f"Valeur par défaut : {default}")
                return default
            n = int(v)
            if n > 0:
                return n
            else:
                print("Veuillez entrer un entier positif.")
        except ValueError:
            print("Veuillez entrer un entier positif.")

def askYN(message):
    while True:
        v = input(message).lower()
        if v in ["y", "yes"]:
            return True
        elif v in ["n", "no", ""]:
            return False
        else:
            print("Veuillez répondre par 'y' ou 'n'.")

def main():
    nbrGames = askInt("Nombre de partie : ", 3)
    playerLs = files.playerLs(files.uuidList())
    print("Liste des joueurs :")
    for player in playerLs:
        print(f"{player}", end=" ")
    print()
    if askYN("Voulez vous modifier la list des joueur ? (y/N) : "):
        playerLs = gui.secletPlayer(playerLs)

    zoom = askInt("Zoom : ", 6)

    numberResponse = 4

    score = 0

    json = files.playerFiltre(playerLs, files.homesLs(files.uuidList()))

    for _ in range(nbrGames):
        element = random.choice(json)
        other = files.otherHomes(element, json)

        url = f"{URL}/?worldname=world&mapname=surface&zoom={zoom}&x={element["pos"][0]}&y=64&z={element["pos"][1]}"
        reponseId = random.randint(0, numberResponse-1)

        ls = [None] * numberResponse
        ls[reponseId] = element
        for i, e in enumerate(ls):
            if e:
                pass
            else:
                o = random.choice(other)
                other = files.otherHomes(o, json)
                ls[i] = o

        responseLs = [f"{e["name"]} ({e["player"]})" for e in ls]

        print("chargement...")
        response = browser.main(url, responseLs)
        if response == reponseId:
            score += 1
            gui.retour(True, score, responseLs[reponseId])
        else:
            gui.retour(False, score, responseLs[reponseId])

    print("fin")
    

if __name__ == "__main__":
    main()