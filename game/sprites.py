"""Sprite classes for the Flappy Bird game."""
import pygame
from .config import IMAGE_PATHS, SCROLL_SPEED, PIPE_GAP, SCREEN_HEIGHT, WHITE


class Bird(pygame.sprite.Sprite):
    """Bird sprite with animation and physics."""
    
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(IMAGE_PATHS['bird'].format(i)) for i in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False
    
    def update(self, flying, game_over, countdown_active):
        """Update bird position and animation."""
        if flying and not countdown_active:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += self.vel
        
        if not game_over and flying:
            keys = pygame.key.get_pressed()
            space_pressed = keys[pygame.K_SPACE]
            
            if space_pressed and not self.clicked:
                self.clicked = True
                self.vel = -10  # Flap!
            
            if not space_pressed:
                self.clicked = False
            
            # Animation
            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        elif game_over:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    """Pipe obstacle sprite."""
    
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load(IMAGE_PATHS['pipe'])
        self.rect = self.image.get_rect()
        
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, y + PIPE_GAP // 2)
    
    def update(self):
        """Update pipe position."""
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


class Button:
    """Image-based button."""
    
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        """Draw button and return True if clicked."""
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        
        screen.blit(self.image, self.rect)
        return action


class TextButton:
    """Text-based button with hover effect."""
    
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.clicked = False
    
    def draw(self, screen):
        """Draw button and return True if clicked."""
        pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(pos) else self.bg_color
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        action = False
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        return action

