import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="sql8.freemysqlhosting.net",  # Replace 'localhost' with your database host
    user="sql8682576",  # Replace 'your_username' with your database username
    password="KfgvCyW3yN",  # Replace 'your_password' with your database password
    database="sql8682576"  # Replace 'your_database' with your database name
)

# Check if the connection is successful
if connection.is_connected():
    print("Connected to MySQL database")

    # Perform database operations here

    
else:
    print("Failed to connect to MySQL database")
