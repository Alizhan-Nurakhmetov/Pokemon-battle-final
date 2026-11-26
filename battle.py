import json
from functools import lru_cache
from random import choice
from urllib.request import Request, urlopen
from moves import damage

def starters():
    """List the three starters"""
    return ("bulbasaur", "charmander", "squirtle")

@lru_cache(maxsize = 3)
def fetch_pokemon(name):
    """Load type and HP"""
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
    request = Request(url, headers={"User-Agent": "StarterBattle/2.0"})
    with urlopen(request, timeout = 3) as response:
        data = json.load(response)
    kind = data["types"][0]["type"]["name"]
    for stat in data["stats"]:
        if stat["stat"]["name"] == "hp":
            return {"name" : data["name"].title(), "type":kind, "hp": stat["base_stat"], "source": "PokeAPI"}
    raise ValueError("Missing HP")

def get_pokemon(name):
    """Use an offline card if needed"""
    if name not in starters():
        raise ValueError("choose one of the three starters")
    try:
        return fetch_pokemon(name)
    except (OSError, ValueError, KeyError, IndexError, TypeError):
            cards= {"bulbasaur":("grass", 45), "charmander":("fire", 39), "squirtle":("water", 44)}
    kind, hp = cards[name]
    return {"name": name.title(), "type": kind, "hp":hp, "source":"Offline card"}

def start(name):
    """Set up a battle"""
    rivals = list(starters())
    if name not in rivals:
        raise ValueError("Choose one of the three starters")
    rivals.remove(name)
    player = get_pokemon(name)
    rival = get_pokemon(choice(rivals))
    return {"fighters": [player, rival], "hp": [player["hp"], rival["hp"]]}

def play(battle, attack):
    """Play a turn and return a message"""
    attacks = ("Basic", "Type")
    if not battle or 0 in battle["hp"]:
        raise ValueError("Start a new battle first")
    if attack not in attacks:
        raise ValueError("Choose Basic or Type")
    player, rival = battle["fighters"]
    hp = battle["hp"].copy()
    hit = damage(attack, player, rival)
    hp[1] = max(0, hp[1] - hit)
    message = f"{player['name']} dealt {hit} damage"
    if hp[1] == 0:
        message += ". You win!"
    else:
        reply = choice(attacks)
        hit = damage (reply, rival, player)
        hp[0] = max(0, hp[0] - hit)
        message += f" {rival['name']} dealt {hit} damage"
        if hp[0] == 0:
            message += ". You lose!"
    return {"fighters": battle["fighters"], "hp": hp}, message

