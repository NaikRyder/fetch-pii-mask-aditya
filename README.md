# fetch-pii-mask-aditya

### Steps to run the program (Run in terminal):
    1. pip install -r requirements.txt
    2. docker compose up
    3. python3 main.py

### Questions:
    1. How would you deploy this application in production?
        a. We can deploy the application  as a .zip package file on the servers.
        b. We can then unzip the package, run main.py file on the server.

    2. What other components would you want to add to make this production ready?
        a. We can add some more exceptions to catch enexpected scenarios.
        b. We can also store credentials and configurations in different files and mask them
        c. We can segregate the code in app.py into different files like db.py and processing.py

    3. How can this application scale with a growing dataset
        a. We can poll the queue to capture new incoming data in real-time
        b. We can have multiple servers for the database and implement techniques like sharding and clustering to scale out the database.
        c. We can also migrate the database on cloud such as Amazon Aurora to auto scale the database.

    4. How can PII be recovered later on?
        a. I have used SHA256 to mask PII which is irreversible
        b. For reversible masking, we can use ciphertext that has a key to reverse the data.

    5. What are the assumptions you made?
        a. New data is not continuously coming into the system (Batch processing).