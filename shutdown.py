import tkinter as tk
import subprocess


def shutdown_computer():
    time = entry.get()
    if time == '' or not time.isnumeric():
        error_label.config(text="Text the time in minut.")
        return
    else:
        subprocess.Popen(f"shutdown /s /t {int(time)*60}")


def cancel():
    subprocess.Popen(f"shutdown /a")


def onehour():
    subprocess.Popen(f"shutdown /s /t 3600")


def halfhour():
    subprocess.Popen(f"shutdown /s /t 1800")


def fifteenminutes():
    subprocess.Popen(f"shutdown /s /t 900")


root = tk.Tk()
root.title("Shutdown")

label = tk.Label(root, text="Text the shutdown time in minut:")
label.grid(row=0, column=0, sticky="nsew")

entry = tk.Entry(root)
entry.grid(row=0, column=1, sticky="nsew")

yes_button = tk.Button(root, text="Custom Time", command=shutdown_computer)
yes_button.grid(row=0, column=2,  sticky="nsew")

yes_button = tk.Button(root, text="One hour", command=onehour)
yes_button.grid(row=1, column=0, sticky="nsew")

yes_button = tk.Button(root, text="Half hour", command=halfhour)
yes_button.grid(row=1, column=1,  sticky="nsew")

yes_button = tk.Button(root, text="15 minute", command=fifteenminutes)
yes_button.grid(row=1, column=2,  sticky="nsew")

cancel_button = tk.Button(root, text="Cancel", command=cancel)
cancel_button.grid(row=2, column=0,  sticky="nsew")

no_button = tk.Button(root, text="No", command=root.quit)
no_button.grid(row=2, column=1,  sticky="nsew")

error_label = tk.Label(root, text="")
error_label.grid(row=3, column=0, columnspan=2,  sticky="nsew")

root.mainloop()
