from flask import Flask, request, render_template_string, send_file
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        input_path = os.path.join(UPLOAD_FOLDER, f.filename)
        output_path = os.path.join(UPLOAD_FOLDER, f"enrichi_{f.filename}")
        f.save(input_path)

        subprocess.run(['python3', 'script_pappers.py', input_path, output_path])

        return send_file(output_path, as_attachment=True)

    return render_template_string('''
        <h2>Uploader un fichier CSV</h2>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Uploader>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)

from mon_app_scraping.script_pappers import lancer_collecte_pappers

@app.route("/scraper", methods=["POST"])
def scraper_pappers():
    codes_postaux_str = request.form.get("codes_postaux", "")
    age_max = int(request.form.get("age_max", "1"))
    max_total = int(request.form.get("max_total", "10"))

    codes_postaux = [cp.strip() for cp in codes_postaux_str.split(",") if cp.strip()]

    try:
        nom_fichier = lancer_collecte_pappers(
            dossier_sortie="mon_app_scraping/static",
            codes_postaux=codes_postaux,
            max_age_annees=age_max,
            max_total=max_total
        )
        return redirect(f"/static/{nom_fichier}")
    except Exception as e:
        return f"Erreur : {str(e)}"



