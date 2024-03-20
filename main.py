import json
import pyodbc
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

host = secrets["host"]
database = secrets["database"]
user = secrets["user"]
password = secrets["password"]

conn = pyodbc.connect (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={secrets["host"]};'
    f'DATABASE={secrets["database"]};'
    f'UID={secrets["user"]};'
    f'PWD={secrets["password"]}'
)
cursor = conn.cursor()

insert_query = 'INSERT INTO companies (Ranking, CompanyName, Industry, Revenue, RevenueGrowth, Employees, Headquarters) VALUES (?, ?, ?, ?, ?, ?, ?)'


for row in rows:
    cursor.execute(insert_query, tuple(row))

# Commit changes
conn.commit()

# Close the connection
cursor.close()
conn.close()


