/* Get calculated stats about parcels grouped by city. */
SELECT
	city,
	CAST(COUNT(*) AS CHAR) AS count_of_parcels,
	CAST(ROUND(AVG(area), 4) AS CHAR) AS average_parcel_area,
	CAST(ROUND(MIN(area), 4) AS CHAR) AS minimum_parcel_area,
	CAST(ROUND(MAX(area), 4) AS CHAR) AS maximum_parcel_area
FROM latest_parcels
WHERE dataset = %(dataset)s
GROUP BY city
ORDER BY city
