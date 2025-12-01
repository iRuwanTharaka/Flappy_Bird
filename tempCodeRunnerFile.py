except:
    print("Warning: Could not load game assets. Please ensure image files are present.")
    # Use fallback images or fill if actual assets fail
    background_image = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    background_image.fill((135, 206, 235)) # Sky Blue
    bird_image = pygame.Surface((bird_width, bird_height))
    bird_image.fill((255, 255, 0)) # Yellow
    top_pipe_image = pygame.Surface((pipe_width, pipe_height))
    top_pipe_image.fill((0, 255, 0)) # Green
    bottom_pipe_image = pygame.Surface((pipe_width, pipe_height))
    bottom_pipe_image.fill((0, 255, 0)) # Green