'''
olympics-api.py

A Flask app used for simple queries on the olympics database.

Code by Cole Weinstein, 21 October 2021

Credits: Jeff Ondich - flask_sample.py

For use in the "olympics" assignment from Carleton's
CS 257 Software Design class, Fall 2021.
'''

import sys
import argparse
import flask
import json

import psycopg2
import config

app = flask.Flask(__name__)

def connect():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        return connection
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/games')
def get_games():
    '''
        Returns a JSON list of dictionaries, where each dictionary represents a different olympic games. A games's dictionary is formatted as follows:
            game_dictionary = {'id' : games.id, 'year' : games.year, 'season' : seasons.season, 'city' : games.city}
        The JSON list is sorted by each games's year.
    '''

    connection = connect()

    query = '''SELECT games.id, games.year, seasons.season, games.city FROM games, seasons
                WHERE games.season_id = seasons.id
                ORDER BY games.year'''
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()
    
    games_list = []
    for row in cursor:
        id = row[0]
        year = row[1]
        season = row[2]
        city = row[3]

        game_dictionary = {'id' : id, 'year' : year, 'season' : season, 'city' : city}
        games_list.append(game_dictionary)
    
    connection.close()
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    '''
        Returns a JSON list of dictionaries, where each dictionary represents a different national olypmic committee (NOC). An NOC's dictionary is formatted as follows:
            noc_dictionary = {'abbreviation' : noc_regions.code, 'name' : noc_regions.region}
        The JSON list is sorted alphabetically by NOC abbreviation.
    '''

    connection = connect()

    query = '''SELECT DISTINCT code, region FROM noc_regions
                ORDER BY code'''
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()
    
    nocs_list = []
    for row in cursor:
        code = row[0]
        region = row[1]

        noc_dictionary = {'abbreviation' : code, 'name' : region}
        nocs_list.append(noc_dictionary)
    
    connection.close()
    return json.dumps(nocs_list)


@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    '''
        Returns a JSON list of dictionaries, where each dictionary represents a different athlete. An athlete's dictionary is formatted as follows:
            athlete_dictionary = {'athlete_id' : athletes.id, 'athlete_name' : athletes.name, 'athlete_sex' : biometrics.sex, 'sport' : sports.name, 'event' : events.name, 'medal' : medals.medal}
        An athlete's dictionary is only included if the athlete medaled in the given event. Additionally, if an NOC abbreviation is supplied, athletes not from that NOC will be excluded.
    '''

    connection = connect()

    query = '''SELECT DISTINCT athletes.id, athletes.athlete_name, biometrics.sex, sports.sport, events.event, medals.medal
                FROM athletes, athletes_biometrics, athletes_super_table, biometrics, events, medals, noc_regions, sports
                WHERE athletes_biometrics.athletes_id = athletes.id
                AND athletes_biometrics.biometrics_id = biometrics.id
                AND athletes_super_table.athletes_biometrics_id = athletes_biometrics.id
                AND events.sport_id = sports.id
                AND athletes_super_table.event_id = events.id
                AND athletes_super_table.medal_id = medals.id
                AND medals.medal NOT LIKE 'NA'
                AND athletes_super_table.games_id = %s'''

    noc_code = flask.request.args.get('noc')
    if noc_code is not None:
        query = query + '''AND noc_regions.code LIKE %s
                            AND athletes_super_table.noc_id = noc_regions.id'''
    query = query + ''';'''
    
    try:
        cursor = connection.cursor()
        if noc_code is not None:
            cursor.execute(query, (games_id, noc_code))
        else:
            cursor.execute(query, (games_id,))
    except Exception as e:
        print(e, file=sys.stderr)
        exit()
    
    print(cursor.rowcount)
    medalists_list = []
    for row in cursor:
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]
        sport = row[3]
        event = row[4]
        medal = row[5]

        medalist_dictionary = {'athlete_id' : athlete_id, 'athlete_name' : athlete_name, 'athlete_sex' : athlete_sex, 'sport' : sport, 'event' : event, 'medal' : medal}
        medalists_list.append(medalist_dictionary)
    
    connection.close()
    return json.dumps(medalists_list)

@app.route('/help')
def help():
    return flask.render_template('help.html')

# main code credited to Jeff Ondich, from flask-sample.py.
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A Flask API used to query the olympics database')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)