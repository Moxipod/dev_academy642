

def checkIftalmidin(dick):
    for key in dick:
        if "talmid" in key:
            return True
    return False
    



#tirgol 1-5
dick =  {"name":"john","lastname":"nightrain","age":30,"grade2":20,"grade3":35,"grade4":123}
print(dick)
dick["talmid"]= "harel"
dick ["grade1"] = 99
print(dick)
dick ["grade1"] = 12
print(dick)
sum=0
counter=0
for key in dick:
    
    if "grade" in key:
        sum+= dick[key]
        counter+=1
sum/=counter
print(sum)

del dick["talmid"]
print(dick)
dick["talmid2"] = 4
print(checkIftalmidin(dick))


# i forgot i can use in 
def checkNumInTuple (tuple,num):
    for item in tuple:
        if item == num:
            return True
    return False



#tirgol 

list = [2,5,7,3,2]
list.append(7)
list.append(9)
list =tuple(list)
len = list.__le__
print(list)
num = int(input("chose!"))
print(checkNumInTuple(list,num))

#תירגול סוף הקורס 

#targil1
def checkIfKeyExisits(dic,key1):
    for key in dic:
        if key == key1:
            return dic[key1]
    return "key not in dic"

# to check 
print(checkIfKeyExisits({"id1":1344235,"id2":3452234,"id3":243512},"id5"))

#targil2

def  union_sets(set1,set2):
    return set1.union(set2)

#to test
print(union_sets({1, 2, 3},{3, 4, 5}))

#targil 3

def count_elements_in_tuples (list):
    dic = {}
    for i in range(len(list)):
        num=2
        for j in range(len(list[i])):
            key = list[i][j]
            if key not in dic:
                dic[key] =1
            else:
                 dic[key]+=1   
    return dic   
#check
list1 = [('a', 'b'), ('a', 'c'), ('d', 'b'), ('e', 'f'), ('a', 'b')]
print(count_elements_in_tuples(list1))
