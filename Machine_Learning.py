import pandas as pd

from ML_Model import train_model
from Utils import *
from Mysql_Connection_General import *
from threading import Thread

age_param = "age"
is_male_param = "is_male"
height_param = "height"
weight_param = "weight"
country_id_param = "country_id"
activity_factor_param = "activity_factor"
diet_type_param = "diet_type"
weight_goal_param = "weight_goal"
is_vegan_param = "is_vegan"
is_vegetarian_param = "is_vegetarian"
is_gluten_free_param = "is_gluten_free"
is_lactose_free_param = "is_lactose_free"
continent_id_param = "continent_id"

def get_activity_factor_num(activity_factor_value):
    activity_factor_dict = {}
    for i in range(5):
        activity_factor_dict[round(1.2 + i * 0.175, 3)] = i + 1
    return activity_factor_dict.get(activity_factor_value, -1)

def get_diet_type_num(diet_type_fat, diet_type_carb, diet_type_protein):
    return {(0.2, 0.35, 0.45): 1, (0.4, 0.3, 0.3): 2, (0.5, 0.2, 0.3): 3}.\
        get((diet_type_carb, diet_type_fat, diet_type_protein), -1)

def get_weight_goal_num(weight_goal_value):
    weight_goal_dict = {}
    for i in range(9):
        weight_goal_dict[-1 + (i * 0.25)] = i + 1
    return weight_goal_dict.get(weight_goal_value, -1)


def get_user_info(mysql_record):
    error = False
    user_info_dict = None

    weight_goal = get_weight_goal_num(mysql_record[weight_goal_field_mysql])
    diet_type = get_diet_type_num(mysql_record[diet_type_fat_field_mysql], mysql_record[diet_type_carb_field_mysql],
                                  mysql_record[diet_type_protein_field_mysql])
    activity_factor = get_activity_factor_num(mysql_record[activity_factor_field_mysql])

    if weight_goal == error_value or diet_type == error_value or activity_factor == error_value:
        error = True

    if not error:
        user_info_dict = {age_param: mysql_record[age_field_mysql],
                          is_male_param: mysql_record[is_male_field_mysql],
                          weight_param: mysql_record[weight_field_mysql],
                          height_param: mysql_record[height_field_mysql],
                          country_id_param: mysql_record[country_id_field_mysql],
                          activity_factor_param: activity_factor,
                          diet_type_param: diet_type,
                          weight_goal_param: weight_goal,
                          is_vegan_param: mysql_record[is_vegan_field_mysql],
                          is_vegetarian_param: mysql_record[is_vegetarian_field_mysql],
                          is_gluten_free_param: mysql_record[is_gluten_free_field_mysql],
                          is_lactose_free_param: mysql_record[is_lactose_free_field_mysql],
                          continent_id_param: mysql_record[continent_id_field_mysql]}
    return error, user_info_dict

def get_users_records(mysql_records):
    users_dict = {}
    error = False

    for record in mysql_records:
        ingredients_dict = {}
        error, user_info = get_user_info(record)

        if not error:
            id = record[id_field_mysql]
            if id in users_dict:
                _, ingredients_dict = users_dict[id]
            if record[ingredient_id_field_mysql] is not None:
                ingredients_dict[record[ingredient_id_field_mysql]] = record[total_ingredient_amount]
            users_dict[id] = (user_info, ingredients_dict)

    return error, users_dict

def append_to_columns(new_column, columns, columns_dict):
    index = len(columns)
    columns.append(new_column)
    columns_dict[new_column] = index

def append_some_to_columns(elements, columns, columns_dict):
    for element in elements:
        append_to_columns(element, columns, columns_dict)

def get_count_by_table(table_name, count_param, min_param):
    return f"SELECT '{table_name}_id', COUNT(*) as {count_param}," \
           f" MIN({id_field_mysql}) as {min_param} FROM {table_name}"

def get_counters(cursor):
    country_counter, continent_counter, ingredient_counter = [], [], []
    min_country, count_country, min_continent, count_continent, min_ingredient, count_ingredient = \
        -1, -1, -1, -1, -1, -1
    counters_dict = {f"{food_ingredients_table_mysql}_id": ingredient_counter,
                     f"{continents_table_mysql}_id": continent_counter,
                     f"{countries_table_mysql}_id": country_counter}
    count_param = "count"
    min_param = "min"

    query = f"{get_count_by_table(food_ingredients_table_mysql, count_param, min_param)}" \
            f" UNION {get_count_by_table(countries_table_mysql, count_param, min_param)}" \
            f" UNION {get_count_by_table(continents_table_mysql, count_param, min_param)}"
    error, result = mysql_get_data(cursor, query, False)

    if not error and result:
        for record in result:
            curr_counter_arr = counters_dict[record[f"{food_ingredients_table_mysql}_id"]]
            curr_counter_arr.append(record[f"{min_param}"])
            curr_counter_arr.append(record[f"{count_param}"])
        min_country, count_country, min_continent, count_continent, min_ingredient, count_ingredient = \
            country_counter[0], country_counter[1], continent_counter[0], continent_counter[1], ingredient_counter[0], \
            ingredient_counter[1]

    return error, min_country, count_country, min_continent, count_continent, min_ingredient, count_ingredient

