CREATE TABLE IF NOT EXISTS data (
  timestamp TIMESTAMP NOT NULL,
  wind_speed DOUBLE PRECISION,
  power DOUBLE PRECISION,
  ambient_temperature DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_data_timestamp ON data (timestamp);
