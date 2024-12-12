from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import datetime
import json
import uuid


# Flask app for inference
app = Flask(__name__)

# Define your connection details
host = 'bookswap-db.cjysyg8487dw.us-east-2.rds.amazonaws.com'  # e.g., 'mydbinstance.c1abcd2efghz.us-west-2.rds.amazonaws.com'
db_username = 'admin'
password = '#Cloud1234'

#tests connection to db
def test_connection():
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # Example query (fetching server version)
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print("MySQL Server version:", db_version[0])

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# Returns all books from metadata
@app.route('/allBooks', methods=['GET'])
def all_books():
    print("GET to /allBooks")
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # Example query (fetching server version)
            cursor.execute("SELECT * FROM book_info.nyt_data")
            row_headers = [x[0] for x in cursor.description]
            book_data = cursor.fetchall()
            return format_json_response(row_headers, book_data), 201

    except Error as e:
        print(f"Error while getting books: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

@app.route('/getRequestInfo', methods=['GET'])
def get_request_info():
    req_id = request.args.get('request_id')
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # get request
            sql_statement = "SELECT * FROM libary_data.library_request where request_id = '%s'"
            params = (req_id)
            cursor.execute(sql_statement, params)
            row_headers = [x[0] for x in cursor.description]
            lib_req = cursor.fetchone()
            return format_json_response(row_headers, lib_req), 201

    except Error as e:
        print(f"Error while getting req info: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# Get info about user
@app.route('/getUserInfo', methods=['GET'])
def get_user_info():
    un = request.args['username']
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # get request
            sql_statement = "SELECT * FROM user_data.user where username = '" + un + "'"
            cursor.execute(sql_statement)
            user_info = cursor.fetchone()
            return jsonify(user_info), 201

    except Error as e:
        print(f"Error while getting req info: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# User makes offer
# {isbn, username, library}
@app.route('/offer', methods=['POST'])
def offer():
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        #get payload
        data = request.get_json()

        unique_id = str(uuid.uuid4())
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        # insert into request table
        sql_statement = "INSERT INTO library_data.library_request (request_id, library, request_type, isbn, request_date, request_user, fulfill_date, fulfill_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (unique_id, data.library, 'offer', data.username, data.isbn, datetime.datetime.now(), data.username, 'NULL', 'NULL' )
        cursor.execute(sql_statement, params)
        connection.commit()

        response_data = {
            "message": "Offer made successfully",
            "received": data
        }

        return jsonify(response_data), 201

    except Error as e:
        print(f"Error while connecting making offer: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# User makes ask
# {isbn, username, library}
@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        #get payload
        data = request.get_json()

        unique_id = str(uuid.uuid4())
        # Create a cursor object to execute queries
        cursor = connection.cursor()
        # insert into request table
        sql_statement = "INSERT INTO library_data.library_request (request_id, library, request_type, isbn, request_date, request_user, fulfill_date, fulfill_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (unique_id, data.library, 'ask', data.username, data.isbn, datetime.datetime.now(), data.username, 'NULL', 'NULL' )
        cursor.execute(sql_statement, params)
        connection.commit()

        response_data = {
            "message": "Ask made successfully",
            "received": data
        }

        return jsonify(response_data), 201

    except Error as e:
        print(f"Error while connecting making offer: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# Get pre-generated recommendations for user
# {username}
@app.route('/getRecs', methods=['POST'])
def get_recs():
    try:

        data = request.get_json()
        
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # query
            sql_statement =  "SELECT lr.* FROM user_data.user_recommendation ur INNER JOIN library_data.library_request lr ON ur.request_id = lr.request_id WHERE ur.username = '%s' and lr.fulfill_date IS NULL"
            param = data.username
            cursor.execute(sql_statement, param)
            row_headers = [x[0] for x in cursor.description]
            recs = cursor.fetchall()
            return format_json_response(row_headers, recs), 201

    except Error as e:
        print(f"Error while getting recs: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")
            
# Subscribe user to library feed
# {username, library}
@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:

        data = request.get_json()
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # insert into subscription table
            sql_statement = "INSERT INTO library_data.library_subscription (username, library) VALUES (%s, %s)"
            params = (data.username, data.library)
            cursor.execute(sql_statement, params)
            connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"success": data.username + " is subscribed to " + data.library}), 201

    except Error as e:
        print(f"Error while subscribing: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# Get feed for user
# {username}
@app.route('/getFeed', methods=['POST'])
def get_feed():
    try:

        data = request.get_json()
        
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # Get user subscriptions
            libraries = get_user_subscriptions(data.username, connection)
            feed = list()
            for lib in libraries:
                sql_statement =  "SELECT lr.* FROM library_data.library_request lr WHERE lr.fulfill_date IS NULL and lr.library = '%s' ORDER BY lr.request_date"
                param = lib
                cursor.execute(sql_statement, param)
                row_headers = [x[0] for x in cursor.description]
                library_requests = cursor.fetchall()
                feed.extend(library_requests)
                cursor.reset()

            return format_json_response(row_headers, feed), 201

    except Error as e:
        print(f"Error while getting feed: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")


# Get feed for user
# {username}
@app.route('/getSubscriptions', methods=['POST'])
def get_subscriptions():
    try:

        data = request.get_json()
        
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Get user subscriptions
            libraries = get_user_subscriptions(data.username, connection)

            return jsonify(libraries), 201

    except Error as e:
        print(f"Error while getting subscriptions: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")

@app.route('/getBookByIsbn')
def get_book_by_isbn():
    isbn = request.args.get('isbn')
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # get request
            sql_statement = "SELECT * FROM book_info.nyt_data where isbn13 = " + isbn
            cursor.execute(sql_statement)
            book_info = cursor.fetchone()
            return jsonify(book_info), 201

    except Error as e:
        print(f"Error while getting req info: {e}")
        return jsonify({"error": str(e)}), 500 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")


def get_user_subscriptions(username, connection):
    try:
        # Create a cursor object to execute queries
        sub_cursor = connection.cursor()

        # Get user subscriptions
        sql_statement =  "SELECT library FROM libary_subscription WHERE username = '%s' "
        sub_cursor.execute(sql_statement, username)
        subscriptions = sub_cursor.fetchall()
        sub_cursor.close()
        return subscriptions
    except Error as e:
        sub_cursor.close()
    finally:
        sub_cursor.close()

def format_json_response(row_headers, rows):
    json_data = []
    for r in rows:
        json_data.append(dict(zip(row_headers, r)))

    return jsonify(json_data)

if __name__ == '__main__':
    app.run()


#todo make getBookByISBN