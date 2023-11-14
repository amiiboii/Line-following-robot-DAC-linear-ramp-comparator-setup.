import subprocess
import time

# Step 1: Run login_manager.py
try:
    subprocess.run(["python3", "login_manager.py"], check=True)
except subprocess.CalledProcessError:
    print("Error running login_manager.py")

while True:
    # Step 2: Read login_signal file
    with open("login_signal.txt", "r") as signal_file:
        signal = signal_file.read().strip()

    # Step 3: Check if login_signal is 1 and run gui.py and test.py simultaneously, or wait 1 second if it's 0
    if signal == "1":
        try:
            # Start gui.py and test.py concurrently
            gui_process = subprocess.Popen(["python3", "gui.py"])
            test_process = subprocess.Popen(["python3", "test.py"])

            # Wait for both processes to complete
            gui_process.wait()
            test_process.wait()
        except subprocess.CalledProcessError:
            print("Error running gui.py or test.py")
    elif signal == "0":
        print("Waiting for 1 second...")
        time.sleep(1)  # Wait for 1 second
