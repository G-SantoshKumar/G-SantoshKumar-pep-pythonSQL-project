import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    with open(file_path, mode='r') as userfile:
        users = csv.reader(userfile)
        next(users) 
        for row in users:
            if len(row) == 2 and all(record.strip() for record in row):
                first_name, last_name = row
                cursor.execute('''
                    INSERT INTO users (firstName, lastName)
                    VALUES (?, ?)
                ''', (first_name.strip(), last_name.strip()))
        conn.commit() 




    

# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    with open(file_path, mode='r') as callfile:
        calllogs = csv.reader(callfile)
        next(calllogs) 
        for row in calllogs:
            if len(row) == 5 and all(row):
                phone_number, start_time, end_time, direction, user_id = row
                cursor.execute('''
                    INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId)
                    VALUES (?, ?, ?, ?, ?)
                ''', (phone_number.strip(), int(start_time), int(end_time), direction.strip(), int(user_id)))
        conn.commit() 



# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as analyticsfile:
        writer = csv.writer(analyticsfile)
        cursor.execute('''
            SELECT userId, 
                   AVG(endTime - startTime) AS avgDuration, 
                   COUNT(callId) AS totalCalls
            FROM callLogs
            GROUP BY userId
        ''')
        rows = cursor.fetchall()
        writer.writerow(['userId', 'avgDuration', 'totalCalls'])
        for record in rows:
            writer.writerow(record)



# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        cursor.execute('''
            SELECT * 
            FROM callLogs
            ORDER BY userId, startTime
        ''')
        writer.writerow(['callId', 'phoneNumber', 'startTime', 'endTime', 'direction', 'userId'])
        rows = cursor.fetchall()
        for record in rows:
            writer.writerow(record)

    

# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
