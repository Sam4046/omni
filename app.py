from flask import Flask, render_template, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# === Statusdateien ===
CMD_PATH = "ipc/command.json"
STATUS_PATH = "ipc/last_status.json"

@app.route('/')
def index():
    # Status aus Datei lesen
    try:
        with open(STATUS_PATH, "r") as f:
            status = json.load(f)
    except:
        status = {"frei": "?", "tor_offen": False}

    return render_template('index.html',
                           frei=status.get("frei", "?"),
                           status="offen" if status.get("tor_offen") else "geschlossen",
                           running=True)

@app.route('/tor-auf')
def tor_auf():
    return redirect(url_for('send_cmd', cmd="tor_auf"))

@app.route('/tor-zu')
def tor_zu():
    return redirect(url_for('send_cmd', cmd="tor_zu"))

@app.route('/key')
def key_control():
    return render_template('key.html')


@app.route('/api/status')
def status():
    try:
        with open(STATUS_PATH, "r") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"frei": "?", "tor_offen": False})

@app.route('/api/send/<cmd>')
def send_cmd(cmd):
    erlaubte_befehle = [
        "tor_auf", "tor_zu",
        "step_up", "step_down",
        "reset_pos", "reset_parkp"
    ]

    if cmd not in erlaubte_befehle:
        return jsonify(success=False, error="Ungültiger Befehl")

    try:
        with open("ipc/command.json", "w") as f:
            json.dump({"action": cmd}, f)
        return jsonify(success=True, cmd=cmd)
    except Exception as e:
        return jsonify(success=False, error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)