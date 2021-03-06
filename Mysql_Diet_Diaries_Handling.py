from Machine_Learning import get_last_record, append_new_rows, train_model_async
from Main import samples_mutex
from Mysql_Connection_General import *
from Macros import *

# ======================================================================================================================
# check_diet_diary QUERY

def check_diet_diary_query(cursor, diet_diary_name, username):
    found = False
    user_id = None

    checking_query = f"SELECT {users_table_mysql}.{id_field_mysql}, {diet_diary_name_field_mysql}" \
                     f" FROM {users_table_mysql} LEFT JOIN {diet_diaries_table_mysql}" \
                     f" ON {users_table_mysql}.{id_field_mysql} = {diet_diaries_table_mysql}.{user_id_field_mysql}" \
                     f" WHERE {username_field_mysql} = %s"
    val = (username,)

    error, result = mysql_getting_action(cursor, checking_query, val, False)
    error = error or result is None
    if not error:
        for record in result:
            user_id = record[f"{id_field_mysql}"]
            if record[diet_diary_name_field_mysql] == diet_diary_name:
                found = True
                break

    return user_id, found, error

def check_diet_diary(diet_diary_name, username):
    conn, cursor, error = get_mysql_cursor()
    record = None
    found = False
    if not error:
        record, found, error = check_diet_diary_query(cursor, diet_diary_name, username)
    close_connection(conn, cursor)
    return record, found, error

# ======================================================================================================================
# insert_diet_diary QUERY

def insert_main_diet_diary_query(cursor, diet_diary_name, user_id):
    query = f"INSERT INTO {diet_diaries_table_mysql}" \
            f" ({diet_diary_name_field_mysql},{user_id_field_mysql}) VALUES (%s,%s)"
    val = (diet_diary_name, user_id)
    cursor.execute(query, val)

    return cursor.lastrowid

def insert_diet_diary_meal_query(cursor, diet_diary_id, meal_id):
    query = f"INSERT INTO {diet_diary_meals_table_mysql}" \
            f" ({diet_diary_id_field_mysql},{meal_id_field_mysql}) VALUES (%s,%s)"
    val = (diet_diary_id, meal_id)
    cursor.execute(query, val)

    return cursor.lastrowid

def insert_meal_dish_query(cursor, meal_public_id, dishes, dish_name):
    percent = dishes[dish_name]

    query = f"INSERT INTO {meal_dishes_table_mysql}" \
            f" ({meal_public_id_field_mysql},{dish_id_field_mysql},{dish_percent_field_mysql})" \
            f" SELECT %s,{dishes_table_mysql}.{id_field_mysql},%s" \
            f" FROM {dishes_table_mysql} WHERE {dish_name_field_mysql} = %s"
    val = (meal_public_id, percent, dish_name)

    cursor.execute(query, val)
    return cursor.rowcount == 0

def insert_meal_ingredient_query(cursor, meal_public_id, ingredients, ingredient_name):
    amount = ingredients[ingredient_name]

    query = f"INSERT INTO {meal_ingredients_table_mysql}" \
            f" ({meal_public_id_field_mysql},{ingredient_id_field_mysql},{ingredient_amount_field_mysql})" \
            f" SELECT %s,{food_ingredients_table_mysql}.{id_field_mysql},%s" \
            f" FROM {food_ingredients_table_mysql} WHERE {ingredient_name_field_mysql} = %s"
    val = (meal_public_id, amount, ingredient_name)

    cursor.execute(query, val)
    return cursor.rowcount == 0

def insert_diet_diary_transaction_func(cursor, args):
    user_id = args[0]
    diet_diary_name = args[1]
    meals_dict = args[2]

    with samples_mutex:
        error, last_records, columns_dict, columns = get_last_record(cursor, user_id)
        all_dishes = set()
        all_ingredients = set()

        if error:
            raise ValueError()

        diet_diary_id = insert_main_diet_diary_query(cursor, diet_diary_name, user_id)
        for meal_id in meals_dict:
            meal_public_id = insert_diet_diary_meal_query(cursor, diet_diary_id, meal_id)
            dishes, ingredients = meals_dict[meal_id]
            for dish_name in dishes:
                if insert_meal_dish_query(cursor, meal_public_id, dishes, dish_name):
                    raise ValueError()
            for ingredient_name in ingredients:
                if insert_meal_ingredient_query(cursor, meal_public_id, ingredients, ingredient_name):
                    raise ValueError()
            all_dishes.update(dishes)
            all_ingredients.update(ingredients)

        if append_new_rows(cursor, last_records, columns_dict, columns, all_ingredients, all_dishes):
            raise ValueError()

    # train model in separated thread if mutex is available and return
    train_model_async()

