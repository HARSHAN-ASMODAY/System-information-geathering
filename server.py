#!/usr/bin/env python3

import socket
import json
import threading
import datetime
import os
from colorama import init, Fore, Style

init()  # Initialize colorama

class InfoServer:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.connections = []
        self.data_dir = 'collected_data'
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def start(self):
        """Start the server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        
        print(f"{Fore.GREEN}[+] Server listening on {self.host}:{self.port}{Style.RESET_ALL}")
        
        try:
            while True:
                client, address = server.accept()
                self.connections.append(client)
                
                # Start a new thread to handle the client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, address)
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Server shutting down...{Style.RESET_ALL}")
            server.close()
    
    def handle_client(self, client_socket, address):
        """Handle incoming client connections"""
        print(f"{Fore.GREEN}[+] New connection from {address[0]}:{address[1]}{Style.RESET_ALL}")
        
        try:
            # Receive data
            data = b''
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
            
            # Process received data
            if data:
                try:
                    system_info = json.loads(data.decode())
                    self.save_system_info(address[0], system_info)
                    self.display_system_info(address[0], system_info)
                except json.JSONDecodeError:
                    print(f"{Fore.RED}[!] Error decoding data from {address[0]}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error handling client {address[0]}: {str(e)}{Style.RESET_ALL}")
        
        finally:
            client_socket.close()
            if client_socket in self.connections:
                self.connections.remove(client_socket)
    
    def save_system_info(self, ip, info):
        """Save received system information to file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_dir}/{ip}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(info, f, indent=4)
            print(f"{Fore.GREEN}[+] Data saved to {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving data: {str(e)}{Style.RESET_ALL}")
    
    def display_system_info(self, ip, info):
        """Display received system information"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"System Information from {ip}")
        print(f"{'='*50}{Style.RESET_ALL}")
        
        # Display basic system info
        print(f"{Fore.GREEN}[+] Hostname: {info.get('hostname', 'N/A')}")
        print(f"[+] OS: {info.get('os', 'N/A')} {info.get('os_release', '')}")
        print(f"[+] Username: {info.get('username', 'N/A')}")
        print(f"[+] Architecture: {info.get('architecture', 'N/A')}")
        
        # Display network info
        network = info.get('network', {})
        print(f"\n{Fore.YELLOW}[*] Network Information:")
        print(f"    Local IP: {network.get('ip_address', 'N/A')}")
        print(f"    Public IP: {network.get('public_ip', 'N/A')}")
        
        # Display drive information
        drives = info.get('drives', [])
        if drives:
            print(f"\n{Fore.YELLOW}[*] Drive Information:")
            for drive in drives:
                print(f"    Drive: {drive.get('drive', 'N/A')}")
                print(f"    Total Space: {drive.get('total_space', 'N/A')}")
                print(f"    Free Space: {drive.get('free_space', 'N/A')}")
        
        # Display installed software
        software = info.get('installed_software', [])
        if software:
            print(f"\n{Fore.YELLOW}[*] Installed Software (Top {len(software)} items):")
            for item in software:
                print(f"    - {item}")
        
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def main():
    try:
        server = InfoServer()
        server.start()
    except Exception as e:
        print(f"{Fore.RED}[!] Server error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Server terminated by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {str(e)}{Style.RESET_ALL}")
