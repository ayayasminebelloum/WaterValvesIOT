import json
import time
from azure.iot.device import IoTHubDeviceClient, Message
import RPi.GPIO as GPIO

# Azure IoT Hub connection parameters
device_connection_string = "HostName=WaterValves.azure-devices.net;DeviceId=Valve1;SharedAccessKey=k/DtGT+J60IbObQGsfVU6oDSiKHmiWOPAAIoTBVYwOU="

# Raspberry Pi GPIO pin for the LED
led_pin = 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

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

        # Check if the valve is open (modify the condition as needed)
        if json_payload["ValveStatus"] == 1:
            # Turn on the LED
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            # Turn off the LED
            GPIO.output(led_pin, GPIO.LOW)

        # Check if the LED is on
        if GPIO.input(led_pin) == GPIO.HIGH:
            print("LED is ON")
        else:
            print("LED is OFF")

        # Wait for a specified time before sending the next message
        time.sleep(5)  # Sleep for 5 seconds (adjust as needed)

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C) to gracefully exit the loop
    pass
finally:
    # Turn off the LED and clean up GPIO
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.cleanup()

    # Disconnect from Azure IoT Hub
    client.disconnect()
