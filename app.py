from flask import Flask, request, send_file
import os
import subprocess
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def download_file(url, dest_path):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error on bad status
    with open(dest_path, 'wb') as file:
        file.write(response.content)

def run_blender_script(video_path, aston_band_path, output_path):
    blender_path = "C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe"
    if not os.path.exists(blender_path):
        raise FileNotFoundError(f"Blender executable not found: {blender_path}")

    command = [
        blender_path,
        "--background",
        "--python",
        "G:\\TruAd\\Aston Band\\server\\blender.py",
        "--",
        video_path,
        aston_band_path,
        output_path
    ]

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video path not found: {video_path}")
    if not os.path.exists(aston_band_path):
        raise FileNotFoundError(f"Aston band script path not found: {aston_band_path}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Blender process failed with error: {e}")

@app.route('/process', methods=['POST'])
def process():
    video_url = request.form['video_url']
    aston_band_url = request.form['aston_band_url']

    video_path = os.path.join(app.instance_path, 'video.mp4')
    aston_band_path = os.path.join(app.instance_path, 'aston_band.png')
    output_path = os.path.join(app.instance_path, 'output.mp4')

    if os.path.exists(output_path):
        os.remove(output_path)

    try:
        # Download the files from the provided URLs
        download_file(video_url, video_path)
        download_file(aston_band_url, aston_band_path)

        # Run the Blender script
        run_blender_script(video_path, aston_band_path, output_path)
    except Exception as e:
        return str(e), 500
    finally:
        # Delete input files after processing
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(aston_band_path):
            os.remove(aston_band_path)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "Output file was not created", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
