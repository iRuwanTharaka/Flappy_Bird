"""Heart puzzle lifeline logic."""
import time
import pygame
from .config import HEART_TIME_LIMIT


class HeartPuzzle:
    """Manages heart puzzle lifeline state and logic."""
    
    def __init__(self, puzzle_api):
        self.puzzle_api = puzzle_api
        self.active = False
        self.image = None
        self.answer = None
        self.input = ""
        self.start_time = 0
        self.solved = False
        self.time_limit = HEART_TIME_LIMIT
    
    def activate(self):
        """Activate the heart puzzle lifeline."""
        success, image, answer = self.puzzle_api.fetch_puzzle()
        if success:
            self.active = True
            self.image = image
            self.answer = answer
            self.input = ""
            self.start_time = time.time()
            self.solved = False
            return True
        return False
    
    def deactivate(self):
        """Deactivate the heart puzzle."""
        self.active = False
        self.image = None
        self.answer = None
        self.input = ""
        self.solved = False
    
    def get_remaining_time(self):
        """Get remaining time in seconds."""
        if not self.active:
            return 0
        elapsed = int(time.time() - self.start_time)
        remaining = self.time_limit - elapsed
        return max(0, remaining)
    
    def is_time_up(self):
        """Check if time limit has been exceeded."""
        return self.get_remaining_time() <= 0
    
    def check_answer(self):
        """Check if the current input matches the answer."""
        if self.input == self.answer:
            self.solved = True
            self.deactivate()
            return True
        return False
    
    def handle_input(self, event):
        """Handle keyboard input for the puzzle."""
        if not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1]
            elif event.key == pygame.K_RETURN:
                return self.check_answer()
            elif event.unicode and event.unicode.isdigit():
                self.input += event.unicode
                if len(self.input) > 5:
                    self.input = self.input[:5]
        return False

