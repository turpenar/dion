
import tkinter as tk

text = 1
root = tk.Tk()
root2 = tk.Toplevel()

label = tk.Label(root2, bg="green", text=text, fg="blue")
label.place(relx=0.1, rely=0.1, relheight=0.3, relwidth=0.3)

def plus():
    global text, root2, label
    if not root2.winfo_exists():  # checks if the window is closed or not
        root2 = tk.Toplevel()
        label = tk.Label(root2, bg="green", text=text, fg="blue")
        label.place(relx=0.1, rely=0.1, relheight=0.3, relwidth=0.3)

    text += 1
    label['text'] = text

button = tk.Button(root, bg="blue", text="Button", command=plus)
button.pack()

root.mainloop()
