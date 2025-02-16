import os
import functools
import yaml
import json

@functools.cache
def uuidList(dossier=r".\player"):
    try:
        return [os.path.splitext(f)[0] for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    except FileNotFoundError:
        print(f"Le dossier '{dossier}' n'existe pas.")
        return []
    except PermissionError:
        print(f"Permission refusée pour accéder au dossier '{dossier}'.")
        return []

def homesLs(uuidLs):
    """Convertit un fichier YAML en JSON avec les positions arrondies."""
    ls = []
    for uuid in uuidLs:
        full_path = os.path.join(r".\player", uuid + ".yml")
        with open(full_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        
        homes = data.get("homes", {})
        player = data.get("lastAccountName", {})
        ls += [{"player": player, "name": name, "pos": [round(home["x"]), round(home["z"])]} for name, home in homes.items() if home["world"] == "world"]
        
    return ls

def playerFiltre(playerLs, json_data):
    new_json = []
    for e in json_data:
        if e["player"] in playerLs:
            new_json += [e]
    return new_json

def playerLs(uuidLs):
    """Convertit un fichier YAML en JSON avec les positions arrondies."""
    ls = []
    for uuid in uuidLs:
        full_path = os.path.join(r".\player", uuid + ".yml")
        with open(full_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        
        player = data.get("lastAccountName", {})
        ls += [player]
        
    return ls

def distanceVerif(coord1, coord2, r=32):
    """Vérifie si les coordonnées sont à plus de r unités de distance."""
    x1, z1 = coord1
    x2, z2 = coord2
    return abs(x1 - x2) > r or abs(z1 - z2) > r

def otherHomes(homeJson, json):
    pos = homeJson["pos"]
    return [e for e in json if distanceVerif(pos, e["pos"])]