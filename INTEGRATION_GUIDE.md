# Flappy Bird Backend Integration Guide

## Overview

The Flappy Bird game is now integrated with a Node.js backend API that provides:
- User authentication (JWT)
- Score submission and tracking
- Leaderboard with rankings
- User profiles

## Setup Instructions

### 1. Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   - Copy `env.example` to `.env`
   - Edit `.env` and set your PostgreSQL credentials:
     ```
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=flappy_bird_db
     DB_USER=postgres
     DB_PASSWORD=your_password
     JWT_SECRET=your_secret_key_here
     ```

4. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE flappy_bird_db;
   ```

5. **Run database migrations:**
   ```bash
   npm run migrate
   ```

6. **Start the backend server:**
   ```bash
   npm run dev
   ```
   The server will run on `http://localhost:3000`

### 2. Game Setup

1. **Install Python dependencies:**
   ```bash
   pip install pygame requests
   ```

2. **Configure API URL (if needed):**
   - Open `flappy.py`
   - Line 33: `API_BASE_URL = "http://localhost:3000/api"`
   - Change if your backend is on a different host/port

3. **Run the game:**
   ```bash
   python flappy.py
   ```

## How to Use

### Keyboard Shortcuts

- **L** - Login/Profile
  - If not logged in: Opens login screen
  - If logged in: Shows your profile with stats and rank

- **R** - Leaderboard
  - Shows top 10 players with their highest scores

- **ESC** - Close any open screen (login, register, leaderboard, profile)

- **SPACE** - Start game / Flap (during gameplay)

- **TAB** - Switch between input fields (in login/register screens)

### Authentication Flow

1. **Register a new account:**
   - Press **L** to open login screen
   - Click "Register" button
   - Fill in:
     - Username (min 3 characters)
     - Email (valid email format)
     - Password (min 6 characters)
   - Click "Register"

2. **Login:**
   - Press **L** to open login screen
   - Enter username/email and password
   - Click "Login"

3. **View Profile:**
   - Press **L** while logged in
   - See your stats:
     - Username and email
     - Highest score
     - Games played
     - Current rank

### Score Submission

- Scores are **automatically submitted** when the game ends (if you're logged in)
- You'll see "Score submitted!" message on game over screen
- If not logged in, you'll see a prompt to login

### Leaderboard

- Press **R** to view the leaderboard
- Shows top 10 players ranked by highest score
- Your rank is displayed at the bottom if you're logged in

## Features

### User Features
- ✅ User registration with email
- ✅ Secure login with JWT tokens
- ✅ Automatic score submission
- ✅ Personal statistics tracking
- ✅ Global leaderboard
- ✅ Real-time rank display

### Game Features
- ✅ All original game functionality preserved
- ✅ Heart puzzle checkpoint system
- ✅ Score tracking
- ✅ Game over handling

## Troubleshooting

### Backend Connection Issues

**Error: "Connection error"**
- Make sure the backend server is running (`npm run dev` in backend folder)
- Check that `API_BASE_URL` in `flappy.py` matches your backend URL
- Verify PostgreSQL is running and database exists

**Error: "Invalid credentials"**
- Double-check username/email and password
- Make sure you've registered first

### Database Issues

**Error: "relation does not exist"**
- Run migrations: `npm run migrate` in backend folder
- Or manually run `setup.sql` in PostgreSQL

**Error: "connection refused"**
- Check PostgreSQL is running
- Verify database credentials in `.env` file

### Game Issues

**Scores not submitting:**
- Make sure you're logged in (press L to check)
- Check backend server is running
- Verify network connection

**Leaderboard not loading:**
- Press R again to refresh
- Check backend server is running
- Verify database has score data

## API Endpoints Used

The game uses these backend endpoints:

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get user profile
- `POST /api/scores/submit` - Submit score
- `GET /api/scores/leaderboard` - Get leaderboard
- `GET /api/scores/my-rank` - Get user rank

## Development Notes

- JWT tokens are stored in memory (lost on game restart)
- Scores are submitted automatically on game over
- Leaderboard updates in real-time when you press R
- All API calls have 5-second timeout

## Next Steps

You can extend this integration by:
- Adding persistent token storage (local file)
- Implementing score history view
- Adding friend comparisons
- Creating achievements system
- Adding multiplayer features

