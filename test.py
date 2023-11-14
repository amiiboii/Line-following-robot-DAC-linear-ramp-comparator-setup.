import serial
import json
import keyboard
import time


# Autonomous Mode
autonomous_dac_values = {
    "straight": {"dac1": 255, "dac2": 255},
    "right": {"dac1": 11, "dac2": 5},
    "left": {"dac1": 5, "dac2": 11},
    "stop": {"dac1": 9, "dac2": 9},
}


# Crawl Mode
crawl_dac_values = {
    "straight": {"dac1": 3, "dac2": 3},
    "right": {"dac1": 3, "dac2": 5},
    "left": {"dac1": 5, "dac2": 3},
    "stop": {"dac1": 9, "dac2": 9},
}

# Nitros Mode
nitros_dac_values = {
    "straight": {"dac1": 255, "dac2": 255},
    "right": {"dac1": 3, "dac2": 5},
    "left": {"dac1": 5, "dac2": 3},
    "stop": {"dac1": 9, "dac2": 9},
}

# Autonomous Direction Variables
going_left = False
going_right = False

# Crawl Direction Variables
going_left_crawl = False
going_right_crawl = False

# Nitros Direction Variables
going_left_nitros = False
going_right_nitros = False


while True:

    try:
        # Load the configuration from a JSON file
        with open('to_firm.json', 'r') as config_file:
            config = json.load(config_file)

        # print("Configuration loaded")
        
    except json.decoder.JSONDecodeError as e:
        print(f"Error while decoding JSON: {e}")
        # time.sleep(1)  # Sleep for a moment and then retry
        continue
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # time.sleep(1)  # Sleep for a moment and then retry
        continue

    # Define the serial port and baud rate (update with your Arduino's settings)
    serial_port = '/dev/tty.usbserial-1120'  # Change to the appropriate port
    baud_rate = 9600
    ser = serial.Serial(serial_port, baud_rate)

    # print(f"Connected to {serial_port} at {baud_rate} baud")

    # Function to send a command to set DAC values
    def set_dac_values(dac1_value, dac2_value):
        command = f"SET_DAC {dac1_value} {dac2_value}\n"
        ser.write(command.encode())  # Send the command to set DAC values
        print(command)
        

    def daci(dac1_value, dac2_value):
        data["dac1_value"] = dac1_value
        data["dac2_value"] = dac2_value
        
        with open(log_file, 'w') as log:
            json.dump(data, log)

    print("DAC values function defined")

    # Create a dictionary to hold the data
    data = {
        "serial_port": serial_port,
        "baud_rate": baud_rate,
        "connected": ser.is_open,
        "left_value": 0,
        "right_value": 0,
        "left_color": "white",  # Initialize color to "white"
        "right_color": "white",  # Initialize color to "white"
        "command_sent": None,
        "dac1_value": 0,  # Initialize DAC 1 value
        "dac2_value": 0,  # Initialize DAC 2 value
    }





    log_file = 'to_gui.json'                                                    


    print(config["start_toggle_status"])
    # Check if the "start_toggle_status" is true
    if config["start_toggle_status"]:
        print("Start toggle is true")
        
        # Read the threshold value from the configuration
        threshold = config["threshold_value"]
        print(f"Threshold set to {threshold}")

        while True:
            # set_dac_values(dac1, dac2)
            # daci(dac1, dac2)
            # Check the "start_toggle_status" and exit if it's False

            try:
                # Load the configuration from a JSON file
                with open('to_firm.json', 'r') as config_file:
                    config = json.load(config_file)

                # print("Configuration loaded")
                
            except json.decoder.JSONDecodeError as e:
                print(f"Error while decoding JSON: {e}")
                # time.sleep(1)  # Sleep for a moment and then retry
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                # time.sleep(1)  # Sleep for a moment and then retry
                continue


            # Check if the "emergency_stop_status" is true
            if config["emergency_stop_status"]:
                print("Emergency stop status is true")
                dac1 = 9
                dac2 = 9
                set_dac_values(dac1, dac2)
                daci(dac1, dac2)
                print("Emergency stop command sent")
                # You may want to log the emergency stop action as well
            elif config["manual_toggle_status"]:   
                print("Manual toggle status is true")
                # Manual control mode
                # Manual control mode
                time.sleep(0.05)
                if config["w_status"]:
                    dac1 = 255
                    dac2 = 255
                    set_dac_values(dac1, dac2)
                    daci(dac1, dac2)
                    data["command_sent"] = "front"
                    print("Manual control - front")
                    
                elif config["a_status"]:
                    set_dac_values(autonomous_dac_values["left"]["dac1"], autonomous_dac_values["left"]["dac2"])
                    daci(autonomous_dac_values["left"]["dac1"], autonomous_dac_values["left"]["dac2"])
                    data["command_sent"] = "left"
                    print("Manual mode - Left")
                elif config["s_status"]:
                    dac1 = 0
                    dac2 = 0
                    set_dac_values(dac1, dac2)
                    daci(dac1, dac2)
                    data["command_sent"] = "back"
                    print("Manual control - back")
                elif config["d_status"]:
                    set_dac_values(autonomous_dac_values["right"]["dac1"], autonomous_dac_values["right"]["dac2"])
                    daci(autonomous_dac_values["right"]["dac1"], autonomous_dac_values["right"]["dac2"])
                    data["command_sent"] = "right"
                    print("Autonomous mode - Right")
                else:
                    set_dac_values(autonomous_dac_values["stop"]["dac1"], autonomous_dac_values["stop"]["dac2"])
                    daci(autonomous_dac_values["left"]["dac1"], autonomous_dac_values["left"]["dac2"])
                    data["command_sent"] = "left"
                    print("Manual mode - Left")

            else:
                # Read data from the sensor
                sensor_data = ser.readline().decode().strip()

                if sensor_data:
                    # Split and convert sensor data
                    sensor_data = sensor_data.split(',')
                    left = int(sensor_data[0])
                    right = int(sensor_data[1])

                    # time.sleep(0.1)

                    # Update the data dictionary with sensor values and colors
                    data["left_value"] = left
                    data["right_value"] = right
                    
                    if right > threshold:
                        data["right_color"] = "black"
                    if left > threshold:
                        data["left_color"] = "black"

                    with open(log_file, 'w') as log:
                        json.dump(data, log)

                        
                    if not config["crawl_on_status"] and not config["nitros_on_status"]:
                        if left < threshold or right < threshold:
                            if left < threshold and right < threshold:
                                set_dac_values(autonomous_dac_values["straight"]["dac1"], autonomous_dac_values["straight"]["dac2"])
                                data["dac1_value"] = autonomous_dac_values["straight"]["dac1"]
                                data["dac2_value"] = autonomous_dac_values["straight"]["dac2"]
                                with open(log_file, 'w') as log:
                                    json.dump(data, log)
                                data["command_sent"] = "straight"
                                print("Autonomous mode - Straight")
                                going_right = False
                                going_left = False
                                
                            elif left > threshold:
                                set_dac_values(autonomous_dac_values["right"]["dac1"], autonomous_dac_values["right"]["dac2"])
                                daci(autonomous_dac_values["right"]["dac1"], autonomous_dac_values["right"]["dac2"])
                                data["command_sent"] = "right"
                                print("Autonomous mode - Right")
                                going_right = True
                            elif right > threshold:
                                set_dac_values(autonomous_dac_values["left"]["dac1"], autonomous_dac_values["left"]["dac2"])
                                daci(autonomous_dac_values["left"]["dac1"], autonomous_dac_values["left"]["dac2"])
                                data["command_sent"] = "left"
                                print("Autonomous mode - Left")
                                going_left = True
                        elif left > threshold or right > threshold:
                            # set_dac_values(autonomous_dac_values["stop"]["dac1"], autonomous_dac_values["stop"]["dac2"])
                            data["command_sent"] = "out"
                            print("Autonomous mode - Stop")
                            print(going_left, going_right)
                            if going_left:
                                set_dac_values(5, 3)
                                daci(5, 3)
                                data["command_sent"] = "right"
                                print("Autonomous mode - g Turn right")
                            elif going_right:
                                set_dac_values(3,5) 
                                daci(3,5)
                                data["command_sent"] = "left"
                                print("Autonomous mode - g Turn left")

                    # Crawl Mode
                    elif config["crawl_on_status"]:
                        if left < threshold or right < threshold:
                            if left < threshold and right < threshold:
                                set_dac_values(crawl_dac_values["straight"]["dac1"], crawl_dac_values["straight"]["dac2"])
                                data["dac1_value"] = crawl_dac_values["straight"]["dac1"]
                                data["dac2_value"] = crawl_dac_values["straight"]["dac2"]
                                with open(log_file, 'w') as log:
                                    json.dump(data, log)
                                data["command_sent"] = "crawl_straight"
                                print("Crawl mode - Straight")
                            elif left > threshold:
                                set_dac_values(crawl_dac_values["right"]["dac1"], crawl_dac_values["right"]["dac2"])
                                daci(crawl_dac_values["right"]["dac1"], crawl_dac_values["right"]["dac2"])
                                data["command_sent"] = "crawl_right"
                                print("Crawl mode - Right")
                                going_right_crawl = True
                            elif right > threshold:
                                set_dac_values(crawl_dac_values["left"]["dac1"], crawl_dac_values["left"]["dac2"])
                                daci(crawl_dac_values["left"]["dac1"], crawl_dac_values["left"]["dac2"])
                                data["command_sent"] = "crawl_left"
                                print("Crawl mode - Left")
                                going_left_crawl = True
                        elif left > threshold or right > threshold:
                            # set_dac_values(crawl_dac_values["stop"]["dac1"], crawl_dac_values["stop"]["dac2"])
                            data["command_sent"] = "crawl_stop"
                            print("Crawl mode - Stop")
                            print(going_left_crawl, going_right_crawl)
                            if going_left_crawl:
                                set_dac_values(crawl_dac_values["left"]["dac1"], crawl_dac_values["left"]["dac2"])
                                daci(crawl_dac_values["left"]["dac1"], crawl_dac_values["left"]["dac2"])
                                data["command_sent"] = "crawl_left"
                                print("Crawl mode - Turn right")
                            elif going_right_crawl:
                                set_dac_values(crawl_dac_values["right"]["dac1"], crawl_dac_values["right"]["dac2"])
                                daci(crawl_dac_values["right"]["dac1"], crawl_dac_values["right"]["dac2"])
                                data["command_sent"] = "crawl_left"
                                print("Crawl mode - Turn left")

                    # Nitros Mode
                    elif config["nitros_on_status"]:
                        if left < threshold or right < threshold:
                            if left < threshold and right < threshold:
                                set_dac_values(nitros_dac_values["straight"]["dac1"], nitros_dac_values["straight"]["dac2"])
                                data["dac1_value"] = nitros_dac_values["straight"]["dac1"]
                                data["dac2_value"] = nitros_dac_values["straight"]["dac2"]
                                with open(log_file, 'w') as log:
                                    json.dump(data, log)
                                data["command_sent"] = "nitros_straight"
                                print("Nitros mode - Straight")
                            elif left > threshold:
                                set_dac_values(nitros_dac_values["right"]["dac1"], nitros_dac_values["right"]["dac2"])
                                daci(nitros_dac_values["right"]["dac1"], nitros_dac_values["right"]["dac2"])
                                data["command_sent"] = "nitros_right"
                                print("Nitros mode - Right")
                                going_right_nitros = True
                            elif right > threshold:
                                set_dac_values(nitros_dac_values["left"]["dac1"], nitros_dac_values["left"]["dac2"])
                                daci(nitros_dac_values["left"]["dac1"], nitros_dac_values["left"]["dac2"])
                                data["command_sent"] = "nitros_left"
                                print("Nitros mode - Left")
                                going_left_nitros = True
                        elif left > threshold or right > threshold:
                            # set_dac_values(nitros_dac_values["stop"]["dac1"], nitros_dac_values["stop"]["dac2"])
                            data["command_sent"] = "nitros_stop"
                            print("Nitros mode - Stop")
                            print(going_left_nitros, going_right_nitros)
                            if going_left_nitros:
                                set_dac_values(nitros_dac_values["left"]["dac1"], nitros_dac_values["left"]["dac2"])
                                daci(nitros_dac_values["left"]["dac1"], nitros_dac_values["left"]["dac2"])
                                data["command_sent"] = "nitros_right"
                                print("Nitros mode - Turn right")
                            elif going_right_nitros:
                                set_dac_values(nitros_dac_values["right"]["dac1"], nitros_dac_values["right"]["dac2"])
                                daci(nitros_dac_values["right"]["dac1"], nitros_dac_values["right"]["dac2"])
                                data["command_sent"] = "nitros_right"
                                print("Nitros mode - Turn right g")
            
            # Determine sensor colors based on the threshold

            

    if not config["start_toggle_status"]:
        # If the "start_toggle_status" is not true, send feedback to Arduino
        while True:
            dac1 = 9
            dac2 = 9
            set_dac_values(dac1, dac2)
            daci(dac1, dac2)
            time.sleep(0.1)  # Add a small delay
            try:
                # Load the configuration from a JSON file
                with open('to_firm.json', 'r') as config_file:
                    config = json.load(config_file)

                # print("Configuration loaded")
                
            except json.decoder.JSONDecodeError as e:
                print(f"Error while decoding JSON: {e}")
                # time.sleep(1)  # Sleep for a moment and then retry
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                # time.sleep(1)  # Sleep for a moment and then retry
                continue

            if config["start_toggle_status"]:
                break
        
    # Update the JSON file with the current data
    with open(log_file, 'w') as log:
            json.dump(data, log)

        # Don't forget to close the serial port when you're done
    ser.close()
