CREATE TABLE medals(
id SMALLSERIAL,
type TEXT
);

CREATE TABLE sports(
id SMALLSERIAL,
name TEXT
);

CREATE TABLE events(
id SMALLSERIAL,
sport_id INT,
name TEXT
);

CREATE TABLE games(
id SMALLSERIAL,
title TEXT,
year INT,
season TEXT,
city TEXT
);

CREATE TABLE noc_regions(
id SMALLSERIAL,
code TEXT,
region TEXT,
team_name TEXT
);

CREATE TABLE athletes(
id SERIAL,
name TEXT
);

CREATE TABLE biometrics(
id SERIAL,
sex TEXT,
age INT,
weight INT,
height INT
);

CREATE TABLE athletes_biometrics(
id SERIAL,
athletes_id INT,
biometrics_id INT
);

CREATE TABLE athletes_events(
id SERIAL,
athletes_biometrics_id INT,
games_id INT,
noc_id INT,
event_id INT,
medal_id INT
);

