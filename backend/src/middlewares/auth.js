const jwt = require('jsonwebtoken');
const UserRepository = require('../repositories/userRepository');
const AppError = require('../utils/AppError');
const constants = require('../utils/constants');
const logger = require('../utils/logger');

/**
 * Authentication middleware - verifies JWT token
 */
const authenticateToken = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      throw new AppError(constants.MESSAGES.TOKEN_REQUIRED, 401);
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Verify user still exists
    const user = await UserRepository.findById(decoded.userId);

    if (!user) {
      throw new AppError(constants.MESSAGES.USER_NOT_FOUND, 401);
    }

    req.user = user;
    next();
  } catch (error) {
    // Let error handler middleware handle AppError and JWT errors
    next(error);
  }
};

module.exports = { authenticateToken };

