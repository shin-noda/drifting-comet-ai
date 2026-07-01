# main.py
import os
import time
import subprocess
from src.network import CometNetworkManager
from src.agent import SimpleAgent

def main():
    # 1. Define the local path to your Desktop executable
    desktop_path = "/Users/shinnosukenoda/Desktop/drifting_comet.app/Contents/MacOS/Drifting Comet Local"
    
    if not os.path.exists(desktop_path):
        print(f"Error: Could not find game executable at: {desktop_path}")
        print("Please check the path and try again.")
        return

    # 2. Initialize our modular components
    server = CometNetworkManager(ip="127.0.0.1", port=4242)
    
    # -------------------------------------------------------------
    # Update agent configurations or handle logic inline
    # Setting a negative ceiling because the comet flies UP by default!
    # -------------------------------------------------------------
    SAFETY_CEILING = -450.0
    print(f"Agent initialized. Safety ceiling set at Y = {SAFETY_CEILING}")
    
    # Start the local UDP port listener
    server.start_server()

    # 3. Launch the frozen game environment as a background process
    print("\nLaunching Drifting Comet environment...")
    game_process = subprocess.Popen(desktop_path)
    
    print("Handshake loop initialized. Waiting for Godot telemetry data...\n")
    print("Frame | Position (X, Y) | Action Sent")
    print("-" * 45)

    try:
        # 4. Master Control Loop
        while True:
            # Check if the game window was closed by the user
            if game_process.poll() is not None:
                print("\nGame environment closed by user.")
                break

            # Listen for a telemetry packet (1.0s timeout stops it from freezing)
            state, client_address = server.receive_state()
            
            if state is None:
                continue # No packet this millisecond, check again

            # Extract our Phase 1 state variables
            px = state.get("px", 0.0)
            py = state.get("py", 0.0)
            frame = state.get("frame", 0)

            # -------------------------------------------------------------
            # CEILING LOGIC: If the comet flies UP past our negative threshold, 
            # intercept and override the command to trigger the gravity flip!
            # -------------------------------------------------------------
            if py < SAFETY_CEILING:
                action = "FLIP_GRAVITY"
            else:
                action = "NONE"

            # Immediately pipe the decision back to the game over the socket
            server.send_action(action, client_address)

            # Print live diagnostics to your terminal so you can trace the frames
            print(f"{frame:<5} | ({px:>6.1f}, {py:>6.1f}) | {action}")

    except KeyboardInterrupt:
        print("\nShutting down AI controller via terminal signal...")
    finally:
        # 5. Clean up resources cleanly
        server.close()
        if game_process.poll() is None:
            game_process.terminate()
            print("Game environment terminated cleanly.")

if __name__ == "__main__":
    main()