# Flappy Bird + Scoreboard

A Pygame-based Flappy Bird clone with login/registration, persistent scores, leaderboard, and a heart-puzzle lifeline. The Python game talks to a Node/Express + PostgreSQL backend for auth and score tracking.

## Project Overview
- Python game in `flappy.py` with modules in `game/` (rendering, state, API client).
- Node/Express API in `backend/` for authentication, score submission, leaderboard, and rank.
- PostgreSQL database (migrations provided) plus a small SQL dump in `db/flappy_bird_db.sql`.
- Assets live in `img/` (background, bird sprites, pipes, buttons).

## Requirements
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 13+ (any recent version works)
- Pygame-capable environment (desktop with a display; not headless)

## Quick Start (Game Only)
1) Install Python deps
```
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
2) Start the game (uses `http://localhost:3000/api` by default)
```
python flappy.py
```
If you only want to fly locally without backend features, the game still runs, but login/leaderboard calls will fail until the API is up.

## Backend Setup (Express + Postgres)
1) Install deps
```
cd backend
npm install
```
2) Create a `.env` in `backend/` (example):
```
PORT=3000
JWT_SECRET=change_me
CORS_ORIGIN=http://localhost:3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flappy_bird_db
DB_USER=postgres
DB_PASSWORD=your_password
```
3) Create the database and run migrations
```
createdb flappy_bird_db         # or use psql/GUI
npm run migrate                  # creates users, scores, leaderboard view
```
4) Start the API
```
npm run dev   # or: npm start
```
Health check: `GET http://localhost:3000/health`

## API Endpoints (used by the game)
- `POST /api/auth/register` `{username,email,password}` -> `{token,user}`
- `POST /api/auth/login` `{username,password}` -> `{token,user}`
- `GET /api/auth/me` (Bearer token) -> current user
- `POST /api/scores/submit` `{score, level}` (Bearer token)
- `GET /api/scores/leaderboard?limit=10`
- `GET /api/scores/my-rank` (Bearer token)

`game/config.py` points `API_BASE_URL` to `http://localhost:3000/api`. Update it if you host the API elsewhere.

## How to Play
- Launch: `python flappy.py`
- Controls: `Space` to flap when in-game; `ESC` to return to home or exit screens.
- Auth screens: type username/password/email; use `Tab` to switch fields; `Enter` to submit.
- Heart puzzle lifeline: on collision you may get a timed puzzle fetched from `https://marcconrad.com/uob/heart/api.php`. Enter the numeric answer; failing or timing out ends the run.
- Game over auto-returns to home after 3 seconds and submits score if logged in.

## Project Structure
```
flappy.py               # game entry point
game/                   # game logic, rendering, API client, state
backend/                # Express server (auth + scores)
db/flappy_bird_db.sql   # SQL dump (reference)
img/                    # sprites and UI assets
requirements.txt        # Python deps (pygame, requests)
```

## Development Tips
- Change screen size, speeds, or API URL in `game/config.py`.
- Logs for the API use a simple logger in `backend/src/utils/logger.js`.
- Run `npm run test-db` to quickly verify DB connectivity with current `.env`.

## License
Copyright (c) [2025] [iRuwanTharaka]

Copyright (c) [2025] [iRuwanTharaka]

