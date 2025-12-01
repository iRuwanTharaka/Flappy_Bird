"""Centralized game state management."""
from enum import Enum


class ScreenState(Enum):
    """Enumeration of possible screen states."""
    LOGIN = "login"
    REGISTER = "register"
    HOME = "home"
    LEADERBOARD = "leaderboard"
    PROFILE = "profile"
    GAME = "game"


class GameState:
    """Manages all game state variables."""
    
    def __init__(self):
        # Screen state
        self.current_screen = ScreenState.LOGIN
        self.game_started = False
        
        # Game variables
        self.ground_scroll = 0
        self.flying = False
        self.game_over = False
        self.last_pipe = 0
        self.score = 0
        self.pass_pipe = False
        
        # Heart puzzle state
        self.heart_active = False
        self.heart_image = None
        self.heart_answer = None
        self.heart_input = ""
        self.heart_start_time = 0
        self.puzzle_solved = False
        self.heart_lifeline_used = False
        
        # Countdown state
        self.countdown_active = False
        self.countdown_end_time = 0
        
        # Input fields
        self.login_username = ""
        self.login_password = ""
        self.register_username = ""
        self.register_email = ""
        self.register_password = ""
        self.current_input_field = None
        
        # Game over screen
        self.game_over_screen_timer = 0
        
        # Error messages (for UI feedback)
        self.login_error_message = ""
        self.register_error_message = ""
        self.register_success_message = ""
    
    def reset_game(self):
        """Reset game to initial state."""
        self.flying = False
        self.game_over = False
        self.score = 0
        self.pass_pipe = False
        self.heart_lifeline_used = False
        self.game_over_screen_timer = 0
        self.puzzle_solved = False
        self.heart_active = False
        self.countdown_active = False
    
    def clear_messages(self):
        """Clear all error/success messages."""
        self.login_error_message = ""
        self.register_error_message = ""
        self.register_success_message = ""
    
    def start_new_game(self):
        """Initialize state for a new game."""
        self.reset_game()
        self.game_started = True
        self.current_screen = ScreenState.GAME
    
    def return_to_home(self):
        """Return to home screen."""
        self.game_started = False
        self.current_screen = ScreenState.HOME
        self.reset_game()
    
    def is_in_game(self):
        """Check if currently in game mode."""
        return (self.game_started and 
                self.current_screen == ScreenState.GAME)

