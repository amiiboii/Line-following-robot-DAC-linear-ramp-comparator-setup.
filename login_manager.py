import tkinter as tk
from PIL import Image, ImageTk

def login():
    # Check the user's credentials (e.g., username and password)
    # For this example, let's consider "user" and "password" as valid credentials
    if username_entry.get() == "User" and password_entry.get() == "admin":
        # Successful login, write a file to signal the main GUI
        with open("login_signal.txt", "w") as file:
            file.write("1")
        login_window.destroy()

def toggle_visibility():
    current_show = password_entry.cget("show")
    if current_show == "*":
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("960x540")  # Set window size to 960x540

# Create an image frame
image_frame = tk.Frame(login_window, width=960, height=200)
image_frame.pack()

image = Image.open("frame.png")
image = ImageTk.PhotoImage(image)

image_label = tk.Label(image_frame, image=image)
image_label.pack()

# Customize the Entry widgets
entry_style = {
    'background': 'white',
    'highlightthickness': 1,
}

# Calculate the center position for the login form
center_x = 390
center_y = 200  # Adjust 200 for the image frame height

username_entry = tk.Entry(login_window)
username_entry.place(x=center_x, y=center_y + 40)  # Position username entry field

password_entry = tk.Entry(login_window, show="*")
password_entry.place(x=center_x, y=center_y + 100)  # Position password entry field

# Create a clickable text item in a rectangle
quit_button_x = center_x
quit_button_y = center_y + 160

canvas = tk.Canvas(login_window, width=185, height=40)
canvas.place(x=quit_button_x, y=quit_button_y)
canvas.create_rectangle(0, 0, 200, 40, fill="white")
quit_button_text_item = canvas.create_text(100, 20, text="LOGIN", fill="grey")

def quit(event):
    login()  # This will stop the code gracefully

def toggle_password_visibility(event):
    toggle_visibility()

# Bind the "LOGIN" button to the login function
canvas.tag_bind(quit_button_text_item, '<Button-1>', quit)
# Bind a right-click event to toggle password visibility
canvas.tag_bind(quit_button_text_item, '<Button-3>', toggle_password_visibility)

login_window.mainloop()
