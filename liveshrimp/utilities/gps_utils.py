import gpsd
import time

# Connect to the GPSD service
def connect_to_gpsd():
    """
    Connect to the GPSD daemon to retrieve GPS data.
    """
    try:
        gpsd.connect()
        print("Connected to GPSD.")
    except Exception as e:
        print(f"Failed to connect to GPSD: {e}")

# Retrieve the current GPS data
def get_gps_data():
    """
    Fetch and return current GPS data: latitude, longitude, speed, elevation, and time.

    Returns:
        dict: Contains lat, lon, speed, elevation, and timestamp.
    """
    try:
        # Get GPS position
        gps_data = gpsd.get_current()

        # Extract required values
        gps_info = {
            "latitude": gps_data.lat,
            "longitude": gps_data.lon,
            "speed": gps_data.hspeed,  # Horizontal speed in m/s
            "elevation": gps_data.alt,  # Altitude in meters
            "time": gps_data.time  # Timestamp of the data
        }
        return gps_info
    except Exception as e:
        print(f"Error retrieving GPS data: {e}")
        return None

# Format GPS data for display
def format_gps_data(gps_data):
    """
    Format the GPS data into a readable string for display purposes.

    Args:
        gps_data (dict): Dictionary containing GPS data.

    Returns:
        str: A formatted string with GPS data.
    """
    if gps_data is None:
        return "GPS Data unavailable"

    gps_string = (
        f"Latitude: {gps_data['latitude']:.6f}\n"
        f"Longitude: {gps_data['longitude']:.6f}\n"
        f"Speed: {gps_data['speed']} m/s\n"
        f"Elevation: {gps_data['elevation']} meters\n"
        f"Time: {gps_data['time']}"
    )

    return gps_string

# Function to get GPS data and format for overlay
def get_and_format_gps_data():
    """
    Retrieve and format GPS data for overlay or display on the stream.

    Returns:
        str: Formatted GPS data string for overlay.
    """
    gps_data = get_gps_data()
    return format_gps_data(gps_data)

# Handle GPS signal loss
def check_gps_signal():
    """
    Check if the GPS signal is available. If not, return a fallback message.

    Returns:
        str: "GPS Signal Lost" if no signal, otherwise returns the GPS data.
    """
    gps_data = get_gps_data()
    if gps_data is None:
        return "GPS Signal Lost"
    return format_gps_data(gps_data)

if __name__ == "__main__":
    # Example: Connect to GPS and get GPS data every 5 seconds
    connect_to_gpsd()

    while True:
        gps_data = get_and_format_gps_data()
        print(gps_data)
        time.sleep(5)  # Sleep for 5 seconds before checking again
