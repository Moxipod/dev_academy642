import tkinter as tk
from tkinter import filedialog

def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filepath:
        file_label.config(text=filepath)

root = tk.Tk()
root.title("File Upload UI")
root.geometry("500x200")
root.configure(bg="#2b2b2b")

tk.Label(root, text="Upload a File", font=("Arial", 18), bg="#2b2b2b", fg="#eeeeee").pack(pady=15)
tk.Button(root, text="Browse...", command=open_file, bg="#4caf50", fg="white", padx=10, pady=5).pack()
file_label = tk.Label(root, text="No file selected", bg="#2b2b2b", fg="#cccccc", wraplength=480)
file_label.pack(pady=10)

root.mainloop()
/