const express = require('express');
const { body } = require('express-validator');
const ScoreController = require('../controllers/scoreController');
const { authenticateToken } = require('../middlewares/auth');
const { validate } = require('../middlewares/validation');

const router = express.Router();

// Get available score endpoints
router.get('/', ScoreController.getInfo);

// Submit a new score (requires authentication)
router.post(
  '/submit',
  authenticateToken,
  [
    body('score').isInt({ min: 0 }).withMessage('Score must be a non-negative integer'),
    body('level').optional().isInt({ min: 1 }).withMessage('Level must be a positive integer'),
  ],
  validate,
  ScoreController.submitScore
);

// Get leaderboard (public)
router.get('/leaderboard', ScoreController.getLeaderboard);

// Get user's personal scores (requires authentication)
router.get('/my-scores', authenticateToken, ScoreController.getUserScores);

// Get user's rank (requires authentication)
router.get('/my-rank', authenticateToken, ScoreController.getUserRank);

module.exports = router;

