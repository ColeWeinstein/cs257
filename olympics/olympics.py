'''
olympics.py

A command line program used to query data from the related olympics database.

Code by Cole Weinstein, 21 October 2021

Credits: Jeff Ondich - psycopg2-sample.py

For use in the "olympics" assignment from Carleton's
CS 257 Software Design class, Fall 2021.


'''
import argparse
import config
import psycopg2

def get_parsed_arguments():
    '''
        Gets arguments from command line.
    '''
    # Help descriptions for each argument and the argparser.
    arg_parse_description = '''Finds information about the athletes registered under a specific NOC (National Olympic Committee), the athletes who have participated in a given event, the athletes who participated in a certain year, and the athletes who have medaled.
    
    Additionally, finds the number of gold medals each NOC has won.

    The -e, -m, -n, and -y flags can all be combined in any order. The -g flag can only be modified by the -e and -y flags.'''
    
    noc_help = 'Queries the olympics database for every athlete from a given NOC'
    gold_help = 'Queries the olympics database for every NOC sorted by the number of gold medals won'
    event_help = 'Queries the olympics database for every athlete that has participated in the given event. When used with -n, restricts the query to all athletes from a certain NOC who have also participated in the specified event. When used with -g, restricts the query to all medals won by an NOC in the specified event.'
    year_help = 'Queries the olympics database for every athlete that participated in the given year. When used with -n, restricts the query to all athletes from a certain NOC who participated in the given year. When used with -g, restricts the query to all medals won by each NOC in a certain year. When used with -e, restricts the query to all athlete from a certain event who participated in the given year.'
    medal_help = 'Queries the olympics database for every athlete that has medaled, sorted by the number of medals won. When used with -n, -e, or -y restricts the query to all athletes who have medaled.'

    # Creates an argument parser and all flags for the program. --author, --title, and --year are all mutually exclusive, as are --titlesort and --yearsort.
    parser = argparse.ArgumentParser(description=arg_parse_description)
        
    parser.add_argument('-n', '--noc', metavar='NOC_CODE', nargs=1, type=str, help=noc_help)
    parser.add_argument('-g', '--gold', action='store_true', help=gold_help)
    parser.add_argument('-e', '--event', metavar='EVENT_NAME', nargs=1, type=str, help=event_help)
    parser.add_argument('-y', '--year', metavar='YEAR', nargs=1, type=int, help=year_help)
    parser.add_argument('-m', '--medal', action='store_true', help=medal_help)

    parsed_arguments = parser.parse_args()
    
    # Prevents -g flag from being used with -a or -m flag
    if parsed_arguments.gold and (parsed_arguments.noc or parsed_arguments.medal):
        parser.error('-g/--gold cannot be used with -n/--noc or -m/--medal')

    return parsed_arguments

def form_variable_query(noc_code, event, medal, year):
    query = 'SELECT '
    fields = ['athletes.athlete_name', 'noc_regions.code', 'noc_regions.region', 'events.event', 'sports.sport', 'games.title', 'medals.medal']
    tables = ['athletes', 'athletes_biometrics', 'athletes_super_table', 'noc_regions', 'events', 'sports', 'games', 'medals']
    where_statements = ['athletes_biometrics.athletes_id = athletes.id', 'athletes_super_table.athletes_biometrics_id = athletes_biometrics.athletes_id', 'athletes_super_table.noc_id = noc_regions.id', 'athletes_super_table.event_id = events.id', 'events.sport_id = sports.id', 'athletes_super_table.games_id = games.id', 'athletes_super_table.medal_id = medals.id']
    
    # The commented line in this if statement should be in the code, and they work. However, for clarity purposes, they have been excluded to prove that the query returned the correct results.
    if noc_code:
        #fields.remove('noc_regions.code')
        fields.remove('noc_regions.region')
        where_statements.append('noc_regions.code LIKE \'{noc_code}\'')
    if event:
        fields.remove('sports.sport')
        #fields.remove('events.event')
        where_statements.append('events.event LIKE \'{event_name}\'')
    if year:
        #fields.remove('games.title')
        where_statements.append('cast(games.year AS TEXT) LIKE cast(\'{games_year}\' AS TEXT)')
    if medal:
        where_statements.append('medals.medal NOT LIKE \'NA\'')
    
    for item in fields:
        query += item + ', '
    # Removes the last comma from the query string
    query = query[:-2] + '\n'

    query += 'FROM '

    for item in tables:
        query += item + ', '
    # Removes the last comma from the query string
    query = query[:-2] + '\n'

    query += 'WHERE '

    for item in where_statements:
        query += item + '\nAND '
    # Removes the last 'AND' from the query string
    query = query[:-4]

    # Orders the list by the type of medals won (adapted from https://stackoverflow.com/questions/6332043/sql-order-by-multiple-values-in-specific-order)
    if medal:
        query += '''ORDER BY
                        CASE
                            WHEN medals.medal = \'Gold\' THEN 1 
                            WHEN medals.medal = \'Silver\' THEN 2 
                            WHEN medals.medal = \'Bronze\' THEN 3 
                        END'''
    
    query += ';'

    print(query)

    return query


