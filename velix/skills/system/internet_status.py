import speedtest

def test_internet_speed():
    try:
        print("Testing internet speed... Please wait.")
        
        # Create Speedtest object
        st = speedtest.Speedtest()
        
        # Get the best server based on ping
        st.get_best_server()
        
        # Perform download and upload tests
        download_speed = st.download()
        upload_speed = st.upload()
        ping_result = st.results.ping
        
        # Convert speeds from bits/sec to Mbps
        download_mbps = round(download_speed / 1_000_000, 2)
        upload_mbps = round(upload_speed / 1_000_000, 2)
        
        # Display results
        print(f"Ping: {ping_result} ms")
        print(f"Download Speed: {download_mbps} Mbps")
        print(f"Upload Speed: {upload_mbps} Mbps")
    
    except speedtest.ConfigRetrievalError:
        print("Error: Unable to retrieve speedtest configuration. Check your internet connection.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_internet_speed()
