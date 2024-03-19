import json
import psycopg2
import random
import base64
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

heading = soup.find(id="List_of_the_largest_public_/_publicly_traded_companies")
table = heading.find_next("table")

headers = [header.text.strip() for header in table.find_all('th')]

rows = []
for row in table.find_all('tr')[1:]:  # Exclude header row
    cols = [col.text.strip() for col in row.find_all(['td', 'th'])]
    rows.append(cols)

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

insert_query = 'INSERT INTO companies (Ranking, CompanyName, Industry, Revenue, Revenue_growth, Employees, Headquarters) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

for row in rows:
    cur.execute(insert_query, row)

# Commit changes
conn.commit()

# Close the connection
cur.close()
conn.close()


