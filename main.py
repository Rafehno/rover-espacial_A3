import os
from flask import Flask, request, jsonify, send_from_directory

from models.lexer import tokenize
from models.parser import parse
from models.interpreter import interpret
from models.rover import Rover
from models.grid import Grid

app = Flask(__name__)

FRONTEND = os.path.join(os.path.dirname(__file__), "frontend")


# ── Static pages ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(os.path.join(FRONTEND, "html"), "index.html")

@app.route("/docs")
def docs():
    return send_from_directory(os.path.join(FRONTEND, "html"), "docs.html")

@app.route("/about")
def about():
    return send_from_directory(os.path.join(FRONTEND, "html"), "about.html")

@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(FRONTEND, "css"), filename)

@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(os.path.join(FRONTEND, "js"), filename)


# ── API routes ───────────────────────────────────────────────────────────────

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json(force=True)
    tokens, lex_errors = tokenize(data.get("script", ""))
    success, errors = parse(tokens, lex_errors)
    return jsonify({"success": success, "errors": errors})


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json(force=True)

    tokens, lex_errors = tokenize(data.get("script", ""))
    success, errors = parse(tokens, lex_errors)

    if not success:
        return jsonify({"success": False, "errors": errors, "steps": [], "log": [], "final_state": None, "grid": None})

    rover = Rover(
        x=data.get("start_x", 0),
        y=data.get("start_y", 0),
        direction=data.get("start_dir", "N"),
    )
    grid = Grid(
        width=data.get("width", 10),
        height=data.get("height", 10),
        obstacles=data.get("obstacles", []),
    )

    steps, log = interpret(tokens, rover, grid)

    return jsonify({
        "success": True,
        "errors": [],
        "steps": steps,
        "log": log,
        "final_state": rover.to_dict(),
        "grid": grid.to_dict(),
    })


if __name__ == "__main__":
    app.run(debug=True)
