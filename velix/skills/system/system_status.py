import psutil
import time
import os

def clear_screen():
    """Clear terminal screen for live updates."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_system_info():
    """Fetch and display system information."""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()

    # Memory usage
    mem = psutil.virtual_memory()

    # Disk usage
    disk = psutil.disk_usage('/')

    # Network stats
    net = psutil.net_io_counters()

    # Battery info (if available)
    battery = psutil.sensors_battery()

    print("=== Live System Status ===")
    print(f"CPU Usage per core: {cpu_percent} %")
    print(f"CPU Frequency: {cpu_freq.current:.2f} MHz")
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Used RAM: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    print(f"Disk Usage: {disk.percent}% ({disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB)")
    print(f"Network Sent: {net.bytes_sent / (1024**2):.2f} MB")
    print(f"Network Received: {net.bytes_recv / (1024**2):.2f} MB")
    if battery:
        print(f"Battery: {battery.percent}% {'Charging' if battery.power_plugged else 'Discharging'}")
    else:
        print("Battery: Not available")

if __name__ == "__main__":
    try:
        while True:
            clear_screen()
            get_system_info()
            time.sleep(10)  # Update every second
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
