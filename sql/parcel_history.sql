/* Get all records for a particular parcel. */
SELECT
  id,
  dataset,
  CAST(as_of AS CHAR) AS as_of,
  apn,
  objectid,
  city,
  CAST(ROUND(x_coordinate, 4) AS CHAR) AS x_coordinate,
  CAST(ROUND(y_coordinate, 4) AS CHAR) AS y_coordinate,
  CAST(ROUND(area, 4) AS CHAR) AS area,
  CAST(ROUND(length, 4) AS CHAR) AS length
FROM parcels
WHERE dataset = %(dataset)s
  AND apn = %(apn)s
ORDER BY as_of DESC
