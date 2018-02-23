import bleach
import psycopg2
from datetime import datetime

import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Database_initial_connection import connect_for_table_and_database_creation


def create_database():
    connection = None
    try:
        connection, cursor = connect_for_table_and_database_creation()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        #Change this before doing anything else with this code
        cursor.execute('DROP DATABASE IF EXISTS {};'.format('script_reader_database'))
        cursor.execute('CREATE DATABASE {};'.format('script_reader_database'))
    except Exception as e:
        print("This is broken, error {}".format(e))
        connection.exit(1)


def create_tables():
    connection, cursor = connect_for_table_and_database_creation()
    tables = [
    """
    CREATE TABLE IF NOT EXISTS scripts(\
        script_no SERIAL PRIMARY KEY,\
        script_name TEXT,\
        script_uploaded_at TIMESTAMP WITH TIME ZONE\
        );
        """,
    """
    CREATE TABLE IF NOT EXISTxS locations_info(
        location_no SERIAL PRIMARY KEY,
        scene_no VARCHAR(10),
        int_or_ext VARCHAR(8),
        location_type TEXT,
        time_of_day VARCHAR(20),
        script_no INT,
        FOREIGN KEY (script_no)
            REFERENCES scripts (script_no)
        );
        """]
    for table in tables:
        cursor.execute(table)
        connection.commit()
    connection.close()


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a
    script_reader_database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def add_to_Scripts_DB(scriptname):
    database, command = connect('script_reader_database')
    scriptname = bleach.clean(scriptname)
    scriptname = (str(scriptname), datetime.now())
    SQL = "INSERT INTO scripts (script_name, script_uploaded_at) VALUES (%s, %s)"
    command.execute(SQL, scriptname)
    database.commit()
    database.close()


def add_to_LocationsInfo_DB(locations_info, scriptname):
    database, command = connect('script_reader_database')
    information_for_database = []
    for information in locations_info:
        information = bleach.clean(information)
        information_for_database += [information]
    scriptname = str(bleach.clean(scriptname))
    SQL1 = "SELECT script_no FROM scripts WHERE script_name = '%s' ORDER BY script_no DESC LIMIT 1;"
    command.execute(SQL1 % scriptname)
    ScriptNo = command.fetchone()[0]
    information_for_database += [ScriptNo]
    SQL2 = "INSERT INTO locations_info (scene_no, int_or_ext, location_type, \
    time_of_day, script_no) VALUES (%s, %s, %s, %s, %s);"
    command.execute(SQL2, information_for_database)
    database.commit()
    database.close()
