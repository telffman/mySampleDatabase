import json
import psycopg2
import random
import base64

secrets = json.load(open('secrets.json'))

host = secrets["HOST"]
database = secrets["DATABASE"]
user = secrets["USERNAME"]
password = secrets["PASSWORD"]

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

cursor = conn.cursor()
