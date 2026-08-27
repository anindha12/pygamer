from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("New Game")
root.geometry("400x400")

# Function to display the alert box
def msg():
    messagebox.showinfo("Alert", "Stop! Virus detected! Please take necessary precautions!")

# Create the button
button = Button(root, text="Scan for viruses", command=msg)

# Use ONLY place to position the button
button.place(x=140, y=180)

root.mainloop()
