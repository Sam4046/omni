from flask import Flask, render_template, redirect, url_for
from classes.mojo import Mojo  # dein bestehendes Modul
pk = Mojo()

app = Flask(__name__)

@app.route('/')
def index():
    frei = pk.get_parkp()
    return render_template('index.html', frei=frei)

@app.route('/tor-auf')
def tor_auf():
    pk.tor_auf()
    return redirect(url_for('index'))

@app.route('/tor-zu')
def tor_zu():
    pk.tor_zu()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)