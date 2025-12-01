const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const UserRepository = require('../repositories/userRepository');
const AppError = require('../utils/AppError');
const constants = require('../utils/constants');
const logger = require('../utils/logger');

/**
 * Auth Service - Business logic for authentication
 */
class AuthService {
  /**
   * Register a new user
   */
  static async register(userData) {
    const { username, email, password } = userData;

    // Check if user already exists
    const userExists = await UserRepository.exists(username, email);
    if (userExists) {
      throw new AppError(constants.MESSAGES.USER_EXISTS, 400);
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);

    // Create user
    const user = await UserRepository.create({
      username,
      email,
      passwordHash,
    });

    // Generate JWT token
    const token = this.generateToken(user.id, user.username);

    logger.info(`User registered: ${username}`);

    return {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
      },
      token,
    };
  }

  /**
   * Login user
   */
  static async login(credentials) {
    const { username, password } = credentials;

    // Find user by username or email
    const user = await UserRepository.findByUsernameOrEmail(username);
    if (!user) {
      throw new AppError(constants.MESSAGES.INVALID_CREDENTIALS, 401);
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {
      throw new AppError(constants.MESSAGES.INVALID_CREDENTIALS, 401);
    }

    // Generate JWT token
    const token = this.generateToken(user.id, user.username);

    logger.info(`User logged in: ${username}`);

    return {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
      },
      token,
    };
  }

  /**
   * Get user profile with stats
   */
  static async getProfile(userId) {
    const profile = await UserRepository.getProfileWithStats(userId);
    if (!profile) {
      throw new AppError(constants.MESSAGES.USER_NOT_FOUND, 404);
    }
    return profile;
  }

  /**
   * Generate JWT token
   */
  static generateToken(userId, username) {
    return jwt.sign(
      { userId, username },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || constants.JWT_DEFAULT_EXPIRES_IN }
    );
  }
}

module.exports = AuthService;

