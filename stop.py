import serial
import json
import time

# Define the serial port and baud rate (update with your Arduino's settings)
serial_port = '/dev/tty.usbserial-1120'  # Change to the appropriate port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# Threshold for the sensors
threshold = 400

# Variables to track the last direction the robot was going
going_left = False
going_right = False

# Function to send a command to set DAC values
def set_dac_values(dac1_value, dac2_value):
    command = f"SET_DAC {dac1_value} {dac2_value}\n"
    ser.write(command.encode())

while True:
    response = {}

    # Check if the serial connection is open or not
    response['serial_port'] = serial_port
    response['serial_connected'] = ser.is_open

    # Read data from the sensor
    sensor_data = ser.readline().decode().strip()
    sensor_data = sensor_data.split(',')
    left = int(sensor_data[0])
    right = int(sensor_data[1])

    print(left, right)

    # Store sensor readings
    response['left_sensor'] = left
    response['right_sensor'] = right



    print(going_left,going_right)

    # # Check if either sensor reading is below the threshold
    # if left < threshold or right < threshold:
    #     # If at least one sensor is below the threshold, adjust motor direction
    #     if left < threshold and right < threshold:
    #         # Both sensors below threshold, go straight
    #         set_dac_values(3, 3)
    #         response['motor_direction'] = 'straight'
    #         print("straight")
    #     elif left > threshold:
    #         # Left sensor below threshold, turn right
    #         set_dac_values(3, 5)
    #         response['motor_direction'] = 'right'
    #         print("right")
            
    #         going_right = True  # Robot is going right
    #     elif right > threshold:
    #         # Right sensor below threshold, turn left
    #         set_dac_values(5, 3)
    #         response['motor_direction'] = 'left'
    #         print("left")
    #         going_left = True  # Robot is going left

        

        

    # elif left > threshold or right > threshold:
    #     # Both sensors above threshold, stop
    #     # 
    #     # set_dac_values(9, 9)
    #     response['motor_direction'] = 'stop'
    #     print("stop")

    #     print(going_left,going_right)

    #     # Check the last direction the robot was going and turn to the opposite side
    #     if going_left:
    #         set_dac_values(3, 5)  # Turn right
    #         response['motor_direction'] = 'right'
    #         print("g right")
    #     elif going_right:
    #         set_dac_values(5, 3)  # Turn left
    #         response['motor_direction'] = 'left'
    #         print("g left")

    set_dac_values(9, 9)

    print("##############")
    # Print the JSON object
    json_response = json.dumps(response, indent=2)
    # print(json_response)

# Don't forget to close the serial port when you're done
ser.close()
