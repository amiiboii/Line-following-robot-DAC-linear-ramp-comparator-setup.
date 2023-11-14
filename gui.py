import tkinter as tk
import json
import time
import subprocess
import sys
import psutil
import os

# Create the main window
root = tk.Tk()
root.geometry("960x540")
root.title("LYNY")

emergency_stop_status = False
nitros_on_status = False
crawl_on_status = False

w_status = False
a_status = False
s_status = False
d_status = False

test_process = None
#8 17

# Function to create a rounded rectangle
def round_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1]

    return canvas.create_polygon(*points, **kwargs, smooth=True)

# Define the coordinates and dimensions for the four main parts
part1 = (44, 74, 460, 250)
part2 = (44, 290, 460, 520)
part3 = (501, 74, 916, 304)
part4 = (501, 340, 916, 516)
top_bar = (0, 0, 960, 54)

# Create a canvas to draw the rounded rectangles
canvas = tk.Canvas(root, width=960, height=540, background="#ebebeb")
canvas.pack()

# Function to update the top bar sections with JSON data
def update_top_bar(data):
    top_bar_part1_text = f"Serial Port: {data.get('serial_port', 'N/A')}"

    top_bar_part2_text = f"Baud Rate: {data.get('baud_rate', 'N/A')}"

    if 'connected' in data:
        if data['connected']:
            top_bar_part3_fill = "green"
            top_bar_part3_text = "Connected"
        else:
            top_bar_part3_fill = "black"
            top_bar_part3_text = "Not Connected"
    else:
        # Handle the case where 'connected' key is not present in 'data'
        top_bar_part3_fill = "black"
        top_bar_part3_text = "Not Connected"
    
    # Update the text on the canvas items
    canvas.itemconfig(top_bar_part1_text_item, text=top_bar_part1_text)
    canvas.itemconfig(top_bar_part2_text_item, text=top_bar_part2_text,font =144)
    canvas.itemconfig(top_bar_part3_text_item, text=top_bar_part3_text, fill=top_bar_part3_fill, font =144)

def calculate_duty_cycle(dac_value):
    # Calculate y using the equation y = 0.3631x + 1E-13
    y = 0.3631 * dac_value + 1E-13
    return y

# Read the JSON data from a file
with open('to_gui.json', 'r') as file:
    json_data = json.load(file)

# Draw the four main rounded rectangles with the specified fill colors
round_rectangle(canvas, *part1, radius=30, fill="#ffffff")
round_rectangle(canvas, *part2, radius=30, fill="#ffffff")
round_rectangle(canvas, *part3, radius=30, fill="#ffffff")
round_rectangle(canvas, *part4, radius=30, fill="#ffffff")
round_rectangle(canvas, *top_bar, radius=0, fill="gray")

# Add additional parts in the top bar with corner radius of 14 and specified dimensions and colors
top_bar_part1 = (44, 10, 230, 46)
top_bar_part2 = (252, 10, 438, 46)
top_bar_part3 = (501, 10, 687, 46)
top_bar_part4 = (730, 10, 916, 46)

if json_data['connected']:
    contfill = "#42fe65"
else:
    contfill = "#fe4243"


round_rectangle(canvas, *top_bar_part1, radius=14, fill="#ebebeb")
round_rectangle(canvas, *top_bar_part2, radius=14, fill="#ebebeb")
round_rectangle(canvas, *top_bar_part3, radius=14, fill=contfill)
round_rectangle(canvas, *top_bar_part4, radius=14, fill="#515151")

# Create text items to display information in the top bar with "Syne" font
font = ("Syne", 11)

top_bar_part1_text_item = canvas.create_text(137, 28, text="", fill="black", font=font)
top_bar_part2_text_item = canvas.create_text(345, 28, text="", fill="black", font=font)
top_bar_part3_text_item = canvas.create_text(594, 28, text="", fill="white", font=font)



# Create text items to display information in part1 with the updated coordinates
font_size_24 = ("Syne", 24)
font_size_20 = ("Syne", 20)


