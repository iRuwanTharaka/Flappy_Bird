const AuthService = require("../services/authService");
const constants = require("../utils/constants");

/**
 * Auth Controller - Handles HTTP requests/responses for authentication
 */
class AuthController {
  /**
   * Get API info
   */
  static getInfo(req, res) {
    res.json({
      message: "Authentication API",
      endpoints: {
        "POST /api/auth/register": "Register a new user",
        "POST /api/auth/login": "Login user",
        "GET /api/auth/me":
          "Get current user profile (requires authentication)",
      },
      example: {
        register: {
          method: "POST",
          url: "/api/auth/register",
          body: {
            username: "player1",
            email: "player1@example.com",
            password: "password123",
          },
        },
        login: {
          method: "POST",
          url: "/api/auth/login",
          body: {
            username: "player1",
            password: "password123",
          },
        },
      },
    });
  }

  /**
   * Register endpoint info (GET request handler)
   */
  static getRegisterInfo(req, res) {
    res.status(405).json({
      error: "Method not allowed",
      message: "Use POST method to register a new user",
      method: "POST",
      url: "/api/auth/register",
      body: {
        username: "string (3-50 characters)",
        email: "string (valid email)",
        password: "string (minimum 6 characters)",
      },
      example: {
        username: "player1",
        email: "player1@example.com",
        password: "password123",
      },
    });
  }

  /**
   * Register a new user
   */
  static async register(req, res, next) {
    try {
      const result = await AuthService.register(req.body);
      res.status(201).json({
        message: constants.MESSAGES.USER_CREATED,
        ...result,
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Login endpoint info (GET request handler)
   */
  static getLoginInfo(req, res) {
    res.status(405).json({
      error: "Method not allowed",
      message: "Use POST method to login",
      method: "POST",
      url: "/api/auth/login",
      body: {
        username: "string (username or email)",
        password: "string",
      },
      example: {
        username: "player1",
        password: "password123",
      },
    });
  }

  /**
   * Login user
   */
  static async login(req, res, next) {
    try {
      const result = await AuthService.login(req.body);
      res.json({
        message: constants.MESSAGES.LOGIN_SUCCESS,
        ...result,
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get current user profile
   */
  static async getProfile(req, res, next) {
    try {
      const profile = await AuthService.getProfile(req.user.id);
      res.json({
        user: profile,
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = AuthController;
