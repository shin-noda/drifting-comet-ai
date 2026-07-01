# src/agent.py

class SimpleAgent:
    def __init__(self, threshold_y=450.0):
        # In 2D screens, (0,0) is top-left. As objects fall down, Y increases.
        # Let's pick a safety line where the comet should invert its gravity.
        self.threshold_y = threshold_y
        print(f"Agent initialized. Safety floor set at Y = {self.threshold_y}")

    def decide(self, px, py):
        """
        Evaluates the current state coordinates and returns an action string.
        """
        # If the comet falls below our safety floor line (higher Y value),
        # trigger a gravity inversion!
        if py > self.threshold_y:
            return "INVERT_GRAVITY"
        
        # Otherwise, maintain current trajectory
        return "NONE"