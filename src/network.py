# src/network.py
import socket
import json

class CometNetworkManager:
    def __init__(self, ip="127.0.0.1", port=4242):
        self.ip = ip
        self.port = port
        self.sock = None

    def start_server(self):
        """Initializes the UDP socket and binds it to localhost."""
        # AF_INET = IPv4 protocol, SOCK_DGRAM = UDP datagrams
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        
        # 1-second timeout prevents Python from freezing forever if the game stops
        self.sock.settimeout(1.0)
        print(f"UDP Server listening on {self.ip}:{self.port}...")

    def receive_state(self):
        """Listens for an incoming state packet from Godot."""
        try:
            # 1024 bytes buffer is plenty for our small telemetry packets
            data, addr = self.sock.recvfrom(1024)
            
            # Decode raw bytes into string, then parse the JSON into a dictionary
            state_data = json.loads(data.decode('utf-8'))
            return state_data, addr
        except socket.timeout:
            return None, None
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None, None

    def send_action(self, action_string, addr):
        """Sends the AI's action choice back to Godot."""
        try:
            # Package the clean action string back into raw network bytes
            packet = action_string.encode('utf-8')
            self.sock.sendto(packet, addr)
        except Exception as e:
            print(f"Error sending data: {e}")

    def close(self):
        """Cleans up the network socket resources safely."""
        if self.sock:
            self.sock.close()
            print("Socket closed successfully.")