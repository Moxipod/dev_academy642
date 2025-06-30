def decrypt_and_uncrypt(file,xor_key):
    """
    enter the name of the file you want to decrypt or uncrypt 
    and decryption and uncription is done by the same func just make sure that you use the same
    to decrypt just enter a non decrypted fie to uncrypt enter the name of the file with the right xor_key
    xor key. 
    """
    with open(file, 'r+b') as f:
        data =f.read()
        f.seek(0) #reset file pointer to zero
        for byte in data:
            f.write(bytes([byte ^ xor_key]))
    





filename = input("Enter filename: with end . for example if name is text enter text.txt you need to have that file in same folder") #try with dogi.jpeg
xor_key = 13
decrypt_and_uncrypt(filename,xor_key)


    

      