def insert_diet_diary_query(conn, cursor, user_id, diet_diary_name, meals_dict):
    return transaction_execute(conn, cursor, insert_diet_diary_transaction_func,
                               (user_id, diet_diary_name, meals_dict))

def check_dish_params(dish):
    return isinstance(dish, dict) and dish_name_field_param in dish and \
           dish_percent_field_param in dish and len(dish) == 2

def check_ingredient_params(ingredient):
    return isinstance(ingredient, dict) and ingredient_name_field_param in ingredient and \
           ingredient_amount_field_param in ingredient and len(ingredient) == 2

def check_meal_params(meal):
    return isinstance(meal, dict) and meal_id_field_param in meal and \
           dishes_field_param in meal and ingredients_field_param in meal and len(meal) == 3

def get_meal_dishes(dishes):
    error = not isinstance(dishes, list)
    dishes_dict = {}

    if not error:
        for dish in dishes:
            if not check_dish_params(dish):
                error = True
                break
            percent = dish[dish_percent_field_param]
            dish_name = dish[dish_name_field_param]
            if dish_name in dishes_dict:
                percent += dishes_dict[dish_name]
            dishes_dict[dish_name] = percent

    return error, dishes_dict


def get_meal_ingredients(ingredients):
    error = not isinstance(ingredients, list)
    ingredients_dict = {}

    if not error:
        for ingredient in ingredients:
            if not check_ingredient_params(ingredient):
                error = True
                break
            amount = ingredient[ingredient_amount_field_param]
            ingredient_name = ingredient[ingredient_name_field_param]
            if ingredient_name in ingredients_dict:
                amount += ingredients_dict[ingredient_name]
            ingredients_dict[ingredient_name] = amount

    return error, ingredients_dict

def fill_single_meal(meals_dict, meal):
    dishes = None
    ingredients = None
    meal_id = None
    error = not check_meal_params(meal)

    if not error:
        meal_id = meal[meal_id_field_param]
        error = meal_id in meals_dict
    if not error:
        error, dishes = get_meal_dishes(meal[dishes_field_param])
    if not error:
        error, ingredients = get_meal_ingredients(meal[ingredients_field_param])
    if not error:
        meals_dict[meal_id] = (dishes, ingredients)

    return error, meals_dict


def fill_meals_dict(meals):
    error = not isinstance(meals, list)
    meals_dict = {}

    if not error:
        for meal in meals:
            error, meals_dict = fill_single_meal(meals_dict, meal)
            if error:
                break

    return error, meals_dict

def insert_diet_diary(user_id, diet_diary_name, meals):
    conn, cursor, error = get_mysql_cursor()
    meals_dict = None

    if not error:
        error, meals_dict = fill_meals_dict(meals)
    if not error:
        error = insert_diet_diary_query(conn, cursor, user_id, diet_diary_name, meals_dict)

    close_connection(conn, cursor)
    return error


# ======================================================================================================================
# get_diet_diary QUERY

def update_meal_dishes(dishes, meal_id, dish_name, percent):
    meal_dishes = []
    if meal_id in dishes:
        meal_dishes = dishes[meal_id]
    meal_dishes.append({f"{dish_name_field_param}": dish_name,
                        f"{dish_percent_field_param}": percent})
    dishes[meal_id] = meal_dishes
    return dishes

def update_meal_info(meals_info, meal_id, fat, carb, fiber, protein):
    total_fat = fat
    total_carb = carb
    total_fiber = fiber
    total_protein = protein
    if meal_id in meals_info:
        total_fat += meals_info[meal_id][0]
        total_carb += meals_info[meal_id][1]
        total_fiber += meals_info[meal_id][2]
        total_protein += meals_info[meal_id][3]
    meals_info[meal_id] = (total_fat, total_carb, total_fiber, total_protein)
    return meals_info

def fill_meal_dishes_by_records(records, meals_info):
    dishes = {}
    for record in records:
        meal_id = record[meal_id_field_mysql]
        meals_info = update_meal_info(meals_info, meal_id, record[calc_prefix(fat_field_mysql)],
                                      record[calc_prefix(carb_field_mysql)],
                                      record[calc_prefix(fiber_field_mysql)],
                                      record[calc_prefix(protein_field_mysql)])
        dishes = update_meal_dishes(dishes, meal_id, record[dish_name_field_mysql], record[dish_percent_field_mysql])
    return meals_info, dishes

