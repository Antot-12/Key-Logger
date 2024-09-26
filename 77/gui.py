import tkinter as tk

def show_gui():
    root = tk.Tk()
    root.title("Key Logger")

    label = tk.Label(root, text="Key Logger is running", padx=20, pady=20)
    label.pack()

    stop_button = tk.Button(root, text="Stop Logging", command=root.quit, padx=10, pady=10)
    stop_button.pack()

    root.mainloop()
