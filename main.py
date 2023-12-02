import tkinter as tk
from mediacontroller import HandGestureController
from virtualmouse import GestureController
from carcontroller import CarController
from tkinter import messagebox
def button_click():
    hand_gesture_controller = HandGestureController()
    hand_gesture_controller.process_gestures()
def button_click2():
    virtual_mouse_controller = GestureController()
    virtual_mouse_controller.start()
def button_click3():
    car_controller = CarController()
    car_controller.hand_gesture_control()
def quit_application():
    response = messagebox.askokcancel("Quit", "Do you really want to quit?")
    if response:
        root.destroy()


# Create the main window
root = tk.Tk()
root.title("Main Page")

# Create a label on the main window
label = tk.Label(root, text="Choose an option")
label.pack(pady=10)

# Create a button on the main window
button = tk.Button(root, text="Media Control", command=button_click)
button.pack(pady=10)

button2 = tk.Button(root, text="Mouse Control", command=button_click2)
button2.pack(pady=10)

button3 = tk.Button(root, text="Car Control", command=button_click3)
button3.pack(pady=10)

button_quit = tk.Button(root, text="Quit", command=quit_application)
button_quit.pack(pady=10)
# Run the main event loop
root.mainloop()
