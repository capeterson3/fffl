import psycopg2
from psycopg2 import Error

def create_table():
    try:
        connection = psycopg2.connect(user = "postgres",
                                  password = "rodgers12",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "fffl")


        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE scores
          (ID INT PRIMARY KEY NOT NULL,
          YEAR INT      NOT NULL,
          WEEK INT    NOT NULL,
          TEAM TEXT   NOT NULL,
          PTS_FOR FLOAT8 NOT NULL,
          OPPONENT TEXT   NOT NULL,
          PTS_AGAINST FLOAT8 NOT NULL); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def drop_table(table_name):
    try:
        connection = psycopg2.connect(user = "postgres",
                                  password = "rodgers12",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "fffl")


        cursor = connection.cursor()
        create_table_query = ' DROP TABLE IF EXISTS %s' % (table_name)

        cursor.execute(create_table_query)
        connection.commit()
        print("Table dropped successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def bulkInsert(records):
    try:
        connection = psycopg2.connect(user = "postgres",
                                  password = "rodgers12",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "fffl")
        cursor = connection.cursor()

        sql_insert_query = """ INSERT INTO scores (id, year, week, team, pts_for, opponent, pts_against)
                           VALUES (%s,%s,%s,%s,%s,%s,%s)
                           ON CONFLICT (id) 
                           DO UPDATE SET (id, year, week, team, pts_for, opponent, pts_against) = 
                           (EXCLUDED.id, EXCLUDED.year, EXCLUDED.week, EXCLUDED.team, EXCLUDED.pts_for, EXCLUDED.opponent, EXCLUDED.pts_against)"""

        # executemany() to insert multiple rows rows
        result = cursor.executemany(sql_insert_query, records)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into mobile table {}".format(error))

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# records_to_insert = [ (2019125, 2019, 12, "Winks", 56.46, "Ceej", 64.98)]
# bulkInsert(records_to_insert)

if __name__ == '__main__':
    # drop_table('weekly_scoreboard')
    create_table()
