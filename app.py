from flask import Flask, render_template, request, redirect, url_for, send_file
from flask import Flask, request, render_template
import os
from steganography import encode_text, decode_text

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files or "message" not in request.form:
        return "No image or message provided!"

    image = request.files["image"]
    message = request.form["message"]

    if image.filename == "":
        return "No file selected!"

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded.png")
    image.save(save_path)

    output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.png")
    encode_text(save_path, message, output_path)

    return render_template("result.html", mode="encrypt", output_image="output.png")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files:
        return "No image provided!"

    image = request.files["image"]

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded.png")
    image.save(save_path)

    hidden_text = decode_text(save_path)

    return render_template("result.html", mode="decrypt", hidden_text=hidden_text)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)