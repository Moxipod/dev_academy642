import threading
import time
global_counter=0

def loop_plus_hunderd_k ():
    global global_counter
    for i in range (0,100000):
        global_counter +=1

def loop_minus_hunderd_k ():
    global global_counter
    for i in range (0,100000):
        global_counter -=1


threading.Thread(target=loop_plus_hunderd_k).start()
print(global_counter)
threading.Thread(target=loop_minus_hunderd_k).start()
print(global_counter)
time.sleep(5)
print(global_counter)