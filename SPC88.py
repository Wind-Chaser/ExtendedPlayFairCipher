import string
import itertools
import re
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
    
gg = encode("anur@g bro wh#re @re u ?","RAJA@RAM")
print gg
print decode(gg,"RAJA@RAM")






        
