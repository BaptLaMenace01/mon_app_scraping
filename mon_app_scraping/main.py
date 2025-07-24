from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import os
from script_pappers import lancer_collecte_pappers
from enrichisseur import lancer_enrichissement

app = Flask(__name__)
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    fichier_enrichi = request.args.get("fichier")
    return render_template("index.html", fichier=fichier_enrichi)

@app.route("/pappers", methods=["POST"])
def run_pappers():
    try:
        output_csv = lancer_collecte_pappers(UPLOAD_FOLDER)
        return redirect(url_for("index", fichier=output_csv))
    except Exception as e:
        return f"Erreur scraping Pappers : {e}"

@app.route("/enrich", methods=["POST"])
def run_enrich():
    if "fichier" not in request.files:
        return "Fichier manquant"
    fichier = request.files["fichier"]
    chemin = os.path.join(UPLOAD_FOLDER, fichier.filename)
    fichier.save(chemin)
    try:
        output = lancer_enrichissement(chemin)
        return redirect(url_for("index", fichier=output))
    except Exception as e:
        return f"Erreur enrichissement : {e}"

@app.route("/static/<path:filename>")
def telecharger(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
