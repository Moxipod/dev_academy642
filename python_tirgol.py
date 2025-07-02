import string
import sys


def count_all_words_in_file():
    dic = {}
    try:
        with open("myfile.txt", "r") as file:
            for line in file:
                for word in line.split():
                    cleaned = word.lower().strip(string.punctuation)
                    if cleaned in dic:
                        dic[cleaned] += 1
                    else:
                        dic[cleaned] = 1
    except FileNotFoundError:
        print("Error: File 'myfile.txt' not found.")
    return dic





def main():
    
    N = int(sys.argv[1])
    dic = count_all_words_in_file()
    sorte = sorted(dic.items(), key=lambda x: x[1],reverse=True)
    for i in range(N):
        print(sorte[i])

if __name__ == "__main__":
    main()