def turn_to_negative(is_str):
    is_str.replace("is_","")
    return f"is_not_{is_str}"

def create_columns(cursor):
    columns = []
    columns_dict = {}
    error, min_country, count_country, min_continent, count_continent, min_ingredient, count_ingredient = \
        get_counters(cursor)

    if not error:
        append_some_to_columns([age_param, is_male_param, turn_to_negative(is_male_param), height_param, weight_param,
                                activity_factor_param, diet_type_param, weight_goal_param,
                                is_vegan_param, turn_to_negative(is_vegan_param),
                                is_vegetarian_param, turn_to_negative(is_vegetarian_param),
                                is_gluten_free_param, turn_to_negative(is_gluten_free_param),
                                is_lactose_free_param, turn_to_negative(is_lactose_free_param)], columns, columns_dict)
        for i in range(min_country, min_country + count_country):
            append_to_columns(f"country_{i}", columns, columns_dict)
        for i in range(min_continent, min_continent + count_continent):
            append_to_columns(f"continent_{i}", columns, columns_dict)
        for i in range(min_ingredient, min_ingredient + count_ingredient):
            append_to_columns(f"ingredient_{i}", columns, columns_dict)
        append_to_columns(f"{ingredient_label}", columns, columns_dict)

    return error, columns, columns_dict

def fill_param_or_negative(row, columns_dict, user_info, param):
    if user_info[param] == 1:
        row[columns_dict[param]] = 1
    else:
        row[columns_dict[turn_to_negative(param)]] = 1

def create_row_and_fill_info(columns_dict, user_info, columns):
    row = [0] * len(columns)
    regular_params = [age_param, height_param, weight_param, activity_factor_param, diet_type_param, weight_goal_param]
    negative_params = [is_male_field_mysql, is_gluten_free_param, is_vegan_param, is_vegetarian_param,
                       is_lactose_free_param]

    for param in regular_params:
        row[columns_dict[param]] = user_info[param]
    for param in negative_params:
        fill_param_or_negative(row, columns_dict, user_info, param)

    row[columns_dict[f"country_{user_info[country_id_param]}"]] = 1
    row[columns_dict[f"continent_{user_info[continent_id_param]}"]] = 1

    return row

def create_featured_row(columns_dict, user_info, ingredients_dict, columns):
    row = create_row_and_fill_info(columns_dict, user_info, columns)
    for ingredient in ingredients_dict:
        row[columns_dict[f"ingredient_{ingredient}"]] = ingredients_dict[ingredient]
    return row

def create_new_rows(columns_dict, user_info, ingredients_dict, columns, new_ingredients_records):
    new_rows = []
    featured_row = create_featured_row(columns_dict, user_info, ingredients_dict, columns)
    for record in new_ingredients_records:
        new_ingredient = record[id_field_mysql]
        new_row = featured_row.copy()
        new_row[columns_dict[f"{ingredient_label}"]] = new_ingredient
        new_rows.append(new_row)
    return new_rows

def fill_file_rows(rows, columns_dict, user_info, ingredients_dict, columns):
    default_row = create_row_and_fill_info(columns_dict, user_info, columns)
    for ingredient in ingredients_dict:
        row = default_row.copy()
        row[columns_dict[f"{ingredient_label}"]] = ingredient
        rows.append(row)

def write_records(users_records, columns, columns_dict):
    rows = [columns]
    for id in users_records:
        user_info, ingredients_dict = users_records[id]
        if len(ingredients_dict) == 0:
            continue
        fill_file_rows(rows, columns_dict, user_info, ingredients_dict, columns)

    create_path_if_needed(samples_file_path)
    return write_rows_to_file(rows, samples_file_path, True)

def get_select_line(dish_percent_addition):
    select_line = f"SELECT {users_table_mysql}.*," \
                  f" {countries_table_mysql}.{continent_id_field_mysql} as {continent_id_field_mysql}," \
                  f" {food_ingredients_table_mysql}.{id_field_mysql} as {ingredient_id_field_mysql}," \
                  f" SUM({dish_percent_addition}{ingredient_amount_field_mysql}) as {ingredient_amount_field_mysql}"
    return select_line

