import tkinter as tk
import os

def shutdown_computer():
    time = entry.get()
    if time == '' or not time.isnumeric() :
        error_label.config(text="Saniye cinsinden bir süre girin.")
        return
    else:
        os.system(f"shutdown /s /t {time}")
def cancell():
    os.system(f"shutdown /a")
root = tk.Tk()
root.title("Pc kapa")

label = tk.Label(root, text="Kapatma süresibi saniye cinsinden girin:")
label.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10)

yes_button = tk.Button(root, text="Yes", command=shutdown_computer)
yes_button.grid(row=1, column=0, padx=10, pady=10)
cancell_button = tk.Button(root, text="Cancell", command=cancell)
cancell_button.grid(row=1, column=1, padx=10, pady=10)
no_button = tk.Button(root, text="No", command=root.quit)
no_button.grid(row=1, column=2, padx=10, pady=10)

error_label = tk.Label(root, text="")
error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()