def calc_prefix(string):
    return f"calc_{string}"

def get_diet_diary_dishes_query(cursor, diet_diary_name, username, meals_info):
    dishes = {}

    query = f"SELECT {meal_id_field_mysql}," \
            f" {dishes_table_mysql}.{dish_name_field_mysql} AS {dish_name_field_mysql}," \
            f" {dish_percent_field_mysql}," \
            f" SUM({fat_field_mysql}*{ingredient_amount_field_mysql}*{dish_percent_field_mysql}/100) AS" \
            f" {calc_prefix(fat_field_mysql)}," \
            f" SUM({carb_field_mysql}*{ingredient_amount_field_mysql}*{dish_percent_field_mysql}/100) AS" \
            f" {calc_prefix(carb_field_mysql)}," \
            f" SUM({fiber_field_mysql}*{ingredient_amount_field_mysql}*{dish_percent_field_mysql}/100) AS" \
            f" {calc_prefix(fiber_field_mysql)}," \
            f" SUM({protein_field_mysql}*{ingredient_amount_field_mysql}*{dish_percent_field_mysql}/100) AS" \
            f" {calc_prefix(protein_field_mysql)}" \
            f" FROM {diet_diaries_table_mysql} JOIN {diet_diary_meals_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
            f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}" \
            f" JOIN {meal_dishes_table_mysql}" \
            f" ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
            f" {meal_dishes_table_mysql}.{meal_public_id_field_mysql}" \
            f" JOIN {dishes_table_mysql}" \
            f" ON {dishes_table_mysql}.{id_field_mysql} = {meal_dishes_table_mysql}.{dish_id_field_mysql}" \
            f" JOIN {dish_ingredients_table_mysql}" \
            f" ON {meal_dishes_table_mysql}.{dish_id_field_mysql} =" \
            f" {dish_ingredients_table_mysql}.{dish_id_field_mysql}" \
            f" JOIN {food_ingredients_table_mysql}" \
            f" ON {dish_ingredients_table_mysql}.{ingredient_id_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{id_field_mysql}" \
            f" JOIN {users_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{user_id_field_mysql} = {users_table_mysql}.{id_field_mysql}" \
            f" WHERE {diet_diary_name_field_mysql} = %s AND {username_field_mysql} = %s" \
            f" GROUP BY {meal_id_field_mysql}, {dish_name_field_mysql}"
    val = (diet_diary_name, username)
    error, result = mysql_getting_action(cursor, query, val, False)

    if not error and result:
        meals_info, dishes = fill_meal_dishes_by_records(result, meals_info)

    return error, meals_info, dishes

def update_meal_ingredients(ingredients, meal_id, ingredient_name, is_liquid, amount):
    meal_ingredients = []
    if meal_id in ingredients:
        meal_ingredients = ingredients[meal_id]
    meal_ingredients.append({f"{ingredient_name_field_param}": ingredient_name,
                             f"{is_liquid_field_param}": is_liquid == 1,
                             f"{ingredient_amount_field_param}": amount})
    ingredients[meal_id] = meal_ingredients
    return ingredients

def fill_meal_ingredients_by_records(records, meals_info):
    ingredients = {}
    for record in records:
        meal_id = record[meal_id_field_mysql]
        meals_info = update_meal_info(meals_info, meal_id, record[calc_prefix(fat_field_mysql)],
                                      record[calc_prefix(carb_field_mysql)],
                                      record[calc_prefix(fiber_field_mysql)],
                                      record[calc_prefix(protein_field_mysql)])
        ingredients = update_meal_ingredients(ingredients, meal_id, record[ingredient_name_field_mysql],
                                              record[is_liquid_field_mysql], record[ingredient_amount_field_mysql])
    return meals_info, ingredients

