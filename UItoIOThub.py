import streamlit as st
import json
from azure.iot.device import IoTHubDeviceClient, Message, exceptions as iot_exceptions
from datetime import datetime

# Define all connections for valves
device_connection_strings = [
    "HostName=WaterValves.azure-devices.net;DeviceId=Valve1;SharedAccessKey=k/DtGT+J60IbObQGsfVU6oDSiKHmiWOPAAIoTBVYwOU=",
    "HostName=WaterValves.azure-devices.net;DeviceId=Valve2;SharedAccessKey=8Qp34bgyQaLss7xQVEg0Fl3SV0k/oe8y7AIoTM2+m3I=",
    "HostName=WaterValves.azure-devices.net;DeviceId=Valve3;SharedAccessKey=JG2yofiTk6EnmG1fkgWsC+uLF9V4jfmmeAIoTAzJvBQ=",
    "HostName=WaterValves.azure-devices.net;DeviceId=Valve4;SharedAccessKey=hNYff1RtPAuzDWYo/gV1i8MnQETbitA6WAIoTBGNhlU="
]

#Login page so that only admin can change the valve status
def login_page():
    st.title("Welcome to our Water Treament Plant")

    # Button to choose role
    role = st.radio("Choose your role:", ("User", "Admin"))

    if role == "Admin":
        password = st.text_input("Enter password:", type="password")
        return role, password

    elif role == "User":
        st.button("Log In")
        return role, None

# Initialize status dictionary
valve_status = {}


def connect_to_hub(i):
    """Connect to Azure IoT Hub and return the client"""
    print("Hub", device_connection_strings[i-1])
    return IoTHubDeviceClient.create_from_connection_string(device_connection_strings[i-1])

def send_message_and_disconnect(client, json_payload):
    """Send a message to Azure IoT Hub and disconnect"""
    client.connect()
    client.send_message(json.dumps(json_payload))
    client.disconnect()

def open_valve(i):
    try:
        """Open the valve by sending a message to Azure IoT Hub"""
        client = connect_to_hub(i)
        json_payload = {"ValveStatus": 1}
        send_message_and_disconnect(client, json_payload)
        valve_status[i] = "Open"
    except iot_exceptions.ConnectionFailedError as e:
        print(f"Error connecting to IoT Hub: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def close_valve(i):
    """Close the valve by sending a message to Azure IoT Hub"""
    try:
        client = connect_to_hub(i)
        json_payload = {"ValveStatus": 0}
        send_message_and_disconnect(client, json_payload)
        valve_status[i] = "Closed"
    except iot_exceptions.ConnectionFailedError as e:
        print(f"Error connecting to IoT Hub: {e}")
        # Handle the error as needed, e.g., inform the user or log the error.
        # valve_status[i] = "Error"  # Optionally, set a status indicating an error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle the error as needed.
        # valve_status[i] = "Error"  # Optionally, set a status indicating an error

def read_valve_status_for_ui():
    try:
        with open("valve_status.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        for i in range(1, 5):
            data = {"Valve Number": {i: {"Valve Status": 0}}}
    return data

def write_valve_status_for_ui(data):
    with open("valve_status.json", "w") as file:
        json.dump(data, file)

def admin():
    data = read_valve_status_for_ui()  # Read existing data
    # Control valves
    for i in range(1, 5):
        current_datetime = datetime.now()
        if current_datetime.hour >= 0 and current_datetime.hour < 6:
            valve_status[i] = "Closed"
        elif current_datetime.hour > 6 and current_datetime.hour < 12:
            valve_status[i] = "Open"
        elif current_datetime.hour > 12 and current_datetime.hour > 18:
            valve_status[i] = "Closed"
        else:
            valve_status[i] = "Open"
        st.subheader(f"Control Valve: {i}")

        # Check if the user manually opened or closed the valve
        if st.button("Open Valve", key=f"open_{i}"):
            # Connect With Hub
            open_valve(i)

        if st.button("Close Valve", key=f"close_{i}"):
            close_valve(i)
        
        st.write(f"Valve {i} status: {valve_status[i]}")


        # Save data to be used by the user view 
        data["Valve Number"][str(i)] = {"Valve Status": valve_status[i]}

    # Save the updated data
    write_valve_status_for_ui(data)

def user():
      data = read_valve_status_for_ui()  # Read existing data
      for i in range(1,5):
        st.subheader(f"Control Valve: {i}")
        if i in valve_status:
            st.write(f"Valve {i} status: {valve_status[i]}")
        else:
            current_datetime = datetime.now()
            if current_datetime.hour >= 0 and current_datetime.hour < 6:
                valve_status[i] = "Closed"
            elif current_datetime.hour > 6 and current_datetime.hour < 12:
                valve_status[i] = "Open"
            elif current_datetime.hour > 12 and current_datetime.hour > 18:
                valve_status[i] = "Closed"
            else:
                valve_status[i] = "Open"

            st.write(f"Valve {i} status: {valve_status[i]}")


def ui():
    role, password = login_page()

    if role == "Admin":
        if password == "WATER":
            admin()
        elif password is not None:
            st.warning("Incorrect password. Please try again.")

    elif role == "User":
        user()

# Run the app if the script is executed
if __name__ == "__main__":
    ui()