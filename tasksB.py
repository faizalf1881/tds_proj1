import os
import requests
import sqlite3
import duckdb
import markdown
from PIL import Image
from flask import Flask, request, jsonify
import subprocess
import pandas as pd

def B12(filepath):
    if filepath.startswith('/data'):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        return None
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

def B4(repo_url, commit_message):
    repo_path = "/data/repo"
    if not B12(repo_path):
        return None
    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git Operation Failed: {e}")

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(db_path):
        return None
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not B12(image_path):
        return None
    if not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

def B8(audio_path):
    import openai
    if not B12(audio_path):
        return None
    try:
        with open(audio_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript
    except Exception as e:
        print(f"Audio Transcription Failed: {e}")

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

app = Flask(__name__)

@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    try:
        data = request.json
        csv_path = data.get('csv_path')
        filter_column = data.get('filter_column')
        filter_value = data.get('filter_value')

        if not B12(csv_path):
            return jsonify({"error": "Access Denied"}), 403

        df = pd.read_csv(csv_path)
        filtered = df[df[filter_column] == filter_value]
        return jsonify(filtered.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500