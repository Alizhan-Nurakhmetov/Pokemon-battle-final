from pathlib import Path
import logging
import sqlite3
from contextlib import closing

def database():
    """Open the battle database"""
    return sqlite3.connect(Path(__file__).with_name("battles.db"))

def setup_history():
    """Set up the database and log"""
    logging.basicConfig(filename=Path(__file__).with_name("game.log"), level = logging.INFO, format="%(asctime)s %(message)s")
    with closing(database()) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS turns (battle_id TEXT, turn INTEGER, trainer TEXT, move TEXT,message TEXT, won INTEGER, PRIMARY KEY (battle_id, turn))""")
        db.commit()

def save(battle, move, message, won=None):
    """Save one turn and its result"""
    values = (battle["id"], battle["turn"], battle ["trainer"], move, message, won)
    with closing(database()) as db:
        try:
            db.execute("INSERT INTO turns VALUES (?, ?, ?, ?, ?, ?)", values)
            db.commit()
        except sqlite3.IntegrityError:
            raise ValueError("This turn was already played. Refresh the page") from None
    logging.info("%s | %s | %s", battle["trainer"], move, message)

def read_history():
    """Get the last 30 turns"""
    with closing(database()) as db:
        return db.execute("SELECT trainer, move, message FROM turns ORDER BY rowid DESC LIMIT 30").fetchall()

