const AppError = require('../utils/AppError');
const logger = require('../utils/logger');
const constants = require('../utils/constants');

/**
 * Global error handling middleware
 */
const errorHandler = (err, req, res, next) => {
  let error = { ...err };
  error.message = err.message;

  // Log error
  logger.error(`Error: ${err.message}`, {
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = 'Resource not found';
    error = new AppError(message, 404);
  }

  // Validation error
  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map((val) => val.message).join(', ');
    error = new AppError(message, 400);
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    error = new AppError(constants.MESSAGES.INVALID_TOKEN, 403);
  }

  if (err.name === 'TokenExpiredError') {
    error = new AppError(constants.MESSAGES.TOKEN_EXPIRED, 403);
  }

  // PostgreSQL errors
  if (err.code === '23505') {
    // Unique violation
    error = new AppError(constants.MESSAGES.USER_EXISTS, 400);
  }

  res.status(error.statusCode || 500).json({
    error: error.message || constants.MESSAGES.INTERNAL_ERROR,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};

module.exports = errorHandler;

