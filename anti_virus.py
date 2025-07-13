import threading
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import time

headers = {
    "accept": "application/json",
    "x-apikey": "e3caa8bf9f7dd4cd7a715cd828f9767bd7d716d7cbd82349eb472cb3c0ff193b",
}

file_path = 0
is_scanning = False  # For animation control

def get_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        result_label.config(text=f"Selected: {file_path}")
    else:
        result_label.config(text="No file selected.")

def upload_file_to_get_id(file_path):
    url = "https://www.virustotal.com/api/v3/files"
    with open(file_path, "rb") as f:
        files = {'file': f}
        response1 = requests.post(url, headers=headers, files=files)
    if response1.status_code == 200:
        data = response1.json()
        return data['data']['id']
    else:
        result_label.config(text=f"Failed to upload file: {response1.status_code}")
        return None

def get_analysis(id):
    url = f"https://www.virustotal.com/api/v3/analyses/{id}"
    max_tries = 20  # 100 seconds max
    tries = 0
    while tries < max_tries:
        response = requests.get(url, headers=headers)
        result = response.json()
        status = result['data']['attributes'].get('status')
        if status == 'completed':
            return result['data']['attributes']['stats']
        time.sleep(5)
        tries += 1
    result_label.config(text="Scan took too long. Please try again later.")
    return None

def verdict_from_stats(stats):
    if stats['malicious'] > 0:
        return "File is a VIRUS"
    elif stats['suspicious'] > 0:
        return "File is LIKELY SUSPICIOUS"
    elif stats['undetected'] > 0 and stats['malicious'] == 0 and stats['suspicious'] == 0:
        return "File is CLEAN"
    else:
        return "Analysis INCONCLUSIVE"

def animate_loading():
    if is_scanning:
        current_text = result_label.cget("text")
        if current_text.endswith("..."):
            result_label.config(text="Scanning")
        else:
            result_label.config(text=current_text + ".")
        window.after(500, animate_loading)

def full_scan():
    global is_scanning
    if file_path != 0:
        result_label.config(text="Scanning")
        is_scanning = True
        animate_loading()
        id = upload_file_to_get_id(file_path)
        if id:
            stats = get_analysis(id)
            if stats:
                verdict = verdict_from_stats(stats)
                result_label.config(text=verdict)
        is_scanning = False
    else:
        result_label.config(text="Please select a file first.")

def threaded_full_scan():
    threading.Thread(target=full_scan).start()

# --- UI Setup ---
window = Tk()
window.geometry("800x600")

bg_image_raw = Image.open("C:\\Users\\User\\Downloads\\—Pngtree—blue technology cyber security poster_1056272.jpg")  # <-- Put your image path here
bg_image_raw = bg_image_raw.resize((800, 600))  # Match window size
bg_image = ImageTk.PhotoImage(bg_image_raw)

# Set background label
bg_label = Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
window.title("Virus Scan Tool")
window.resizable(False, False)




# HEADLINE
headline_label = Label(
    text="Guy's AntiVirus", 
    font=("Arial", 24, "bold"), 
    bg="#2c3e50", 
    fg="white"
)
headline_label.place(relx=0.5, rely=0.1, anchor="center")

separator = Frame(window, bg="white", height=2, width=400)
separator.place(relx=0.5, rely=0.17, anchor="center")

button_bg = "#3498db"
button_fg = "white"

button = Button(
    text="Select File", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg=button_bg, fg=button_fg, relief="flat",
    activebackground="#2980b9", activeforeground="white",
    command=get_file
)
button2 = Button(
    text="Scan for Virus", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg=button_bg, fg=button_fg, relief="flat",
    activebackground="#2980b9", activeforeground="white",
    command=threaded_full_scan
)
result_label = Label(
    text="", font=("Arial", 14),
    bg="#2c3e50", fg="white", wraplength=700, justify="center"
)

button.place(relx=0.5, rely=0.35, anchor='center')
button2.place(relx=0.5, rely=0.5, anchor='center')
result_label.place(relx=0.5, rely=0.7, anchor='center')

window.mainloop()
