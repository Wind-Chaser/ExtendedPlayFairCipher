from flask import Flask, redirect, url_for, request,jsonify,render_template
import numpy as np
from PIL import Image
from flask import send_file,send_from_directory
import re
import string
import itertools
import sys
import os
####+++++++++++++++++++++MAIN PROGRAM STARTS HERE++++++++++++++++++++++++++++++++++++####
#$$$$$$$$$$$$$$$$$$$$$$$$KKKKKKKKKKKKKKKKKKDDDDDDDDDDDDDDDDDDDDDDDDD$$$$$$$$$$$$$$$$$$$$
#________________________________________________________________________________#

def chunker(seq, size):
    it = iter(seq)
    while True:
       chunk = tuple(itertools.islice(it, size))
       if not chunk:
           return
       yield chunk



def prepare_input(dirty):
    """
    Prepare the plaintext by up-casing it
    and separating repeated letters with X's
    """
   
    dirty = re.sub('\s+', '|', dirty)  
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+={}[]|\:;\"'<>./?"
    dirty = ''.join([c.upper() for c in dirty if c in (alphabet)])
    clean = ""
    
    if len(dirty) < 2:
        return dirty
    
    for i in range(len(dirty)-1):
        clean += dirty[i]
        
        if dirty[i] == dirty[i+1]:
            clean += '^'
    
    clean += dirty[-1]

    if len(clean) & 1:
        clean += '|'

    return clean

def generate_table(key):


    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+={}[]|\:;\"'<>./?"
    
 
    table = []

    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)


    for char in alphabet:
        if char not in table:
            table.append(char)
   
    return table

def encode(plaintext, key):
    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    ciphertext = ""
    print plaintext
    
    for char1, char2 in chunker(plaintext, 2):
        row1, col1 = divmod(table.index(char1), 8)
        row2, col2 = divmod(table.index(char2), 8)

        if row1 == row2:
            ciphertext += table[row1*8+(col1+1)%8]
            ciphertext += table[row2*8+(col2+1)%8]
        elif col1 == col2:
            ciphertext += table[((row1+1)%8)*8+col1]
            ciphertext += table[((row2+1)%8)*8+col2]
        else: # rectangle
            ciphertext += table[row1*8+col2]
            ciphertext += table[row2*8+col1]

    return ciphertext


def decode(ciphertext, key):
    table = generate_table(key)
    plaintext = ""


    for char1, char2 in chunker(ciphertext, 2):
        row1, col1 = divmod(table.index(char1), 8)
        row2, col2 = divmod(table.index(char2), 8)

        if row1 == row2:
            plaintext += table[row1*8+(col1-1)%8]
            plaintext += table[row2*8+(col2-1)%8]
        elif col1 == col2:
            plaintext += table[((row1-1)%8)*8+col1]
            plaintext += table[((row2-1)%8)*8+col2]
        else: # rectangle
            plaintext += table[row1*8+col2]
            plaintext += table[row2*8+col1]
            
    while plaintext.find("^")!=-1 :
       plaintext =plaintext.replace("^","")
    while plaintext.find("|")!=-1:
        plaintext=plaintext.replace("|"," ")            
    return plaintext
    

  
# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
          
        # list of binary codes 
        # of given data 
        newd = []  
          
        for i in data: 
            newd.append(format(ord(i), '08b')) 
        return newd 
          
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
      
    datalist = genData(data) 
    lendata = len(datalist) 
    imdata = iter(pix) 
    

    
    for i in range(lendata): 
          
        # Extracting 3 pixels at a time 
        pix = [value for value in imdata.next()[:3] +
                                  imdata.next()[:3] +
                                  imdata.next()[:3]] 
        #print pix                                  
        # Pixel value should be made  
        # odd for 1 and even for 0 
        for j in range(0, 8): 
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
                  
                if (pix[j]% 2 != 0): 
                    pix[j] += 1
                      
            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
                pix[j] += 1
                  
        # Eigh^th pixel of every set tells  
        # whether to stop ot read further. 
        # 0 means keep reading; 1 means the 
        # message is over. 
        if (i == lendata - 1): 
            if (pix[-1] % 2 == 0): 
                pix[-1] += 1
        else: 
            if (pix[-1] % 2 != 0): 
                pix[-1] += 1
  
        pix = tuple(pix) 
        yield pix[0:3] 
        yield pix[3:6] 
        yield pix[6:9] 
  
def encode_enc(newimg, data): 
    w = newimg.size[0] 
    (x, y) = (0, 0) 
      
    for pixel in modPix(newimg.getdata(), data): 
          
        # Putting modified pixels in the new image 
        newimg.putpixel((x, y), pixel) 
        if (x == w - 1): 
            x = 0
            y += 1
        else: 
            x += 1
              
# Encode data into image 
def encodeIntoImage(data,img): 
    # img = input("Enter image name(with extension): ") 
    image = Image.open(img, 'r') 
      
    # data = input("Enter data to be encoded : ") 
    if (len(data) == 0): 
        raise ValueError('Data is empty') 
          
    newimg = image.copy() 
    print img.filename
    encode_enc(newimg, data) 
    f = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    newimg.save(f)  
    # new_img_name = input("Enter the name of new image(with extension): ") 
    # newimg.save(new_img_name, str(new_img_name.split(".")[1].upper())) 
    #newimg.save(img.filename)
    return jsonify({"value":1,"imageName":img.filename})
  
# Decode the data in the image 
def decodeIntoText(img): 
    # img.show()
    image = Image.open(img, 'r') 
      
    data = '' 
    imgdata = iter(image.getdata()) 
      
    while (True): 
        pixels = [value for value in imgdata.next()[:3] +
                                     imgdata.next()[:3] +
                                     imgdata.next()[:3]] 
        # string of binary data 
        #print pixels
        binstr = '' 
          
        for i in pixels[:8]: 
            if (i % 2 == 0): 
                binstr += '0'
            else: 
                binstr += '1'
                  
        data += chr(int(binstr, 2)) 
        if (pixels[-1] % 2 != 0): 
            return data

        

#print "Email is "+ str(round((1-(pred[0]))*100))+" %  safe (percentage on the scale of 100 )\n"
app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
        return render_template("index.html")

@app.route('/<filename>')
def send_image(filename):
    
    return send_file(filename,mimetype='image/gif')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/encrypt',methods = ['POST'])
def login():
   if request.method == 'POST': 
        gg1 = (request.form['message'])
        gg2 = (request.form['key'])
        gg3 = (request.files['image'])
       # image = Image.open(gg3, 'r') 
	#print content
   msg = str(gg1)
   key = str(gg2)
   ans = encode(msg,key)
   print ans
   return encodeIntoImage(ans,gg3)



@app.route('/dencrypt',methods = ['POST'])
def dencrypt():
   if request.method == 'POST': 
        gg2 = (request.form['key'])
        gg3 = (request.files['image'])
       # image = Image.open(gg3, 'r') 
	#print content
   key = str(gg2)
   text = decodeIntoText(gg3)
   ans= decode(text,key)
   print ans 
   msg = {"value":2,"encryptedMessage":ans}
   return jsonify(msg)


if __name__ == '__main__':
   app.run(debug = True)

