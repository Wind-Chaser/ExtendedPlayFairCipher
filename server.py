from flask import Flask, redirect, url_for, request,jsonify,render_template
import numpy as np
from numpy import array
from numpy import reshape
from PIL import Image
from flask import send_file,send_from_directory
import re
import string
import itertools
import sys
import os
####+++++++++++++++++++++MAIN PROGRAM STARTS HERE++++++++++++++++++++++++++++++++++++####
#________________________________________________________________________________#

def chunker(seq, size):

    it = iter(seq)
    while True:
       chunk = tuple(itertools.islice(it, size))
       if not chunk:
           return
       yield chunk

def prepare_input(dirty):

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

def fence(lst, numrails):

    fence = [[None] * len(lst) for n in range(numrails)]
    rails = range(numrails - 1) + range(numrails - 1, 0, -1)
    for n, x in enumerate(lst):
        fence[rails[n % len(rails)]][n] = x

    if 0: 
        for rail in fence:
            print ''.join('.' if c is None else str(c) for c in rail)

    return [c for rail in fence for c in rail if c is not None]

def encodeIntoCipherText(plaintext, key):

    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    print ("Input : " + plaintext)
    ciphertext = ""
    ttcpy = array(table)    
    ttcpy = ttcpy.reshape((8,8))
    ttcpy = ttcpy.transpose()
    ttcpy = ttcpy.reshape((64,1))
    tcpy = table

    for i in range(64):
        tcpy[i] = ttcpy[i][0] 
   
    i = 0    
    for char1, char2 in chunker(plaintext, 2):
        if i%2==0:
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
        else:       
            row1, col1 = divmod(tcpy.index(char1), 8)
            row2, col2 = divmod(tcpy.index(char2), 8)

            if row1 == row2:
                ciphertext += tcpy[row1*8+(col1+1)%8]
                ciphertext += tcpy[row2*8+(col2+1)%8]
            elif col1 == col2:
                ciphertext += tcpy[((row1+1)%8)*8+col1]
                ciphertext += tcpy[((row2+1)%8)*8+col2]
            else: # rectangle
                ciphertext += tcpy[row1*8+col2]
                ciphertext += tcpy[row2*8+col1]    
        i=i+1   
    
    print ("Cipher Text After Transpose : "+ ciphertext)
    print("Cipher Text After Rail Fence(3) : " + ''.join(fence(ciphertext, 3)))                              
    return ''.join(fence(ciphertext, 3))


def decodeIntoPlainText(ciphertext, key):

    rng = range(len(ciphertext))
    pos = fence(rng, 3)
    ctext=''.join(ciphertext[pos.index(n)] for n in rng)
    ciphertext=ctext
    table = generate_table(key)
    plaintext = ""
    ttcpy = array(table)    
    ttcpy = ttcpy.reshape((8,8))
    ttcpy = ttcpy.transpose()
    ttcpy = ttcpy.reshape((64,1))
    tcpy = table

    for i in range(64):
        tcpy[i] = ttcpy[i][0] 
    
    i =0
    for char1, char2 in chunker(ciphertext, 2):
        if i%2 ==0: 
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
        else:       
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
        i=i+1   
    
    while plaintext.find("^")!=-1 :
       plaintext =plaintext.replace("^","")
    while plaintext.find("|")!=-1:
        plaintext=plaintext.replace("|"," ")            
    return plaintext
    

  
 
def genData(data):  

    newd = []    

    for i in data: 
        newd.append(format(ord(i), '08b')) 
    return newd 
          

def modPix(pix, data): 
      
    datalist = genData(data) 
    lendata = len(datalist) 
    imdata = iter(pix) 
    
    for i in range(lendata): 
        
        pix = [value for value in imdata.next()[:3] +
                                  imdata.next()[:3] +
                                  imdata.next()[:3]] 
       
        for j in range(0, 8): 
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
                  
                if (pix[j]% 2 != 0): 
                    pix[j] += 1
                      
            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
                pix[j] += 1
       
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
        newimg.putpixel((x, y), pixel) 
        if (x == w - 1): 
            x = 0
            y += 1
        else: 
            x += 1

def encodeIntoImage(data,img): 

    image = Image.open(img, 'r') 
    if (len(data) == 0): 
        raise ValueError('Data is empty')           
    newimg = image.copy()   
    encode_enc(newimg, data) 
    f = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    newimg.save(f,"png")   
    return jsonify({"value":1,"imageName":img.filename})
 
def decodeIntoText(img):  

    image = Image.open(img, 'r')       
    data = '' 
    imgdata = iter(image.getdata()) 

    while (True): 
        pixels = [value for value in imgdata.next()[:3] +
                                     imgdata.next()[:3] +
                                     imgdata.next()[:3]]        
        binstr = ''           
        for i in pixels[:8]: 
            if (i % 2 == 0): 
                binstr += '0'
            else: 
                binstr += '1'                  
        data += chr(int(binstr, 2)) 
        if (pixels[-1] % 2 != 0): 
            return data       

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<filename>')
def send_image(filename):
    if filename.split('.')[1] != 'ico':
        return send_file(filename,mimetype='image/gif')
    return "okay"    

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/encrypt',methods = ['POST'])
def encrypt():
   if request.method == 'POST': 
        message = (request.form['message'])
        key = (request.form['key'])
        image = (request.files['image'])
       
   msg = str(message)
   key = str(key)
   cipherText = encodeIntoCipherText(msg,key)
   print ("Encrypted Message : " + cipherText)
   return encodeIntoImage(cipherText,image)

@app.route('/decrypt',methods = ['POST'])
def decrypt():
   if request.method == 'POST': 
        key = (request.form['key'])
        encryptedImage = (request.files['image'])
       
   key = str(key)
   cipherText = decodeIntoText(encryptedImage)
   ans = decodeIntoPlainText(cipherText,key)
   print ("Dencrypted Message : " + ans) 
   msg = {"value":2,"encryptedMessage":ans}
   return jsonify(msg)

if __name__ == '__main__':
   app.run(debug = True)

