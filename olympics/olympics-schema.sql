CREATE TABLE medals(
id SMALLSERIAL,
medal TEXT
);

CREATE TABLE sports(
id SMALLSERIAL,
sport TEXT
);

CREATE TABLE events(
id SMALLSERIAL,
event TEXT,
sport_id INT
);

CREATE TABLE games(
id SMALLSERIAL,
title TEXT,
year INT,
season_id INT,
city TEXT
);

CREATE TABLE seasons(
id SMALLSERIAL,
season TEXT
);

CREATE TABLE noc_regions(
id SMALLSERIAL,
code TEXT,
region TEXT,
team_name TEXT
);

CREATE TABLE athletes(
id SERIAL,
athlete_name TEXT
);

CREATE TABLE biometrics(
id SERIAL,
sex TEXT,
age INT,
weight DECIMAL(6,2),
height DECIMAL(6,2)
);

CREATE TABLE athletes_biometrics(
id SERIAL,
athletes_id INT,
biometrics_id INT
);

CREATE TABLE athletes_super_table(
id SERIAL,
athletes_biometrics_id INT,
games_id INT,
noc_id INT,
event_id INT,
medal_id INT
);