# Change the coordinates for the text items
right_sensor_label_item = canvas.create_text(140, 100, text="", fill="black", font=font_size_24)
right_value_text_item = canvas.create_text(255, 100, text="", fill="#23D692", font=font_size_20)
right_color_text_item = canvas.create_text(337, 100, text="", fill="black", font=font_size_20)

left_sensor_label_item = canvas.create_text(135, 138, text="", fill="black", font=font_size_24)
left_value_text_item = canvas.create_text(255, 138, text="", fill="#23D692", font=font_size_20)
left_color_text_item = canvas.create_text(337, 138, text="", fill="black", font=font_size_20)

# Function to update part1 with JSON data
def update_part1(data):
    right_sensor_label = f"Right Sensor"
    right_value_text = f"{data.get('right_value', 'N/A')}"
    right_color_text = f"{data.get('right_color', 'N/A')}"

    
    left_sensor_label = f"Left Sensor"
    left_value_text = f"{data.get('left_value', 'N/A')}"
    left_color_text = f"{data.get('left_color', 'N/A')}"

    # Update the text on the canvas items
    canvas.itemconfig(right_sensor_label_item, text=right_sensor_label)
    canvas.itemconfig(right_value_text_item, text=right_value_text)
    canvas.itemconfig(right_color_text_item, text=right_color_text)
    
    canvas.itemconfig(left_sensor_label_item, text=left_sensor_label)
    canvas.itemconfig(left_value_text_item, text=left_value_text)
    canvas.itemconfig(left_color_text_item, text=left_color_text)


# Use the get method with a default value of 'N/A' for dac1_value
dac1_value = json_data.get('dac1_value', 'N/A')

# Use the get method with a default value of 'N/A' for dac2_value
dac2_value = json_data.get('dac2_value', 'N/A')


# Calculate duty cycles using the given equation
dac1_duty_cycle = (0.3631 * dac1_value + 1E-13)/100
dac2_duty_cycle = (0.3631 * dac2_value + 1E-13)/100
# Create text items for the duty cycles
dac1_duty_cycle_label_item = canvas.create_text(140, 175, text="Duty Cycles:", fill="black", font=font_size_24)
dac1_duty_cycle_text_item = canvas.create_text(260, 175, text="", fill="black", font=font_size_20)
dac2_duty_cycle_text_item = canvas.create_text(337, 175, text="", fill="black", font=font_size_20)

# Function to calculate and update DAC duty cycles
def update_dac_duty_cycles(dac1_value,dac2_value):

    

    if isinstance(dac1_value, (int, float)):
        dac1_duty_cycle = (0.3631 * dac1_value + 1E-13) / 100
    else:
        # Handle the case where dac1_value is not numeric
        dac1_duty_cycle = 0  # or set a default value or take appropriate action
        
        # Check if dac1_value is numeric before performing the calculation
    if isinstance(dac2_value, (int, float)):
        dac2_duty_cycle = (0.3631 * dac2_value + 1E-13) / 100
    else:
        # Handle the case where dac1_value is not numeric
        dac2_duty_cycle = 0  # or set a default value or take appropriate action


    # Update the text on the canvas items
    canvas.itemconfig(dac1_duty_cycle_text_item, text=f"{dac1_duty_cycle:.2%}")
    canvas.itemconfig(dac2_duty_cycle_text_item, text=f"{dac2_duty_cycle:.2%}")

    return dac1_duty_cycle, dac2_duty_cycle 

# Add text label for the threshold
threshold_label_item = canvas.create_text(130, 213, text="Threshold:", fill="black", font=font_size_24)

# Add a slider with a default value of 500
slider = tk.Scale(root, from_=0, to=1000, orient='horizontal', length=200, troughcolor="white", sliderlength=20)
slider.set(500)  # Set the initial value to 500
slider_item = canvas.create_window(340, 213, window=slider)


live_motion_text = canvas.create_text(580, 100, text="Live motion", fill="black", font=font_size_24)


# Define the toggle_live_motion function before creating live_motion_toggle
def toggle_live_motion():
    if live_motion_var.get():
        # Start displaying live motion data
        display_live_motion_data()
    else:
        # Handle turning off live motion (if needed)
        pass
    root.after(100, toggle_live_motion)


