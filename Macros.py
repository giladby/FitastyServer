# Mysql General Macros :
#mysql_host = "fitasty-db.cc4qtocqbg7k.us-east-2.rds.amazonaws.com"
mysql_host = "127.0.0.1"
#mysql_user = "admin"
mysql_user = "root"
#mysql_password = "epsilonEP2"
mysql_password = "123456"
#mysql_database = "fitasty"
mysql_database = "fitasty_demo"

samples_file_path = "samples.csv"

name_exist_field_param = 'name_exist'
found_field_param = 'found'

# Continents and Countries Macros :
# Params :
countries_field_param = 'countries'

# Mysql :
id_field_mysql = 'id'
continent_id_field_mysql = 'continent_id'
country_field_mysql = 'country'
countries_table_mysql = 'countries'
continents_table_mysql = 'continents'

# Users Macros :
# Params :
username_field_param = 'username'
prev_username_field_param = 'prev_username'
password_field_param = 'password'
age_field_param = 'age'
is_male_field_param = 'is_male'
height_field_param = 'height'
weight_field_param = 'weight'
activity_factor_field_param = 'activity_factor'
diet_type_field_param = 'diet_type'
diet_type_carb_field_param = 'carb'
diet_type_protein_field_param = 'protein'
diet_type_fat_field_param = 'fat'
weight_goal_field_param = 'weight_goal'
country_field_param = 'country_name'
is_vegan_field_param = 'is_vegan'
is_vegetarian_field_param = 'is_vegetarian'
is_gluten_free_field_param = 'is_gluten_free'
is_lactose_free_field_param = 'is_lactose_free'

# Mysql :
username_field_mysql = 'username'
password_field_mysql = 'password'
age_field_mysql = 'age'
is_male_field_mysql = 'is_male'
height_field_mysql = 'height'
weight_field_mysql = 'weight'
activity_factor_field_mysql = 'activity_factor'
diet_type_fat_field_mysql = 'diet_type_fat'
diet_type_carb_field_mysql = 'diet_type_carb'
diet_type_protein_field_mysql = 'diet_type_protein'
weight_goal_field_mysql = 'weight_goal'
is_vegan_field_mysql = 'vegan'
is_vegetarian_field_mysql = 'vegetarian'
is_gluten_free_field_mysql = 'gluten_free'
is_lactose_free_field_mysql = 'lactose_free'
country_id_field_mysql = 'country_id'
users_table_mysql = 'users'

# Food Macros:
# Params:
ingredient_name_field_param = 'ingredient_name'
name_begin_field_param = 'name_begin'
is_liquid_field_param = 'is_liquid'
fat_field_param = 'fat'
carb_field_param = 'carb'
fiber_field_param = 'fiber'
protein_field_param = 'protein'
serving_size_field_param = 'serving'
include_dish_field_param = 'include_dishes'
include_ingredient_field_param = 'include_ingredients'
ingredients_field_param = 'ingredients'
min_percent_field_param = 'min_percent'
max_percent_field_param = 'max_percent'

# Mysql :
ingredient_id_field_mysql = 'ingredient_id'
ingredient_name_field_mysql = 'ingredient_name'
is_liquid_field_mysql = 'liquid'
fat_field_mysql = 'fat'
carb_field_mysql = 'carb'
fiber_field_mysql = 'fiber'
protein_field_mysql = 'protein'
serving_size_field_mysql = 'serving'
food_ingredients_table_mysql = 'food_ingredients'

# Dishes Macros:
# Params:
ingredient_amount_field_param = 'amount'
dishes_field_param = 'dishes'
dish_name_field_param = 'dish_name'
dish_percent_field_param = 'percent'

# Mysql :
dish_id_field_mysql = 'dish_id'
dish_name_field_mysql = 'dish_name'
dishes_table_mysql = 'dishes'

ingredient_amount_field_mysql = 'ingredient_amount'
dish_ingredients_table_mysql = 'dish_ingredients'

# Diet Diaries Macros:
# Params:
diet_diary_name_field_param = 'diet_diary_name'
prev_diet_diary_name_field_param = 'prev_diet_diary_name'
meals_field_param = 'meals'
meal_id_field_param = 'meal_id'
diet_diaries_field_param = 'diet_diaries'

# Mysql :
user_id_field_mysql = 'user_id'
diet_diary_id_field_mysql = 'diet_diary_id'
diet_diary_name_field_mysql = 'diet_diary_name'
diet_diaries_table_mysql = 'diet_diaries'

meal_public_id_field_mysql = 'meal_public_id'
meal_id_field_mysql = 'meal_id'
diet_diary_meals_table_mysql = 'diet_diary_meals'

dish_percent_field_mysql = 'dish_percent'
meal_dishes_table_mysql = 'meal_dishes'

meal_ingredients_table_mysql = 'meal_ingredients'
