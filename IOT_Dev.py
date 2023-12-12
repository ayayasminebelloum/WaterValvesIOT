import json  # Add this import statement
import time  # Import the time module
from azure.iot.device import IoTHubDeviceClient,Message

# Azure IoT Hub connection parameters
device_connection_string = "YOURCONNECTIONSTRING"

# Create an instance of the device client
client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

# Connect to Azure IoT Hub
client.connect()

try:
    while True:  # Infinite loop
        # Your JSON payload (replace this with your actual data)
        json_payload = {"ValveStatus": 1}

        # Send the JSON payload to Azure IoT Hub
        client.send_message(json.dumps(json_payload))

        print("Message sent:", json_payload)

        # Wait for a specified time before sending the next message
        time.sleep(5)  # Sleep for 5 seconds (adjust as needed)


except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C) to gracefully exit the loop
    pass
finally:
    # Disconnect from Azure IoT Hub
    client.disconnect()
