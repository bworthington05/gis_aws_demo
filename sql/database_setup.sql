/* This table will hold parcel records that have been retrieved
from multiple sources and normalized. */
CREATE TABLE IF NOT EXISTS parcels (
  id BIGINT(21) AUTO_INCREMENT PRIMARY KEY,
  dataset VARCHAR(255) NOT NULL,
  as_of DATETIME NOT NULL,
  apn VARCHAR(255) NULL,
  objectid VARCHAR(255) NULL,
  city VARCHAR(255) NULL,
  x_coordinate DECIMAL(30,15) NULL,
  y_coordinate DECIMAL(30,15) NULL,
  area DECIMAL(30,15) NULL,
  length DECIMAL(30,15) NULL
);

ALTER TABLE parcels ADD INDEX dataset_idx (dataset);
ALTER TABLE parcels ADD INDEX as_of_idx (as_of);
ALTER TABLE parcels ADD INDEX apn_idx (apn);
ALTER TABLE parcels ADD INDEX city_idx (city);

/* This table will hold the most recent parcel records for each dataset.
It will be truncated and refreshed on a regular basis. */
CREATE TABLE IF NOT EXISTS latest_parcels (
  id BIGINT(21) PRIMARY KEY,
  dataset VARCHAR(255) NOT NULL,
  as_of DATETIME NOT NULL,
  apn VARCHAR(255) NULL,
  objectid VARCHAR(255) NULL,
  city VARCHAR(255) NULL,
  x_coordinate DECIMAL(30,15) NULL,
  y_coordinate DECIMAL(30,15) NULL,
  area DECIMAL(30,15) NULL,
  length DECIMAL(30,15) NULL
);

ALTER TABLE latest_parcels ADD INDEX dataset_idx (dataset);
ALTER TABLE latest_parcels ADD INDEX as_of_idx (as_of);
ALTER TABLE latest_parcels ADD INDEX apn_idx (apn);
ALTER TABLE latest_parcels ADD INDEX city_idx (city);
