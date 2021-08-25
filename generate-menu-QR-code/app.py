from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import qrcode
from PIL import Image
import socket
import os
import re
import random
import time

app = Flask(__name__, static_url_path='/static/')
url_domain = 'http://localhost/display_menu/'

app.config['UPLOAD_FOLDER'] = '/static/'
#app.config['MAX_CONTENT_PATH'] = 


#Internal functions
def generate_random_url():
   """Generates and returns 3x english words concatenated to use for random URL"""
   url_string = ''

   f = open('word_file.txt', 'r')
   word_list = f.read().split()
   word_file_length = len(word_list)

   for i in range(3):
      url_string += word_list[random.randint(0,word_file_length)].capitalize()   #Capitalize and add random word from word_list, to string
   
   re.sub(r'\W+', '', url_string.lower().strip())

   print(f'New URL generated: {url_string}')

   return(url_string)


def generate_qr_code(url_subdirectory):
   """When given url_subdirectory, generates QR code to URL, overlays logo file, and saves with URL subdirectory filename"""

   #Set QR code parameters
   qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_H,
      box_size=10,
      border=4,
   )

   #Generate QR code
   qr.add_data(f'{url_domain}{url_subdirectory}')
   qr.make(fit=True)
   img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
   img.save(f'{url_subdirectory}_qrcode.png')
   print('QR code generated')

   #Overlay logo
   logo_display = Image.open(f'{url_subdirectory}_logo.png')
   logo_display.thumbnail((150, 150))
   logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
   img.paste(logo_display, logo_pos)
   print('QR logo overlaid')

   #Save file to directory
   img.save(f'{url_subdirectory}_qrcode_logo.png')
   print(f'New QR code saved to: {url_subdirectory}_qrcode.png')

def generate_pdf(logo):
   """Generates a pdf of the QR code, to print"""
   pass



#Routes
@app.route("/")
def index():
    return redirect('/upload')

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      random_url = generate_random_url()

      f = request.files['menu']
      f.filename = random_url + '_menu' + os.path.splitext(f.filename)[1]
      f.save(secure_filename(f.filename))

      f = request.files['logo']
      f.filename = random_url + '_logo' + os.path.splitext(f.filename)[1]
      f.save(secure_filename(f.filename))

      generate_qr_code(random_url)        #Generate the QR barcode

      time.sleep(1)        #Wait for the QR barcode to be saved properly, to avoid race conditions

      return redirect(f'/display_QR_code/{random_url}')        #Re-direct to page to display QR barcode


@app.route("/display_QR_code/<url_subdirectory>")
def display_QR_code(url_subdirectory):
   context={}
   context['url_subdirectory'] = url_subdirectory
   context['filename'] = url_subdirectory + '_qrcode_logo.png'
   return render_template('display_QR_code.html', context=context)


@app.route("/display_menu/<url_subdirectory>")
def display_subdirectory(url_subdirectory):
   context={}
   context['url_subdirectory'] = url_subdirectory
   context['filename'] = url_subdirectory + '_menu.pdf'
   return render_template('url_subdirectory.html', context=context)


if __name__ == '__main__':
   #ip = socket.gethostbyname(socket.gethostname())
   app.run(debug = True)


generate_qr_code('UpstartleTrisaccharideUntimeously')