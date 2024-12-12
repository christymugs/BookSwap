from kafka import KafkaConsumer
import mysql.connector
from mysql.connector import Error
import sys
import json


# Define your connection details
host = 'book-meta.ckxkonakdsgz.us-east-1.rds.amazonaws.com'  # e.g., 'mydbinstance.c1abcd2efghz.us-west-2.rds.amazonaws.com'
db_username = 'admin'
password = '#Cloud1234'

def consume_library_requests():
    try:
        # Establishing the connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=db_username,
            password=password
        )

        if connection.is_connected():
            print(f"Connected to MySQL database at {host}")
            consumer = KafkaConsumer(
                bootstrap_servers=boostrap_host_and_port,
                auto_offset_reset='latest',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            consumer.subscribe(topics=['library_requests'])
            print("subscribed to library topic")

            for req in consumer:
                request_msg = req.value

                #cursor
                cursor = connection.cursor()
                sql_statement = "INSERT INTO library_data.library_request (request_id, library, request_type, isbn, request_date, request_user) VALUES (%s, %s, %s, %s, %s, %s)"
                params = (request_msg.get('id'), request_msg.get('library'), request_msg.get('request_type'), request_msg.get('isbn'), request_msg.get('request_date'), request_msg.get('request_user'))
                cursor.execute(sql_statement, params)
                connection.commit()



    except Error as e:
        print(f"Error while consuming: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            consumer.close()
            print("Connection closed.")

if __name__ == "__main__":
    boostrap_host_and_port = sys.argv[1] + ":9092"
    mongo_host_and_port = sys.argv[2] + ":27017/"