// Quick database connection test script
require('dotenv').config();
const { Pool } = require('pg');

console.log('Testing database connection...');
console.log('Host:', process.env.DB_HOST || 'localhost');
console.log('Port:', process.env.DB_PORT || 5432);
console.log('Database:', process.env.DB_NAME || 'flappy_bird_db');
console.log('User:', process.env.DB_USER || 'postgres');
console.log('Password:', process.env.DB_PASSWORD ? '***' : 'NOT SET');

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'flappy_bird_db',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
});

pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('\n❌ Connection failed!');
    console.error('Error:', err.message);
    console.error('\nTroubleshooting:');
    console.error('1. Check if PostgreSQL is running');
    console.error('2. Verify your password in .env file');
    console.error('3. Make sure database "flappy_bird_db" exists');
    console.error('4. Check DB_HOST, DB_PORT, DB_USER in .env');
  } else {
    console.log('\n✅ Connection successful!');
    console.log('Current time:', res.rows[0].now);
    console.log('\nYou can now run: npm run migrate');
  }
  pool.end();
});

