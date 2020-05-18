import mysql.connector
import time


def select_query(db_params, query_string, query_params=None):
    """
    This function returns the results of a SQL query as a list of dictionaries where
    each dictionary is a row and the keys are the column names from the select
    statement.
    Requires the following arguments:
        1 - dictionary with database connection info
        2 - the SQL query as a string
        3 - optional dictionary of parameters to pass into the SQL query, default is None
    """
    
    con = create_db_connection(db_params)
    cursor = con.cursor()

    # Combine SQL query with parameters then execute
    cursor.execute(query_string, query_params)
    results = cursor.fetchall()

    # Retrieve column names and store as a tuple
    # cursor.description is a tuple of tuples where [0] for each is the column header
    column_names = tuple([i[0] for i in cursor.description])

    # Convert the results to a list (of tuples)
    results = list(results)

    # Convert the results to a list of dictionaries using column names as the keys
    results = [dict(zip(column_names, row)) for row in results]

    print('query complete, '  + str(len(results)) + ' rows retrieved')
    
    cursor.close()
    con.close()

    return results


def insert_rows(db_params, table, column_names, data):
    """
    This function does a bulk insert of rows into a table.
    Requires the following arguments:
        1 - dictionary with database connection info
        2 - table name
        3 - list of columns names
        4 - data, the dataset to be inserted, must be a list of dictionaries where each
              dictionary will be one row in the database and includes all of the column names
              from the relevant list above as keys
    """

    records_received = len(data)
    records_processed = 0

    # Create a string like "%s, %s, %s, %s" corresponding to number of columns
    values = values_string(len(column_names))

    # Convert data from list of dictionaries to list of tuples
    processed_data = dicts_to_tuples(column_names, data)

    # Convert list of fields to a single string
    column_names = ', '.join(column_names)
    
    insert_statement = 'INSERT INTO ' + table + '(' + column_names + ') VALUES(' + values + ')'
    
    # Max number of records to try to insert at a time
    step = 30000
    n = 0        
    
    while n < len(processed_data):
        
        sub_list = processed_data[n:(n + step)]
        
        # Connect to database... some of this should be outside of the while loop
        con = create_db_connection(db_params)
        cursor = con.cursor()
        
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        try:
            # Insert data (up to the max number of records specified above) into the table
            cursor.executemany(insert_statement, sub_list)
            con.commit()
        
        # In case of error executing the inserts, rollback any changes and make sure
        # to close the connection, then raise the error again so scripts stop
        except MySQLdb.Error as e:
            con.rollback()
            cursor.close()
            con.close()
            raise e
        
        cursor.close()
        con.close()
        
        n += step
        
        records_processed += len(sub_list)
        
        print(str(records_processed) + ' out of ' + str(records_received) + ' records processed')
    
    print('inserted ' + str(records_received) + ' rows into ' + table)


def truncate_table(db_params, table):
    """
    This function truncates a given table.
    Requires the following arguments:
        1 - dictionary with database connection info
        2 - table name
    """

    con = create_db_connection(db_params)

    cursor = con.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    cursor.close()

    cursor = con.cursor()
    cursor.execute('TRUNCATE TABLE ' + table)
    cursor.close()

    cursor = con.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')
    cursor.close()

    con.commit()

    print('truncated the ' + table + ' table')

    con.close()


def create_db_connection(db_params, max_attempts=10, wait_time=0.5):
    """
    Returns a database connection object.
    Requires the following arguments:
        1 - db_params, this is a dictionary that contains:
              'database': the name of the database (e.g., 'pythonanywhereuser$default')
              'user': the db username (e.g., pythonanywhereuser)
              'pw': the db password
              'host': the db host address (e.g., pythonanywhereuser.mysql.pythonanywhere-services.com)
              'port': the db port (usually 3306 for MySQL)
        2 - optional value for max number of attempts to connect, default is 10
        3 - optional value for number of seconds to wait between attempts, default is 0.5
    """
    
    database = db_params['database']
    user     = db_params['user']
    pw       = db_params['pw']
    host     = db_params['host']
    port     = db_params['port']
    
    n = 0
    
    while n < max_attempts:
        
        try:
            return mysql.connector.connect(host=host, port=port, user=user, passwd=pw, db=database)
        
        except Exception as e:
            print(e)
            error = e
        
        time.sleep(wait_time)
        n += 1
    
    raise(error)


def dicts_to_tuples(keys, list_of_dicts):
    """
    Converts a list of dictionaries to a list of tuples.
    Requires the following arguments:
        1 - a list of keys for the dictionaries, should be comprehensive, any
            dictionary that doesn't have all keys present will use None for the
            missing values
        2 - the list of dictionaries
    """

    list_of_tuples = []
    for d in list_of_dicts:
        
        row = []
        for k in keys:
            
            # Using get(key) so that None is returned in case the key is not present
            # in the dictionary being processed
            row.append(d.get(k))
        
        list_of_tuples.append(tuple(row))

    return list_of_tuples


def values_string(n):
    """
    Creates a string of value placeholders (e.g., "%s, %s, %s, %s") for use in
    the MySQL insert statement.
    Requires the following arguments:
        1 - an integer that is the number of fields being inserted
            (the length of the column_names list)
    """

    values = []

    for i in range(n):
        values.append('%s')

    return ', '.join(values)
