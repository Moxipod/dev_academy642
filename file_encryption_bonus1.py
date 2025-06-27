
filename = input("Enter filename: with end . for example if name is text enter text.txt you need to have that file in same folder") #try with dogi.jpeg
xor_key = 13
with open(filename, 'r+b') as f:
    data =f.read()
    f.seek(0) #reset file pointer to zero
    for byte in data:
        f.write(bytes([byte ^ xor_key]))

    

      