-- ranks the bands ordered by the number of fans
SELECT origin, SUM(fans) As nb_fans
	FROM metal_bands
	GROUP BY origin
	ORDER BY nb_fans DESC;
