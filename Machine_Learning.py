import os.path
from os import path
from Macros import *
from Mysql_Connection_General import *

def is_file_exist():
    return path.isfile(samples_file_path)

def write_records(mysql_records):
    # for record
    pass

def get_last_record(cursor, user_id):
    file_exist = is_file_exist()
    query = f"SELECT {user_id_field_mysql}, {id_field_mysql} as {ingredient_id_field_mysql}," \
            f" SUM({ingredient_amount_field_mysql}) as {ingredient_amount_field_mysql}" \
            f" FROM (SELECT {user_id_field_mysql}, {food_ingredients_table_mysql}.{id_field_mysql}," \
            f" SUM({dish_percent_field_mysql} * {ingredient_amount_field_mysql}) as {ingredient_amount_field_mysql}" \
            f" FROM {diet_diaries_table_mysql} JOIN {diet_diary_meals_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
            f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}" \
            f" JOIN {meal_dishes_table_mysql} ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
            f" {meal_dishes_table_mysql}.{meal_public_id_field_mysql}" \
            f" JOIN {dish_ingredients_table_mysql} ON {meal_dishes_table_mysql}.{dish_id_field_mysql} =" \
            f" {dish_ingredients_table_mysql}.{dish_id_field_mysql}" \
            f" JOIN {food_ingredients_table_mysql} ON {food_ingredients_table_mysql}.{id_field_mysql} =" \
            f" {dish_ingredients_table_mysql}.{ingredient_id_field_mysql}"
    if file_exist:
        query += f" WHERE user_id = %s"
    query += f" GROUP BY {food_ingredients_table_mysql}.{id_field_mysql}" \
             f" UNION" \
             f" SELECT {user_id_field_mysql}, {food_ingredients_table_mysql}.{id_field_mysql}," \
             f" SUM({ingredient_amount_field_mysql}) as {ingredient_amount_field_mysql}" \
             f" FROM {diet_diaries_table_mysql} JOIN {diet_diary_meals_table_mysql}" \
             f" ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
             f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}" \
             f" JOIN {meal_ingredients_table_mysql} ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
             f" {meal_ingredients_table_mysql}.{meal_public_id_field_mysql}" \
             f" JOIN {food_ingredients_table_mysql} ON {food_ingredients_table_mysql}.{id_field_mysql} =" \
             f" {meal_ingredients_table_mysql}.{ingredient_id_field_mysql}"
    if file_exist:
        query += f" WHERE user_id = %s"
    query += ") as unioned" \
             f" GROUP BY {id_field_mysql}"

    val = None
    if file_exist:
        val = (user_id, user_id)
    error, result = mysql_getting_action(cursor, query, val, False)

    if not error and not file_exist:
        error = write_records(result)

    return error, result
