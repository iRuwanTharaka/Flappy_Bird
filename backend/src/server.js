const express = require('express');
const cors = require('cors');
require('dotenv').config();

const authRoutes = require('./routes/authRoutes');
const scoreRoutes = require('./routes/scoreRoutes');
const requestLogger = require('./middlewares/requestLogger');
const errorHandler = require('./middlewares/errorHandler');
const logger = require('./utils/logger');

// Validate required environment variables
if (!process.env.JWT_SECRET) {
  logger.error('❌ JWT_SECRET is not set in environment variables!');
  logger.error('Please set JWT_SECRET in your .env file');
  process.exit(1);
}

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true,
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use(requestLogger);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'Flappy Bird API is running' });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/scores', scoreRoutes);

// 404 handler (more informative)
app.use((req, res) => {
  const path = req.originalUrl;
  let suggestion = '';

  // Provide helpful suggestions based on the path
  if (path.includes('/api/auth/register')) {
    suggestion = 'Use POST method instead of GET. POST /api/auth/register with body: {username, email, password}';
  } else if (path.includes('/api/auth/login')) {
    suggestion = 'Use POST method instead of GET. POST /api/auth/login with body: {username, password}';
  } else if (path.includes('/api/auth')) {
    suggestion = 'Available endpoints: GET /api/auth (info), POST /api/auth/register, POST /api/auth/login, GET /api/auth/me';
  } else if (path.includes('/api/scores')) {
    suggestion = 'Available endpoints: GET /api/scores (info), POST /api/scores/submit, GET /api/scores/leaderboard';
  }

  res.status(404).json({
    error: 'Route not found',
    method: req.method,
    path: req.originalUrl,
    suggestion: suggestion || 'Check the API documentation or try GET /api/auth or GET /api/scores for available endpoints',
  });
});

// Error handler (must be last)
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  logger.info(`🚀 Server running on http://localhost:${PORT}`);
  logger.info(`📊 Health check: http://localhost:${PORT}/health`);
  logger.info(`🔐 Auth endpoints: http://localhost:${PORT}/api/auth`);
  logger.info(`🏆 Score endpoints: http://localhost:${PORT}/api/scores`);
});

module.exports = app;

