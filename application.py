from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import qrcode
from PIL import Image
import os
import re
import random
import time

application = Flask(__name__, static_url_path="/static/")

application.config["UPLOAD_PATH"] = "static"
application.config["MAX_CONTENT_PATH"] = 5 * 1024 * 1024  # 5MB max upload size


# Internal functions
def generate_random_url():
    """Generates and returns 3x english words concatenated to use for
    random URL"""

    url_string = ""

    f = open("word_file.txt", "r")
    word_list = f.read().split()
    word_file_length = len(word_list)

    for i in range(3):
        url_string += word_list[
            random.randint(0, word_file_length)
        ].capitalize()  # Capitalize and add random word from word_list

    re.sub(r"\W+", "", url_string.lower().strip())

    print(f"New URL generated: {url_string}")

    return url_string


def generate_qr_code(url_subdirectory):
    """When given url_subdirectory, generates QR code to URL, overlays logo file,
    and saves with URL subdirectory filename"""

    # Set QR code parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Generate QR code
    hostname = request.base_url.rsplit("/", 1)[0]
    qr.add_data(
        f"{hostname}/display_menu/{url_subdirectory}"
    )  # URL for embedded data in QR barcode
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(f"static/{url_subdirectory}_qrcode.png")
    print("QR code generated")

    # Overlay logo
    logo_display = Image.open(f"static/{url_subdirectory}_logo.png")
    logo_display.thumbnail((150, 150))
    logo_pos = (
        (img.size[0] - logo_display.size[0]) // 2,
        (img.size[1] - logo_display.size[1]) // 2,
    )
    img.paste(logo_display, logo_pos)
    print("QR logo overlaid")

    # Save file to directory
    img.save(f"static/{url_subdirectory}_qrcode_logo.png")
    print(f"New QR code saved to: static/{url_subdirectory}_qrcode.png")


# Routes
@application.route("/")
def index():
    return redirect("/upload")


@application.route("/upload")
def upload():
    return render_template("upload.html")


@application.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        random_url = generate_random_url()

        f = request.files["menu"]
        f.filename = secure_filename(
            random_url + "_menu" + os.path.splitext(f.filename)[1]
        )
        f.save(os.path.join(application.config["UPLOAD_PATH"], f.filename))

        f = request.files["logo"]
        f.filename = secure_filename(
            random_url + "_logo" + os.path.splitext(f.filename)[1]
        )
        f.save(os.path.join(application.config["UPLOAD_PATH"], f.filename))

        generate_qr_code(random_url)  # Generate the QR barcode

        time.sleep(1)  # Wait for QR barcode to save, to avoid race conditions

        return redirect(
            f"/display_QR_code/{random_url}"
        )  # Re-direct to page to display QR barcode


@application.route("/display_QR_code/<url_subdirectory>")
def display_QR_code(url_subdirectory):
    context = {}
    context["url_subdirectory"] = url_subdirectory
    context["filename"] = url_subdirectory + "_qrcode_logo.png"
    return render_template("display_QR_code.html", context=context)


@application.route("/display_menu/<url_subdirectory>")
def display_subdirectory(url_subdirectory):
    context = {}
    context["url_subdirectory"] = url_subdirectory
    context["filename"] = url_subdirectory + "_menu.pdf"
    return render_template("url_subdirectory.html", context=context)


if __name__ == "__main__":
    application.run(debug=True)
