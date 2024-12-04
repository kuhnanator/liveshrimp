import psutil
import time

# Battery monitoring constants
LOW_BATTERY_THRESHOLD = 20  # Threshold for low battery warning (percentage)

def get_battery_status():
    """
    Retrieve the current battery status if available.

    Returns:
        dict: Battery status including percentage and whether plugged in.
    """
    battery = psutil.sensors_battery()
    if battery is None:
        return None

    battery_info = {
        "percentage": battery.percent,
        "plugged": battery.power_plugged,
        "time_left": battery.secsleft / 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
    }
    return battery_info

def display_battery_status():
    """
    Display the current battery status on the console or log.
    """
    battery_status = get_battery_status()

    if battery_status is None:
        print("Battery information not available.")
        return

    print(f"Battery Percentage: {battery_status['percentage']}%")
    if battery_status['plugged']:
        print("Power source: External (plugged in)")
    else:
        print("Power source: Battery")

    if battery_status['time_left'] is not None:
        print(f"Time left: {battery_status['time_left']} minutes")
    else:
        print("Battery time left: Unknown")

def is_battery_low():
    """
    Check if the battery percentage is below the low battery threshold.

    Returns:
        bool: True if the battery is low, False otherwise.
    """
    battery_status = get_battery_status()
    if battery_status is None:
        return False

    return battery_status['percentage'] < LOW_BATTERY_THRESHOLD

def alert_on_low_battery():
    """
    Display an alert if the battery is below the low battery threshold.
    """
    if is_battery_low():
        print("Warning: Battery is below the threshold! Consider charging or plugging in.")
    else:
        print("Battery level is sufficient.")

def monitor_battery(interval=60):
    """
    Periodically check battery status and take appropriate action.

    Args:
        interval (int): Interval in seconds between each check (default 60 seconds).
    """
    while True:
        alert_on_low_battery()
        display_battery_status()
        time.sleep(interval)

if __name__ == "__main__":
    # Run battery monitor every 60 seconds
    monitor_battery(interval=60)
