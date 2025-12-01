const pool = require("../config/database");
const logger = require("../utils/logger");

/**
 * Score Repository - Data Access Layer for Score operations
 * Handles all database queries related to scores
 */
class ScoreRepository {
  /**
   * Create a new score
   */
  static async create(scoreData) {
    try {
      const { userId, score, level = 1 } = scoreData;
      const result = await pool.query(
        "INSERT INTO scores (user_id, score, level) VALUES ($1, $2, $3) RETURNING id, score, level, created_at",
        [userId, score, level]
      );
      return result.rows[0];
    } catch (error) {
      logger.error("Error creating score:", error);
      throw error;
    }
  }

  /**
   * Get user's highest score
   */
  static async getHighestScore(userId) {
    try {
      const result = await pool.query(
        "SELECT MAX(score) as highest_score FROM scores WHERE user_id = $1",
        [userId]
      );
      return parseInt(result.rows[0]?.highest_score) || 0;
    } catch (error) {
      logger.error("Error getting highest score:", error);
      throw error;
    }
  }

  /**
   * Get user's scores with pagination
   */
  static async getUserScores(userId, limit = 10, offset = 0) {
    try {
      const result = await pool.query(
        `SELECT 
          id,
          score,
          level,
          created_at
        FROM scores
        WHERE user_id = $1
        ORDER BY score DESC, created_at DESC
        LIMIT $2 OFFSET $3`,
        [userId, limit, offset]
      );
      return result.rows;
    } catch (error) {
      logger.error("Error getting user scores:", error);
      throw error;
    }
  }

  /**
   * Get leaderboard with pagination
   */
  static async getLeaderboard(limit = 10, offset = 0) {
    try {
      const result = await pool.query(
        `SELECT 
          u.id,
          u.username,
          MAX(s.score) as highest_score,
          COUNT(s.id) as games_played,
          MAX(s.created_at) as last_played,
          ROW_NUMBER() OVER (ORDER BY MAX(s.score) DESC NULLS LAST, MAX(s.created_at) DESC) as rank
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        GROUP BY u.id, u.username
        ORDER BY highest_score DESC NULLS LAST, last_played DESC
        LIMIT $1 OFFSET $2`,
        [limit, offset]
      );

      return result.rows.map((row) => ({
        rank: parseInt(row.rank),
        user_id: row.id,
        username: row.username,
        highest_score: parseInt(row.highest_score) || 0,
        games_played: parseInt(row.games_played) || 0,
        last_played: row.last_played,
      }));
    } catch (error) {
      logger.error("Error getting leaderboard:", error);
      throw error;
    }
  }

  /**
   * Get total count of users with scores (for pagination)
   */
  static async getLeaderboardCount() {
    try {
      const result = await pool.query(
        "SELECT COUNT(DISTINCT u.id) as total FROM users u LEFT JOIN scores s ON u.id = s.user_id WHERE s.score IS NOT NULL"
      );
      return parseInt(result.rows[0].total) || 0;
    } catch (error) {
      logger.error("Error getting leaderboard count:", error);
      throw error;
    }
  }

  /**
   * Count users with higher max scores than given score
   * Used for rank calculation
   */
  static async countUsersWithHigherScore(score) {
    try {
      const result = await pool.query(
        `SELECT COUNT(DISTINCT user_id) as count
         FROM (
           SELECT user_id, MAX(score) as max_score
           FROM scores
           GROUP BY user_id
           HAVING MAX(score) > $1
         ) as better_users`,
        [score]
      );
      return parseInt(result.rows[0].count) || 0;
    } catch (error) {
      logger.error("Error counting users with higher score:", error);
      throw error;
    }
  }

  /**
   * Count distinct users with scores higher than given score
   * Used for simpler rank calculation
   */
  static async countUsersWithScoreHigherThan(score) {
    try {
      const result = await pool.query(
        `SELECT COUNT(DISTINCT user_id) as count
         FROM scores
         WHERE score > $1`,
        [score]
      );
      return parseInt(result.rows[0].count) || 0;
    } catch (error) {
      logger.error("Error counting users with score higher than:", error);
      throw error;
    }
  }
}

module.exports = ScoreRepository;
