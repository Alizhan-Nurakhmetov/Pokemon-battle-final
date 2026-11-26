from sqlite3 import Error
from flask import Flask, flash, redirect, render_template, request, session
from battle import starters
from game import begin, take_turn
from history import read_history, setup_history, standings

def create_app():
    """Build the Flask app"""
    app = Flask(__name__)
    app.config.from_pyfile(".env")
    setup_history()
    @app.route("/", methods=["GET", "POST"])
    def page():
        """Handle the players menu choice"""
        if request.method == "POST":
            action = request.form.get("action")
            if action in ("menu", "exit"):
                session.clear()
                return redirect("/?show=exit" if action == "exit" else "/")
            try:
                value = request.form.get("value", "")
                if action == "start":
                    battle, message = begin(request.form.get("trainer", ""), value)
                elif action == "attack":
                    battle, message = take_turn(session.get("battle"), value)
                else:
                    raise ValueError("Unknown menu choice")
                session["battle"] = battle
                flash(message)
            except ValueError as error:
                flash(str(error))
            except (OSError, Error):
                flash ("Could not read or save the game files")
            return redirect("/")
        screen = request.args.get("show")
        rows, total = standings() if screen =="scores" else ([], 0)
        log = read_history() if screen == "history" else ""
        return render_template("index.html", starters=starters(), battle = session.get("battle"), screen = screen,rows = rows, total=total, log = log)
    return app
