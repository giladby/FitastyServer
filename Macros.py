# Mysql General Macros :
#mysql_host = "fitasty-db.cc4qtocqbg7k.us-east-2.rds.amazonaws.com"
mysql_host = "127.0.0.1"
#mysql_user = "admin"
mysql_user = "root"
#mysql_password = "epsilonEP2"
mysql_password = "123456"
#mysql_database = "fitasty"
mysql_database = "fitasty_demo"

name_exist_field_param = 'name_exist'
found_field_param = 'found'

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

# Mysql :
username_field_mysql = 'username'
id_field_mysql = 'id'
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
is_vegan_field_param = 'is_vegan'
is_vegetarian_field_param = 'is_vegetarian'
is_gluten_free_field_param = 'is_gluten_free'
is_lactose_free_field_param = 'is_lactose_free'
max_fat_field_param = 'max_fat'
max_carb_field_param = 'max_carb'
max_fiber_field_param = 'max_fiber'
max_protein_field_param = 'max_protein'
min_fat_field_param = 'min_fat'
min_carb_field_param = 'min_carb'
min_fiber_field_param = 'min_fiber'
min_protein_field_param = 'min_protein'
serving_size_field_param = 'serving'
include_dish_field_param = 'include_dishes'
include_ingredient_field_param = 'include_ingredients'
ingredients_field_param = 'ingredients'

# Mysql :
ingredient_name_field_mysql = 'ingredient_name'
is_liquid_field_mysql = 'liquid'
fat_field_mysql = 'fat'
carb_field_mysql = 'carb'
fiber_field_mysql = 'fiber'
protein_field_mysql = 'protein'
is_vegan_field_mysql = 'vegan'
is_vegetarian_field_mysql = 'vegetarian'
is_gluten_free_field_mysql = 'gluten_free'
is_lactose_free_field_mysql = 'lactose_free'
serving_size_field_mysql = 'serving'
food_ingredients_table_mysql = 'food_ingredients'

# Dishes Macros:
# Params:
# ingredients_field_param = 'ingredients'
# ingredient_name_field_mysql = 'ingredient_name'
ingredient_amount_field_param = 'amount'
dishes_field_param = 'dishes'
dish_name_field_param = 'dish_name'
dish_percent_field_param = 'percent'

# Mysql :
dish_name_field_mysql = 'dish_name'
dishes_table_mysql = 'dishes'

# dish_name_field_mysql = 'dish_name'
# ingredient_name_field_mysql = 'ingredient_name'
ingredient_amount_field_mysql = 'ingredient_amount'
dish_ingredients_table_mysql = 'dish_ingredients'

# Diet Diaries Macros:
# Params:
diet_diary_name_field_param = 'diet_diary_name'
prev_diet_diary_name_field_param = 'prev_diet_diary_name'
meals_field_param = 'meals'
meal_id_field_param = 'meal_id'
# dishes_field_param = 'dishes'
# dish_name_field_param = 'dish_name'
# dish_percent_field_param = 'percent'
# ingredients_field_param = 'ingredients'
# ingredient_name_field_mysql = 'ingredient_name'
# ingredient_amount_field_param = 'amount'
# fat_field_param = 'fat'
# carb_field_param = 'carb'
# fiber_field_param = 'fiber'
# protein_field_param = 'protein'
diet_diaries_field_param = 'diet_diaries'

# Mysql :
diet_diary_id_field_mysql = 'diet_diary_id'
diet_diary_name_field_mysql = 'diet_diary_name'
id_owner_field_mysql = 'user_id'
diet_diaries_table_mysql = 'diet_diaries'

meal_public_id_field_mysql = 'meal_public_id'
meal_id_field_mysql = 'meal_id'
# diet_diary_id_field_mysql = 'diet_diary_id'
diet_diary_meals_table_mysql = 'diet_diary_meals'

# meal_public_id_field_mysql = 'meal_public_id'
# dish_name_field_mysql = 'dish_name'
dish_percent_field_mysql = 'dish_percent'
meal_dishes_table_mysql = 'meal_dishes'

# meal_public_id_field_mysql = 'meal_public_id'
# ingredient_name_field_mysql = 'ingredient_name'
# ingredient_amount_field_mysql = 'ingredient_amount'
meal_ingredients_table_mysql = 'meal_ingredients'
