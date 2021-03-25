# Mysql General Macros :
#mysql_host = "fitasty-db.cc4qtocqbg7k.us-east-2.rds.amazonaws.com"
mysql_host = "127.0.0.1"
#mysql_user = "admin"
mysql_user = "root"
#mysql_password = "epsilonEP2"
mysql_password = "123456"
#mysql_database = "fitasty"
mysql_database = "fitasty_demo"


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
username_field_mysql_position = 0
password_field_mysql = 'password'
password_field_mysql_position = 1
age_field_mysql = 'age'
age_field_mysql_position = 2
is_male_field_mysql = 'is_male'
is_male_field_mysql_position = 3
height_field_mysql = 'height'
height_field_mysql_position = 4
weight_field_mysql = 'weight'
weight_field_mysql_position = 5
activity_factor_field_mysql = 'activity_factor'
activity_factor_field_mysql_position = 6
diet_type_fat_field_mysql = 'diet_type_fat'
diet_type_fat_field_mysql_position = 7
diet_type_carb_field_mysql = 'diet_type_carb'
diet_type_carb_field_mysql_position = 8
diet_type_protein_field_mysql = 'diet_type_protein'
diet_type_protein_field_mysql_position = 9
weight_goal_field_mysql = 'weight_goal'
weight_goal_field_mysql_position = 10
users_table_mysql = 'users'

# Food Macros:
# Params:
name_field_param = 'name'
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
include_dish_field_param = 'include_dish'
include_dish_positive_param_val = 'True'
include_ingredient_field_param = 'include_ingredient'
include_ingredient_positive_param_val = 'True'
ingredients_field_param = 'ingredients'

# Mysql :
name_field_mysql = 'name'
name_field_mysql_position = 0
is_liquid_field_mysql = 'liquid'
is_liquid_field_mysql_position = 1
fat_field_mysql = 'fat'
fat_field_mysql_position = 2
carb_field_mysql = 'carb'
carb_field_mysql_position = 3
fiber_field_mysql = 'fiber'
fiber_field_mysql_position = 4
protein_field_mysql = 'protein'
protein_field_mysql_position = 5
is_vegan_field_mysql = 'vegan'
is_vegan_field_mysql_position = 6
is_vegetarian_field_mysql = 'vegetarian'
is_vegetarian_field_mysql_position = 7
is_gluten_free_field_mysql = 'gluten_free'
is_gluten_free_field_mysql_position = 8
is_lactose_free_field_mysql = 'lactose_free'
is_lactose_free_field_mysql_position = 9
serving_size_field_mysql = 'serving'
serving_size_field_mysql_position = 10
food_ingredients_table_mysql = 'food_ingredients'

# Dishes Macros:
# Params:
# name_field_param = 'name'
# is_liquid_field_param = 'is_liquid'
# ingredients_field_param = 'ingredients'
ingredient_name_field_param = 'name'
ingredient_amount_field_param = 'amount'
dishes_field_param = 'dishes'
dish_name_field_param = 'dish_name'
dish_percent_field_param = 'percent'

# Mysql :
# name_field_mysql = 'name'
# name_field_mysql_position = 0
# is_liquid_field_mysql = 'liquid'
# is_liquid_field_mysql_position = 1
dishes_table_mysql = 'dishes'


# Dish Ingredients Macros:
# Params:
dish_name_field_param = 'name'

# Mysql :
dish_name_field_mysql = 'dish_name'
dish_name_field_mysql_position = 0
ingredient_name_field_mysql = 'ingredient_name'
ingredient_name_field_mysql_position = 1
ingredient_amount_field_mysql = 'ingredient_amount'
ingredient_amount_field_mysql_position = 2
dish_ingredients_table_mysql = 'dish_ingredients'
