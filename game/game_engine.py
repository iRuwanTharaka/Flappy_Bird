"""Core game engine logic."""
import pygame
import random
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_SPEED, PIPE_FREQUENCY,
    PIPE_GAP, GROUND_HEIGHT, FONT, WHITE
)
from .sprites import Bird, Pipe


class GameEngine:
    """Manages core game logic and mechanics."""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()
        self.bird = None
        self.last_pipe_time = pygame.time.get_ticks() - PIPE_FREQUENCY
        self._initialize_bird()
    
    def _initialize_bird(self):
        """Initialize the bird sprite."""
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
    
    def reset_game(self):
        """Reset game to initial state."""
        self.pipe_group.empty()
        if self.bird:
            self.bird.rect.x = 100
            self.bird.rect.y = SCREEN_HEIGHT // 2
        self.last_pipe_time = pygame.time.get_ticks() - PIPE_FREQUENCY
        self.game_state.pass_pipe = False
    
    def checkpoint_reset(self):
        """Reset pipes and bird position for continuing the game (score remains)."""
        self.pipe_group.empty()
        if self.bird:
            self.bird.rect.x = 100
            self.bird.rect.y = SCREEN_HEIGHT // 2
    
    def update(self):
        """Update game state."""
        if not self.bird:
            return
        
        # Update bird
        self.bird_group.update(
            self.game_state.flying,
            self.game_state.game_over,
            self.game_state.countdown_active
        )
        
        # Generate pipes
        if self.game_state.flying and not self.game_state.game_over:
            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe_time > PIPE_FREQUENCY:
                height = random.randint(-100, 100)
                self.pipe_group.add(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + height, -1))
                self.pipe_group.add(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + height, 1))
                self.last_pipe_time = time_now
            
            self.pipe_group.update()
            
            # Scroll ground
            self.game_state.ground_scroll -= SCROLL_SPEED
            if abs(self.game_state.ground_scroll) > 35:
                self.game_state.ground_scroll = 0
        
        # Score logic
        if len(self.pipe_group) > 0:
            pipe = self.pipe_group.sprites()[0]
            
            if (self.bird.rect.left > pipe.rect.left and 
                self.bird.rect.right < pipe.rect.right and 
                not self.game_state.pass_pipe):
                self.game_state.pass_pipe = True
            
            if self.game_state.pass_pipe and self.bird.rect.left > pipe.rect.right:
                self.game_state.score += 1
                self.game_state.pass_pipe = False
    
    def check_collisions(self):
        """Check for collisions and return True if collision detected."""
        if not self.bird:
            return False
        
        # Check pipe collisions or top boundary
        if (pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or 
            self.bird.rect.top < 0):
            return True
        
        # Check ground collision
        if self.bird.rect.bottom >= GROUND_HEIGHT:
            return True
        
        return False
    
    def draw(self, screen, bg_img, ground_img):
        """Draw game elements."""
        screen.blit(bg_img, (0, 0))
        self.pipe_group.draw(screen)
        self.bird_group.draw(screen)
        screen.blit(ground_img, (self.game_state.ground_scroll, GROUND_HEIGHT))
        
        # Draw score
        draw_text(screen, str(self.game_state.score), FONT, WHITE, SCREEN_WIDTH // 2, 20)


def draw_text(screen, text, font, col, x, y):
    """Helper function to draw text."""
    img = font.render(text, True, col)
    screen.blit(img, (x, y))

