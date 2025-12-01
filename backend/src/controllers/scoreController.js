const ScoreService = require('../services/scoreService');
const constants = require('../utils/constants');

/**
 * Score Controller - Handles HTTP requests/responses for scores
 */
class ScoreController {
  /**
   * Get API info
   */
  static getInfo(req, res) {
    res.json({
      message: 'Scores API',
      endpoints: {
        'POST /api/scores/submit': 'Submit a score (requires authentication)',
        'GET /api/scores/leaderboard': 'Get leaderboard (public)',
        'GET /api/scores/my-scores': 'Get user scores (requires authentication)',
        'GET /api/scores/my-rank': 'Get user rank (requires authentication)',
      },
      example: {
        submit: {
          method: 'POST',
          url: '/api/scores/submit',
          headers: {
            Authorization: 'Bearer YOUR_JWT_TOKEN',
          },
          body: {
            score: 150,
            level: 1,
          },
        },
        leaderboard: {
          method: 'GET',
          url: '/api/scores/leaderboard?limit=10&offset=0',
        },
      },
    });
  }

  /**
   * Submit a new score
   */
  static async submitScore(req, res, next) {
    try {
      const result = await ScoreService.submitScore(req.user.id, req.body);
      res.status(201).json({
        message: constants.MESSAGES.SCORE_SUBMITTED,
        ...result,
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get leaderboard
   */
  static async getLeaderboard(req, res, next) {
    try {
      const { limit, offset } = req.query;
      const result = await ScoreService.getLeaderboard(limit, offset);
      res.json(result);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get user's scores
   */
  static async getUserScores(req, res, next) {
    try {
      const { limit, offset } = req.query;
      const result = await ScoreService.getUserScores(req.user.id, limit, offset);
      res.json(result);
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get user's rank
   */
  static async getUserRank(req, res, next) {
    try {
      const result = await ScoreService.getUserRank(req.user.id);
      res.json({
        ...result,
        username: req.user.username,
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = ScoreController;

