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

