import sqlite3
import pandas as pd
import flask
import functools
import textwrap
from collections import OrderedDict
from configparser import ConfigParser

## utils
def config(filename='config.ini', section = 'sqlite3'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    for param in parser.items(section):
        config[param[0]] = param[1]
    return config
    
class TestLogger:
    def info_log(self, text : str):
        print("INFO |", text)
    def info_query_results(self, results):
        results = [list(map(str, row)) for row in results]
        lengths = [len(max(item, key=len)) for item in zip(*results)]
        print('\n'.join('  '.join(field_value[i].ljust(lengths[i]) for i in range(len(lengths))) for field_value in results))
    def info_error(self, error):
        print("ERROR |", error)

class SQLTask:
    def __init__(self, cursor, logger, query : str):
        self.cursor = cursor
        self.query = query
        self.Logger = logger
    def execute_query(self):
        try:
            self.cursor.execute(self.query)
            results = self.cursor.fetchall()
            columns = tuple([row[0] for row in self.cursor.description])
            results.insert(0, columns)
            assert len(results) > 1
            self.Logger.info_query_results(results)
            self.Logger.info_log("Closing cursor")
            self.cursor.close()
            return results
        except AssertionError:
            self.Logger.info_error("Query returned no data")
            self.Logger.info_log("Closing cursor")
            self.cursor.close()
            flask.abort(400)
class DbManager:
    def __init__(self):
        self.connection = None
        self.Logger = TestLogger()
    def connect(self):
        try:
            params = config()
            self.connection = sqlite3.connect(**params)
            self.Logger.info_log("Connecting to database")            
        except (Exception, sqlite3.DatabaseError) as err:
            self.Logger.info_error(err)
            flask.abort(500)

    def close(self):
        self.Logger.info_log("Closing connection to database")
        self.connection.close()
        self.connection = None

    def execute_query(self, query : str):
        self.connect()
        self.Logger.info_log("Executing query " + query)
        cursor = self.connection.cursor()
        task = SQLTask(cursor, self.Logger, query)
        results = task.execute_query()
        self.close()
        return results

    def execute_script(self, script : str):
        self.connect()
        with open(script, 'r') as file:
            sql_script = file.read()
        self.Logger.info_log("Executing SQL script " + script)
        cursor = self.connection.cursor()
        cursor.executescript(sql_script)
        self.close()

    def init_database(self):
        scripts = config(section="scripts")
        for script in list(scripts.values()):
            self.execute_script(script)
        self.load_file_to_table("BirdsFinal.xlsx")

    def load_file_to_table(self, filename : str):
        self.connect()

        pandas_df = pd.read_excel(filename)
        pandas_df['id'] = pandas_df.index + 1
        clone = pd.DataFrame()
        clone['id'] = pandas_df['id']
        clone['class'] = pandas_df['bird_en']
        clone.to_sql(name='classes', con=self.connection, if_exists='append', index=False)

        clone = pd.DataFrame()
        clone['id'] = pandas_df['id']
        clone['bird_ru'] = pandas_df['bird_ru']
        clone['desc_ru'] = pandas_df['desc_ru']
        clone['size_ru'] = pandas_df['size_ru']
        clone['place_ru'] = pandas_df['place_ru']
        clone['bird_id'] = pandas_df['id']
        clone.to_sql(name='ruBirds', con=self.connection, if_exists='append', index=False)

        clone = pd.DataFrame()
        clone['id'] = pandas_df['id']
        clone['bird_en'] = pandas_df['bird_en']
        clone['desc_en'] = pandas_df['desc_en']
        clone['size_en'] = pandas_df['size_en']
        clone['place_en'] = pandas_df['place_en']
        clone['bird_id'] = pandas_df['id']
        clone.to_sql(name='enBirds', con=self.connection, if_exists='append', index=False)

        self.close()
