SELECT DISTINCT code FROM noc_regions ORDER BY code;

SELECT DISTINCT(athletes.athlete_name), noc_regions.region
FROM athletes, athletes_biometrics, athletes_super_table, noc_regions 
WHERE athletes_biometrics.athletes_id = athletes.id
AND athletes_super_table.athletes_biometrics_id = athletes_biometrics.id
AND athletes_super_table.noc_id = noc_regions.id
AND noc_regions.region LIKE 'Kenya';

SELECT athletes.athlete_name, medals.medal, games.title, events.event
FROM medals, games, events, athletes, athletes_biometrics, athletes_super_table
WHERE athletes.athlete_name LIKE '%Greg%Louganis%'
AND athletes_biometrics.athletes_id = athletes.id
AND athletes_super_table.athletes_biometrics_id = athletes_biometrics.id
AND athletes_super_table.medal_id = medals.id
AND athletes_super_table.games_id = games.id
AND athletes_super_table.event_id = events.id;

SELECT COUNT(medals.medal), noc_regions.code, medals.medal
FROM noc_regions, athletes_super_table, medals
WHERE medals.medal LIKE '%Gold%'
AND athletes_super_table.noc_id = noc_regions.id
AND athletes_super_table.medal_id = medals.id
GROUP BY noc_regions.code
ORDER BY COUNT(medals.medal) DESC, noc_regions.code;