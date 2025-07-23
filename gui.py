import tkinter as tk
import os

# תיקיית שרת מקומית בלי הרשאות מיוחדות
SERVER_FOLDER = "server_folder"

# יצירת תיקייה אם לא קיימת
os.makedirs(SERVER_FOLDER, exist_ok=True)

class ServerFilesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("קבצים בשרת")

        # כותרת
        tk.Label(root, text="רשימת קבצים בתיקיית השרת").pack(pady=10)

        # רשימת קבצים
        self.server_listbox = tk.Listbox(root, width=60)
        self.server_listbox.pack(padx=20, pady=10)

        # כפתור רענון
        self.refresh_button = tk.Button(root, text="download from server", command=self.refresh_list)
        self.refresh_button.pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.server_listbox.delete(0, tk.END)
        for file in os.listdir(SERVER_FOLDER):
            self.server_listbox.insert(tk.END, file)

# הרצה
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerFilesApp(root)
    root.mainloop()
