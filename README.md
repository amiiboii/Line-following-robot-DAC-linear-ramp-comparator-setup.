The autonomous vehicle's motion control relies on the Bang-Bang closed-loop strategy, which functions as a binary system. In this approach, the Arduino firmware communicates specific byte combinations to the DACs based on sensor readings, either fully engaging (ON) or completely disengaging (OFF) the control effort. This binary nature, determined by a single set point, allows adaptability to different track conditions.

The Bang-Bang strategy, effective for scenarios with acceptable output variations, has limitations. Abrupt transitions in control effort may lead to jerky movements, and the binary nature hinders adaptability. An alternative, closed-loop control, continuously compares the system's actual output with a desired setpoint. It provides proportional and proportional-integral (PI) adjustments for smoother responses, offering a more sophisticated approach.

The algorithm, integrated with Arduino firmware and Python script through serial communication, continuously reads sensor data. Based on predefined thresholds, it adjusts motor behavior in autonomous mode using different DAC values for actions such as moving straight, turning right or left, or stopping.

To address scenarios where both sensors detect track deviation, the algorithm includes a memory component. This component identifies the first sensor detecting deviation, ensuring a swift correction for enhanced adaptability. The script operates in an infinite loop for real-time monitoring and navigation adaptability.

The Graphical User Interface (GUI) focuses on monitoring and controlling the robot, designed with user-friendly elements. Users can configure settings such as thresholds, baud rates, and serial port details without modifying code. Safety features include an emergency stop button. Different operating speeds and a manual control feature provide flexibility. A login system ensures secure interaction.

A notable feature of the GUI is real-time visualization of sensor data and robot movement, facilitating effective monitoring and decision-making. Security measures include a robust login system to control access, ensuring only authorized users can interact with the robot and enhancing overall system safety.

<img width="963" alt="Screenshot 2023-11-14 at 7 40 44 PM" src="https://github.com/amiiboii/Line-following-robot-DAC-linear-ramp-comparator-setup./assets/121004983/a24e13d2-aef2-4dcf-a8e4-e77465090dd5"><img width="969" alt="Screenshot 2023-11-14 at 7 40 07 PM" src="https://github.com/amiiboii/Line-following-robot-DAC-linear-ramp-comparator-setup./assets/121004983/d101e498-9f0e-4ad8-b639-8e4f20a0c6f8">


