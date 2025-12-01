const pool = require('../config/database');
const logger = require('../utils/logger');

/**
 * User Repository - Data Access Layer for User operations
 * Handles all database queries related to users
 */
class UserRepository {
  /**
   * Find user by username or email
   */
  static async findByUsernameOrEmail(identifier) {
    try {
      const result = await pool.query(
        'SELECT id, username, email, password_hash FROM users WHERE username = $1 OR email = $1',
        [identifier]
      );
      return result.rows[0] || null;
    } catch (error) {
      logger.error('Error finding user by username/email:', error);
      throw error;
    }
  }

  /**
   * Find user by ID
   */
  static async findById(userId) {
    try {
      const result = await pool.query(
        'SELECT id, username, email FROM users WHERE id = $1',
        [userId]
      );
      return result.rows[0] || null;
    } catch (error) {
      logger.error('Error finding user by ID:', error);
      throw error;
    }
  }

  /**
   * Check if user exists by username or email
   */
  static async exists(username, email) {
    try {
      const result = await pool.query(
        'SELECT id FROM users WHERE username = $1 OR email = $2',
        [username, email]
      );
      return result.rows.length > 0;
    } catch (error) {
      logger.error('Error checking user existence:', error);
      throw error;
    }
  }

  /**
   * Create a new user
   */
  static async create(userData) {
    try {
      const { username, email, passwordHash } = userData;
      const result = await pool.query(
        'INSERT INTO users (username, email, password_hash) VALUES ($1, $2, $3) RETURNING id, username, email, created_at',
        [username, email, passwordHash]
      );
      return result.rows[0];
    } catch (error) {
      logger.error('Error creating user:', error);
      throw error;
    }
  }

  /**
   * Get user profile with stats
   */
  static async getProfileWithStats(userId) {
    try {
      const userResult = await pool.query(
        'SELECT id, username, email FROM users WHERE id = $1',
        [userId]
      );

      if (userResult.rows.length === 0) {
        return null;
      }

      const scoreResult = await pool.query(
        'SELECT MAX(score) as highest_score, COUNT(*) as games_played FROM scores WHERE user_id = $1',
        [userId]
      );

      const user = userResult.rows[0];
      const stats = scoreResult.rows[0];

      return {
        ...user,
        highest_score: parseInt(stats.highest_score) || 0,
        games_played: parseInt(stats.games_played) || 0,
      };
    } catch (error) {
      logger.error('Error getting user profile with stats:', error);
      throw error;
    }
  }
}

module.exports = UserRepository;

