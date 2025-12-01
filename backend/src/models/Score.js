/**
 * Score Model - Pure schema definition
 * Defines the structure of the Score entity
 */

const ScoreSchema = {
  tableName: "scores",
  fields: {
    id: {
      type: "SERIAL",
      primaryKey: true,
      allowNull: false,
    },
    user_id: {
      type: "INTEGER",
      allowNull: false,
      references: {
        model: "users",
        key: "id",
        onDelete: "CASCADE",
      },
    },
    score: {
      type: "INTEGER",
      allowNull: false,
    },
    level: {
      type: "INTEGER",
      defaultValue: 1,
    },
    created_at: {
      type: "TIMESTAMP",
      defaultValue: "CURRENT_TIMESTAMP",
    },
  },
};

module.exports = ScoreSchema;
