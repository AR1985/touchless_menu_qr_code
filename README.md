# Touchless Menu Generator with QR Code
A website that allows you to upload a menu and logo, and generates the QR code with your logo, for touchless ordering

With the rise of COVID-19, the restaurant industry has changed, with many preferring to go with touchless ordering.  This website allows restaurants to create and host their menus in a touchless manner, without the need for excessive costs or complication.

***Please note this website is only a prototype example and not intended to support actual QR codes for websites, which are wiped semi-regularly***


## Version
V1 - MVP
This version was put together as an initial proof of concept, without much thought to architecture.
The architecture employs a manually configured EC2 instance, running a Flask server, and saving uploaded files to the EC2 root directory.


## How to Use
1. Navigate to http://touchless-menu-qr-code.us-east-2.elasticbeanstalk.com/
2. Upload your menu in PDF format and logo in PNG format
3. Download and print the QR code
4. Post the QR code on the restaurant tables


## Example
<img src="https://i.imgur.com/ou1RDBB.jpeg">


## Sign Holders (to hold QR code)
https://www.amazon.ca/s?k=sign+holder+4+x+6&ref=nb_sb_noss



