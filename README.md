# Flappy_Bird 🐦

## What is this

Flappy_Bird is a simple clone/implementation of the classic *Flappy Bird* game — written in Python (with some JavaScript parts). The game lets you control a “bird” and try to navigate through a series of obstacles (pipes) without crashing.  

This project is meant as a fun exercise / demo of basic game-programming concepts: rendering graphics, simple physics (gravity, collision detection), user input (flapping), and game loops.  

## Motivation

I built this project to practice my programming skills and get hands-on experience with game logic, user input handling, rendering, and general project structure. Since I’m studying Computer Science and enjoy learning new things, making a clone of a well-known game felt like a good way to challenge myself.  

## Features

- Basic Flappy Bird gameplay: a bird that “flaps” up on keypress and otherwise falls due to gravity.  
- Obstacle generation: pipes (or obstacles) appear and move toward the bird — the player must avoid them.  
- Simple collision detection (bird vs pipes or ground).  
- Score tracking (optionally — depending on your implementation).  
- Assets support (images, sprites) — the project includes an `img/` folder.  

## Requirements / Prerequisites

- Python 3.x (whatever version you used — specify here)  
- For dependencies listed in `requirements.txt`, you may need to install them via pip.  
- (Optionally) A graphical environment that supports Python rendering (if using a GUI library).  

## How to Install & Run

1. Clone the repository  
   ```bash
   git clone https://github.com/iRuwanTharaka/Flappy_Bird.git
   cd Flappy_Bird
   ```  
2. Create a virtual environment (recommended)  
   ```bash
   python3 -m venv venv  
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```  
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```  
4. Run the game  
   ```bash
   python flappy.py
   ```  

## How to Play

- Run `flappy.py` to start the game.  
- Press a key (e.g. spacebar or mouse/keyboard input — depending on your implementation) to make the bird “flap” (move upward).  
- Avoid hitting the pipes or the ground — try to get the highest score possible.  

## Project Structure (important files / folders)

```
Flappy_Bird/
├── flappy.py            # main game script  
├── requirements.txt     # Python dependencies  
├── img/                 # folder containing image assets (sprites, backgrounds, etc.)  
├── game/                # (if you have modularized code — for game logic, classes, etc.)  
├── backend/             # (if any backend logic or extra modules)  
└── README.md            # this file  
```  

You may have some extra files (e.g. temp files) — those are not essential.  

## Known Issues / To-Do (or Possible Improvements)

- Add more polished graphics / animations (e.g. flapping animation, smoother motion).  
- Add sound effects / background music to enhance the gameplay experience.  
- Add a start menu / game over screen / score display.  
- Add support for different screen resolutions or window resizing.  
- Improve collision detection or physics (for smoother experience).  
- Add high-score saving / persistent score records.  

## Credits & Acknowledgments

- Project created by **You (iRuwanTharaka)**.  
- If you used any tutorials, assets, or external resources (for images, sprites, sounds) — list them here (with links).  
- Inspired by the original *Flappy Bird* game.  

## License

Specify a license under which you are releasing this project (e.g. MIT, GPL, or whichever you choose).  

---  

Enjoy 🙂  