# Create a variable to store the state of the toggle switch
live_motion_var = tk.BooleanVar()

# Create the toggle switch
live_motion_toggle = tk.Checkbutton(root, text="Enable", variable=live_motion_var, font=("Syne", 16), bg="#ffffff", command=toggle_live_motion)
live_motion_toggle.place(x=650, y=88)  # Adjust the coordinates as needed

# Create a list to store live motion data sets
live_motion_data = []

# Create a list to store live motion data sets (as a global variable)
live_motion_data = []

# Function to display live motion data with animation
def display_live_motion_data():
    global live_motion_data  # Declare live_motion_data as a global variable

    # Get the canvas width and height
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Coordinates for part3
    x_start = 750
    y_start = 130

    # Gap between each set of values
    gap = 40

    # Add the new data set to the list
    new_data_set = {
        "command_sent": json_data["command_sent"], 
        "dac1_duty_cycle": dac1_duty_cycle,  
        "dac2_duty_cycle": dac2_duty_cycle, 
    }
    
    # Append the new data set and keep only the last 4 data sets
    live_motion_data.append(new_data_set)
    # Ensure that the list contains a maximum of 4 data sets
    if len(live_motion_data) > 4:
        live_motion_data.pop(0)  # Remove the oldest data set

    # Clear the part3 areax
    canvas.create_rectangle(650, 80,850 ,300, fill="white")

    for data_set in live_motion_data:
        # Display the data on part3
        data_text = f"{data_set['command_sent']}   {data_set['dac1_duty_cycle']:.2%}   {data_set['dac2_duty_cycle']:.2%}"
        canvas.create_text(x_start, y_start, text=data_text, fill="black", font=("Syne", 20))

        # Move down for the next set of values
        y_start += gap

        # Update the GUI
        root.update()

        # Pause for a short time to create an animation effect
        time.sleep(0.3)  # Adjust the duration as needed

# Coordinates for the "Quit" button
quit_button_x = 823
quit_button_y = 28

# Create the "Quit" button as text without a background
quit_button_text_item = canvas.create_text(quit_button_x, quit_button_y, text="Quit", fill="black", font=25)

def quit():
    global test_process  # Declare test_process as a global variable

    # Terminate the subprocess if it is running
    if test_process and test_process.poll() is None:
        test_process.terminate()

    # Exit the Tkinter application
    root.quit()  # This will stop the code gracefully

    # Wait for the subprocess to complete (timeout: 5 seconds)
    if test_process:
        test_process.wait(timeout=5)

canvas.tag_bind(quit_button_text_item, '<Button-1>', lambda event: quit())


# Create frames within part4 with different variables
start_frame = (612, 352, 805, 394)          # Start frame
emergency_stop_frame = (612, 412, 805, 454)  # Emergency Stop frame
nitros_frame = (547, 473, 675, 510)         # Nitros frame
crawl_frame = (739, 473, 868, 510)          # Crawl frame

# Create rounded rectangles for the frames
round_rectangle(canvas, *start_frame, radius=30, fill="#EBEBEB")
round_rectangle(canvas, *emergency_stop_frame, radius=30, fill="#FE4243")
round_rectangle(canvas, *nitros_frame, radius=30, fill="#42A4FE")
round_rectangle(canvas, *crawl_frame, radius=30, fill="#FEA842")


# Add the text "Start" to the frame
canvas.create_text(708, 373, text="START!", fill="black", font=("Syne", 24))

# Create a larger and more prominent toggle switch within the frame
start_toggle_var = tk.BooleanVar()
start_toggle = tk.Checkbutton(root, variable=start_toggle_var, onvalue=True, offvalue=False, font=("Syne", 16), bg="#EBEBEB")
start_toggle_item = canvas.create_window(769, 374, window=start_toggle)



# Create the "Manual Control" text in part2
manual_control_text_item = canvas.create_text(159, 310, text="Manual Control", fill="black", font=("Syne", 24))

# Create a toggle switch for manual control in part2
manual_control_toggle_var = tk.BooleanVar()
manual_control_toggle = tk.Checkbutton(root, variable=manual_control_toggle_var, onvalue=True, offvalue=False, font=("Syne", 16), bg="white")
manual_control_toggle_item = canvas.create_window(269, 310, window=manual_control_toggle)


