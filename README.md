# WaterValvesIOT
This project simulates a water management plant. Please note you will need a password to access the admin panel. The password is: "cloud"

## Requirements
- Python 3.10
- pip
- virtualenv
- Raspeberry Pi Simulator: https://azure-samples.github.io/raspberry-pi-web-simulator
- Azure IoT Hub: https://azure.microsoft.com/en-us/services/iot-hub/

## Installation
1. Please note that yoy may either run the application locally or use the deployed version https://cloudcomputing-igat2asrcpa9uypua2fmbc.streamlit.app. 
   - If you want to run the application locally, please follow the steps below. If you want to use the deployed version, please skip to step 7.
2. Clone the repository
3. Create a virtual environment: `virtualenv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Run the application: streamlit run UItoIOThub.py or click on used the deployed version https://cloudcomputing-igat2asrcpa9uypua2fmbc.streamlit.app
 -- Please note that if you want to see the valve status print in the console, you need to run the application locally.
7. Open the Raspberry Pi Simulator and paste the code from `raspberry_pi_connection.js` in the code section of the Raspery Pi Simulator (right-hand side)
8. Click on the `Run` button.
9. You are now ready to interact with the UI!

## The Project
The project is divided into two parts: the UI and the Raspberry Pi Simulator.
The back-end essentially works as follows:

The script establishes a connection to Azure IoT Hub using the IoTHubRegistryManager from the azure.iot.hub module. It utilizes a connection string specified in the CONNECTION_STRING variable. The script manages valve status and devices in a water treatment plant, with a list of device IDs representing valves and a dictionary (valve_status) tracking their current status (open/closed).

Several functions are defined:
- connect_to_hub(): Establishes a connection to Azure IoT Hub and returns a registry manager instance.
- send_message_and_disconnect(device_id, json_payload): Sends a message to Azure IoT Hub with a JSON payload for a specific device and disconnects afterward.
- open_valve(device_id): Opens a valve when an open button is pressed by sending a message with a payload indicating an open status to Azure IoT Hub.
- close_valve(device_id): Closes a valve when a close button is pressed by sending a message with a payload indicating a closed status to Azure IoT Hub.
- read_valve_status_for_ui(): Reads valve status from a file (valve_status.json) for user interface display.
- write_valve_status_for_ui(data): Writes valve status to a file for user interface display.
- admin_login(): Takes an admin password as input from the user using Streamlit's text_input.
- admin_actions(): Displays admin actions (open/close valves) and a sleep button for a specified duration.
- user_actions(): Displays user actions (view valve status).
- sleep_function(sleep_duration): Sleeps for a specified duration meaning that the status of the valves is only check 
after this time has passed
