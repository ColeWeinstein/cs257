SELECT noc_regions.code FROM noc_regions ORDER BY noc_regions.code;

SELECT athletes.name 
FROM athletes, athletes_biometrics, athletes_super_table, noc_regions 
WHERE athletes_biometrics.athletes_id = athletes.id
AND athletes_super_table.athletes_biometrics_id = athletes_biometrics.id
AND athletes_super_table.noc_id = noc_regions.id
AND noc_regions.region LIKE 'Kenya';

SELECT medals.type, games.title
FROM medals, games, athletes, athletes_biometrics, athletes_super_table
WHERE athletes_biometrics.athletes_id = athletes.id
AND athletes_super_table.athletes_biometrics_id = athletes_biometrics.id
AND athletes_super_table.medal_id = medals.id
AND athletes_super_table.games_id = games.id