def get_diet_diary_ingredients_query(cursor, diet_diary_name, username, meals_info):
    ingredients = {}

    query = f"SELECT {meal_id_field_mysql}," \
            f" {food_ingredients_table_mysql}.{ingredient_name_field_mysql} AS {ingredient_name_field_mysql}," \
            f" {ingredient_amount_field_mysql}, {is_liquid_field_mysql}," \
            f" SUM({fat_field_mysql}*{ingredient_amount_field_mysql}/100) AS" \
            f" {calc_prefix(fat_field_mysql)}," \
            f" SUM({carb_field_mysql}*{ingredient_amount_field_mysql}/100) AS" \
            f" {calc_prefix(carb_field_mysql)}," \
            f" SUM({fiber_field_mysql}*{ingredient_amount_field_mysql}/100) AS" \
            f" {calc_prefix(fiber_field_mysql)}," \
            f" SUM({protein_field_mysql}*{ingredient_amount_field_mysql}/100) AS" \
            f" {calc_prefix(protein_field_mysql)}" \
            f" FROM {diet_diaries_table_mysql}" \
            f" JOIN {diet_diary_meals_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
            f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}" \
            f" JOIN {meal_ingredients_table_mysql}" \
            f" ON {diet_diary_meals_table_mysql}.{id_field_mysql} =" \
            f" {meal_ingredients_table_mysql}.{meal_public_id_field_mysql}" \
            f" JOIN {food_ingredients_table_mysql}" \
            f" ON {meal_ingredients_table_mysql}.{ingredient_id_field_mysql} =" \
            f" {food_ingredients_table_mysql}.{id_field_mysql}" \
            f" JOIN {users_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{user_id_field_mysql} =" \
            f" {users_table_mysql}.{id_field_mysql}" \
            f" WHERE {diet_diary_name_field_mysql} = %s AND {username_field_mysql} = %s" \
            f" GROUP BY {meal_id_field_mysql}, {ingredient_name_field_mysql}"
    val = (diet_diary_name, username)
    error, result = mysql_getting_action(cursor, query, val, False)

    if not error and result:
        meals_info, ingredients = fill_meal_ingredients_by_records(result, meals_info)

    return error, meals_info, ingredients

def make_diet_diary_dict(meals_info, dishes, ingredients, diet_diary_name):
    meals = []
    for meal_id in sorted(meals_info):
        curr_info = meals_info[meal_id]
        curr_dishes = dishes[meal_id] if meal_id in dishes else []
        curr_ingredients = ingredients[meal_id] if meal_id in ingredients else []
        meals.append({f"{meal_id_field_param}": meal_id,
                      f"{dishes_field_param}": curr_dishes,
                      f"{ingredients_field_param}": curr_ingredients,
                      f"{fat_field_param}": curr_info[0],
                      f"{carb_field_param}": curr_info[1],
                      f"{fiber_field_param}": curr_info[2],
                      f"{protein_field_param}": curr_info[3]})
    return {f"{diet_diary_name_field_param}": diet_diary_name,
            f"{meals_field_param}": meals}

def get_diet_diary_query(cursor, diet_diary_name, username):
    meals_info = {}
    ingredients = None
    result = None
    found = False

    error, meals_info, dishes = \
        get_diet_diary_dishes_query(cursor, diet_diary_name, username, meals_info)

    if not error:
        error, meals_info, ingredients = \
            get_diet_diary_ingredients_query(cursor, diet_diary_name, username, meals_info)

    if not error:
        found = len(meals_info) > 0
        result = make_diet_diary_dict(meals_info, dishes, ingredients, diet_diary_name)

    return error, found, result

def get_diet_diary(diet_diary_name, username):
    result = None
    found = False
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, found, result = get_diet_diary_query(cursor, diet_diary_name, username)
    close_connection(conn, cursor)
    return error, found, result

# ======================================================================================================================
# get_diet_diaries QUERY

def make_diet_diaries_dict(records, diet_diaries):
    for record in records:
        diet_diary_name = record[diet_diary_name_field_mysql]
        if diet_diary_name:
            diet_diaries.append({f"{diet_diary_name_field_param}": diet_diary_name})
    return {f"{diet_diaries_field_param}": diet_diaries}

def get_diet_diaries_query(cursor, username):
    diet_diaries = []

    query = f"SELECT {users_table_mysql}.{id_field_mysql}, {diet_diary_name_field_mysql}" \
            f" FROM {users_table_mysql} JOIN {diet_diaries_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{user_id_field_mysql} = {users_table_mysql}.{id_field_mysql}" \
            f" WHERE {username_field_mysql} = %s"
    val = (username,)

    error, result = mysql_getting_action(cursor, query, val, False)
    if not error and result is not None:
        result = make_diet_diaries_dict(result, diet_diaries)
    else:
        error = True

    return error, result

def get_diet_diaries_names(username):
    result = None
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error, result = get_diet_diaries_query(cursor, username)
    close_connection(conn, cursor)
    return error, result

# ======================================================================================================================
# delete_diet_diary QUERY

def delete_diet_diary_main(cursor, diet_diary_name, user_id, all_diaries):
    query = f"DELETE FROM {diet_diaries_table_mysql}" \
            f" WHERE {user_id_field_mysql} = %s"
    val = (user_id,)
    if not all_diaries:
        query += f" AND {diet_diary_name_field_mysql} = %s"
        val += (diet_diary_name,)
    cursor.execute(query, val)

def meals_join_diaries(all_diaries):
    query = f"JOIN {diet_diaries_table_mysql}" \
            f" ON {diet_diaries_table_mysql}.{id_field_mysql} =" \
            f" {diet_diary_meals_table_mysql}.{diet_diary_id_field_mysql}" \
            f" WHERE {user_id_field_mysql} = %s"
    if not all_diaries:
        query += f" AND {diet_diary_name_field_mysql} = %s"
    return query

def delete_meal_component(cursor, diet_diary_name, user_id, table_name, all_diaries):
    query = f"DELETE {table_name} FROM {table_name}" \
            f" JOIN {diet_diary_meals_table_mysql}" \
            f" ON {table_name}.{meal_public_id_field_mysql} =" \
            f" {diet_diary_meals_table_mysql}.{id_field_mysql} " + meals_join_diaries(all_diaries)

    val = (user_id,)
    if not all_diaries:
        val += (diet_diary_name,)
    cursor.execute(query, val)

def delete_meal_dishes(cursor, diet_diary_name, user_id, all_diaries):
    delete_meal_component(cursor, diet_diary_name, user_id, meal_dishes_table_mysql, all_diaries)

def delete_meal_ingredients(cursor, diet_diary_name, user_id, all_diaries):
    delete_meal_component(cursor, diet_diary_name, user_id, meal_ingredients_table_mysql, all_diaries)

def delete_meals(cursor, diet_diary_name, user_id, all_diaries):
    query = f"DELETE {diet_diary_meals_table_mysql}" \
            f" FROM {diet_diary_meals_table_mysql} " + meals_join_diaries(all_diaries)

    val = (user_id,)
    if not all_diaries:
        val += (diet_diary_name,)
    cursor.execute(query, val)

def delete_diet_diary_transaction_func(cursor, args):
    diet_diary_name = args[0]
    user_id = args[1]
    all_diaries = args[2]

    delete_meal_dishes(cursor, diet_diary_name, user_id, all_diaries)
    delete_meal_ingredients(cursor, diet_diary_name, user_id, all_diaries)
    delete_meals(cursor, diet_diary_name, user_id, all_diaries)
    delete_diet_diary_main(cursor, diet_diary_name, user_id, all_diaries)

def delete_diet_diary_query(conn, cursor, diet_diary_name, user_id, all_diaries):
    return transaction_execute(conn, cursor, delete_diet_diary_transaction_func,
                               (diet_diary_name, user_id, all_diaries))

def delete_diet_diary(diet_diary_name, user_id):
    conn, cursor, error = get_mysql_cursor()
    if not error:
        error = delete_diet_diary_query(conn, cursor, diet_diary_name, user_id, False)
    close_connection(conn, cursor)
    return error

# ======================================================================================================================
# update_diet_diary QUERY

def update_diet_diary_transaction_func(cursor, args):
    prev_diet_diary_name = args[0]
    diet_diary_name = args[1]
    user_id = args[2]
    meals_dict = args[3]

    delete_diet_diary_transaction_func(cursor, (prev_diet_diary_name, user_id, False))
    insert_diet_diary_transaction_func(cursor, (user_id, diet_diary_name, meals_dict))

def update_diet_diary_query(conn, cursor, prev_diet_diary_name, diet_diary_name, user_id, meals_dict):
    return transaction_execute(conn, cursor, update_diet_diary_transaction_func,
                               (prev_diet_diary_name, diet_diary_name, user_id, meals_dict))

def update_diet_diary(prev_diet_diary_name, user_id, diet_diary_name, meals):
    conn, cursor, error = get_mysql_cursor()
    meals_dict = {}
    if not error:
        error, meals_dict = fill_meals_dict(meals)
    if not error:
        error = update_diet_diary_query(conn, cursor, prev_diet_diary_name, diet_diary_name, user_id, meals_dict)
    close_connection(conn, cursor)
    return error