def get_inner_query_body(dishes_option, file_exist):
    dish_percent_addition = f"{dish_percent_field_mysql} * " if dishes_option else ""

    select_line = get_select_line(dish_percent_addition)

    query_body = f"FROM {users_table_mysql}" \
                 f" JOIN {countries_table_mysql} ON {users_table_mysql}.{country_id_field_mysql} =" \
                 f" {countries_table_mysql}.{id_field_mysql}" \
                 f" LEFT JOIN {diet_diaries_table_mysql} ON {users_table_mysql}.{id_field_mysql} =" \
                 f" {diet_diaries_table_mysql}.{user_id_field_mysql}" \
                 f" LEFT JOIN {diet_diary_meals_table_mysql} ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
                 f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}"

    if dishes_option:
        rest_body = f"LEFT JOIN {meal_dishes_table_mysql} ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
                    f" {meal_dishes_table_mysql}.{meal_public_id_field_mysql}" \
                    f" LEFT JOIN {dish_ingredients_table_mysql} ON {meal_dishes_table_mysql}.{dish_id_field_mysql} =" \
                    f" {dish_ingredients_table_mysql}.{dish_id_field_mysql}" \
                    f" LEFT JOIN {food_ingredients_table_mysql} ON {food_ingredients_table_mysql}.{id_field_mysql} =" \
                    f" {dish_ingredients_table_mysql}.{ingredient_id_field_mysql}"
    else:
        rest_body = f"LEFT JOIN {meal_ingredients_table_mysql} ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
                    f" {meal_ingredients_table_mysql}.{meal_public_id_field_mysql}" \
                    f" LEFT JOIN {food_ingredients_table_mysql} ON {food_ingredients_table_mysql}.{id_field_mysql} =" \
                    f" {meal_ingredients_table_mysql}.{ingredient_id_field_mysql}"
    rest_body += f" WHERE {users_table_mysql}.{id_field_mysql} = %s" if file_exist else ""
    rest_body += f" GROUP BY {id_field_mysql}, {food_ingredients_table_mysql}.{id_field_mysql}"

    return f"{select_line} {query_body} {rest_body}"

def get_last_record(cursor, user_id):
    file_exist = is_file_exist(samples_file_path)
    union_table = "unioned"
    val = None
    users_records = None
    columns = None
    columns_dict = None

    query = f"SELECT {union_table}.*, SUM({ingredient_amount_field_mysql}) as {total_ingredient_amount}" \
            f" FROM ({get_inner_query_body(True, file_exist)} UNION {get_inner_query_body(False, file_exist)})" \
            f" as {union_table} GROUP BY {id_field_mysql}, {ingredient_id_field_mysql}"

    if file_exist:
        val = (user_id, user_id)
    error, result = mysql_getting_action(cursor, query, val, False)

    if not error:
        error, users_records = get_users_records(result)

    if not error:
        error, columns, columns_dict = create_columns(cursor)

    if not error and not file_exist:
        error = write_records(users_records, columns, columns_dict)

    if not error:
        error = user_id not in users_records

    if not error:
        result = users_records[user_id]

    return error, result, columns_dict, columns

def get_new_ingredients_ids(cursor, ingredients, dishes):
    unioned_tuple = tuple(ingredients)
    if dishes:
        dishes = tuple(dishes)
        unioned_tuple = unioned_tuple + dishes if unioned_tuple else dishes

    union = " UNION " if dishes and ingredients else ""
    ingredient_select = f"SELECT {id_field_mysql} FROM {food_ingredients_table_mysql}" \
                        f" WHERE {ingredient_name_field_mysql}" \
                        f" IN ({get_prepared_string(len(ingredients) if ingredients else 0)})" if ingredients else ""
    dish_select = f"SELECT {ingredient_id_field_mysql} as {id_field_mysql} FROM {dishes_table_mysql}" \
                  f" JOIN {dish_ingredients_table_mysql}" \
                  f" ON {dishes_table_mysql}.{id_field_mysql} = {dish_ingredients_table_mysql}.{dish_id_field_mysql}" \
                  f" WHERE {dish_name_field_mysql} IN ({get_prepared_string(len(dishes) if dishes else 0)})"\
                  if dishes else ""

    query = f"{ingredient_select}{union}{dish_select}"
    print(query)
    print(unioned_tuple)
    return mysql_getting_action(cursor, query, unioned_tuple, False)

def append_new_rows(cursor, last_records, columns_dict, columns, ingredients, dishes):
    user_info, ingredients_dict = last_records
    error, new_ingredients_records = get_new_ingredients_ids(cursor, ingredients, dishes)

    if not error:
        new_rows = create_new_rows(columns_dict, user_info, ingredients_dict, columns, new_ingredients_records)
        error = write_rows_to_file(new_rows, samples_file_path, False)

    return error

def get_featured_row(cursor, user_id):
    featured_row = None
    error, last_records, columns_dict, columns = get_last_record(cursor, user_id)

    if not error:
        user_info, ingredients_dict = last_records
        featured_row = create_featured_row(columns_dict, user_info, ingredients_dict, columns)

    return error, featured_row

def add_new_ingredient_column(ingredient_id):
    error = False

    if is_file_exist(samples_file_path):
        try:
            df = pd.read_csv(samples_file_path)
            df.insert(len(df.columns) - 1, f"ingredient_{ingredient_id}", 0)
            df.to_csv(samples_file_path, index=False)
        except:
            error = True

    return error

def train_model_async():
    thread = Thread(target=train_model, args=(False, None))
    thread.start()

def get_model_accuracy(accuracy_percent):
    return train_model(True, accuracy_percent)