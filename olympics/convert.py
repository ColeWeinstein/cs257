'''
    convert.py
    Code by Cole Weinstein, October 14th, 2021

    For use in the "olympics" database design project for Carleton's CS 257 course.
'''

import csv

sports_dict = {} # sport_name : id_number
events_dict = {} # event_name|sport_id : id_number
games_dict = {} # game_title|year|season|city : id_number
seasons_dict = {} # season_name : id_number
medals_dict = {} # medal_type : id_number
noc_regions_dict = {} # noc_code|region|team_name : id_number
athletes_dict = {} # athlete_name : id_number 
biometrics_dict = {} # sex|age|weight|height : id_number
athletes_biometrics_dict = {} # athlete_id|biometric_id : id_number
athletes_super_table_dict = {} # athlete_biometric_id|game_id|noc_id|event_id|medal_id : id_number

def create_files():
  '''
      Checks if these files exist already. If they do, clear all contents. If not, make them.
  '''
  with open('athletes.csv', 'w') as file:
    file.truncate()
  with open('athletes_biometrics.csv', 'w') as file:
    file.truncate()
  with open('athletes_super_table.csv', 'w') as file:
    file.truncate()
  with open('biometrics.csv', 'w') as file:
    file.truncate()
  with open('events.csv', 'w') as file:
    file.truncate()
  with open('games.csv', 'w') as file:
    file.truncate()
  with open('seasons.csv', 'w') as file:
    file.truncate()
  with open('medals.csv', 'w') as file:
    file.truncate()
  with open('noc.csv', 'w') as file:
    file.truncate()
  with open('sports.csv', 'w') as file:
    file.truncate()


def populate_csv_files():
  '''
    Kaggle's athletes file looks as follows:
      id,name,sex,age,height,weight,team,NOC,games,year,season,city,sport,event,medal

    Kaggle's noc_regions file looks as follows:
      NOC,region,notes

    This __init__ method parses the specified csv files and creates a number of smaller csv files...
  '''

  athletes_file = open('athlete_events.csv', 'r')
  athletes_reader = csv.reader(athletes_file)
  next(athletes_file) #skips header line

  noc_regions_file = open('noc_regions.csv', 'r')
  noc_regions_reader = csv.reader(noc_regions_file)
  next(noc_regions_file) #skips header line

  medals_file = open('medals.csv', 'w')
  medals_writer = csv.writer(medals_file)

  sports_file = open('sports.csv', 'w')
  sports_writer = csv.writer(sports_file)

  events_file = open('events.csv', 'w')
  events_writer = csv.writer(events_file)

  games_file = open('games.csv', 'w')
  games_writer = csv.writer(games_file)

  seasons_file = open('seasons.csv', 'w')
  seasons_writer = csv.writer(seasons_file)

  noc_file = open('noc.csv', 'w')
  noc_writer = csv.writer(noc_file)

  athletes_file = open('athletes.csv', 'w')
  athletes_writer = csv.writer(athletes_file)

  biometrics_file = open('biometrics.csv', 'w')
  biometrics_writer = csv.writer(biometrics_file)

  athletes_biometrics_file = open('athletes_biometrics.csv', 'w')
  athletes_biometrics_writer = csv.writer(athletes_biometrics_file)

  athletes_super_table_file = open('athletes_super_table.csv', 'w')
  athletes_super_table_writer = csv.writer(athletes_super_table_file)


  temp_noc_dict = {} #temporarily stores contents of noc_regions.csv. format - {NOC_CODE : region_name}
  
  #iterate through every line in noc_regions.csv and add each noc to the temporary dictionary above.
  for row in noc_regions_reader:
    if row[0] not in temp_noc_dict:
      #note: often, the notes column often has more detailed region names, if it exists for the noc. thus, we'll use the more detailed region name for better clarity.
      if row[2]:
        temp_noc_dict.update({row[0] : row[2]})
      else:
        temp_noc_dict.update({row[0] : row[1]})

  for row in athletes_reader:
    #stores each field as a separate variable (for readability)
    athlete_name = row[1]
    sex = row[2]
    age = row[3]
    height = row[4]
    weight = row[5]
    team_name = row[6]
    noc_code = row[7]
    region = temp_noc_dict.get(noc_code)
    game_title = row[8]
    year = row[9]
    season = row[10]
    city = row[11]
    sport_name = row[12]
    event_name = row[13]
    medal_type = row[14]

    populate_athletes_super_table(athlete_name, sex, age, height, weight, game_title, year, season, city, noc_code, region, team_name, sport_name, event_name, medal_type)


  #writes each entry in the following dictionaries to the appropriate file

  for sport_string in sports_dict:
    sport_string_row = sport_string.split("|")
    sport_string_row.insert(0, sports_dict.get(sport_string))
    sports_writer.writerow(sport_string_row)
  
  for event_string in events_dict:
    event_string_row = event_string.split("|")
    event_string_row.insert(0, events_dict.get(event_string))
    events_writer.writerow(event_string_row)

  for game_string in games_dict:
    game_string_row = game_string.split("|")
    game_string_row.insert(0, games_dict.get(game_string))
    games_writer.writerow(game_string_row)

  for season_string in seasons_dict:
    season_string_row = season_string.split("|")
    season_string_row.insert(0, seasons_dict.get(season_string))
    seasons_writer.writerow(season_string_row)

  for medal_string in medals_dict:
    medal_string_row = medal_string.split("|")
    medal_string_row.insert(0, medals_dict.get(medal_string))
    medals_writer.writerow(medal_string_row)

  for noc_region_string in noc_regions_dict:
    noc_region_string_row = noc_region_string.split("|")
    noc_region_string_row.insert(0, noc_regions_dict.get(noc_region_string))
    noc_writer.writerow(noc_region_string_row)

  for athlete_string in athletes_dict:
    athlete_string_row = athlete_string.split("|")
    athlete_string_row.insert(0, athletes_dict.get(athlete_string))
    athletes_writer.writerow(athlete_string_row)

  for biometric_string in biometrics_dict:
    biometric_string_row = biometric_string.split("|")
    biometric_string_row.insert(0, biometrics_dict.get(biometric_string))
    biometrics_writer.writerow(biometric_string_row)

  for athlete_biometric_string in athletes_biometrics_dict:
    athlete_biometric_string_row = athlete_biometric_string.split("|")
    athlete_biometric_string_row.insert(0, athletes_biometrics_dict.get(athlete_biometric_string))
    athletes_biometrics_writer.writerow(athlete_biometric_string_row)

  for athlete_super_table_string in athletes_super_table_dict:
    athlete_super_table_string_row = athlete_super_table_string.split("|")
    athlete_super_table_string_row.insert(0, athletes_super_table_dict.get(athlete_super_table_string))
    athletes_super_table_writer.writerow(athlete_super_table_string_row)
  

  athletes_file.close()
  noc_regions_file.close()
  medals_file.close()
  sports_file.close()
  events_file.close()
  games_file.close()
  seasons_file.close()
  noc_file.close()
  athletes_file.close()
  biometrics_file.close()
  athletes_biometrics_file.close()
  athletes_super_table_file.close()
  




