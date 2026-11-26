import re
from uuid import uuid4
from battle import play, start
from history import save

def trainer_name(text):
    """Check the trainer name"""
    name = text.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{1,15}", name):
        raise ValueError("Use 2-16 letters, numbers or underscores. Start with a letter")
    return name
 
def begin(name, starter):
    """Save the opening matchup"""
    trainer = trainer_name(name)
    battle = start(starter)
    battle["trainer"] = trainer
    battle["id"] = uuid4().hex
    battle["turn"] = 0
    player, rival = battle["fighters"]
    message = f"{player['name']} faces {rival['name']}"
    save(battle, starter, message)
    return battle, message

def take_turn(battle, move):
    """Play and save one turn"""
    updated, message = play(battle, move)
    updated["trainer"] = battle["trainer"]
    updated["id"] = battle["id"]
    updated["turn"] = battle["turn"] + 1
    won = None
    if 0 in updated["hp"]:
        won = int(updated["hp"][1] == 0)
    save(updated, move, message, won)
    return updated, message
