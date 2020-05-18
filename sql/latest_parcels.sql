/* Get the most recently retrieved parcels per dataset. */
SELECT
  p.id,
  p.dataset,
  p.as_of,
  p.apn,
  p.objectid,
  p.city,
  p.x_coordinate,
  p.y_coordinate,
  p.area,
  p.length
FROM parcels AS p
  INNER JOIN (
    SELECT
      dataset,
      apn,
      MAX(as_of) AS as_of
    FROM parcels
    GROUP BY dataset, apn
  ) AS p_max ON p.dataset = p_max.dataset
      AND p.apn = p_max.apn
      AND p.as_of = p_max.as_of
ORDER BY p.id
