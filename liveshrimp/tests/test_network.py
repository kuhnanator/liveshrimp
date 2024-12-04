import os
import time
import socket
import requests
from urllib.request import urlopen

def check_network():
    """
    Check if the device is connected to a network (Wi-Fi or Ethernet).
    """
    try:
        # Use the 'ping' command to check for network connectivity
        response = os.system("ping -c 1 google.com")

        if response == 0:
            print("Network is connected!")
            return True
        else:
            print("Network is not connected.")
            return False
    except Exception as e:
        print(f"Error checking network: {e}")
        return False

def check_internet():
    """
    Check if the device has internet access by pinging an external server.
    This example uses google.com, but you can replace it with any server you trust.
    """
    try:
        # Attempt to open a URL (using an external service like google.com or any other web page)
        urlopen("http://google.com", timeout=5)
        print("Internet is accessible!")
        return True
    except:
        print("No internet access.")
        return False

def check_specific_server(url="http://example.com"):
    """
    Check if the device can access a specific server or service (e.g., for video uploads or streaming).
    """
    try:
        # Attempt to connect to a specific server or service
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            print(f"Connected to {url} successfully.")
            return True
        else:
            print(f"Failed to connect to {url}. Status Code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        return False

def check_cellular_connection():
    """
    Check if the device has cellular connection (if applicable), for example, by checking if mobile data is available.
    """
    # This is a placeholder. The actual check for cellular connection may vary depending on your hardware and setup.
    # For example, you could use the `usb_modeswitch` or a mobile modem, or check if the Pi is connected to the cellular network.
    # You could also check the signal strength if the device supports this.
    print("Cellular connection check: Not implemented. Check your hardware setup.")
    return False

def test_network():
    """
    Main function to test the network connection.
    It checks the overall network, internet, server connectivity, and optional cellular connection.
    """
    print("Checking network...")
    if check_network():
        print("Network check passed.")
    else:
        print("Network check failed.")

    print("Checking internet connectivity...")
    if check_internet():
        print("Internet check passed.")
    else:
        print("Internet check failed.")

    print("Checking specific server connectivity...")
    server_url = "http://your-server-url.com"  # Replace with your server URL
    if check_specific_server(server_url):
        print("Server check passed.")
    else:
        print("Server check failed.")

    # If you have a cellular setup, you can check it
    print("Checking cellular connection...")
    if check_cellular_connection():
        print("Cellular connection check passed.")
    else:
        print("Cellular connection check failed.")

if __name__ == "__main__":
    test_network()