#for all populate methods, the following rules apply:
#   1) call helper methods if needed
#   2) create a general string to concatenate information if there is more than one parameter
#   3) check if the aforementioned string is already in the appropriate dictionary. if it isn't, add iter
#   4) get the id value of the string from the dictionary and return it.
#      -Note: this is different for populate_athletes_events, which just returns the string since there is no dictioanry for it.

def populate_sports(sport_name):
  if sport_name not in sports_dict:
    sports_dict.update({sport_name : len(sports_dict)})
    
  return sports_dict.get(sport_name)

def populate_events(event_name, sport_name):
  sport_id = populate_sports(sport_name)
  event_string = event_name + "|" + str(sport_id)

  if event_string not in events_dict:
    events_dict.update({event_string : len(events_dict)})
   
  return events_dict.get(event_string)

def populate_games(game_title, year, season, city):
  season_id = populate_seasons(season)
  game_string = game_title + "|" + str(year) + "|" + str(season_id) + "|" + city

  if game_string not in games_dict:
    games_dict.update({game_string : len(games_dict)})

  return games_dict.get(game_string)

def populate_seasons(season):
  if season not in seasons_dict:
    seasons_dict.update({season : len(seasons_dict)})

  return seasons_dict.get(season)

def populate_medals(medal_type):
  if medal_type not in medals_dict:
    medals_dict.update({medal_type : len(medals_dict)})
    
  return medals_dict.get(medal_type)

def populate_noc_regions(noc_code, region, team_name):
  noc_string = noc_code + "|" + region + "|" + team_name

  if noc_string not in noc_regions_dict:
    noc_regions_dict.update({noc_string : len(noc_regions_dict)})
    
  return noc_regions_dict.get(noc_string)

def populate_athletes(athlete_name):
  if athlete_name not in athletes_dict:
    athletes_dict.update({athlete_name : len(athletes_dict)})
  
  return athletes_dict.get(athlete_name)

def populate_biometrics(sex, age, weight, height):
  biometric_string = sex + "|" + str(age) + "|" + str(weight) + "|" + str(height)

  if biometric_string not in biometrics_dict:
    biometrics_dict.update({biometric_string : len(biometrics_dict)})

  return biometrics_dict.get(biometric_string)

def populate_athletes_biometrics(athlete_name, sex, age, weight, height):
  athlete_id = populate_athletes(athlete_name)
  biometric_id = populate_biometrics(sex, age, weight, height)
  athlete_biometric_string = str(athlete_id) + "|" + str(biometric_id)

  if athlete_biometric_string not in athletes_biometrics_dict:
    athletes_biometrics_dict.update({athlete_biometric_string : len(athletes_biometrics_dict)})

  return athletes_biometrics_dict.get(athlete_biometric_string)

def populate_athletes_super_table(athlete_name, sex, age, weight, height, game_title, year, season, city, noc_code, region, team_name, sport_name, event_name, medal_type):
  athlete_biometric_id = populate_athletes_biometrics(athlete_name, sex, age, weight, height)
  game_id = populate_games(game_title, year, season, city)
  noc_id = populate_noc_regions(noc_code, region, team_name)
  event_id = populate_events(event_name, sport_name)
  medal_id = populate_medals(medal_type)

  athlete_super_table_string = str(athlete_biometric_id) + "|" + str(game_id) + "|" + str(noc_id) + "|" + str(event_id) + "|" + str(medal_id)

  if athlete_super_table_string not in athletes_super_table_dict:
    athletes_super_table_dict.update({athlete_super_table_string : len(athletes_super_table_dict)})

  return athletes_super_table_dict.get(athlete_super_table_string)



def main():
  '''
      Main method to create/flush the .csv files, then populate them appropriately.
  '''
  create_files()
  populate_csv_files()

if __name__ == '__main__':
  main()