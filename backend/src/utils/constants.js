/**
 * Application constants
 */

module.exports = {
  // JWT
  JWT_DEFAULT_EXPIRES_IN: '7d',

  // Pagination
  DEFAULT_LIMIT: 10,
  DEFAULT_OFFSET: 0,
  MAX_LIMIT: 100,

  // Validation
  USERNAME_MIN_LENGTH: 3,
  USERNAME_MAX_LENGTH: 50,
  PASSWORD_MIN_LENGTH: 6,
  EMAIL_MAX_LENGTH: 100,

  // HTTP Status Messages
  MESSAGES: {
    USER_CREATED: 'User created successfully',
    LOGIN_SUCCESS: 'Login successful',
    SCORE_SUBMITTED: 'Score submitted successfully',
    INVALID_CREDENTIALS: 'Invalid credentials',
    USER_EXISTS: 'Username or email already exists',
    TOKEN_REQUIRED: 'Access token required',
    INVALID_TOKEN: 'Invalid token',
    TOKEN_EXPIRED: 'Token expired',
    USER_NOT_FOUND: 'User not found',
    NO_SCORES: 'No scores submitted yet',
    INTERNAL_ERROR: 'Internal server error',
  },
};

