const ScoreRepository = require('../repositories/scoreRepository');
const logger = require('../utils/logger');

/**
 * Rank Service - Business logic for ranking calculations
 */
class RankService {
  /**
   * Calculate user's rank based on their highest score
   * Rank = number of users with higher max scores + 1
   */
  static async calculateUserRank(userId) {
    try {
      // Get user's highest score
      const userHighestScore = await ScoreRepository.getHighestScore(userId);

      if (userHighestScore === 0) {
        return null; // No scores yet
      }

      // Count users with higher max scores
      const count = await ScoreRepository.countUsersWithHigherScore(userHighestScore);
      return count + 1;
    } catch (error) {
      logger.error('Error calculating user rank:', error);
      throw error;
    }
  }

  /**
   * Calculate rank based on a specific score value
   * Used when submitting a new score
   */
  static async calculateRankByScore(score) {
    try {
      const count = await ScoreRepository.countUsersWithHigherScore(score);
      return count + 1;
    } catch (error) {
      logger.error('Error calculating rank by score:', error);
      throw error;
    }
  }

  /**
   * Get user rank using a simpler method (for my-rank endpoint)
   */
  static async getUserRankSimple(userId) {
    try {
      const userHighestScore = await ScoreRepository.getHighestScore(userId);

      if (userHighestScore === 0) {
        return null;
      }

      // Count distinct users with higher scores
      const count = await ScoreRepository.countUsersWithScoreHigherThan(userHighestScore);
      return count + 1;
    } catch (error) {
      logger.error('Error getting user rank (simple):', error);
      throw error;
    }
  }
}

module.exports = RankService;

