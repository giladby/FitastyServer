# libraries
import urllib.request
import csv

import mysql.connector


def read_urls():
    file = open('urls.txt', 'r')
    return file.readlines()


def is_float(string):
    error = False
    try:
        string = float(string)
    except:
        error = True
    return error, string


def get_amount(filter, string, liquid):
    error = True
    amount = ""
    string = string.split(filter)[0]
    if "(" in string:
        parts = string.split("(")
        amount = parts[len(parts) - 1]
        error, amount = is_float(amount)
        if liquid:
            amount *= 29.5735296
        else:
            amount *= 28.3495231
    return error, amount


def get_measure(string):
    liquid = False
    amount = 0
    if " fl. oz)" in string:
        liquid = True
        error, amount = get_amount(" fl. oz)", string, liquid)
    elif " oz)" not in string:
        error = True
    else:
        error, amount = get_amount(" oz)", string, liquid)
    return error, liquid, amount


def convert_size(double_str, amount):
    error, double_val = is_float(double_str)
    if not error:
        double_val = 100 / amount * double_val
        double_val = "{:.2f}".format(double_val)
    return error, double_val


def remove_less(string):
    return string.split("&lt; ")[1] if "&lt; " in string else string


def run_script():
    rowsString = []

    urls = read_urls()

    # Fetching the html
    for url in urls:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Chrome"})
        res = urllib.request.urlopen(req)

        all_str = res.read().decode("utf-8")

        type = all_str.split(
            "<div class=\"MuiSelect-root MuiSelect-select MuiSelect-selectMenu MuiInputBase-input MuiInput-input\" "
            "tabindex=\"0\" role=\"button\" aria-haspopup=\"listbox\">")[2]
        type = type.split("<")[0]
        error, liquid, amount = get_measure(type)
        if error:
            continue

        food = all_str.split("How many calories in</span>")[1]
        food = food.split("</h1>")[0]

        parts = all_str.split("MuiTableRow-root jss382")

        fat = parts[1].split(
            "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
            1]
        fat = fat.split("<")[0]
        fat = remove_less(fat)
        error, fat = convert_size(fat, amount)
        if error:
            continue

        carbs = parts[2].split(
            "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
            1]
        carbs = carbs.split("<")[0]
        carbs = remove_less(carbs)
        error, carbs = convert_size(carbs, amount)
        if error:
            continue

        fiber = parts[3].split(
            "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
            1]
        fiber = fiber.split("<")[0]
        fiber = remove_less(fiber)
        error, fiber = convert_size(fiber, amount)
        if error:
            continue

        protein = parts[4].split(
            "MuiTypography-root MuiTypography-h5 MuiTypography-noWrap MuiTypography-alignCenter MuiTypography-displayBlock\">")[
            1]
        protein = protein.split("<")[0]
        protein = remove_less(protein)
        error, protein = convert_size(protein, amount)
        if error:
            continue

        rowsString.append((food, "1" if liquid else "0", fat, carbs, fiber, protein, "1", "1", "1", "1", amount))

    with open("foods.csv", mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["name", "liquid", "fat", "carbs", "fiber", "protein", "vegan", "vegetarian", "gluten-free",
                      "lactose-free", "serving"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in rowsString:
            writer.writerow({"name": row[0], "liquid": row[1], "fat": row[2], "carbs": row[3], "fiber": row[4],
                             "protein": row[5], "vegan": row[6], "vegetarian": row[7], "gluten-free": row[8],
                             "lactose-free": row[9], "serving": row[10]})

if __name__ == '__main__':
    run_script()