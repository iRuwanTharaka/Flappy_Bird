/**
 * User Model - Pure schema definition
 * Defines the structure of the User entity
 */

const UserSchema = {
  tableName: 'users',
  fields: {
    id: {
      type: 'SERIAL',
      primaryKey: true,
      allowNull: false,
    },
    username: {
      type: 'VARCHAR(50)',
      unique: true,
      allowNull: false,
    },
    email: {
      type: 'VARCHAR(100)',
      unique: true,
      allowNull: false,
    },
    password_hash: {
      type: 'VARCHAR(255)',
      allowNull: false,
    },
    created_at: {
      type: 'TIMESTAMP',
      defaultValue: 'CURRENT_TIMESTAMP',
    },
    updated_at: {
      type: 'TIMESTAMP',
      defaultValue: 'CURRENT_TIMESTAMP',
    },
  },
};

module.exports = UserSchema;
