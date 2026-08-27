from tkinter import *

win1 = Tk()
win1.title("Event handler")
win1.geometry("400x400")

# Function for keyboard key presses
def handle_key(event):
    print("Key pressed:", event.char)

# Function for mouse button clicks
def handle_mouse(event):
    print("Button clicked at coordinates:", event.x, event.y)

# Bind any keyboard key press to the window
win1.bind("<Key>", handle_key)

# Create and pack the button
button = Button(win1, text="Click me")
button.pack(pady=20)

# Bind the left mouse click to the button
button.bind("<Button-1>", handle_mouse)

win1.mainloop()
