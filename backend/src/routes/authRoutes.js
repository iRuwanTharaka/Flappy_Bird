const express = require('express');
const { body } = require('express-validator');
const AuthController = require('../controllers/authController');
const { authenticateToken } = require('../middlewares/auth');
const { validate } = require('../middlewares/validation');
const constants = require('../utils/constants');

const router = express.Router();

// Get available auth endpoints
router.get('/', AuthController.getInfo);

// Register endpoint info (GET request)
router.get('/register', AuthController.getRegisterInfo);

// Register new user
router.post(
  '/register',
  [
    body('username')
      .trim()
      .isLength({ min: constants.USERNAME_MIN_LENGTH, max: constants.USERNAME_MAX_LENGTH })
      .withMessage(`Username must be ${constants.USERNAME_MIN_LENGTH}-${constants.USERNAME_MAX_LENGTH} characters`),
    body('email').isEmail().withMessage('Valid email required'),
    body('password')
      .isLength({ min: constants.PASSWORD_MIN_LENGTH })
      .withMessage(`Password must be at least ${constants.PASSWORD_MIN_LENGTH} characters`),
  ],
  validate,
  AuthController.register
);

// Login endpoint info (GET request)
router.get('/login', AuthController.getLoginInfo);

// Login user
router.post(
  '/login',
  [
    body('username').notEmpty().withMessage('Username required'),
    body('password').notEmpty().withMessage('Password required'),
  ],
  validate,
  AuthController.login
);

// Get current user profile (requires authentication)
router.get('/me', authenticateToken, AuthController.getProfile);

module.exports = router;