image = tk.PhotoImage(file='manual.png')

# Create a canvas image item at point (45, 332)
image_item = canvas.create_image(45, 332, anchor='nw', image=image)

# Create a vertical slider at coordinates (x=281, y=337)
vertical_slider = tk.Scale(root, from_=100, to=0, orient='vertical', length=170, troughcolor="white", sliderlength=20,)
vertical_slider.set(0)  # Set the initial value
vertical_slider_item = canvas.create_window(265, 430, window=vertical_slider)

# Define the coordinates and dimensions for the gauge
gauge_x = 315
gauge_y = 435
gauge_width = 130
gauge_height = 147

# Create a gauge on the canvas
gauge = canvas.create_arc(gauge_x, gauge_y, gauge_x + gauge_width, gauge_y + gauge_height, start=0, extent=0, fill="#FE4243", width=2)

# Function to update the gauge with the average value
def update_gauge(average_value):
    # Calculate the extent based on the average value (assuming the range is 0-100)
    extent = average_value * 1.8  # Scale the extent for the gauge

    # Update the gauge on the canvas
    canvas.itemconfig(gauge, extent=extent)

update_gauge(dac2_duty_cycle*100 )

# Define the coordinates and dimensions for the new gauge
new_gauge_x = 315
new_gauge_y = 350
gauge_width = 130
gauge_height = 147

# Create a new gauge on the canvas
new_gauge = canvas.create_arc(new_gauge_x, new_gauge_y, new_gauge_x + gauge_width, new_gauge_y + gauge_height, start=0, extent=0, fill="#FE4243", width=2)

# Function to update the new gauge with the average value
def update_new_gauge(average_value):
    
    # Calculate the extent based on the average value (assuming the range is 0-100)
    extent = average_value * 1.8  # Scale the extent for the gauge

    # Update the new gauge on the canvas
    canvas.itemconfig(new_gauge, extent=extent)


update_new_gauge(dac1_duty_cycle*100 )

crawl_button_text_item = canvas.create_text(805, 492, text="Snail", fill="#804500", font=("Syne", 20))
# Add the "Emergency Stop" text to the frame
emergency_stop_text_item = canvas.create_text(708, 433, text="EMERGENCY STOP", fill="#A60000", font=("Syne", 20))
nitros_button_text_item = canvas.create_text(612, 492, text="Nitros", fill="#00386B", font=("Syne", 20))

