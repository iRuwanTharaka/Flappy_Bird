# Flappy Bird Project Structure

## Directory Structure

```
flappy_bird-main/
├── flappy.py              # Main entry point
├── game/                  # Game package
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration constants
│   ├── api_client.py       # API communication (backend & heart puzzle)
│   ├── sprites.py          # Sprite classes (Bird, Pipe, Button, TextButton)
│   ├── game_state.py       # Game state management
│   ├── game_engine.py      # Core game logic
│   ├── heart_puzzle.py     # Heart puzzle lifeline logic
│   └── screens.py          # UI screen rendering
├── img/                   # Game assets (images)
│   ├── bg.png
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── ground.png
│   └── pipe.png
└── backend/               # Backend API (Node.js)
    ├── server.js
    ├── routes/
    ├── middleware/
    └── ...
```

## Module Responsibilities

### `game/config.py`
- **Purpose**: Centralized configuration
- **Contains**: Screen dimensions, fonts, colors, API URLs, game settings, image paths
- **Dependencies**: pygame (for font initialization)

### `game/api_client.py`
- **Purpose**: API communication layer
- **Classes**: 
  - `APIClient`: Backend API (auth, scores, leaderboard)
  - `HeartPuzzleAPI`: Heart puzzle API
- **Dependencies**: requests, pygame

### `game/sprites.py`
- **Purpose**: Sprite classes
- **Classes**: `Bird`, `Pipe`, `Button`, `TextButton`
- **Dependencies**: pygame, config

### `game/game_state.py`
- **Purpose**: State management
- **Classes**: `GameState`, `ScreenState` (enum)
- **Dependencies**: enum (standard library)

### `game/game_engine.py`
- **Purpose**: Core game mechanics
- **Classes**: `GameEngine`
- **Responsibilities**: Collision detection, scoring, pipe generation, bird/pipe updates
- **Dependencies**: pygame, config, sprites

### `game/heart_puzzle.py`
- **Purpose**: Heart puzzle lifeline
- **Classes**: `HeartPuzzle`
- **Dependencies**: pygame, config, api_client

### `game/screens.py`
- **Purpose**: UI rendering
- **Classes**: `ScreenRenderer`
- **Responsibilities**: All screen drawing functions (login, register, home, leaderboard, profile, game over, etc.)
- **Dependencies**: pygame, config, sprites, game_state

### `flappy.py`
- **Purpose**: Main orchestrator
- **Classes**: `FlappyBirdGame`
- **Responsibilities**: Event handling, main game loop, component coordination
- **Dependencies**: pygame, game package

## Design Principles

### High Cohesion
- Each module has a single, well-defined responsibility
- Related functionality is grouped together
- Modules are focused and cohesive

### Low Coupling
- Modules depend on abstractions (config, interfaces) rather than implementations
- Minimal dependencies between modules
- Clear separation of concerns
- No circular dependencies

### Benefits
- **Maintainability**: Easy to locate and modify specific functionality
- **Testability**: Modules can be tested independently
- **Scalability**: Easy to add new features without affecting existing code
- **Readability**: Clear structure makes code easier to understand

## Running the Game

```bash
python flappy.py
```

## Import Examples

```python
# Import from game package
from game import GameState, ScreenState, GameEngine
from game import APIClient, HeartPuzzleAPI
from game import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Or import specific modules
from game.config import SCREEN_WIDTH
from game.sprites import Bird, Pipe
```

