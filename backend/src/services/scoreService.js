const ScoreRepository = require('../repositories/scoreRepository');
const RankService = require('./rankService');
const constants = require('../utils/constants');
const logger = require('../utils/logger');

/**
 * Score Service - Business logic for scores
 */
class ScoreService {
  /**
   * Submit a new score
   */
  static async submitScore(userId, scoreData) {
    const { score, level = 1 } = scoreData;

    // Create score
    const newScore = await ScoreRepository.create({
      userId,
      score,
      level,
    });

    // Get user's highest score
    const highestScore = await ScoreRepository.getHighestScore(userId);

    // Calculate rank
    const rank = await RankService.calculateRankByScore(highestScore);

    logger.info(`Score submitted: User ${userId}, Score: ${score}, Rank: ${rank}`);

    return {
      score: newScore,
      stats: {
        highest_score: highestScore,
        rank,
      },
    };
  }

  /**
   * Get leaderboard
   */
  static async getLeaderboard(limit = constants.DEFAULT_LIMIT, offset = constants.DEFAULT_OFFSET) {
    // Validate and clamp limit
    const validLimit = Math.min(Math.max(parseInt(limit) || constants.DEFAULT_LIMIT, 1), constants.MAX_LIMIT);
    const validOffset = Math.max(parseInt(offset) || constants.DEFAULT_OFFSET, 0);

    const leaderboard = await ScoreRepository.getLeaderboard(validLimit, validOffset);
    const total = await ScoreRepository.getLeaderboardCount();

    return {
      leaderboard,
      pagination: {
        limit: validLimit,
        offset: validOffset,
        total,
      },
    };
  }

  /**
   * Get user's scores
   */
  static async getUserScores(userId, limit = constants.DEFAULT_LIMIT, offset = constants.DEFAULT_OFFSET) {
    const validLimit = Math.min(Math.max(parseInt(limit) || constants.DEFAULT_LIMIT, 1), constants.MAX_LIMIT);
    const validOffset = Math.max(parseInt(offset) || constants.DEFAULT_OFFSET, 0);

    const scores = await ScoreRepository.getUserScores(userId, validLimit, validOffset);
    const rank = await RankService.calculateUserRank(userId);

    return {
      scores,
      rank: rank || 1,
      pagination: {
        limit: validLimit,
        offset: validOffset,
      },
    };
  }

  /**
   * Get user's rank
   */
  static async getUserRank(userId) {
    const highestScore = await ScoreRepository.getHighestScore(userId);

    if (highestScore === 0) {
      return {
        rank: null,
        highest_score: 0,
        message: constants.MESSAGES.NO_SCORES,
      };
    }

    const rank = await RankService.getUserRankSimple(userId);

    return {
      rank,
      highest_score: highestScore,
    };
  }
}

module.exports = ScoreService;

