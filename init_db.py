# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
# cursor.execute("drop table if exists Users;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(50) DEFAULT NULL,
      email       VARCHAR(50) DEFAULT NULL,
      comment     TEXT DEFAULT NULL,
      avatar      TEXT DEFAULT NULL,
      school      VARCHAR(50) DEFAULT NULL,
      degree      VARCHAR(50) DEFAULT NULL,
      major       VARCHAR(50) DEFAULT NULL,
      date        VARCHAR(50) DEFAULT NULL,
      title       VARCHAR(50) DEFAULT NULL,
      description TEXT DEFAULT NULL,
      link        VARCHAR(50) DEFAULT NULL,
      image_src   VARCHAR(50) DEFAULT NULL,
      team        TEXT DEFAULT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Users table already exists. Not recreating it.")

# Insert Records

query = "insert into Users (name, email, comment, avatar, school, degree, major, date, title, description, link, image_src, team, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
values = [
  ('David Bian', 'jibian@ucsd.edu', 'Great Job!',
  'https://tinyurl.com/amcxb3j2', 
  'UCSD', 'B.S.', 'ECE', 'FALL 2021', 
  'look at yourself', 'A smart mirror that can listen to your commends', 
  'no mirror link', 'no mirror picture', 'api_link: 164.90.144.97, 143.198.98.101',
  '2021-05-16 12:00:00')
]
cursor.executemany(query, values)
db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()