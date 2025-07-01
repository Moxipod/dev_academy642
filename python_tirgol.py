import string
import sys
N = int(sys.argv[1])


def count_all_words_in_file():
   """
    counts all words in file
    and make a dic in evry word it writes how meany times it was
    return the dic
   """
   dic = {}
   with open("myfile.txt", "r") as file:
    for line in file:
        for word in line.split():
            if word in dic:
             dic[word.lower().strip(string.punctuation)]+=1
            else:
               dic[word.lower().strip(string.punctuation)]=1
    return dic






dic = count_all_words_in_file()
sorte = sorted(dic.items(), key=lambda x: x[1],reverse=True)
for i in range(N):
   print (sorte[i])

    