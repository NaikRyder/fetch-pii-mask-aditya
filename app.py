import hashlib
import json
import subprocess
import psycopg2
from datetime import date

# Function to encode/ mask PII values
def hash_pii(val):
    return hashlib.sha256(val.encode()).hexdigest()


# Function to convert version to type integer
def int_version(ver):
    parts = ver.split('.')
    parts = [part.zfill(2) for part in parts]
    return int(''.join(parts))


# Function to convert json message object to array to enter in SQL query
def get_msg_val(msg):
    msg_body = json.loads(msg['Body'])

    user_id = msg_body['user_id']
    device_type = msg_body['device_type']

    # Masking IP
    masked_ip = hash_pii(msg_body['ip'])

    # Masking device_id
    masked_device_id = hash_pii(msg_body['device_id'])

    locale = msg_body['locale']

    # Converting version to integer
    app_version = int_version(msg_body['app_version'])

    # Getting current date
    create_date = date.today()

    # Storing the above formatted values into an array of objects
    vals = (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)

    return vals


# Function to extract message from queue
def get_msg_from_queue(comm):
    data = subprocess.run(comm, capture_output=True, text=True, shell=True, executable="/bin/bash")
    json_data = json.loads(data.stdout)
    return json_data['Messages']


# Function to insert formatted message into database
def insert_msg_into_db(messages, cur):
    for msg in messages:
        vals = get_msg_val(msg)
    cur.execute(
        "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, "
        "create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", vals)

    print("\nNew record in table:\n", vals)


# Function to get all records from user_logins table
def get_all_user_logins():
    cur.execute("select * from user_logins;")
    return cur.fetchall()


# Initializing db connection variable to None
conn = None

# Initializing connection cursor variable to None
cur = None

# Initializing bash command to get messages from local queue
comm = "awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue"

try:
    # Connecting to Postgres database by passing parameters
    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='localhost', port='5432')

    # Getting cursor value to traverse the database results
    cur = conn.cursor()

    # Execute query to return existing records in user login table
    res = get_all_user_logins()
    print("\nExisting table results:\n", res)

    # Get new message from queue
    messages = get_msg_from_queue(comm)

    # Insert new message into database
    insert_msg_into_db(messages, cur)

    # Committing the current transaction
    conn.commit()

except psycopg2.DatabaseError() as e:
    print("\nDatabase connection error: ", e)

# Execute query to return all records in user login table
res = get_all_user_logins()
print("\nUpdated table results:\n", res)

# Closing cursor so that it has no reference to existing connection
cur.close()

# Closing database connection
conn.close()