def form_golden_query(event, year):
    query = 'SELECT '
    fields = ['COUNT(medals.medal)', 'noc_regions.region']
    tables = ['medals', 'athletes_super_table', 'noc_regions']
    where_statements = ['athletes_super_table.medal_id = medals.id', 'medals.medal LIKE \'Gold\'', 'athletes_super_table.noc_id = noc_regions.id']
    
    if event:
        tables.append('events')
        tables.append('sports')
        where_statements.append('athletes_super_table.event_id = events.id')
        where_statements.append('events.sport_id = sports.id')
        where_statements.append('events.event LIKE \'{event_name}\'')
    if year:
        tables.append('games')
        where_statements.append('athletes_super_table.games_id = games.id')
        where_statements.append('cast(games.year AS TEXT) LIKE cast(\'{games_year}\' AS TEXT)')
    
    for item in fields:
        query += item + ', '
    # Removes the last comma from the query string
    query = query[:-2] + '\n'

    query += 'FROM '

    for item in tables:
        query += item + ', '
    # Removes the last comma from the query string
    query = query[:-2] + '\n'

    query += 'WHERE '

    for item in where_statements:
        query += item + '\nAND '
    # Removes the last 'AND' from the query string
    query = query[:-4]

    query += 'GROUP BY noc_regions.region\n'
    query += 'ORDER BY COUNT(medals.medal) DESC, noc_regions.region;'

    return query

def run_variable_query(cursor, noc_code='', event_name='', medal=False, games_year=0):
    noc = False
    if noc_code != '':
        noc = True
    event = False
    if event_name != '':
        event = True
    year = False
    if games_year != 0:
        year = True
    
    query = form_variable_query(noc, event, medal, year)
    try:
        cursor.execute(query.format(noc_code=noc_code, event_name=event_name, games_year=games_year))
    except Exception as e:
        print(e)
        exit()

def run_golden_query(cursor, event_name='', games_year=0):
    event = False
    if event_name != '':
        event = True
    year = False
    if games_year != 0:
        year = True
    
    query = form_golden_query(event, year)
    try:
        cursor.execute(query.format(event_name=event_name, games_year=games_year))
    except Exception as e:
        print(e)
        exit()

def fix_single_quotes(broken_string):
    temp_string_array = broken_string.split('\'')
    fixed_string = ''
    for substring in temp_string_array:
        fixed_string += substring + '%'
    fixed_string = fixed_string[:-1]
    return fixed_string

def user_input_identifier(cursor, input_string, field, table):
    query = 'SELECT {table}.{primary_field}'
    if table == 'noc_regions':
        query += ', noc_regions.region'
    elif table == 'events':
        query += ', sports.sport'
    query += ' FROM {table}'
    if table == 'events':
        query += ', sports'
    query += ' WHERE cast({table}.{primary_field} AS TEXT) ILIKE cast(\'%{input_string}%\' AS TEXT)'
    if table == 'noc_regions':
        query += ' OR noc_regions.region ILIKE \'%{input_string}%\''
        query += ' GROUP BY noc_regions.code, noc_regions.region'
    elif table == 'events':
        query += ' AND events.sport_id = sports.id'
    
    query += ';'

    try:
        cursor.execute(query.format(primary_field=field, table=table, input_string=input_string))
    except Exception as e:
        print(e)
        exit()
    
    """ print(query.format(primary_field=field, table=table, input_string=input_string))
    print(cursor.rowcount)
    exit() """
    
    if cursor.rowcount == 0:
        print('That string is not present in the appropriate table. Please run the program again.')
        exit()
    if cursor.rowcount == 1:
        temp_query_list = cursor.fetchall()
        if len(temp_query_list) == 2: # When the events or noc_regions table was queried
            return temp_query_list[0][0]
        return temp_query_list[0][0]
    else:
        print('Did you mean one of the following?')
        if table == 'noc_regions':
            print('    Code' + '  ' + 'Region')
            print('=' * 30)
        elif table == 'events':
            print('    Events' + ' ' * (54) + 'Sports')
            print('=' * 100)
        else:
            print(field)
            print('=' * 30)
        
        cursor_items = []
        line_count = 1
        for row in cursor:
            if len(row) == 2:
                if table == 'noc_regions':
                    string_to_print = row[0] + '   ' + row[1]
                elif table == 'events':
                    string_to_print = row[0] + ' ' * (60 - len(row[0])) + row[1]
                print(str(line_count) + ' ' * (4 - len(str(line_count))) + string_to_print)
            else:
                print(str(line_count) + ' ' * (4 - len(str(line_count))) + row[0])
            cursor_items.append(row[0])
            line_count += 1
        print()

        input_clarifier = input('Which {field} did you mean? (Please enter the field\'s number.) '.format(field=field))
        try:
            return cursor_items[int(input_clarifier) - 1]
        except Exception as e:
            print('Error. Invalid input given.')
            exit()

    


def main():
    # Connect to the database (database connection code from Jeff Ondich's psycopg2-sample.py)
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print(e)
        exit()

    try:
        cursor = connection.cursor()
    except Exception as e:
        print(e)
        exit()

    arguments = get_parsed_arguments()
    noc_code = ''
    if arguments.noc:
        noc_code = user_input_identifier(cursor, arguments.noc[0], 'code', 'noc_regions')
        print(noc_code)
    event_name = ''
    if arguments.event:
        event_name = fix_single_quotes(user_input_identifier(cursor, arguments.event[0], 'event', 'events'))
        print(event_name)
    games_year = 0
    if arguments.year:
        games_year = user_input_identifier(cursor, arguments.year[0], 'year', 'games')
        print(games_year)
    medal = False
    if arguments.medal:
        medal = True
    
    try:
        if arguments.gold:
            #query = form_golden_query(arguments.gold, arguments.event, arguments.year)
            run_golden_query(cursor, event_name, games_year)
        else:
            #query = form_variable_query(arguments.athlete, arguments.event, arguments.medal, arguments.year)
            run_variable_query(cursor, noc_code, event_name, medal, games_year)
    except Exception as e:
        print(e)
        exit()
    
    print('Output:')
    line_count = 0
    for row in cursor:
        string_to_print = ''
        for element in row:
            string_to_print += str(element) + ' ' * (60 - len(str(element)))
        print(string_to_print)
        line_count += 1
        if line_count == 5:
            exit()
    print()

    connection.close()

if __name__ == '__main__':
    main()