def update_gui():
    # Read the JSON data from a fil
    try:
        # Read the JSON data from a file
        with open('to_gui.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        # Handle the exception (print an error message or take other actions)
        print(f"Error: {e}")
        json_data = {}  # Set a default value or an empty dictionary if the JSON loading fails


    # Update the top bar
    update_top_bar(json_data)

    # Update part1
    update_part1(json_data)
    # Use the get method with a default value of 'N/A' for dac1_value
    dac1_value = json_data.get('dac1_value', 'N/A')

    # Use the get method with a default value of 'N/A' for dac2_value
    dac2_value = json_data.get('dac2_value', 'N/A')

    update_dac_duty_cycles(dac1_value,dac2_value)

    
    toggle_live_motion
    # Schedule the update every 1 second
    root.after(100, update_gui)


    # Define the Emergency Stop button function
    def emergency_stop_action():
        global emergency_stop_status  # Make sure to use the global variable
        emergency_stop_status = not emergency_stop_status  # Toggle the status
        # Implement the logic to send commands or perform actions based on emergency_stop_status
        if emergency_stop_status:
            # If emergency_stop_status is True, perform the corresponding action
            emergency_stop_status = True

        else:
            # If emergency_stop_status is False, perform the corresponding action
            emergency_stop_status = False


    # Bind the "Emergency Stop" button text to the emergency_stop_action function
    canvas.tag_bind(emergency_stop_text_item, '<Button-1>', lambda event: emergency_stop_action())

    # Define the Nitros button function
    def nitros_button_action():
        global nitros_on_status  # Make sure to use the global variable
        nitros_on_status = not nitros_on_status  # Toggle the status
        # Implement the logic to send commands or perform actions based on nitros_on_status
        if nitros_on_status:
            # If nitros_on_status is True, perform the corresponding action
            nitros_on_status = True

        else:
            # If nitros_on_status is False, perform the corresponding action
            nitros_on_status = False


    # Bind the "Nitros" button text to the nitros_button_action function
    canvas.tag_bind(nitros_button_text_item, '<Button-1>', lambda event: nitros_button_action())

    # Define the Crawl button function
    def crawl_button_action():
        global crawl_on_status  # Make sure to use the global variable
        crawl_on_status = not crawl_on_status  # Toggle the status
        # Implement the logic to send commands or perform actions based on crawl_on_status
        if crawl_on_status:
            # If crawl_on_status is True, perform the corresponding action
            crawl_on_status = True

        else:
            # If crawl_on_status is False, perform the corresponding action
            crawl_on_status = False


    # Bind the "Crawl" button text to the crawl_button_action function
    canvas.tag_bind(crawl_button_text_item, '<Button-1>', lambda event: crawl_button_action())


    # Function to handle manual control state
    def handle_manual_control():
        global w_status, a_status, s_status, d_status
        if manual_control_toggle_var.get():
        
            # Manual control is enabled


            def on_key_press(event):
                global w_status, a_status, s_status, d_status
                key = event.keysym
                if key == "w":
                    # Handle the "W" key press (move the car forward)
                    w_status = True
                elif key == "a":
                    # Handle the "A" key press (move the car left
                    a_status = True
                elif key == "s":
                    # Handle the "S" key press (move the car backward)
                    s_status = True
                elif key == "d":
                    # Handle the "D" key press (move the car right)
            
                    d_status = True

            # Bind key presses to the on_key_press function
            root.bind("<KeyPress>", on_key_press)

            def on_key_release(event):
                global w_status, a_status, s_status, d_status
                key = event.keysym
                if key == "w":
                    w_status = False
                elif key == "a":
                    a_status = False
                elif key == "s":
                    s_status = False
                elif key == "d":
                    d_status = False

            # Bind key releases to the on_key_release function
            root.bind("<KeyRelease>", on_key_release)


    handle_manual_control()

    global w_status, a_status, s_status, d_status

    data_to_write = {
        "start_toggle_status": start_toggle_var.get(),  # Get the status of the Start toggle
        "emergency_stop_status": emergency_stop_status, 
        "nitros_on_status": nitros_on_status,  
        "crawl_on_status": crawl_on_status,  
        "threshold_value": slider.get(),  # Get the value from the slider
        "manual_toggle_status": manual_control_toggle_var.get(),  # Get the status of the Manual Control toggle
        "duty_cycle_slider_value": vertical_slider.get(),  # Get the value from the duty cycle slider
        "w_status":w_status,
        "a_status":a_status,
        "s_status":s_status,
        "d_status":d_status
    }

    json_file_path = 'to_firm.json'  # Update this with the actual file path

    # Write the data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data_to_write, json_file, indent=4)  # The 'indent' argument is optional and provides pretty-printing


    # Update the colors of the Nitros, Crawl, and Emergency Stop buttons based on their status
    if nitros_on_status:
        canvas.itemconfig(nitros_button_text_item, fill="#42FE65")  # Change color to green when Nitros is on
    else:
        canvas.itemconfig(nitros_button_text_item, fill="#00386B")  # Change color back to the original color

    if crawl_on_status:
        canvas.itemconfig(crawl_button_text_item, fill="#42FE65")  # Change color to green when Crawl is on
    else:
        canvas.itemconfig(crawl_button_text_item, fill="#804500")  # Change color back to the original color

    if emergency_stop_status:
        canvas.itemconfig(emergency_stop_text_item, fill="#FEA842")  # Change color to orange when Emergency Stop is on
    else:
        canvas.itemconfig(emergency_stop_text_item, fill="#A60000")  # Change color back to the original color


    update_gauge(data_to_write["duty_cycle_slider_value"])
    

update_gui()
# Start the GUI
root.mainloop()
