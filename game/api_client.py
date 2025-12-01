"""API client for backend communication and heart puzzle API."""
import requests
import io
import pygame


class APIClient:
    """Handles all API communication with the backend."""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.auth_token = None
        self.user_info = None
        self.leaderboard_data = None
        self.user_rank = None
        self.score_submitted = False
        self.last_submitted_score = 0
    
    def register(self, username, email, password):
        """Register a new user."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "email": email, "password": password},
                timeout=5
            )
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get("token")
                self.user_info = data.get("user")
                return True, "Registration successful!"
            else:
                try:
                    error_msg = response.json().get("error", "Registration failed")
                except:
                    error_msg = f"Registration failed (Status: {response.status_code})"
                return False, error_msg
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def login(self, username, password):
        """Login user."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                self.user_info = data.get("user")
                return True, "Login successful!"
            else:
                try:
                    error_msg = response.json().get("error", "Login failed")
                except:
                    error_msg = f"Login failed (Status: {response.status_code})"
                return False, error_msg
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def submit_score(self, score_value, level=1):
        """Submit score to backend."""
        if not self.auth_token:
            return False, "Not logged in"
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.post(
                f"{self.base_url}/scores/submit",
                json={"score": score_value, "level": level},
                headers=headers,
                timeout=5
            )
            if response.status_code == 201:
                self.score_submitted = True
                self.last_submitted_score = score_value
                return True, "Score submitted!"
            else:
                try:
                    error_msg = response.json().get("error", "Failed to submit score")
                except:
                    error_msg = f"Failed to submit score (Status: {response.status_code})"
                return False, error_msg
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_leaderboard(self, limit=10):
        """Get leaderboard."""
        try:
            response = requests.get(
                f"{self.base_url}/scores/leaderboard?limit={limit}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.leaderboard_data = data.get("leaderboard", [])
                return True
            return False
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            return False
    
    def get_user_rank(self):
        """Get current user's rank."""
        if not self.auth_token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(
                f"{self.base_url}/scores/my-rank",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.user_rank = data
                return True
            return False
        except Exception as e:
            print(f"Error fetching rank: {e}")
            return False
    
    def get_profile(self):
        """Get current user profile."""
        if not self.auth_token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(
                f"{self.base_url}/auth/me",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.user_info = data.get("user")
                return True
            return False
        except Exception as e:
            print(f"Error fetching profile: {e}")
            return False
    
    def logout(self):
        """Logout current user."""
        self.auth_token = None
        self.user_info = None
        self.user_rank = None
        self.score_submitted = False
        self.last_submitted_score = 0


class HeartPuzzleAPI:
    """Handles heart puzzle API communication."""
    
    def __init__(self, api_url, time_limit):
        self.api_url = api_url
        self.time_limit = time_limit
    
    def fetch_puzzle(self):
        """Fetch a new heart puzzle from the API."""
        try:
            resp = requests.get(self.api_url, timeout=8).json()
            answer = str(resp["solution"])
            img_url = resp["question"]
            img_data = requests.get(img_url, timeout=8).content
            
            heart_image = pygame.image.load(io.BytesIO(img_data))
            heart_image = pygame.transform.scale(heart_image, (400, 400))
            
            return True, heart_image, answer
        except Exception as e:
            print(f"Error loading heart puzzle: {e}")
            return False, None, None

