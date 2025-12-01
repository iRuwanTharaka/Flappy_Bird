"""Main entry point for Flappy Bird game."""
import pygame
from pygame.locals import *
import time

from game import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGE_PATHS,
    TINY_FONT, BLUE, GRAY, API_BASE_URL, HEART_PUZZLE_API_URL, HEART_TIME_LIMIT,
    APIClient, HeartPuzzleAPI, GameState, ScreenState,
    GameEngine, HeartPuzzle, ScreenRenderer
)


class FlappyBirdGame:
    """Main game class that orchestrates all components."""
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird + Heart Puzzle")
        
        # Load images
        self.bg = pygame.image.load(IMAGE_PATHS['bg'])
        self.ground_img = pygame.image.load(IMAGE_PATHS['ground'])
        
        # Initialize components
        self.game_state = GameState()
        self.api_client = APIClient(API_BASE_URL)
        self.heart_puzzle_api = HeartPuzzleAPI(HEART_PUZZLE_API_URL, HEART_TIME_LIMIT)
        self.heart_puzzle = HeartPuzzle(self.heart_puzzle_api)
        self.game_engine = GameEngine(self.game_state)
        self.screen_renderer = ScreenRenderer(self.screen, self.game_state, self.api_client)
        
        self.running = True
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            # Handle heart puzzle input
            if self.heart_puzzle.active:
                self._handle_heart_puzzle_input(event)
    
    def _handle_keydown(self, event):
        """Handle keyboard input."""
        # ESC key handling
        if event.key == pygame.K_ESCAPE:
            if self.game_state.current_screen in [ScreenState.LEADERBOARD, ScreenState.PROFILE]:
                self.game_state.current_screen = ScreenState.HOME
            elif self.game_state.game_started:
                self.game_state.return_to_home()
            elif self.game_state.current_screen == ScreenState.REGISTER:
                self.game_state.current_screen = ScreenState.LOGIN
                self.game_state.current_input_field = "login_username"
        
        # Input field handling
        if self.game_state.current_screen in [ScreenState.LOGIN, ScreenState.REGISTER]:
            self._handle_input_field(event)
        
        # Game controls
        if (event.key == pygame.K_SPACE and 
            self.game_state.game_started and 
            not self.game_state.flying and 
            not self.game_state.game_over and 
            not self.heart_puzzle.active and 
            not self.game_state.countdown_active):
            self.game_state.flying = True
    
    def _handle_input_field(self, event):
        """Handle input field keyboard events."""
        if event.key == pygame.K_TAB:
            self._cycle_input_field()
        elif event.key == pygame.K_BACKSPACE:
            self._handle_backspace()
        elif event.unicode and event.unicode.isprintable():
            self._handle_text_input(event.unicode)
    
    def _cycle_input_field(self):
        """Cycle through input fields with TAB."""
        if self.game_state.current_screen == ScreenState.LOGIN:
            if self.game_state.current_input_field == "login_username":
                self.game_state.current_input_field = "login_password"
            else:
                self.game_state.current_input_field = "login_username"
        elif self.game_state.current_screen == ScreenState.REGISTER:
            if self.game_state.current_input_field == "register_username":
                self.game_state.current_input_field = "register_email"
            elif self.game_state.current_input_field == "register_email":
                self.game_state.current_input_field = "register_password"
            else:
                self.game_state.current_input_field = "register_username"
    
    def _handle_backspace(self):
        """Handle backspace in input fields."""
        if self.game_state.current_screen == ScreenState.LOGIN:
            if self.game_state.current_input_field == "login_username":
                self.game_state.login_username = self.game_state.login_username[:-1]
            elif self.game_state.current_input_field == "login_password":
                self.game_state.login_password = self.game_state.login_password[:-1]
        elif self.game_state.current_screen == ScreenState.REGISTER:
            if self.game_state.current_input_field == "register_username":
                self.game_state.register_username = self.game_state.register_username[:-1]
            elif self.game_state.current_input_field == "register_email":
                self.game_state.register_email = self.game_state.register_email[:-1]
            elif self.game_state.current_input_field == "register_password":
                self.game_state.register_password = self.game_state.register_password[:-1]
    
    def _handle_text_input(self, char):
        """Handle text input in fields."""
        if self.game_state.current_screen == ScreenState.LOGIN:
            if self.game_state.current_input_field == "login_username":
                self.game_state.login_username += char
            elif self.game_state.current_input_field == "login_password":
                self.game_state.login_password += char
        elif self.game_state.current_screen == ScreenState.REGISTER:
            if self.game_state.current_input_field == "register_username":
                self.game_state.register_username += char
            elif self.game_state.current_input_field == "register_email":
                self.game_state.register_email += char
            elif self.game_state.current_input_field == "register_password":
                self.game_state.register_password += char
    
    def _handle_heart_puzzle_input(self, event):
        """Handle input for heart puzzle."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.heart_puzzle.input = self.heart_puzzle.input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.heart_puzzle.check_answer():
                    # Correct answer - continue game
                    self.game_state.countdown_active = True
                    self.game_state.countdown_end_time = time.time() + 3
                    self.game_engine.checkpoint_reset()
                    self.game_state.heart_lifeline_used = False
                else:
                    # Wrong answer - game over
                    self.heart_puzzle.deactivate()
                    self.game_state.game_over = True
                    self.game_state.heart_lifeline_used = True
            elif event.unicode and event.unicode.isdigit():
                self.heart_puzzle.input += event.unicode
                if len(self.heart_puzzle.input) > 5:
                    self.heart_puzzle.input = self.heart_puzzle.input[:5]
    
    def update_game(self):
        """Update game logic."""
        if not self._should_update_game():
            return
        
        # Normal game mode
        if not self.heart_puzzle.active and not self.game_state.countdown_active:
            self.game_engine.update()
            
            # Check collisions
            if self.game_engine.check_collisions():
                if not self.game_state.heart_lifeline_used:
                    # Activate heart puzzle as lifeline
                    if self.heart_puzzle.activate():
                        self.game_state.heart_lifeline_used = True
                        self.game_state.flying = False
                    else:
                        # API failure - game over
                        self.game_state.game_over = True
                else:
                    # Lifeline already used, game over
                    self.game_state.game_over = True
            
            # Handle game over
            if self.game_state.game_over:
                self._handle_game_over()
        
        # Heart puzzle mode
        elif self.heart_puzzle.active:
            if self.heart_puzzle.is_time_up():
                self.heart_puzzle.deactivate()
                self.game_state.game_over = True
                self.game_state.heart_lifeline_used = True
        
        # Countdown mode
        elif self.game_state.countdown_active:
            remaining_time = int(self.game_state.countdown_end_time - time.time())
            if remaining_time <= 0:
                self.game_state.countdown_active = False
                self.game_state.game_over = False
                self.game_state.flying = True
                self.game_state.puzzle_solved = False
    
    def _should_update_game(self):
        """Check if game should be updated."""
        return (self.game_state.game_started and 
                self.game_state.current_screen == ScreenState.GAME)
    
    def _handle_game_over(self):
        """Handle game over logic."""
        # Submit score if logged in and not already submitted
        if (self.api_client.auth_token and 
            self.game_state.score > 0 and 
            (not self.api_client.score_submitted or 
             self.game_state.score != self.api_client.last_submitted_score)):
            success, msg = self.api_client.submit_score(self.game_state.score)
            if success:
                self.api_client.get_user_rank()
        
        # Auto-redirect to home after 3 seconds
        if self.game_state.game_over_screen_timer == 0:
            self.game_state.game_over_screen_timer = time.time()
        
        elapsed = time.time() - self.game_state.game_over_screen_timer
        if elapsed >= 3:
            self.game_engine.reset_game()
            self.game_state.return_to_home()
            self.api_client.score_submitted = False
            self.api_client.last_submitted_score = 0
    
    def render(self):
        """Render the current screen."""
        # Render UI screens
        if self.game_state.current_screen == ScreenState.LOGIN:
            self.screen_renderer.draw_login_screen()
        elif self.game_state.current_screen == ScreenState.REGISTER:
            self.screen_renderer.draw_register_screen()
        elif self.game_state.current_screen == ScreenState.HOME:
            self.screen_renderer.draw_home_screen()
        elif self.game_state.current_screen == ScreenState.LEADERBOARD:
            self.screen_renderer.draw_leaderboard_screen()
        elif self.game_state.current_screen == ScreenState.PROFILE:
            if self.api_client.auth_token:
                self.screen_renderer.draw_profile_screen()
        
        # Render game
        if self._should_update_game():
            if not self.heart_puzzle.active and not self.game_state.countdown_active:
                if not self.game_state.game_over:
                    self.game_engine.draw(self.screen, self.bg, self.ground_img)
                else:
                    # Game over screen
                    remaining = int(3 - (time.time() - self.game_state.game_over_screen_timer))
                    self.screen_renderer.draw_game_over_screen(
                        self.bg, self.ground_img, self.game_state.ground_scroll,
                        self.game_engine.bird_group, self.game_state.score, remaining
                    )
            elif self.heart_puzzle.active:
                self.screen_renderer.draw_heart_puzzle_screen(self.heart_puzzle)
            elif self.game_state.countdown_active:
                remaining_time = int(self.game_state.countdown_end_time - time.time())
                if remaining_time < 0:
                    remaining_time = 0
                self.screen_renderer.draw_countdown_screen(
                    self.bg, self.ground_img, self.game_state.ground_scroll,
                    self.game_engine.bird_group, self.game_state.score, remaining_time,
                    self.game_state.flying, self.game_state.game_over, self.game_state.countdown_active
                )
            
            # Show user info overlay in game
            if self.api_client.auth_token and self.api_client.user_info:
                user_text = f"User: {self.api_client.user_info.get('username', 'N/A')}"
                if self.api_client.user_rank:
                    user_text += f" | Rank: #{self.api_client.user_rank.get('rank', 'N/A')}"
                self._draw_text(user_text, TINY_FONT, BLUE, 10, 10)
                self._draw_text("ESC: Home", TINY_FONT, GRAY, 10, SCREEN_HEIGHT - 20)
        
        pygame.display.update()
    
    def _draw_text(self, text, font, col, x, y):
        """Helper to draw text."""
        img = font.render(text, True, col)
        self.screen.blit(img, (x, y))
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_game()
            self.render()
        
        pygame.quit()


def main():
    """Entry point."""
    game = FlappyBirdGame()
    game.run()


if __name__ == "__main__":
    main()
