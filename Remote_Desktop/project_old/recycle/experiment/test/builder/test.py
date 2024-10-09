import os
import psutil
import time

def set_dns():
    # OpenDNS FamilyShield DNS addresses
    primary_dns = "185.228.168.10"
    secondary_dns = "185.228.169.11"
    
    # Command to change DNS settings using netsh
    change_dns_command = f'netsh interface ip set dns name="Wi-Fi" static {primary_dns} primary'
    os.system(change_dns_command)
    add_secondary_dns_command = f'netsh interface ip add dns name="Wi-Fi" {secondary_dns} index=2'
    os.system(add_secondary_dns_command)
    
    # Flush DNS cache
    flush_dns_command = 'ipconfig /flushdns'
    os.system(flush_dns_command)
    
    print("DNS settings updated to use OpenDNS FamilyShield and DNS cache flushed.")

def main():
    previous_networks = set()

    while True:
        current_networks = set(psutil.net_if_addrs().keys())
        
        # If a new network is detected
        if current_networks != previous_networks:
            print("Network change detected.")
            set_dns()
            previous_networks = current_networks

        time.sleep(5)  # Check for network changes every 5 seconds

if __name__ == "__main__":
    main()
