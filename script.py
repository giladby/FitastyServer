# libraries
import urllib.request
import csv

import mysql.connector


class MySQLConnectionFields:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

def get_db_fields():
    host = "127.0.0.1"
    user = "root"
    password = "123456"
    database = "fitasty_demo"
    return MySQLConnectionFields(host, user, password, database)

def get_mysql_connection(mysql_fields):
    return mysql.connector.connect(
        host=mysql_fields.host,
        user=mysql_fields.user,
        passwd=mysql_fields.password,
        database=mysql_fields.database)

def close_connection(conn, cursor):
    if conn is not None:
        conn.close()
    if cursor is not None:
        cursor.close()

def get_mysql_cursor():
    conn = None
    cursor = None
    error = False
    try:
        db_fields = get_db_fields()
        conn = get_mysql_connection(db_fields)
        cursor = conn.cursor()
    except:
       error = True
    return conn, cursor, error

def insert_foods_query(conn, cursor, foods_arr):
    error = False
    if cursor:
        try:
            query = f"INSERT IGNORE INTO food_ingredient (name, fat, carbs, fiber, protein) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(query, foods_arr)

            conn.commit()
        except:
            error = True
    return error

rowsString = []

urls = ["https://www.calorieking.com/us/en/foods/f/calories-in-fresh-fruits-apples-with-skin-raw/9PkqpzWLSwupYVk2vXG_pA",
        "https://www.calorieking.com/us/en/foods/f/calories-in-sugars-granulated-white-sugar/gqBMIR0gQj6_xXTVqdaavg",
        "https://www.calorieking.com/us/en/foods/f/calories-in-fresh-fruits-avocados-average-all-varieties-raw/zU9a9g9oQ5W3RHKaVFtG7A"]

# Fetching the html
for url in urls:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Chrome"})
    res = urllib.request.urlopen(req)

    all_str = res.read().decode("utf-8")
    parts = all_str.split("MuiTableRow-root jss382")
    food = all_str.split("How many calories in</span>")[1]
    food = food.split("</h1>")[0]
    fat = parts[1].split(
        "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[1]
    fat = fat.split("<")[0]
    carbs = parts[2].split(
        "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[1]
    carbs = carbs.split("<")[0]
    fiber = parts[3].split(
        "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
        1]
    fiber = fiber.split("<")[0]
    protein = parts[4].split(
        "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
        1]
    protein = protein.split("<")[0]
    rowsString.append((food, fat, carbs, fiber, protein))

conn, cursor, error = get_mysql_cursor()
result = None
if not error:
    error = insert_foods_query(conn, cursor, rowsString)
close_connection(conn, cursor)