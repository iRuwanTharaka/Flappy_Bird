"""UI screen rendering functions."""
import pygame
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FONT, SMALL_FONT, LARGE_FONT, TINY_FONT,
    WHITE, BLACK, RED, GREEN, BLUE, GRAY, GROUND_HEIGHT, IMAGE_PATHS
)
from .sprites import TextButton
from .game_state import ScreenState


def draw_text(screen, text, font, col, x, y):
    """Draw text on screen."""
    img = font.render(text, True, col)
    screen.blit(img, (x, y))


def draw_input_field(screen, x, y, width, height, text, active, label=""):
    """Draw an input field."""
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    
    if label:
        label_surface = TINY_FONT.render(label, True, WHITE)
        screen.blit(label_surface, (x, y - 20))
    
    display_text = text if text else ""
    if active:
        display_text += "|"  # Cursor
    
    text_surface = SMALL_FONT.render(display_text, True, WHITE)
    screen.blit(text_surface, (x + 5, y + 5))


class ScreenRenderer:
    """Handles rendering of all UI screens."""
    
    def __init__(self, screen, game_state, api_client):
        self.screen = screen
        self.game_state = game_state
        self.api_client = api_client
        # Auth (login/register) background
        self.auth_bg = pygame.transform.scale(
            pygame.image.load(IMAGE_PATHS['cover']),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        # Home background image
        self.home_bg = pygame.transform.scale(
            pygame.image.load(IMAGE_PATHS['home']),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        # Heart puzzle background image
        self.heart_bg = pygame.transform.scale(
            pygame.image.load(IMAGE_PATHS['heartbg']),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        # Shared background for profile and leaderboard
        self.profile_bg = pygame.transform.scale(
            pygame.image.load(IMAGE_PATHS['dp']),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
    
    def draw_login_screen(self):
        """Draw login screen."""
        # Background image
        self.screen.blit(self.auth_bg, (0, 0))

        # Layout helpers for centering form
        form_width = 500
        field_height = 50
        center_x = SCREEN_WIDTH // 2 - form_width // 2

        # Title centered with slight shadow
        title_x = SCREEN_WIDTH // 2 - 90
        draw_text(self.screen, "LOGIN", LARGE_FONT, BLACK, title_x - 2, 43)
        draw_text(self.screen, "LOGIN", LARGE_FONT, WHITE, title_x, 40)
        
        # Username field (centered, placed lower on screen)
        draw_input_field(
            self.screen, center_x, 460, form_width, field_height,
            self.game_state.login_username,
            self.game_state.current_input_field == "login_username",
            "Username / Email"
        )
        
        # Password field
        draw_input_field(
            self.screen, center_x, 540, form_width, field_height,
            "*" * len(self.game_state.login_password),
            self.game_state.current_input_field == "login_password",
            "Password"
        )
        
        # Buttons centered under fields
        btn_width = 200
        btn_y = 630
        dark_bg = (20, 20, 20)
        hover_bg = (70, 130, 180)

        login_btn = TextButton(
            SCREEN_WIDTH // 2 - btn_width - 10, btn_y,
            btn_width, 50, "Login", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        register_btn = TextButton(
            SCREEN_WIDTH // 2 + 10, btn_y,
            btn_width, 50, "Register", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        
        if login_btn.draw(self.screen):
            success, message = self.api_client.login(
                self.game_state.login_username,
                self.game_state.login_password
            )
            if success:
                self.game_state.current_screen = ScreenState.HOME
                self.game_state.current_input_field = None
                self.game_state.login_username = ""
                self.game_state.login_password = ""
                self.game_state.login_error_message = ""
                self.api_client.get_profile()
                self.api_client.get_user_rank()
            else:
                self.game_state.login_error_message = message
        
        # Draw error message if present
        if self.game_state.login_error_message:
            draw_text(
                self.screen,
                self.game_state.login_error_message,
                SMALL_FONT,
                RED,
                center_x,
                740,
            )
        
        if register_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.REGISTER
            self.game_state.current_input_field = "register_username"
    
    def draw_register_screen(self):
        """Draw register screen."""
        # Background image
        self.screen.blit(self.auth_bg, (0, 0))

        # Layout helpers for centering form
        form_width = 500
        field_height = 50
        center_x = SCREEN_WIDTH // 2 - form_width // 2

        # Title centered with slight shadow
        title_x = SCREEN_WIDTH // 2 - 160
        draw_text(self.screen, "REGISTER", LARGE_FONT, BLACK, title_x - 2, 43)
        draw_text(self.screen, "REGISTER", LARGE_FONT, WHITE, title_x, 40)
        
        # Username field (lower on screen)
        draw_input_field(
            self.screen, center_x, 460, form_width, field_height,
            self.game_state.register_username,
            self.game_state.current_input_field == "register_username",
            "Username"
        )
        
        # Email field
        draw_input_field(
            self.screen, center_x, 540, form_width, field_height,
            self.game_state.register_email,
            self.game_state.current_input_field == "register_email",
            "Email"
        )
        
        # Password field
        draw_input_field(
            self.screen, center_x, 620, form_width, field_height,
            "*" * len(self.game_state.register_password),
            self.game_state.current_input_field == "register_password",
            "Password"
        )
        
        # Buttons (centered). Place "Back to Login" lower so a single
        # long mouse click doesn't instantly trigger both screens.
        btn_width = 180
        register_btn_y = 680
        back_btn_y = 681
        dark_bg = (20, 20, 20)
        hover_bg = (70, 130, 180)

        register_btn = TextButton(
            SCREEN_WIDTH // 2 - btn_width - 10, register_btn_y,
            btn_width, 50, "Register", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        back_btn = TextButton(
            SCREEN_WIDTH // 2 + 10, back_btn_y,
            btn_width, 50, "Back to Login", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        
        if register_btn.draw(self.screen):
            self.game_state.register_error_message = ""
            self.game_state.register_success_message = ""
            if len(self.game_state.register_username) < 3:
                self.game_state.register_error_message = "Username too short"
            elif len(self.game_state.register_password) < 6:
                self.game_state.register_error_message = "Password too short"
            else:
                success, message = self.api_client.register(
                    self.game_state.register_username,
                    self.game_state.register_email,
                    self.game_state.register_password
                )
                if success:
                    self.game_state.current_screen = ScreenState.LOGIN
                    self.game_state.current_input_field = "login_username"
                    self.game_state.login_username = self.game_state.register_username
                    self.game_state.register_username = ""
                    self.game_state.register_email = ""
                    self.game_state.register_password = ""
                    self.game_state.register_success_message = "Registration successful! Please login."
                else:
                    self.game_state.register_error_message = message
        
        # Draw error/success messages if present
        if self.game_state.register_error_message:
            draw_text(
                self.screen,
                self.game_state.register_error_message,
                SMALL_FONT,
                RED,
                center_x,
                740,
            )
        elif self.game_state.register_success_message:
            draw_text(
                self.screen,
                self.game_state.register_success_message,
                SMALL_FONT,
                GREEN,
                center_x,
                740,
            )
        
        if back_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.LOGIN
            self.game_state.current_input_field = "login_username"
            self.game_state.clear_messages()
    
    def draw_home_screen(self):
        """Draw home screen with Play button."""
        # Background
        self.screen.blit(self.home_bg, (0, 0))
        # Title with a subtle shadow for readability
        draw_text(self.screen, "FLAPPY BIRD", LARGE_FONT, BLACK, SCREEN_WIDTH // 2 - 202, 102)
        draw_text(self.screen, "FLAPPY BIRD", LARGE_FONT, WHITE, SCREEN_WIDTH // 2 - 200, 100)
        
        if self.api_client.user_info:
            welcome_text = f"Welcome, {self.api_client.user_info.get('username', 'Player')}!"
            draw_text(self.screen, welcome_text, SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 150, 200)
            
            if self.api_client.user_info.get('highest_score', 0) > 0:
                high_score_text = f"High Score: {self.api_client.user_info.get('highest_score', 0)}"
                draw_text(self.screen, high_score_text, SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 100, 250)
        
        # Buttons with colors chosen to stand out on the background
        dark_bg = (20, 20, 20)
        hover_bg = (70, 130, 180)  # steel blue

        # Play button
        play_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, 350, 200, 60,
            "PLAY", LARGE_FONT, WHITE, dark_bg, hover_bg
        )
        if play_btn.draw(self.screen):
            self.game_state.start_new_game()
            self.api_client.score_submitted = False
            self.api_client.last_submitted_score = 0
        
        # Leaderboard button
        leaderboard_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, 450, 200, 50,
            "Leaderboard", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        if leaderboard_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.LEADERBOARD
            self.api_client.get_leaderboard()
            if self.api_client.auth_token:
                self.api_client.get_user_rank()
        
        # Profile button
        profile_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, 520, 200, 50,
            "Profile", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        if profile_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.PROFILE
            self.api_client.get_profile()
            self.api_client.get_user_rank()
        
        # Logout button
        logout_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, 590, 200, 50,
            "Logout", SMALL_FONT, WHITE, dark_bg, hover_bg
        )
        if logout_btn.draw(self.screen):
            self.api_client.logout()
            self.game_state.current_screen = ScreenState.LOGIN
            self.game_state.game_started = False
    
    def draw_leaderboard_screen(self):
        """Draw leaderboard screen."""
        self.screen.blit(self.profile_bg, (0, 0))
        # Title with shadow for contrast
        draw_text(self.screen, "LEADERBOARD", LARGE_FONT, BLACK, SCREEN_WIDTH // 2 - 202, 22)
        draw_text(self.screen, "LEADERBOARD", LARGE_FONT, WHITE, SCREEN_WIDTH // 2 - 200, 20)
        
        if self.api_client.leaderboard_data:
            y_offset = 100
            for i, entry in enumerate(self.api_client.leaderboard_data[:10]):
                rank_text = f"#{entry.get('rank', i+1)}"
                username_text = entry.get('username', 'Unknown')
                score_text = str(entry.get('highest_score', 0))
                
                draw_text(self.screen, rank_text, SMALL_FONT, WHITE, 50, y_offset)
                draw_text(self.screen, username_text, SMALL_FONT, WHITE, 220, y_offset)
                draw_text(self.screen, score_text, SMALL_FONT, WHITE, 600, y_offset)
                y_offset += 50
        else:
            draw_text(self.screen, "No data available", SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 100, 200)
        
        back_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50,
            "Back (ESC)", SMALL_FONT, WHITE, (20, 20, 20), (70, 130, 180)
        )
        if back_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.HOME
        
        # Show user rank if logged in
        if self.api_client.auth_token and self.api_client.user_rank:
            rank_info = f"Your Rank: #{self.api_client.user_rank.get('rank', 'N/A')} | High Score: {self.api_client.user_rank.get('highest_score', 0)}"
            draw_text(self.screen, rank_info, TINY_FONT, BLUE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150)
    
    def draw_profile_screen(self):
        """Draw profile screen."""
        self.screen.blit(self.profile_bg, (0, 0))
        # Title with shadow for contrast
        draw_text(self.screen, "PROFILE", LARGE_FONT, BLACK, SCREEN_WIDTH // 2 - 102, 52)
        draw_text(self.screen, "PROFILE", LARGE_FONT, WHITE, SCREEN_WIDTH // 2 - 100, 50)
        
        if self.api_client.user_info:
            draw_text(self.screen, f"Username: {self.api_client.user_info.get('username', 'N/A')}", SMALL_FONT, WHITE, 200, 150)
            draw_text(self.screen, f"Email: {self.api_client.user_info.get('email', 'N/A')}", SMALL_FONT, WHITE, 200, 200)
            draw_text(self.screen, f"High Score: {self.api_client.user_info.get('highest_score', 0)}", SMALL_FONT, WHITE, 200, 250)
            draw_text(self.screen, f"Games Played: {self.api_client.user_info.get('games_played', 0)}", SMALL_FONT, WHITE, 200, 300)
        
        if self.api_client.user_rank:
            draw_text(self.screen, f"Rank: #{self.api_client.user_rank.get('rank', 'N/A')}", SMALL_FONT, WHITE, 200, 350)
        
        back_btn = TextButton(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50,
            "Back (ESC)", SMALL_FONT, WHITE, (20, 20, 20), (70, 130, 180)
        )
        if back_btn.draw(self.screen):
            self.game_state.current_screen = ScreenState.HOME
    
    def draw_heart_puzzle_screen(self, heart_puzzle):
        """Draw heart puzzle lifeline screen."""
        # Background image for heart puzzle
        self.screen.blit(self.heart_bg, (0, 0))
        # Title with shadow for contrast
        draw_text(self.screen, "LIFELINE!", LARGE_FONT, BLACK, SCREEN_WIDTH // 2 - 122, 22)
        draw_text(self.screen, "LIFELINE!", LARGE_FONT, WHITE, SCREEN_WIDTH // 2 - 120, 20)
        draw_text(self.screen, "Count the hearts to continue", SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 180, 80)
        
        if heart_puzzle.image:
            self.screen.blit(heart_puzzle.image, (SCREEN_WIDTH // 2 - 200, 120))
        
        remaining = heart_puzzle.get_remaining_time()
        draw_text(self.screen, f"Time Left: {remaining}", SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 80, 560)
        
        # Input box with semi-transparent dark background for better readability
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, 620, 160, 50)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), input_rect)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        draw_text(self.screen, heart_puzzle.input, SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 60, 630)
    
    def draw_countdown_screen(self, bg_img, ground_img, ground_scroll, bird_group, score, remaining_time, flying, game_over, countdown_active):
        """Draw countdown screen after successful lifeline."""
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(ground_img, (ground_scroll, GROUND_HEIGHT))
        bird_group.update(flying, game_over, countdown_active)
        bird_group.draw(self.screen)
        
        draw_text(self.screen, str(score), FONT, WHITE, SCREEN_WIDTH // 2, 20)
        
        if remaining_time > 0:
            draw_text(self.screen, "LIFELINE SUCCESSFUL!", SMALL_FONT, GREEN, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150)
            draw_text(self.screen, f"Continue in {remaining_time}", FONT, WHITE, SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 100)
    
    def draw_game_over_screen(self, bg_img, ground_img, ground_scroll, bird_group, score, remaining_time):
        """Draw game over screen."""
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(ground_img, (ground_scroll, GROUND_HEIGHT))
        bird_group.draw(self.screen)
        
        draw_text(self.screen, "GAME OVER", LARGE_FONT, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
        draw_text(self.screen, f"Final Score: {score}", SMALL_FONT, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20)
        
        if self.api_client.auth_token:
            if self.api_client.score_submitted and score == self.api_client.last_submitted_score:
                draw_text(self.screen, "Score submitted!", TINY_FONT, GREEN, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 40)
        
        if remaining_time > 0:
            draw_text(self.screen, f"Returning to home in {remaining_time}...", TINY_FONT, GRAY, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 80)

